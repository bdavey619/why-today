#!/usr/bin/env python3
"""
Renderer for the Why Today? recognitions publication.

Reads docs/patterns/data.json and writes docs/patterns/index.html.
The recognitions page is the primary reader-facing publication.

Usage: python3 scripts/render_patterns.py
Reads:  docs/patterns/data.json
Writes: docs/patterns/index.html
"""

import json
import html
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "docs" / "patterns" / "data.json"
OUTPUT_PATH = ROOT / "docs" / "patterns" / "index.html"

MOMENTUM_LABELS = {
    "building":     "Building",
    "accelerating": "Accelerating",
    "peaking":      "Peaking now",
    "fading":       "Fading",
    "acute":        "Acute",
    "persistent":   "Persistent",
}

MOMENTUM_ORDER = ["acute", "peaking", "accelerating", "building", "persistent", "fading"]


def load_data():
    if not DATA_PATH.exists():
        return {"week": datetime.now(timezone.utc).date().isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "recognitions": []}
    return json.loads(DATA_PATH.read_text())


def fmt_week(iso_date):
    d = datetime.fromisoformat(iso_date)
    return d.strftime("Week of %B %-d, %Y")


def fmt_updated(iso_dt):
    dt = datetime.fromisoformat(iso_dt.replace("Z", "+00:00"))
    return dt.strftime("Updated %B %-d, %Y")


def fmt_evidence_date(date_str):
    """Format an evidence date for display. Handles full ISO, year-month, and 'annual'."""
    if not date_str:
        return ""
    s = date_str.strip().lower()
    if s == "annual":
        return "Annual"
    try:
        # Full date: YYYY-MM-DD
        d = datetime.fromisoformat(s)
        return d.strftime("%b %-d")
    except ValueError:
        pass
    try:
        # Year-month: YYYY-MM
        parts = s.split("-")
        if len(parts) == 2:
            d = datetime(int(parts[0]), int(parts[1]), 1)
            return d.strftime("%b %Y")
    except (ValueError, IndexError):
        pass
    return date_str


SOURCE_LABELS = {
    "wusf.org":              "WUSF",
    "beinsure.com":          "BEinsure",
    "wine-searcher.com":     "Wine-Searcher",
    "undercurrentnews.com":  "Undercurrent News",
    "aljazeera.com":         "Al Jazeera",
    "eia.gov":               "EIA",
    "gcaptain.com":          "gCaptain",
    "fortune.com":           "Fortune",
    "forbes.com":            "Forbes",
    "techtimes.com":         "Tech Times",
    "accuweather.com":       "AccuWeather",
    "earthsky.org":          "EarthSky",
    "nationaltoday.com":     "National Today",
    "cnn.com":               "CNN",
    "cnbc.com":              "CNBC",
    "pbs.org":               "PBS",
    "npr.org":               "NPR",
    "nytimes.com":           "NYT",
    "washingtonpost.com":    "Washington Post",
    "reuters.com":           "Reuters",
    "apnews.com":            "AP",
    "bbc.com":               "BBC",
    "bbc.co.uk":             "BBC",
    "theguardian.com":       "Guardian",
    "ft.com":                "FT",
    "wsj.com":               "WSJ",
    "bloomberg.com":         "Bloomberg",
    "axios.com":             "Axios",
    "politico.com":          "Politico",
    "forward.com":           "Forward",
    "brookings.edu":         "Brookings",
    "indexbox.io":           "IndexBox",
}


def source_label(url):
    try:
        host = urlparse(url).netloc.lstrip("www.")
        return SOURCE_LABELS.get(host, host)
    except Exception:
        return ""


def render_evidence_item(item):
    domain   = html.escape(item.get("domain", ""))
    text     = html.escape(item.get("text", ""))
    url      = item.get("url", "").strip()
    date_raw = item.get("date", "")
    is_new   = bool(item.get("is_new", False))

    date_label = fmt_evidence_date(date_raw)
    date_el    = f'\n          <time class="ev-date">{html.escape(date_label)}</time>' if date_label else ""
    new_el     = '\n          <span class="ev-new-badge">New</span>' if is_new else ""
    item_class = 'ev-item ev-item--new' if is_new else 'ev-item'

    if url:
        read_more = (
            f'\n          <a href="{html.escape(url)}" class="ev-read-more" '
            f'target="_blank" rel="noopener">Read more &#x2192;</a>'
        )
    else:
        read_more = ""

    return f"""\
        <li class="{item_class}">
          <div class="ev-meta">
            <span class="ev-domain">{domain}</span>{new_el}{date_el}
          </div>
          <div class="ev-body">
            <p class="ev-text">{text}</p>{read_more}
          </div>
        </li>"""


