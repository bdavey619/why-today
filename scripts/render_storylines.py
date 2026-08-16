#!/usr/bin/env python3
"""
Deterministic renderer for the public cabinet-of-curiosities page.

Organizes entries by five collecting streams (Natural World, Human Rituals,
Places, Curiosities, Headlines). Within the Headlines stream, entries are
grouped by their existing category field for backward compatibility.

Handles both old-style entries (category field only, no stream) and new-style
entries (stream field present). Old-style entries are treated as stream=headlines.

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

STREAM_ORDER = [
    "natural_world",
    "human_rituals",
    "places",
    "curiosities",
    "markets",
    "headlines",
]

STREAM_LABELS = {
    "natural_world": "Natural World",
    "human_rituals": "Human Rituals",
    "places": "Places",
    "curiosities": "Curiosities",
    "markets": "Markets",
    "headlines": "Headlines",
}

# Within headlines stream, category display order
CATEGORY_ORDER = [
    "Politics & World",
    "Business & Markets",
    "Tech & Science",
    "Sports",
    "Culture & Entertainment",
    "Odd & Human Interest",
]

POTENTIAL_RANK = {"high": 0, "medium": 1, "low": 2}


def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def now_utc():
    return datetime.now(timezone.utc)


def get_stream(s):
    """Return the stream for an entry. Old entries without stream default to headlines."""
    return s.get("stream") or "headlines"


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
    """Remove entries past the stale window unless they are dormant (preserve those)."""
    cutoff = now_utc() - timedelta(days=STALE_AFTER_DAYS)
    data["storylines"] = [
        s for s in data["storylines"]
        if s.get("status") == "dormant" or parse_dt(s["last_seen"]) >= cutoff
    ]
    return data


def cap_history(data):
    """Bound history growth in the data file itself, not just at render time."""
    for s in data["storylines"]:
        if s.get("history"):
            s["history"] = s["history"][-5:]
    return data


def fmt_date(dt):
    return dt.strftime("%b %-d")


MAX_HISTORY = 5

STATUS_LABELS = {
    "captured": "captured",
    "curious": "curious",
    "investigating": "investigating",
    "thread_found": "thread found",
    "ready_to_shape": "ready to shape",
    "published": "published",
    "dormant": "dormant",
}


def render_card(s):
    first = parse_dt(s["first_seen"])
    last = parse_dt(s["last_seen"])
    freshness = fmt_date(first)
    if last.date() != first.date():
        freshness += f"&ndash;{fmt_date(last)}"
    times = s.get("appearances", 1)
    if times > 1:
        freshness += f" &middot; {times}&times;"

    history = s.get("history", [])
    freshness_attrs = ""
    if history:
        tooltip = "; ".join(
            f"{parse_dt(h['date']).strftime('%b %-d')}: {h['note']}" for h in history[-MAX_HISTORY:]
        )
        freshness_attrs = f' title="{html.escape(tooltip)}"'
        freshness += " &middot; evolving"

    # Title / moment link
    url = s.get("url", "")
    title_text = s.get("title") or s.get("moment") or ""
    if url and title_text:
        title_html = f'<a href="{html.escape(url)}" class="storyline-moment" target="_blank" rel="noopener">{html.escape(title_text)}</a>'
    elif title_text:
        title_html = f'<strong class="storyline-moment">{html.escape(title_text)}</strong>'
    else:
        title_html = ""

    # Editorial potential chip
    potential = s.get("editorial_potential", "")
    potential_html = ""
    if potential:
        potential_html = f'<span class="storyline-potential potential-{html.escape(potential)}">{html.escape(potential)}</span> '

    # Status chip (show for non-default statuses)
    status = s.get("status", "captured")
    status_html = ""
    if status and status not in ("captured", ""):
        label = STATUS_LABELS.get(status, status)
        status_html = f'<span class="curiosity-status status-{html.escape(status)}">{html.escape(label)}</span> '

    # Observation ("I noticed…")
    observation = s.get("observation", "")
    observation_html = ""
    if observation:
        observation_html = f'\n        <p class="curiosity-observation">{html.escape(observation)}</p>'

    # Question ("I wonder…") — prefer `question`, fall back to `hidden_question`
    question = s.get("question") or s.get("hidden_question", "")
    question_html = ""
    if question:
        question_html = f'\n        <p class="curiosity-question">{html.escape(question)}</p>'

    # For headline-style entries that only have why_now (no observation), show why_now inline
    why_now = s.get("why_now", "")
    main_description = ""
    if not observation and why_now and title_text:
        # Old-style headline card: show title — why_now inline
        main_description = f" &mdash; {html.escape(why_now)}"

    season = s.get("season_or_time_context", "")
    season_html = ""
    if season:
        season_html = f' <span class="curiosity-season">{html.escape(season)}</span>'

    location = s.get("location", "")
    location_html = ""
    if location:
        location_html = f' <span class="curiosity-location">{html.escape(location)}</span>'

    return f"""      <li class="storyline-item">
        <div class="storyline-row">
          <span class="storyline-main">{status_html}{potential_html}{title_html}{main_description}{season_html}{location_html}</span>
          <span class="storyline-freshness"{freshness_attrs}>{freshness}</span>
        </div>{observation_html}{question_html}
      </li>"""


def sort_items(items):
    return sorted(
        items,
        key=lambda s: (
            POTENTIAL_RANK.get(s.get("editorial_potential", ""), 3),
            -s.get("appearances", 1),
        ),
    )


def render_stream_section(stream, items):
    """Render one stream section. For headlines, group by category."""
    if not items:
        return ""

    label = STREAM_LABELS.get(stream, stream.replace("_", " ").title())

    if stream == "headlines":
        # Group by category within headlines
        by_category = {c: [] for c in CATEGORY_ORDER}
        for s in items:
            cat = s.get("category", "Odd & Human Interest")
            by_category.setdefault(cat, []).append(s)

        inner = ""
        for cat in CATEGORY_ORDER:
            cat_items = sort_items(by_category.get(cat, []))
            if not cat_items:
                continue
            cards = "\n".join(render_card(s) for s in cat_items)
            inner += f"""      <div class="storyline-category">
        <p class="storyline-category-label">{html.escape(cat)}</p>
        <ul class="storyline-list">
{cards}
        </ul>
      </div>
