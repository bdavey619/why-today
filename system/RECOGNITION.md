# Pattern Recognition

*The editorial philosophy governing Why Today?'s publication layer. The cabinet is the research. The published patterns are the editorial work. Every architectural decision about recognition should be checked against this document.*

---

## The Pipeline

```
Raw observations (Cabinet)
        ↓
  Pattern Recognition
        ↓
  Published Patterns
```

The cabinet is not the product. The cabinet is the research.

The publication is the editorial act of recognizing patterns across the research.

The value is not collecting interesting observations. The value is helping readers recognize relationships they wouldn't have seen themselves.

The publication should not ask readers to synthesize the cabinet. That's the editorial job.

---

## What a Pattern Is

A pattern is an editorial observation that **explains** multiple observations from different domains.

It is not the connection. It is the explanation of the connection.

The test: if you stated the pattern to someone, would observations from several unrelated domains — ocean ecology, insurance pricing, seasonal harvests — suddenly feel less surprising? If yes, you have a pattern. If they just feel more *connected*, you have a cluster.

The best patterns produce a brief "wait…" moment. Something the reader couldn't have seen from any single observation, but that feels inevitable once they have it.

---

## What a Pattern Is Not

- A topic category ("climate stories this week")
- A news cluster ("five stories about AI")
- A summary of related events
- A trend piece built from similar headlines

The distinction: a category groups things that look similar. A pattern explains things that look different.

---

## How Editorial Judgment Works

The recognition step is not mechanical. It requires noticing — the moment of asking: *Why are these four things, which belong to completely different worlds, all doing the same thing this week?*

The noticing question isn't "which observations are similar?" It's: **which observations shouldn't be in the same room together — but are?**

A strong pattern candidate: observations from domains that don't share vocabulary — fisheries, insurance, agriculture, real estate — all explicable by a single underlying pressure.

A weak pattern candidate: observations that share a topic, a region, or a time period, but don't produce an explanatory insight when combined.

---

## What Deserves Publication

A pattern deserves publication if it passes three tests:

**Does it explain something?**
The pattern should identify a mechanism — not just observe that multiple things are happening, but name why.

**Is the explanation non-obvious?**
If the connection is visible from any single observation, it's not a pattern — it's context. The explanation should be the thing a reader couldn't arrive at without seeing all the evidence together.

**Does it change how the reader sees the week?**
The test is not information — it's a mental model. After reading this pattern, what will the reader notice that they wouldn't have noticed before?

If the answer to any of these is no, keep looking.

---

## What AI Should Do Here

The AI's job in the recognition pass is not to cluster. It's to notice.

The recognition prompt should direct the AI to ask: *What observations from different professional worlds are all evidence of the same underlying shift?*

The AI should be given an explicit count target (4–6 patterns) and explicit rules for evidence selection (3–4 items per pattern, different domains, source URLs required). Fewer strong patterns beat more weak ones every time.

The AI should be told what not to do: don't group observations that share a topic; don't produce thematic categories; don't write explanations that could attach to any week. The pattern explanation should be specific to this week.

---

## The Living Edition

Why Today? publishes one living edition per week, updated daily.

The editorial question after each day's new observations:

**Did today's observations materially strengthen, weaken, or change any existing pattern?**

Most days, the right answer will be to refine an existing pattern — not create a new one:
- Improve the explanation
- Replace a weaker evidence item with a stronger one
- Sharpen the title
- Merge two patterns if they're really the same underlying pressure
- Retire a pattern if it no longer holds

A pattern should earn its place on the page. It should not remain simply because it was generated, and should not be replaced simply because something new arrived.

---

## Evidence Standards

For each published pattern, select 3–4 evidence items. Rules:

- Each item must come from a different domain
- Each item must include a source URL — evidence that can't be followed is incomplete
- Order from most surprising to most clarifying: the first item makes the reader curious; the last makes the pattern feel undeniable
- One or two sentences per item — concrete and specific, not summarized

A fifth strong example weakens the four strong ones. The quality of the evidence is the quality of the pattern.

---

## What Success Looks Like

Why Today? works if a reader finishes with a small number of durable mental models — not a large number of facts.

The mark of success: *"I hadn't connected those things before. Now I can't un-see it."*

Not: *"Those are interesting stories."*

The distinction is the test.

---

## The Why Today Constraint

Patterns should feel like discoveries, not analyses.

The writing should be concrete, curious, and specific — not academic. If an explanation needs more than four sentences, the pattern probably isn't sharp enough yet.

Readers come to Why Today? to have the present moment feel more interesting and legible, not more complicated. Every pattern should enlarge their sense of the world, not burden it.

The trap: getting so interested in the pattern-recognition machinery that the publication starts to feel like a McKinsey report. Why Today?'s value has always been making the ordinary world feel stranger and richer. The architecture should serve that, not replace it.

---

*This document governs the publication layer. The collection phase is governed by `system/COLLECTING.md`. The recognition pass prompt is in `scripts/RECOGNITION_PROMPT.md`. Edition-level construction patterns live in `system/PATTERNS.md`.*
