#!/usr/bin/env python3
"""Create the Instant Proof playlist in your Spotify account.

Stdlib only - nothing to install. Uses the Authorization Code + PKCE flow, so
no client secret is needed.

Setup (about 90 seconds, once):
  1. Go to https://developer.spotify.com/dashboard and click "Create app".
  2. Name it anything. For "Redirect URI" enter exactly:
         http://127.0.0.1:8888/callback
     Tick the Web API checkbox, save.
  3. Copy the Client ID from the app's settings.

Run:
  python3 scripts/spotify_import.py --client-id <YOUR_CLIENT_ID>
  # or: export SPOTIFY_CLIENT_ID=... && python3 scripts/spotify_import.py

Options:
  --name "..."     playlist name (default: "Modern Rap: Instant Proof")
  --public         make the playlist public (default: private)
  --dry-run        resolve tracks and print matches, create nothing
"""
import argparse
import base64
import csv
import hashlib
import json
import os
import re
import secrets
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "knowledge", "modern-rap-instant-proof-playlist.csv")
UNMATCHED = os.path.join(ROOT, "knowledge", "spotify-unmatched.txt")

REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "playlist-modify-private playlist-modify-public"
API = "https://api.spotify.com/v1"

TITLE_ALIASES = {
    "Hot Nigga": "Hot N*gga",
    "Ooouuu": "OOOUUU",
    "Gët Busy": "Get Busy",
}
ARTIST_ALIASES = {
    "Lil Herb & Lil Bibby": "Lil Bibby",
    "GloRilla & Hitkidd": "Hitkidd",
    "iLoveMakonnen": "ILOVEMAKONNEN",
    "A Boogie wit da Hoodie": "A Boogie Wit da Hoodie",
}
FEAT_RE = re.compile(r"\s+(ft\.|feat\.|featuring|with)\s+.*$", re.IGNORECASE)


def primary_artist(artist):
    artist = ARTIST_ALIASES.get(artist.strip(), artist.strip())
    artist = FEAT_RE.sub("", artist)
    for sep in (" & ", ", "):
        if sep in artist:
            artist = artist.split(sep)[0]
    return artist.strip()


def search_title(song):
    return TITLE_ALIASES.get(song.strip(), song.strip())


def build_queries(song, artist):
    """Progressively looser queries; the first hit wins."""
    title, art = search_title(song), primary_artist(artist)
    bare = re.sub(r"\s*\([^)]*\)", "", title).strip()
    queries = [
        f'track:"{title}" artist:"{art}"',
        f'{title} {art}',
    ]
    if bare and bare != title:
        queries.append(f'track:"{bare}" artist:"{art}"')
        queries.append(f'{bare} {art}')
    return queries


# ---------------------------------------------------------------- auth

class _CallbackHandler(BaseHTTPRequestHandler):
    code = None
    error = None

    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _CallbackHandler.code = params.get("code", [None])[0]
        _CallbackHandler.error = params.get("error", [None])[0]
        body = b"<h2>Done. You can close this tab and return to the terminal.</h2>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def get_token(client_id):
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)

    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "code_challenge_method": "S256",
        "code_challenge": challenge,
        "state": state,
    })

    server = HTTPServer(("127.0.0.1", 8888), _CallbackHandler)
    threading.Thread(target=server.handle_request, daemon=True).start()

    print("\nOpening Spotify authorization in your browser.")
    print("If it does not open, paste this URL yourself:\n")
    print(auth_url + "\n")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    print("Waiting for the redirect back to 127.0.0.1:8888 ...")
    for _ in range(300):
        if _CallbackHandler.code or _CallbackHandler.error:
            break
        threading.Event().wait(1)
    server.server_close()

    if _CallbackHandler.error:
        sys.exit(f"Spotify returned an error: {_CallbackHandler.error}")
    if not _CallbackHandler.code:
        sys.exit("Timed out waiting for authorization.")

    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": _CallbackHandler.code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "code_verifier": verifier,
    }).encode()
    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)["access_token"]


# ---------------------------------------------------------------- api

def api(token, method, path, payload=None, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        sys.exit(f"Spotify API {e.code} on {method} {path}: {detail}")


def find_track(token, song, artist):
    for q in build_queries(song, artist):
        res = api(token, "GET", "/search", params={"q": q, "type": "track", "limit": 1})
        items = res.get("tracks", {}).get("items", [])
        if items:
            t = items[0]
            return t["uri"], t["name"], ", ".join(a["name"] for a in t["artists"])
    return None, None, None


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-id", default=os.environ.get("SPOTIFY_CLIENT_ID"))
    ap.add_argument("--name", default="Modern Rap: Instant Proof")
    ap.add_argument("--public", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.client_id:
        sys.exit("Need a client id: --client-id <ID> or SPOTIFY_CLIENT_ID env var. See the header of this file.")

    with open(SRC, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    print(f"Loaded {len(rows)} tracks from {os.path.relpath(SRC, ROOT)}")

    token = get_token(args.client_id)
    me = api(token, "GET", "/me")
    print(f"Signed in as {me.get('display_name') or me['id']}\n")

    uris, missed = [], []
    for i, r in enumerate(rows, 1):
        uri, name, artists = find_track(token, r["song"], r["artist"])
        if uri:
            uris.append(uri)
            print(f"{i:3}. OK   {r['song']} - {r['artist']}  ->  {name} - {artists}")
        else:
            missed.append(f"{r['song']} - {r['artist']}")
            print(f"{i:3}. MISS {r['song']} - {r['artist']}")

    print(f"\nMatched {len(uris)}/{len(rows)}; {len(missed)} not found.")
    if missed:
        with open(UNMATCHED, "w", encoding="utf-8") as fh:
            fh.write("\n".join(missed) + "\n")
        print(f"Unmatched written to {os.path.relpath(UNMATCHED, ROOT)} - add those by hand.")

    if args.dry_run:
        print("\nDry run: no playlist created.")
        return

    pl = api(token, "POST", f"/users/{me['id']}/playlists", payload={
        "name": args.name,
        "public": bool(args.public),
        "description": "Modern rap 2012-2024, selected on ignition velocity. Built from research in this repo.",
    })
    for batch in chunks(uris, 100):
        api(token, "POST", f"/playlists/{pl['id']}/tracks", payload={"uris": batch})

    print(f"\nPlaylist created: {pl['external_urls']['spotify']}")
    print(f"{len(uris)} tracks added.")


if __name__ == "__main__":
    main()
