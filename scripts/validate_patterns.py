#!/usr/bin/env python3
"""
Validator for Why Today? recognitions data.

Reads docs/patterns/data.json and verifies structural integrity before publishing.
Exits with code 1 on any validation failure; prints all errors before exiting.

Usage: python3 scripts/validate_patterns.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "docs" / "patterns" / "data.json"

VALID_MOMENTUMS = {"building", "accelerating", "peaking", "fading", "acute", "persistent"}
URL_RE = re.compile(r"^https?://[^\s]+\.[^\s]+")


def validate(data):
    errors = []

    if "week" not in data:
        errors.append("Missing top-level field: week")
    if "last_updated" not in data:
        errors.append("Missing top-level field: last_updated")
    if "recognitions" not in data:
        errors.append("Missing top-level field: recognitions")
        return errors

    recognitions = data["recognitions"]
    if not isinstance(recognitions, list) or len(recognitions) == 0:
        errors.append("recognitions must be a non-empty list")
        return errors

    seen_ids = set()

    for i, r in enumerate(recognitions):
        rid = r.get("id", f"[recognition {i}]")
        prefix = f"Recognition '{rid}'"

        for field in ("id", "title", "explanation", "momentum", "evidence"):
            if field not in r:
                errors.append(f"{prefix}: missing field '{field}'")

        if rid in seen_ids:
            errors.append(f"{prefix}: duplicate id")
        seen_ids.add(rid)

        momentum = r.get("momentum", "")
        if momentum not in VALID_MOMENTUMS:
            errors.append(f"{prefix}: invalid momentum '{momentum}'")

        explanation = r.get("explanation", "")
        if len(explanation) < 20:
            errors.append(f"{prefix}: explanation too short")

        evidence = r.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{prefix}: evidence must be a list")
            continue

        if len(evidence) < 3:
            errors.append(f"{prefix}: too few evidence items ({len(evidence)}, minimum 3)")
        if len(evidence) > 4:
            errors.append(f"{prefix}: too many evidence items ({len(evidence)}, maximum 4)")

        domains_seen = set()
        for j, ev in enumerate(evidence):
            ev_prefix = f"{prefix} evidence[{j}]"

            domain = ev.get("domain", "").strip()
            text = ev.get("text", "").strip()
            url = ev.get("url", "").strip()

            if not domain:
                errors.append(f"{ev_prefix}: missing or empty 'domain'")
            if not text:
                errors.append(f"{ev_prefix}: missing or empty 'text'")

            if not url:
                errors.append(f"{ev_prefix}: missing URL — evidence without a source cannot be published")
            elif not URL_RE.match(url):
                errors.append(f"{ev_prefix}: URL does not look valid: '{url}'")

            # Optional fields — validate format if present
            date_val = ev.get("date", "")
            if date_val and not isinstance(date_val, str):
                errors.append(f"{ev_prefix}: 'date' must be a string")

            is_new_val = ev.get("is_new", False)
            if not isinstance(is_new_val, bool):
                errors.append(f"{ev_prefix}: 'is_new' must be a boolean")

            if domain and domain in domains_seen:
                errors.append(f"{prefix}: duplicate domain '{domain}' — each evidence item must come from a different domain")
            domains_seen.add(domain)

    return errors


def main():
    if not DATA_PATH.exists():
        print(f"ERROR: {DATA_PATH} not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(DATA_PATH.read_text())
    errors = validate(data)

    recognition_count = len(data.get("recognitions", []))
    evidence_count = sum(len(r.get("evidence", [])) for r in data.get("recognitions", []))

    if errors:
        print(f"VALIDATION FAILED — {len(errors)} error(s):\n", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

    print(f"OK  {DATA_PATH}")
    print(f"    {recognition_count} recognition(s), {evidence_count} evidence item(s), all URLs present")


if __name__ == "__main__":
    main()
