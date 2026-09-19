#!/usr/bin/env python3
"""Generate Spotify-import-friendly files from the master playlist CSV.

Outputs:
  knowledge/spotify-import.csv  -> Track name,Artist name,Album  (TuneMyMusic / Soundiiz)
  knowledge/spotify-import.txt  -> "Artist - Track" per line     (paste-style importers)
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "knowledge", "modern-rap-instant-proof-playlist.csv")
OUT_CSV = os.path.join(ROOT, "knowledge", "spotify-import.csv")
OUT_TXT = os.path.join(ROOT, "knowledge", "spotify-import.txt")

# Titles/credits that differ from how Spotify catalogues them.
TITLE_ALIASES = {
    "Hot Nigga": "Hot N*gga",
    "Ooouuu": "OOOUUU",
    "Gët Busy": "Get Busy",
    "F.N.F. (Let's Go)": "F.N.F. (Let's Go)",
    "Munch (Feelin' U)": "Munch (Feelin' U)",
}
ARTIST_ALIASES = {
    "Lil Herb & Lil Bibby": "Lil Bibby",
    "GloRilla & Hitkidd": "Hitkidd",
    "iLoveMakonnen": "ILOVEMAKONNEN",
    "A Boogie wit da Hoodie": "A Boogie Wit da Hoodie",
    "Lil Herb": "G Herbo",
}

FEAT_RE = re.compile(r"\s+(ft\.|feat\.|featuring|with)\s+.*$", re.IGNORECASE)


def primary_artist(artist: str) -> str:
    """Strip features and secondary credits down to one searchable artist."""
    artist = ARTIST_ALIASES.get(artist.strip(), artist.strip())
    artist = FEAT_RE.sub("", artist)
    for sep in (" & ", ", "):
        if sep in artist:
            artist = artist.split(sep)[0]
    return artist.strip()


def search_title(song: str) -> str:
    return TITLE_ALIASES.get(song.strip(), song.strip())


def load_rows():
    with open(SRC, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    rows = load_rows()
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Track name", "Artist name", "Album"])
        for r in rows:
            w.writerow([search_title(r["song"]), primary_artist(r["artist"]), ""])
    with open(OUT_TXT, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(f"{primary_artist(r['artist'])} - {search_title(r['song'])}\n")
    print(f"wrote {OUT_CSV} and {OUT_TXT} ({len(rows)} tracks)")


if __name__ == "__main__":
    main()