"""
        if not inner:
            return ""

        return f"""  <div class="stream-section" data-stream="{html.escape(stream)}">
    <p class="stream-label">{html.escape(label)}</p>
{inner}  </div>
"""
    else:
        sorted_items = sort_items(items)
        cards = "\n".join(render_card(s) for s in sorted_items)
        return f"""  <div class="stream-section" data-stream="{html.escape(stream)}">
    <p class="stream-label">{html.escape(label)}</p>
    <ul class="storyline-list">
{cards}
    </ul>
  </div>
"""


def render_dormant_section(items):
    """Render dormant curiosities in a separate collapsed section."""
    if not items:
        return ""
    sorted_items = sort_items(items)
    cards = "\n".join(render_card(s) for s in sorted_items)
    return f"""  <div class="stream-section stream-dormant">
    <p class="stream-label">Dormant</p>
    <p class="stream-dormant-note">Set aside — may resurface in a different season or context.</p>
    <ul class="storyline-list">
{cards}
    </ul>
  </div>
"""


def render_page(data):
    week_start = datetime.fromisoformat(data["week_start"]).replace(tzinfo=timezone.utc)
    week_end = week_start + timedelta(days=WEEK_LENGTH_DAYS - 1)
    updated = parse_dt(data["last_updated"])

    # Separate dormant from active
    active = [s for s in data["storylines"] if s.get("status") != "dormant"]
    dormant = [s for s in data["storylines"] if s.get("status") == "dormant"]

    # Group active by stream
    by_stream = {s: [] for s in STREAM_ORDER}
    for s in active:
        stream = get_stream(s)
        by_stream.setdefault(stream, []).append(s)

    sections = "".join(
        render_stream_section(stream, by_stream.get(stream, []))
        for stream in STREAM_ORDER
    )
    dormant_section = render_dormant_section(dormant)

    total_active = len(active)
    total_dormant = len(dormant)
    count_text = f"{total_active} active"
    if total_dormant:
        count_text += f", {total_dormant} dormant"

    # Stream count summary
    stream_counts = []
    for stream in STREAM_ORDER:
        count = len(by_stream.get(stream, []))
        if count:
            label = STREAM_LABELS.get(stream, stream)
            stream_counts.append(f"{label}: {count}")
    stream_summary = " &nbsp;&middot;&nbsp; ".join(stream_counts) if stream_counts else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Why Today? &middot; Cabinet of Curiosities</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,500;1,8..60,300;1,8..60,400&family=Source+Sans+3:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>

  <header class="masthead">
    <a href="../" class="publication-name">Why Today?</a>
    <nav class="masthead-nav">
      <a href="../patterns/" class="masthead-nav-link">Recognitions &rarr;</a>
      <span class="masthead-tagline">A different question for today's conversation.</span>
    </nav>
  </header>

  <section class="hero">
    <p class="hero-eyebrow">Updated automatically</p>
    <h1 class="hero-headline">Cabinet of curiosities.</h1>
    <p class="hero-description">Observations, questions, and threads from six streams: the natural world, human rituals, places, open curiosities, markets, and headlines. Raw material for investigation &mdash; not finished editions.</p>
  </section>

  <div class="storylines-meta-bar">
    <span>Week of {fmt_date(week_start)}&ndash;{fmt_date(week_end)}, {week_start.year}</span>
    <span>{count_text}</span>
    <span>Last updated {updated.strftime('%b %-d, %Y %H:%M UTC')}</span>
  </div>

  {f'<div class="stream-summary">{stream_summary}</div>' if stream_summary else ''}

  <div class="storylines-section">
{sections}{dormant_section}
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
    data = cap_history(data)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(data, indent=2) + "\n")
    OUTPUT_PATH.write_text(render_page(data))

    active = [s for s in data["storylines"] if s.get("status") != "dormant"]
    dormant = [s for s in data["storylines"] if s.get("status") == "dormant"]
    print(f"Wrote {DATA_PATH} ({len(active)} active, {len(dormant)} dormant)")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
