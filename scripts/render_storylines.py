#!/usr/bin/env python3
"""
Deterministic renderer for the public storylines page.

This script owns everything that should NOT depend on an LLM's diligence:
weekly rollover, stale pruning, sorting, and HTML rendering. The only fuzzy
judgment call (does a new search result match an existing storyline) happens
upstream, in the Claude session that runs on each scheduled firing and edits
data.json directly before calling this script.

Usage: python3 scripts/render_storylines.py
Reads/writes: docs/storylines/data.json, docs/storylines/index.html
Writes on rollover: docs/storylines/archive/<week_start>.json
"""

import json
import html
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "docs" / "storylines" / "data.json"
OUTPUT_PATH = ROOT / "docs" / "storylines" / "index.html"
ARCHIVE_DIR = ROOT / "docs" / "storylines" / "archive"

STALE_AFTER_DAYS = 3
WEEK_LENGTH_DAYS = 7

CATEGORY_ORDER = [
    "Politics & World",
    "Business & Markets",
    "Tech & Science",
    "Sports",
    "Culture & Entertainment",
    "Odd & Human Interest",
]


def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def now_utc():
    return datetime.now(timezone.utc)


def load_data():
    if not DATA_PATH.exists():
        return {
            "week_start": now_utc().date().isoformat(),
            "last_updated": now_utc().isoformat(),
            "storylines": [],
        }
    return json.loads(DATA_PATH.read_text())


def maybe_roll_over(data):
    """Archive and reset if we've crossed the week boundary. Pure date math."""
    week_start = datetime.fromisoformat(data["week_start"]).replace(tzinfo=timezone.utc)
    if now_utc() - week_start >= timedelta(days=WEEK_LENGTH_DAYS):
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        archive_path = ARCHIVE_DIR / f"{data['week_start']}.json"
        archive_path.write_text(json.dumps(data, indent=2))
        return {
            "week_start": now_utc().date().isoformat(),
            "last_updated": now_utc().isoformat(),
            "storylines": [],
        }
    return data


def prune_stale(data):
    cutoff = now_utc() - timedelta(days=STALE_AFTER_DAYS)
    data["storylines"] = [
        s for s in data["storylines"] if parse_dt(s["last_seen"]) >= cutoff
    ]
    return data


def fmt_date(dt):
    return dt.strftime("%b %-d")


def render_card(s):
    first = parse_dt(s["first_seen"])
    last = parse_dt(s["last_seen"])
    freshness = f"First noticed {fmt_date(first)}"
    if last.date() != first.date():
        freshness += f" &middot; updated {fmt_date(last)}"
    times = s.get("appearances", 1)
    freshness += f" &middot; mentioned {times}&times;" if times > 1 else " &middot; new"

    return f"""      <li class="storyline-item">
        <p class="storyline-moment">{html.escape(s['moment'])}</p>
        <p class="storyline-why">{html.escape(s['why_now'])}</p>
        <p class="storyline-freshness">{freshness}</p>
      </li>"""


def render_category(category, items):
    if not items:
        return ""
    items_sorted = sorted(
        items, key=lambda s: (s.get("appearances", 1), s["last_seen"]), reverse=True
    )
    cards = "\n".join(render_card(s) for s in items_sorted)
    return f"""    <div class="storyline-category">
      <p class="storyline-category-label">{html.escape(category)}</p>
      <ul class="storyline-list">
{cards}
      </ul>
    </div>
"""


def render_page(data):
    week_start = datetime.fromisoformat(data["week_start"]).replace(tzinfo=timezone.utc)
    week_end = week_start + timedelta(days=WEEK_LENGTH_DAYS - 1)
    updated = parse_dt(data["last_updated"])

    by_category = {c: [] for c in CATEGORY_ORDER}
    for s in data["storylines"]:
        by_category.setdefault(s["category"], []).append(s)

    sections = "\n".join(
        render_category(cat, by_category.get(cat, [])) for cat in CATEGORY_ORDER
    )
    total = len(data["storylines"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Why Today? &middot; This Week's Storylines</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,500;1,8..60,300;1,8..60,400&family=Source+Sans+3:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>

  <header class="masthead">
    <a href="../" class="publication-name">Why Today?</a>
    <span class="masthead-tagline">A different question for today's conversation.</span>
  </header>

  <section class="hero">
    <p class="hero-eyebrow">Updated automatically</p>
    <h1 class="hero-headline">This week's storylines.</h1>
    <p class="hero-description">Unedited, refreshed continuously from the same survey that feeds every edition. This is raw material, not a finished edition &mdash; the actual weekly edition still gets built by hand from whatever proves durable here.</p>
  </section>

  <div class="storylines-meta-bar">
    <span>Week of {fmt_date(week_start)}&ndash;{fmt_date(week_end)}, {week_start.year}</span>
    <span>{total} active storylines</span>
    <span>Last updated {updated.strftime('%b %-d, %Y %H:%M UTC')}</span>
  </div>

  <div class="storylines-section">
{sections}
  </div>

  <footer class="footer">
    <span class="footer-name">Why Today?</span>
    <span class="footer-note">bdavey.co/why-today</span>
  </footer>

</body>
</html>
"""


def main():
    data = load_data()
    data = maybe_roll_over(data)
    data = prune_stale(data)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(data, indent=2) + "\n")
    OUTPUT_PATH.write_text(render_page(data))
    print(f"Wrote {DATA_PATH} ({len(data['storylines'])} active storylines)")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
