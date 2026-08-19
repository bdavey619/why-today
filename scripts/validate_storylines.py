#!/usr/bin/env python3
"""
Validator for Why Today? cabinet data.

Reads docs/storylines/data.json and verifies structural integrity and source
freshness before publishing.

The rule this exists to enforce: a storyline's link must support the newest
sentence on its card. `last_seen` and `url` are independent fields, so bumping
a storyline refreshes its timestamp without touching its source — the card can
advertise freshness the link does not have. This catches that drift.

It also enforces the split between `observation` and `history`. Left alone, an
update session appends the day's development to `observation` and the field
grows a paragraph a week — which is both unreadable and useless for telling what
changed. `observation` is the standing description and is capped; developments
belong in dated `history` notes, which is what the card renders as "what changed".

Entries whose source is a reference rather than a report (seasonal rituals,
structural explainers) can set "source_evergreen": true to opt out of the
freshness check. Dormant entries are skipped — they are set aside, not current.

Exits 1 on any error. Warnings are printed but do not block a render.

Usage: python3 scripts/validate_storylines.py
"""

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "docs" / "storylines" / "data.json"

# A source may lag the last bump by this much before we complain.
STALE_SOURCE_DAYS = 3
# Mirrors STALE_AFTER_DAYS in render_storylines.py — past this, prune drops it.
STALE_AFTER_DAYS = 3

# An observation is a standing description, not a running log. Past the warn
# line it has started absorbing developments; past the error line it is a wall.
OBSERVATION_WARN_WORDS = 45
OBSERVATION_MAX_WORDS = 60
# A change note is one development, not a briefing.
NOTE_WARN_WORDS = 40

VALID_STREAMS = {
    "natural_world", "human_rituals", "places",
    "curiosities", "markets", "headlines",
}

URL_RE = re.compile(r"^https?://[^\s]+\.[^\s]+")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def word_count(text):
    return len((text or "").split())


