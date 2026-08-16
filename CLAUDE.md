# Why Today? — Operational Guide for Claude

This file is the persistent process guide for Claude Code sessions working on this project.

---

## What This Project Is

*Why Today?* is a weekly publication that finds the durable question underneath a shared moment in the news. Two automated systems support the editorial work:

1. **Cabinet of Curiosities** (`docs/storylines/`) — a live feed of observations, threads, and raw material organized into six streams. Rendered by `scripts/render_storylines.py`.
2. **Patterns / Recognitions** (`docs/patterns/`) — named cross-domain patterns that have accumulated enough evidence to be called out explicitly. Rendered by `scripts/render_patterns.py`.

Both deploy to GitHub Pages via GitHub Actions when pushed to `main`.

---

## Daily Sources (User's Core Feed)

finviz, bloomberg, reuters, yahoo finance, ESPN, 10yr / 30yr treasury yields

Cabinet storylines and recognitions should stay grounded in what surfaces from these sources. When a storyline hasn't been visible in these feeds, it's a candidate for dormancy.

---

## Cabinet of Curiosities — Key Rules

**Prune-stale**: `render_storylines.py` removes any storyline with `last_seen` more than 3 days old (dormant entries are preserved). Every active storyline must be bumped at least every 3 days or it disappears on next render.

**Source freshness**: `last_seen` and `url` are independent fields. Bumping a storyline refreshes its *timestamp* without touching its *source*, so a card can advertise freshness its link doesn't have — or worse, make claims the linked article predates.

The rule: **the URL must support the newest sentence on the card.** If you bump a storyline with new facts, replace the source with wherever those facts came from. The bump and the re-source are one action, not two.

Every active storyline carries a `source_date` (`YYYY-MM-DD`) — the publication date of its link. `validate_storylines.py` errors on a missing one and warns when it lags `last_seen` by more than 3 days. Entries whose link is a reference rather than a report — seasonal rituals, structural explainers — set `"source_evergreen": true` to opt out of the freshness check. Dormant entries are skipped.

**Rollover**: `maybe_roll_over()` fires when `now - week_start >= 7 days`. It archives the entire cabinet (active + dormant) to `docs/storylines/archive/<week_start>.json` and returns an empty cabinet. Always check `week_start` before an unattended render.

**Week sync**: `patterns["week"]` must equal `storylines["week_start"]`. `validate_patterns.py` warns if they diverge. Keep them in sync when extending the week or triggering a rollover.

**Streams** (render order): natural_world → human_rituals → places → curiosities → markets → headlines

**Rollover procedure**: When intentionally wiping the cabinet, run `render_storylines.py` *after* `week_start` has passed its 7-day mark — or manually clear `storylines` and reset `week_start` in the data file. Re-seed immediately with the highest-priority storylines.

---

## Update Session Workflow

Every update session:

1. Check `week_start` — is rollover imminent? If so, decide: extend the week or let it roll.
2. Bump all storylines that are still live (anything with `last_seen` approaching 3 days needs a refresh or dormancy decision). Re-source as you bump — a new fact needs the link that carries it, and a new `source_date`.
3. Run the recognition audit (see below).
4. Run `scripts/render_storylines.py` and `scripts/render_patterns.py`.
5. Run `scripts/validate_storylines.py` and `scripts/validate_patterns.py` — resolve any warnings before committing.
6. Commit and push to `main`.

---

## Recognition Review Process

**Run this audit on every update session, not just at weekly rollover.**

The recognitions are the publication's most valuable artifact — the named patterns that cross-domain evidence has earned. They should turn over faster than the cabinet, not slower.

### When to retire a recognition

- Any evidence item is > 10 days old and cannot be refreshed with a new development
- The pattern has resolved (the situation ended, the condition changed)
- Momentum has clearly peaked and nothing new is accumulating

Do not let a recognition sit stale because retiring it feels like losing something. An archived recognition is still available in `docs/patterns/archive/`.

### When to add a new recognition

- A storyline has appeared 3+ times across different domains (Security + Shipping + Markets, for example) and the cross-domain connection can be named
- Ask: what is the single sentence that ties the domains together? If it's sayable in one sentence, it's probably nameable.
- Don't wait for "enough" evidence — three strong items from three different domains is enough to name a pattern.

### Momentum values

`building` → `accelerating` → `peaking` → `fading` → (`acute` | `persistent`)

- **acute**: a time-bounded crisis pattern (wildfires, military operations) — intense, will end
- **persistent**: a structural pattern that resists change — slow-moving, no obvious endpoint

### Evidence rules

- 3–4 evidence items per recognition; one domain per item
- URL required for every item
- Most surprising item first
- `is_new: true` marks current-cycle additions; reset all others to `false` at end of each update session

### Archive process

Move retired recognitions to `docs/patterns/archive/<recognition-id>.json` with a `retired` field noting the date and reason. Remove from `data.json`.

---

## Recognition Audit Questions (ask every session)

1. Is any existing recognition's evidence > 10 days old with nothing new feeding it?
2. Has the pattern's momentum clearly peaked or resolved?
3. Did today's storylines produce a cross-domain convergence worth naming?
4. Are there 3+ storylines from different domains that share a single underlying explanation?

---

## Script Reference

| Script | Purpose |
|---|---|
| `scripts/render_storylines.py` | Renders cabinet HTML; prunes stale; handles rollover |
| `scripts/render_patterns.py` | Renders recognitions HTML |
| `scripts/validate_storylines.py` | Validates cabinet data; errors on missing URL/`source_date`, warns on source drift |
| `scripts/validate_patterns.py` | Validates patterns data; warns on week mismatch, missing URLs, stale evidence |

Run all four in sequence, resolve warnings, then commit.

---

## Branch

All work goes to `main`. GitHub Actions handles deployment.