def render_recognition(r):
    rid         = html.escape(r.get("id", ""))
    title       = html.escape(r.get("title", ""))
    explanation = html.escape(r.get("explanation", ""))
    evidence    = r.get("evidence", [])[:4]

    ev_count  = len(evidence)
    new_count = sum(1 for e in evidence if e.get("is_new", False))
    count_label = f"{ev_count} source{'s' if ev_count != 1 else ''}"
    new_el = f' <span class="ev-summary-new">{new_count} new</span>' if new_count else ""

    ev_items = "\n".join(render_evidence_item(e) for e in evidence)

    return f"""\
    <article class="recognition" id="{rid}">
      <h2 class="recognition-title">{title}</h2>
      <p class="recognition-explanation">{explanation}</p>
      <details class="evidence-details">
        <summary class="evidence-toggle">
          <span class="ev-summary-count">{html.escape(count_label)}</span>{new_el}
        </summary>
        <ul class="evidence-list">
{ev_items}
        </ul>
      </details>
    </article>"""


def sort_recognitions(recognitions):
    return sorted(
        recognitions,
        key=lambda r: MOMENTUM_ORDER.index(r.get("momentum", "building"))
        if r.get("momentum", "building") in MOMENTUM_ORDER else 99
    )


CSS = """\
/* ── TOKENS ── */
:root {
  --bg:           #FAFAF5;
  --bg-warm:      #F2F0E8;
  --text:         #1C1A18;
  --text-2:       #5E5A53;
  --text-3:       #9A968F;
  --accent:       #B5451B;
  --rule:         #DDDAD0;
  --max:          680px;

  --c-building:    #3D5A8A; --c-building-bg:    #EDF1F9;
  --c-accel:       #2D6830; --c-accel-bg:       #EAF3EB;
  --c-peaking:     #9B3A10; --c-peaking-bg:     #FBF0EB;
  --c-fading:      #9A968F; --c-fading-bg:      #F2F0E8;
  --c-acute:       #8B1A1A; --c-acute-bg:       #FBEEEE;
  --c-persist:     #5E5A53; --c-persist-bg:     #F2F0E8;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg:           #131110;
    --bg-warm:      #1C1A17;
    --text:         #EDEAD3;
    --text-2:       #9C9880;
    --text-3:       #6A6758;
    --accent:       #CF6238;
    --rule:         #2C2920;

    --c-building:    #7A9AC4; --c-building-bg:    #151D2C;
    --c-accel:       #7AAF80; --c-accel-bg:       #151F16;
    --c-peaking:     #CF6238; --c-peaking-bg:     #261710;
    --c-fading:      #6A6758; --c-fading-bg:      #1C1A17;
    --c-acute:       #C44040; --c-acute-bg:       #261414;
    --c-persist:     #9C9880; --c-persist-bg:     #1C1A17;
  }
}

:root[data-theme="light"] {
  --bg: #FAFAF5; --bg-warm: #F2F0E8;
  --text: #1C1A18; --text-2: #5E5A53; --text-3: #9A968F;
  --accent: #B5451B; --rule: #DDDAD0;
  --c-building: #3D5A8A; --c-building-bg: #EDF1F9;
  --c-accel: #2D6830; --c-accel-bg: #EAF3EB;
  --c-peaking: #9B3A10; --c-peaking-bg: #FBF0EB;
  --c-fading: #9A968F; --c-fading-bg: #F2F0E8;
  --c-acute: #8B1A1A; --c-acute-bg: #FBEEEE;
  --c-persist: #5E5A53; --c-persist-bg: #F2F0E8;
}

:root[data-theme="dark"] {
  --bg: #131110; --bg-warm: #1C1A17;
  --text: #EDEAD3; --text-2: #9C9880; --text-3: #6A6758;
  --accent: #CF6238; --rule: #2C2920;
  --c-building: #7A9AC4; --c-building-bg: #151D2C;
  --c-accel: #7AAF80; --c-accel-bg: #151F16;
  --c-peaking: #CF6238; --c-peaking-bg: #261710;
  --c-fading: #6A6758; --c-fading-bg: #1C1A17;
  --c-acute: #C44040; --c-acute-bg: #261414;
  --c-persist: #9C9880; --c-persist-bg: #1C1A17;
}

/* ── RESET ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 16px;
  line-height: 1.65;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

/* ── MASTHEAD ── */
.masthead {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 20px;
  padding: 28px 32px;
  border-bottom: 1px solid var(--rule);
}

.pub-name {
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--text);
  text-decoration: none;
}

.pub-week {
  font-size: 12px;
  color: var(--text-3);
  letter-spacing: 0.04em;
}

/* ── LEDE ── */
.lede {
  max-width: var(--max);
  margin: 0 auto;
  padding: 52px 24px 48px;
  border-bottom: 1px solid var(--rule);
}

.lede-headline {
  font-family: "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
  font-size: clamp(28px, 5vw, 40px);
  font-weight: normal;
  line-height: 1.15;
  color: var(--text);
  text-wrap: balance;
  margin-bottom: 16px;
}

.lede-description {
  font-size: 15px;
  color: var(--text-2);
  line-height: 1.6;
  max-width: 520px;
  margin-bottom: 20px;
}

.lede-updated {
  font-size: 12px;
  color: var(--text-3);
  letter-spacing: 0.04em;
}

/* ── RECOGNITIONS ── */
.recognitions {
  max-width: var(--max);
  margin: 0 auto;
  padding: 0 24px 96px;
}

.recognition {
  padding: 48px 0;
  border-bottom: 1px solid var(--rule);
}

.recognition:last-child {
  border-bottom: none;
}

.recognition-title {
  font-family: "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
  font-size: clamp(19px, 3vw, 24px);
  font-weight: normal;
  line-height: 1.25;
  color: var(--text);
  text-wrap: balance;
  margin-bottom: 20px;
}

/* ── EXPLANATION ── */
.recognition-explanation {
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-2);
  margin-bottom: 28px;
}

/* ── EVIDENCE TOGGLE ── */
.evidence-details {
  margin-top: 24px;
}

.evidence-details > summary {
  list-style: none;
  cursor: pointer;
  user-select: none;
  -webkit-user-select: none;
}

.evidence-details > summary::-webkit-details-marker { display: none; }

.evidence-toggle {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 4px 0;
}

.evidence-toggle::after {
  content: "";
  display: inline-block;
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 5px solid var(--text-3);
  transition: transform 0.18s ease;
  position: relative;
  top: 1px;
}

.evidence-details[open] > summary .evidence-toggle::after {
  transform: rotate(180deg);
}

.ev-summary-count {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-3);
}

.ev-summary-new {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
  border: 1px solid var(--accent);
  padding: 1px 6px;
  border-radius: 2px;
}

.evidence-toggle:hover .ev-summary-count { color: var(--text-2); }
.evidence-toggle:hover::after { border-top-color: var(--text-2); }

/* ── EVIDENCE LIST ── */
.evidence-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-top: 12px;
  animation: evidenceIn 0.18s ease-out;
}

@keyframes evidenceIn {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.ev-item {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 0 16px;
  align-items: start;
  padding: 14px 0;
  border-top: 1px solid var(--rule);
}

.ev-item:last-child {
  border-bottom: 1px solid var(--rule);
}

.ev-meta {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding-top: 2px;
}

.ev-domain {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-3);
  line-height: 1.4;
}

.ev-new-badge {
  display: inline-block;
  font-size: 8px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
  border: 1px solid var(--accent);
  padding: 1px 5px;
  border-radius: 2px;
  width: fit-content;
}

.ev-date {
  font-size: 10px;
  color: var(--text-3);
  letter-spacing: 0.03em;
  font-style: normal;
}

.ev-item--new {
  box-shadow: -3px 0 0 var(--accent);
  padding-left: 12px;
}

.ev-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ev-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-2);
  margin: 0;
}

.ev-read-more {
  font-size: 12px;
  color: var(--text-3);
  text-decoration: none;
  letter-spacing: 0.02em;
}

.ev-read-more:hover {
  color: var(--accent);
}

/* ── FOOTER ── */
.footer {
  max-width: var(--max);
  margin: 0 auto;
  padding: 32px 24px 48px;
  display: flex;
  justify-content: space-between;
  border-top: 1px solid var(--rule);
}

.footer-name {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-3);
}

.footer-note {
  font-size: 12px;
  color: var(--text-3);
}

/* ── RESPONSIVE ── */
@media (max-width: 480px) {
  .masthead { padding: 20px 16px; }
  .lede     { padding: 36px 16px 32px; }
  .recognitions { padding: 0 16px 64px; }
  .footer   { padding: 24px 16px 40px; flex-direction: column; gap: 8px; }

  .ev-item {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  .ev-meta { flex-direction: row; flex-wrap: wrap; gap: 6px; align-items: baseline; }
  .ev-date { padding-top: 0; }
}

/* ── FOCUS ── */
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
"""


def render_page(data):
    week_label  = fmt_week(data["week"])
    updated_str = fmt_updated(data["last_updated"])

    recognitions = sort_recognitions(data.get("recognitions", []))
    count        = len(recognitions)

    cards = "\n\n".join(render_recognition(r) for r in recognitions)

    n = count if count > 0 else "No"
    description = (
        f"{n} recognition{'s' if count != 1 else ''} from this week. "
        "These aren't the biggest stories. "
        "They're the hidden dynamics that made many seemingly unrelated stories happen at the same time."
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Why Today? &middot; {html.escape(week_label)}</title>
  <style>
{CSS}  </style>
</head>
<body>

  <header class="masthead">
    <a href="../" class="pub-name">Why Today?</a>
    <span class="pub-week">{html.escape(week_label)}</span>
  </header>

  <section class="lede">
    <h1 class="lede-headline">What the week reveals.</h1>
    <p class="lede-description">{html.escape(description)}</p>
    <p class="lede-updated">{html.escape(updated_str)}</p>
  </section>

  <div class="recognitions">
{cards}
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
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_page(data))

    count = len(data.get("recognitions", []))
    print(f"Read   {DATA_PATH} ({count} recognitions)")
    print(f"Wrote  {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
