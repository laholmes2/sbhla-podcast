"""Shared logic for building podcast RSS feeds from a CSV of episodes.

Each show (Pastor's Conference, Baptist Hour, ...) has its own CSV and its
own thin build_*.py script that supplies a FeedConfig and calls write_feed().
"""

import csv
import html
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class FeedConfig:
    csv_path: Path
    out_path: Path
    title: str
    link: str
    description: str
    image: str
    author: str = "Southern Baptist Historical Library & Archives"
    language: str = "en-us"
    category: str = "Religion &amp; Spirituality"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def parse_duration_to_seconds(duration: str) -> int:
    parts = [int(p) for p in duration.split(":")]
    seconds = 0
    for p in parts:
        seconds = seconds * 60 + p
    return seconds


def rfc822(date_str: str) -> str:
    # Accepts "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" (the latter lets same-day
    # multi-part episodes sort in the right order within a podcast app).
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
            return dt.strftime("%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str!r}")


def build_item(row: dict) -> str:
    title = esc(row["title"])
    full_description = row["description"]
    if row.get("program_pdf"):
        full_description += f" Full printed program: {row['program_pdf']}"
    description = esc(full_description)
    mp3_url = esc(row["mp3_url"])
    length = row["bytes"]
    pub_date = rfc822(row["date"])
    duration_seconds = parse_duration_to_seconds(row["duration"])
    guid = esc(row["mp3_url"])
    source_page = esc(row["source_page"])

    return f"""    <item>
      <title>{title}</title>
      <description>{description}</description>
      <link>{source_page}</link>
      <enclosure url="{mp3_url}" length="{length}" type="audio/mpeg"/>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{pub_date}</pubDate>
      <itunes:duration>{duration_seconds}</itunes:duration>
      <itunes:explicit>false</itunes:explicit>
    </item>"""


def build_feed(rows: list[dict], config: FeedConfig) -> str:
    items = "\n".join(build_item(row) for row in rows)
    last_build = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{esc(config.title)}</title>
    <link>{esc(config.link)}</link>
    <description>{esc(config.description)}</description>
    <language>{config.language}</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <itunes:author>{esc(config.author)}</itunes:author>
    <itunes:explicit>false</itunes:explicit>
    <itunes:category text="{config.category}"/>
    <itunes:image href="{esc(config.image)}"/>
    <image>
      <url>{esc(config.image)}</url>
      <title>{esc(config.title)}</title>
      <link>{esc(config.link)}</link>
    </image>
{items}
  </channel>
</rss>
"""


def write_feed(config: FeedConfig) -> None:
    with config.csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    feed_xml = build_feed(rows, config)
    config.out_path.write_text(feed_xml, encoding="utf-8")
    print(f"Wrote {config.out_path} with {len(rows)} episodes")
    if "REPLACE_WITH_HOSTED_ARTWORK_URL" in config.image:
        print(
            f"WARNING: image for {config.out_path} is still a placeholder. "
            "Update it once the artwork is actually hosted."
        )
