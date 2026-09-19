# Turning the playlist into a Spotify playlist

The master list lives in `knowledge/modern-rap-instant-proof-playlist.csv`.
Two ready-to-use exports are generated from it:

| File | Shape | Use with |
|---|---|---|
| `knowledge/spotify-import.csv` | `Track name,Artist name,Album` | TuneMyMusic, Soundiiz |
| `knowledge/spotify-import.txt` | `Artist - Track`, one per line | paste-style importers |

Regenerate both after editing the master CSV:

```bash
python3 scripts/make_import_files.py
```

Features are stripped to the primary artist and a few titles are mapped to
Spotify's spelling (`Hot Nigga` to `Hot N*gga`, `Ooouuu` to `OOOUUU`,
`Gët Busy` to `Get Busy`), because search matches better that way.

## Option A - no dev account, about 2 minutes

1. Open <https://www.tunemymusic.com/transfer> and click **Let's start**.
2. Source: **File Upload**. Drop in `knowledge/spotify-import.csv`.
3. Destination: **Spotify**, sign in, allow access.
4. Name the playlist and convert.

Free transfers are capped at 500 tracks, so 65 is fine. Soundiiz works the
same way but puts CSV import behind its paid tier.

## Option B - one command, exact control

Needs a free Spotify developer app for the client ID. Nothing to install;
the script is standard library only.

1. Go to <https://developer.spotify.com/dashboard> and click **Create app**.
2. Redirect URI, exactly: `http://127.0.0.1:8888/callback`. Tick **Web API**, save.
3. Copy the **Client ID**.

```bash
python3 scripts/spotify_import.py --client-id <YOUR_CLIENT_ID>
```

A browser tab opens for you to authorize; the script catches the redirect on
localhost, resolves each track, creates a private playlist and prints its URL.

Flags: `--name "..."` to rename, `--public` to make it public, `--dry-run` to
see every match without creating anything.

Each track is searched with a strict `track:"..." artist:"..."` query first,
then progressively looser ones. Anything still unmatched is listed on screen
and written to `knowledge/spotify-unmatched.txt` to add by hand. Expect a
couple of misses: some era-defining records (loosie mixtape cuts, a few
regional street singles) were never licensed to Spotify.