def validate(data, now):
    errors, warnings = [], []

    for field in ("week_start", "last_updated", "storylines"):
        if field not in data:
            errors.append(f"Missing top-level field: {field}")

    # cycle_start is what makes "new" and "updated" derivable instead of
    # hand-flagged. Forget to advance it and every card reads as unchanged.
    cycle_start = None
    if "cycle_start" not in data:
        warnings.append(
            "Missing top-level 'cycle_start' — set it to the previous session's "
            "last_updated so the page can tell new from updated"
        )
    else:
        try:
            cycle_start = parse_dt(data["cycle_start"])
        except ValueError:
            errors.append(f"Unparseable cycle_start '{data['cycle_start']}'")
        else:
            if "last_updated" in data:
                try:
                    if cycle_start >= parse_dt(data["last_updated"]):
                        errors.append(
                            "cycle_start must be earlier than last_updated — it marks "
                            "where this session started, not where it ended"
                        )
                except ValueError:
                    errors.append(f"Unparseable last_updated '{data['last_updated']}'")
    if "storylines" not in data:
        return errors, warnings

    storylines = data["storylines"]
    if not isinstance(storylines, list):
        errors.append("storylines must be a list")
        return errors, warnings

    seen_ids = set()

    for i, s in enumerate(storylines):
        sid = s.get("id", f"[storyline {i}]")
        prefix = f"Storyline '{sid}'"

        for field in ("id", "first_seen", "last_seen"):
            if field not in s:
                errors.append(f"{prefix}: missing field '{field}'")

        if sid in seen_ids:
            errors.append(f"{prefix}: duplicate id")
        seen_ids.add(sid)

        stream = s.get("stream") or "headlines"
        if stream not in VALID_STREAMS:
            errors.append(f"{prefix}: invalid stream '{stream}'")

        if not (s.get("title") or s.get("moment")):
            errors.append(f"{prefix}: needs a 'title' or a 'moment' to render a card")

        n_words = word_count(s.get("observation"))
        if n_words > OBSERVATION_MAX_WORDS:
            errors.append(
                f"{prefix}: observation is {n_words} words (max {OBSERVATION_MAX_WORDS}) "
                f"— move the developments into dated 'history' notes"
            )
        elif n_words > OBSERVATION_WARN_WORDS:
            warnings.append(
                f"{prefix}: observation is {n_words} words (aim for "
                f"{OBSERVATION_WARN_WORDS}) — it is starting to absorb the change log"
            )

        history = s.get("history") or []
        if not isinstance(history, list):
            errors.append(f"{prefix}: history must be a list")
            history = []
        newest_note = None
        for h in history:
            if not isinstance(h, dict) or "date" not in h or "note" not in h:
                errors.append(f"{prefix}: every history entry needs a 'date' and a 'note'")
                continue
            try:
                hd = parse_dt(h["date"])
            except ValueError:
                errors.append(f"{prefix}: unparseable history date '{h['date']}'")
                continue
            if hd > now + timedelta(days=1):
                errors.append(f"{prefix}: history date '{h['date']}' is in the future")
            if newest_note is None or hd > newest_note:
                newest_note = hd
            nw = word_count(h["note"])
            if nw > NOTE_WARN_WORDS:
                warnings.append(
                    f"{prefix}: history note of {h['date'][:10]} is {nw} words "
                    f"(aim for {NOTE_WARN_WORDS}) — one development per note"
                )

        # Dormant entries are set aside, not current — skip source checks.
        if s.get("status") == "dormant":
            continue

        if "last_seen" not in s:
            continue

        try:
            last_seen = parse_dt(s["last_seen"])
        except ValueError:
            errors.append(f"{prefix}: unparseable last_seen '{s['last_seen']}'")
            continue

        # A bump into this cycle with nothing to show for it: the timestamp moved
        # and the card says the same thing it said yesterday.
        if cycle_start is not None and last_seen >= cycle_start:
            if newest_note is None or newest_note < cycle_start:
                warnings.append(
                    f"{prefix}: bumped this cycle with no history note — the card will "
                    f"render as unchanged. Add a note, or leave last_seen alone"
                )

        if now - last_seen >= timedelta(days=STALE_AFTER_DAYS):
            age = (now - last_seen).days
            warnings.append(
                f"{prefix}: last_seen is {age}d old — the next render will prune it"
            )

        url = (s.get("url") or "").strip()
        if not url:
            errors.append(f"{prefix}: active storyline has no URL")
        elif not URL_RE.match(url):
            errors.append(f"{prefix}: URL does not look valid: '{url}'")

        if s.get("source_evergreen"):
            continue

        source_date = (s.get("source_date") or "").strip()
        if not source_date:
            errors.append(
                f"{prefix}: missing 'source_date' — set it, or mark "
                f"'source_evergreen': true if the link is a reference, not a report"
            )
            continue
        if not DATE_RE.match(source_date):
            errors.append(f"{prefix}: source_date must be YYYY-MM-DD, got '{source_date}'")
            continue

        sd = parse_date(source_date)
        if sd > now + timedelta(days=1):
            errors.append(f"{prefix}: source_date '{source_date}' is in the future")
            continue

        drift = (last_seen.date() - sd.date()).days
        if drift > STALE_SOURCE_DAYS:
            warnings.append(
                f"{prefix}: source is {drift}d older than last_seen "
                f"({source_date} vs {last_seen.date().isoformat()}) — "
                f"re-source it or confirm the link still supports the card"
            )

    return errors, warnings


def main():
    if not DATA_PATH.exists():
        print(f"ERROR: {DATA_PATH} not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(DATA_PATH.read_text())
    now = datetime.now(timezone.utc)
    errors, warnings = validate(data, now)

    active = [s for s in data.get("storylines", []) if s.get("status") != "dormant"]
    dormant = [s for s in data.get("storylines", []) if s.get("status") == "dormant"]

    if errors:
        print(f"VALIDATION FAILED — {len(errors)} error(s):\n", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

    print(f"OK  {DATA_PATH}")
    print(f"    {len(active)} active, {len(dormant)} dormant, all active sources dated")

    # What this session actually did to the cabinet. A run that bumps ten cards
    # and collects none is the failure mode this line exists to make obvious.
    cs = data.get("cycle_start")
    if cs:
        cycle_start = parse_dt(cs)
        n_new = n_updated = 0
        for s in active:
            if parse_dt(s["first_seen"]) >= cycle_start:
                n_new += 1
                continue
            notes = [parse_dt(h["date"]) for h in (s.get("history") or []) if "date" in h]
            if notes and max(notes) >= cycle_start:
                n_updated += 1
        n_held = len(active) - n_new - n_updated
        print(f"    this cycle: {n_new} new, {n_updated} updated, {n_held} held")
        if n_new == 0:
            warnings.append(
                "no new storylines this cycle — the cabinet only bumped what it "
                "already had. Collect from the daily sources before publishing"
            )

    if warnings:
        print(f"\n⚠️  {len(warnings)} warning(s):", file=sys.stderr)
        for w in warnings:
            print(f"    {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
