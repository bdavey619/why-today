# Why Today?

An editorial publication that transforms today's shared moments into timeless hidden questions.

Every edition answers one question the reader didn't know to ask — and leaves them seeing something they already knew differently.

**The reader's test:** *"I never thought about it that way."*

---

## Editions

| # | Date | Shared Moment | Hidden Question |
|---|------|--------------|-----------------|
| [001](editions/001-july-4-wrong-date/) | July 1, 2026 | America's 250th birthday | Why is July 4th America's birthday if it isn't the date of anything decisive? |
| [002](editions/002-heat-deaths/) | July 1, 2026 | Heat dome over the Pacific Northwest | What is the deadliest natural disaster in America? |
| [003](editions/003-penalty-kicks/) | July 1, 2026 | World Cup penalty shootout | Why does everyone know the safest penalty kick — and why can't anyone take it? |

---

## How an Edition Is Made

Every edition follows the same process:

1. **Editorial meeting** — survey today's shared moments, generate hidden questions, choose one
2. **Research** — find the surprising sentence; let the question evolve
3. **Writing** — build the edition around the surprising sentence
4. **Review** — document what changed, what almost happened, what was learned

Each edition folder contains:
- `edition.html` — the published edition
- `meeting.md` — the editorial meeting that produced it
- `review.md` — the post-edition review
- `deposit.md` — what was deposited into the knowledge base

---

## Repository Structure

```
editions/          Each edition: HTML + meeting + review + deposit
site/              Static site (deploys to bdavey.co/why-today)
docs/              Editorial operating system
knowledge/         Compounding knowledge base
templates/         Meeting, review, deposit, and edition templates
```

## Editorial Operating System

The process is documented in [`docs/`](docs/):

- [`EDITORIAL_PLAYBOOK.md`](docs/EDITORIAL_PLAYBOOK.md) — how to produce an edition, step by step
- [`ALGORITHM.md`](docs/ALGORITHM.md) — the versioned selection and construction algorithms
- [`HEURISTICS.md`](docs/HEURISTICS.md) — accumulated editorial rules
- [`PATTERNS.md`](docs/PATTERNS.md) — recurring structures observed across editions
- [`FAILURE_MODES.md`](docs/FAILURE_MODES.md) — named failure modes and how to avoid them
- [`QUESTIONS.md`](docs/QUESTIONS.md) — what we still don't know
- [`KNOWLEDGE_ARCHITECTURE.md`](docs/KNOWLEDGE_ARCHITECTURE.md) — how the knowledge base compounds

---

## Current Status

Phase 1 — Editorial Discovery. Producing Editions 004–010.

See [`PROJECT_STATE.md`](PROJECT_STATE.md) for current focus, open questions, and success criteria.
