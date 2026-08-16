#!/usr/bin/env python3
"""
Validator for Why Today? cabinet data.

Reads docs/storylines/data.json and verifies structural integrity and source
freshness before publishing.

The rule this exists to enforce: a storyline's link must support the newest
sentence on its card. `last_seen` and `url` are independent fields, so bumping
a storyline refreshes its timestamp without touching its source — the card can
advertise freshness the link does not have. This catches that drift.

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


def validate(data, now):
    errors, warnings = [], []

    for field in ("week_start", "last_updated", "storylines"):
        if field not in data:
            errors.append(f"Missing top-level field: {field}")
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

    if warnings:
        print(f"\n⚠️  {len(warnings)} warning(s):", file=sys.stderr)
        for w in warnings:
            print(f"    {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
