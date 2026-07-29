#!/usr/bin/env python3
"""
Renderer for the Why Today? patterns publication.

Reads docs/patterns/data.json and writes docs/patterns/index.html.
The patterns page is the primary reader-facing publication.

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
                "patterns": []}
    return json.loads(DATA_PATH.read_text())


def fmt_week(iso_date):
    d = datetime.fromisoformat(iso_date)
    return d.strftime("Week of %B %-d, %Y")


def fmt_updated(iso_dt):
    dt = datetime.fromisoformat(iso_dt.replace("Z", "+00:00"))
    return dt.strftime("Updated %B %-d, %Y")


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
}


def source_label(url):
    try:
        host = urlparse(url).netloc.lstrip("www.")
        return SOURCE_LABELS.get(host, host)
    except Exception:
        return ""


def render_evidence_item(item):
    domain = html.escape(item.get("domain", ""))
    text   = html.escape(item.get("text", ""))
    url    = item.get("url", "").strip()

    if url:
        read_more = (
            f'\n          <a href="{html.escape(url)}" class="ev-read-more" '
            f'target="_blank" rel="noopener">Read more &#x2192;</a>'
        )
    else:
        read_more = ""

    return f"""\
        <li class="ev-item">
          <span class="ev-domain">{domain}</span>
          <div class="ev-body">
            <p class="ev-text">{text}</p>{read_more}
          </div>
        </li>"""


def render_pattern(p):
    pid         = html.escape(p.get("id", ""))
    title       = html.escape(p.get("title", ""))
    explanation = html.escape(p.get("explanation", ""))
    evidence    = p.get("evidence", [])[:4]

    ev_items = "\n".join(render_evidence_item(e) for e in evidence)

    return f"""\
    <article class="pattern" id="{pid}">
      <h2 class="pattern-title">{title}</h2>
      <p class="pattern-explanation">{explanation}</p>
      <ul class="evidence-list">
{ev_items}
      </ul>
    </article>"""


def sort_patterns(patterns):
    return sorted(
        patterns,
        key=lambda p: MOMENTUM_ORDER.index(p.get("momentum", "building"))
        if p.get("momentum", "building") in MOMENTUM_ORDER else 99
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

/* ── PATTERNS ── */
.patterns {
  max-width: var(--max);
  margin: 0 auto;
  padding: 0 24px 96px;
}

.pattern {
  padding: 48px 0;
  border-bottom: 1px solid var(--rule);
}

.pattern:last-child {
  border-bottom: none;
}

.pattern-title {
  font-family: "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
  font-size: clamp(19px, 3vw, 24px);
  font-weight: normal;
  line-height: 1.25;
  color: var(--text);
  text-wrap: balance;
  margin-bottom: 20px;
}

/* ── EXPLANATION ── */
.pattern-explanation {
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-2);
  margin-bottom: 28px;
}

/* ── EVIDENCE ── */
.evidence-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0;
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

.ev-domain {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-3);
  padding-top: 2px;
  line-height: 1.5;
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
  .patterns { padding: 0 16px 64px; }
  .footer   { padding: 24px 16px 40px; flex-direction: column; gap: 8px; }

  .ev-item {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  .ev-domain { padding-top: 0; }
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

    patterns = sort_patterns(data.get("patterns", []))
    count    = len(patterns)

    cards = "\n\n".join(render_pattern(p) for p in patterns)

    n = count if count > 0 else "No"
    description = (
        f"{n} underlying pattern{'s' if count != 1 else ''} explain much of what happened this week. "
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

  <div class="patterns">
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

    count = len(data.get("patterns", []))
    print(f"Read   {DATA_PATH} ({count} patterns)")
    print(f"Wrote  {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
