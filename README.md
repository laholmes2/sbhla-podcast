# SBHLA Podcast (personal proof of concept)

A private RSS feed pointing to audio recordings already hosted publicly by the
Southern Baptist Historical Library & Archives (sbhla.org). No audio is
copied or re-hosted — `feed.xml` only contains metadata and links to SBHLA's
own CDN files.

## Files

- `data/sermons.csv` — episode metadata (title, date, description, mp3 url, byte size, duration, source page, program PDF)
- `build_feed.py` — reads the CSV and writes `feed.xml`
- `feed.xml` — the generated podcast RSS feed
- `artwork/make_artwork.py` — generates `artwork.jpg` (3000x3000 cover art) from SBHLA's real logo
- `artwork/sbhla_logo_source.png` — the actual SBHLA logo (256x256, the largest version hosted on their site)
- `artwork.jpg` — generated podcast cover art (parchment background, real SBHLA seal, title text)

## Usage

Regenerate the feed after editing the CSV:

```bash
python3 build_feed.py
```

Before publishing, update `FEED_IMAGE` in `build_feed.py` from its
placeholder to the real hosted URL of `artwork.jpg` (podcast apps require an
absolute URL for artwork).

Host `feed.xml` (and `artwork.jpg`) somewhere reachable (e.g. GitHub Pages)
and subscribe to the feed URL in a podcast app (Apple Podcasts, Overcast,
Pocket Casts, etc.) via "Add Show by URL".

## Adding more episodes

Add a row to `data/sermons.csv` with the same columns, then rerun
`build_feed.py`. To get `bytes` for a new mp3, run:

```bash
curl -sIL "<mp3-url>" | grep -i content-length
```

## Current content

10 episodes from the 1963 SBC Pastor's Conference (Monday morning through
Tuesday morning, in session order), sourced from:
https://sbhla.org/digital-resources/pastors-conference-audio-recordings/pc-audio-1963/

This collection is organized by conference *session* (e.g. "Monday Morning,
Part 1"), not by individual sermon — each ~1 hour file can span multiple
speakers, and sermons sometimes run across two files. Titles and
descriptions were cross-referenced against SBHLA's printed 1963 conference
program (linked in each episode's description) to attribute real speaker
names and sermon titles to each file. Segment boundaries within a file are
*estimated* from the program's printed schedule (assuming the session
started on time and ran continuously) — they are not verified by listening,
so treat minute-level placement as approximate, especially where a sermon
is noted as continuing into the next or previous file.

Not yet included from the 1963 conference: the rest of Tuesday (including
W. A. Criswell's "The Cross of Christ," Tuesday ~11:40am) and K. Owen
White's "The New Birth" and Jess C. Moody's "The Christian Home." Easy to
add later the same way — pull the next audio file's playlist JSON off the
1963 page and match it against the program PDF.
