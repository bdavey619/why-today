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

**Observation vs. history — the split that keeps cards readable**: a card has two text fields and they do different jobs.

- `observation` is the **standing description**: what this thing is and why it is worth watching. It should read the same next week as it does today. Capped at 45 words (validator warns), 60 hard (validator errors).
- `history` is the **dated record of what changed**: `[{"date": "<ISO>", "note": "..."}]`, one note per session that produced a real development, ~30 words each.

The failure mode this replaces: appending each session's development to `observation` until it is a 200-word wall that nobody can diff against yesterday. If you have a new fact, it goes in a **new history note**, not into the observation. Touch `observation` only when the standing description itself is wrong.

The newest history note renders **in the open** on the card — it is the card's answer to "what changed?" — and older notes fold into a disclosure.

**New vs. updated vs. held**: never flagged by hand. `data.json` carries a top-level `cycle_start`; at the start of an update session set it to the *previous* session's `last_updated`, then set `last_updated` to now. From those two timestamps the renderer derives, per card:

| state | rule | chip |
|---|---|---|
| **new** | `first_seen` >= `cycle_start` | `new` (accent outline) |
| **updated** | newest history note >= `cycle_start` | `updated` (blue) |
| **held** | neither — bumped or untouched, nothing changed | none |

The page header prints the tally: `This update: N new, N updated, N held`. `validate_storylines.py` warns when a card's `last_seen` moved into the cycle with no history note behind it — a silent bump — and warns when the whole cycle produced **0 new** storylines.

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

1. Set `cycle_start` to the previous session's `last_updated` before you change anything else. This is what lets the page distinguish what you added from what you merely bumped.
2. Check `week_start` — is rollover imminent? If so, decide: extend the week or let it roll.
3. **Collect before you bump.** Go to the daily sources and find what is actually new. A session that only refreshes timestamps on cards it already had is not an update — it produces a page that says "updated" and shows the reader nothing. Aim for at least one genuinely new storyline per session; if the feeds honestly produced none, retire or dormant something instead of leaving the cabinet static.
4. Bump the storylines that are still live (anything with `last_seen` approaching 3 days needs a refresh or dormancy decision). For each one that actually moved, **add a history note** — do not extend `observation`. Re-source as you bump: a new fact needs the link that carries it, and a new `source_date`.
5. Run the recognition audit (see below).
6. Set `last_updated` to now.
7. Run `scripts/render_storylines.py` and `scripts/render_patterns.py`.
8. Run `scripts/validate_storylines.py` and `scripts/validate_patterns.py` — resolve any warnings before committing. In particular: "0 new this cycle" and "bumped with no history note" mean go back to step 3.
9. Commit and push to `main`.

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
| `scripts/validate_storylines.py` | Validates cabinet data; errors on missing URL/`source_date` and over-long observations, warns on source drift, silent bumps, and cycles with nothing new |
| `scripts/validate_patterns.py` | Validates patterns data; warns on week mismatch, missing URLs, stale evidence |

Run all four in sequence, resolve warnings, then commit.

---

## Branch

All work goes to `main`. GitHub Actions handles deployment.
