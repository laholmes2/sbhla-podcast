# SBHLA Podcast (personal proof of concept)

Private RSS feeds pointing to audio recordings already hosted publicly by the
Southern Baptist Historical Library & Archives (sbhla.org). No audio is
copied or re-hosted — the feeds only contain metadata and links to SBHLA's
own CDN files.

Two shows so far, each its own feed (so subscribing to one doesn't disturb
the other):

| Show | Feed URL | CSV | Build script |
|---|---|---|---|
| Pastor's Conference Recordings | `https://laholmes2.github.io/sbhla-podcast/feed.xml` | `data/sermons.csv` | `build_feed.py` |
| Baptist Hour Recordings | `https://laholmes2.github.io/sbhla-podcast/baptist_hour_feed.xml` | `data/baptist_hour_1945.csv` | `build_baptist_hour_feed.py` |

Subscribe to either feed URL in a podcast app (Apple Podcasts, Overcast,
Pocket Casts, etc.) via "Add Show by URL".

## Files

- `feedlib.py` — shared feed-building logic (both shows import this)
- `build_feed.py` / `build_baptist_hour_feed.py` — thin per-show config, each writes its own `feed.xml`
- `data/*.csv` — per-show episode metadata (title, date, description, mp3 url, byte size, duration, source page, and optionally a program PDF link)
- `artwork/make_artwork.py` — generates 3000x3000 cover art from SBHLA's real logo; takes `--title-line1/2` and `--out` so each show gets its own art
- `artwork.jpg` / `baptist_hour_artwork.jpg` — generated cover art per show

## Usage

Regenerate a feed after editing its CSV:

```bash
python3 build_feed.py
python3 build_baptist_hour_feed.py
```

Each `build_*.py` script's `FeedConfig(image=...)` must be an absolute,
publicly-hosted URL (podcast apps won't resolve relative image paths).

## Adding more episodes to an existing show

Add a row to that show's CSV with the same columns, then rerun its build
script. To get `bytes` for a new mp3:

```bash
curl -sIL "<mp3-url>" | grep -i content-length
```

## Adding a new show

1. Find the SBHLA collection page and pull its playlist metadata: open the
   page, run in the console `document.querySelector('script[type="application/json"]').textContent` — this is a JSON blob with every track's `src`, `title`, and `meta.length_formatted`.
2. Build a CSV in `data/` with columns `title,date,description,mp3_url,bytes,duration,source_page` (add `program_pdf` too if there's a program to cross-reference, like the Pastor's Conference show).
3. Generate artwork: `python3 artwork/make_artwork.py --title-line1 "..." --title-line2 "..." --out <name>_artwork.jpg`
4. Copy `build_baptist_hour_feed.py` as a template for a new `build_<name>_feed.py` with its own `FeedConfig`.
5. Push, then update the `image` URL in the config to the real hosted artwork URL.

## Current content

### Pastor's Conference Recordings (16 episodes)

All 16 audio files from the complete 1963 SBC Pastor's Conference (Monday
morning through Tuesday afternoon's closing session), sourced from:
https://sbhla.org/digital-resources/pastors-conference-audio-recordings/pc-audio-1963/

This collection is organized by conference *session* (e.g. "Monday Morning,
Part 1"), not by individual sermon — each ~1 hour file can span multiple
speakers, and sermons sometimes run across two files. Titles and
descriptions were cross-referenced against SBHLA's printed 1963 conference
program (linked in each episode's description) to attribute real speaker
names and sermon titles to each file, including notable names like Vance
Havner, W. A. Criswell, and Robert G. Lee. Segment boundaries within a file
are *estimated* from the program's printed schedule (assuming each session
started on time and ran continuously) — they are not verified by listening,
so treat minute-level placement as approximate, especially where a sermon
is noted as continuing into the next or previous file. Two sessions (Monday
evening and Tuesday afternoon) ran noticeably longer than their printed
schedule accounts for; the unaccounted-for time is called out in those
episodes' descriptions rather than guessed at.

To add other years (1954-1980 are all available from SBHLA), pull that
year's page, extract the `script[type="application/json"]` playlist blob
for MP3 URLs/titles/durations, get byte sizes via `curl -sIL <url> | grep
content-length`, and cross-reference against that year's program PDF from
https://sbhla.org/digital-resources/sbc-pc-programs/.

### Baptist Hour Recordings (20 episodes)

All 20 audio files from the 1945 Baptist Hour weekly radio broadcasts,
sourced from:
https://sbhla.org/digital-resources/baptist-hour-audio-recordings/baptist-hour-audio-recordings-1945/

Unlike the Pastor's Conference collection, each file here is already a
standalone ~15-30 minute broadcast with its own preacher and sermon title
baked into SBHLA's own filename/label — no program PDF or timestamp
cross-referencing was needed. Titles and descriptions are taken verbatim
from SBHLA's own display text (including their capitalization/spelling
choices, e.g. "Christian Patroits," "Good Shepard"), rather than
"corrected," to stay faithful to what SBHLA itself publishes. A few notes
worth knowing:

- One recording (Jan 28) is flagged by SBHLA itself as damaged.
- Several sermons are only half-present ("Part 1" or "Part 2" only) — the
  companion half doesn't appear in SBHLA's 1945 digitized set, and each
  such episode's description says so.
- There are calendar gaps (no April 1, and a long gap between mid-June and
  mid-October 1945) where no broadcast appears to have been preserved.

1945 is the only year currently included; other years follow the same
process described above for adding a new show/year.
