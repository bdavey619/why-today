# Recognitions

*The governing definition of the Why Today? weekly recognitions publication.*

---

## The Editorial Unit

A **recognition** is what a reader gains from encountering this publication — not a summary of the week's news, but a frame that permanently changes how they notice the world.

The pipeline reflects this:

- **Observations** are collected from the week's events
- **The system identifies connections** across domains
- **The reader gains a recognition**

The reader is the subject. The recognition is what they leave with.

The cabinet provides observations. The recognizer is responsible for forgetting their boundaries.

---

## The Tests

**Primary test:**

> A recognition names something precisely enough that the reader can notice it again elsewhere.

**Stronger test:**

> Once seen, is it difficult to unsee?

A recognition that passes the stronger test is irreversible — not a piece of information that can be forgotten, but a lens the reader now carries permanently.

---

## What a Recognition Is Not

A recognition is not:

- **A label for a topic.** "AI as Geopolitical Terrain" names a subject. "The AI race has stopped being company vs. company — it's now nation vs. nation" is a recognition.
- **A summary of this week's news.** The news is evidence. The recognition is what the evidence reveals.
- **An observation that resolves itself.** A recognition creates forward motion — the reader immediately wants to apply it to something else.

---

## The Editorial Standard

Every recognition should pass these four tests:

1. **It expresses a clear claim, not just a topic.** A claim can be agreed with, disagreed with, or tested. A topic cannot.
2. **It gives the reader a new lens for interpreting events.** After reading it, the reader sees differently — not just more.
3. **The reader could repeat it naturally in conversation the next day.** If it requires the full explanation to be intelligible, the frame isn't portable enough.
4. **After reading it, the supporting evidence feels inevitable.** The evidence should feel like proof, not illustration.

---

## On Durability

A recognition should survive the story that surfaced it.

Ask: if the news event that made this recognition visible disappeared tomorrow, would the recognition still be worth holding?

- "This week, four institutions kept the authority and quietly removed the accountability" — survives the specific events; names a recurring structure
- "The modern calendar forgot a season" — survives any particular week; names a permanent absence

The evidence is dated. The recognition is not.

---

## Process

Recognitions are not extracted from stories. They emerge from held attention across the whole cabinet. The question is not *what recognition belongs to this story?* but *what stories belong to this recognition?*

**Stage 1 — Immersion**

Read the entire cabinet without producing anything. No notes, no candidate recognitions, no interim analysis. The goal is to hold the full week in mind simultaneously. Any summary written during Stage 1 becomes a new abstraction layer between the material and the synthesis — that layer is what Stage 2 is designed to eliminate.

**Stage 2 — Incubation and Synthesis**

The cabinet disappears. No storyline names, no domains, no sources.

Before generating anything: sit with the material. Let unrelated things collide. Recognitions often emerge from held attention rather than immediate analysis — the pause matters. Only once those collisions begin producing something should anything be written down.

The question is not *what do I now understand?* but *what became recognizable?*

- What became visible this week that is usually invisible?
- What did I suddenly have language for?
- What truth now feels obvious that didn't have a name before?
- What would make a reader stop and think, "I've felt that before, but I never knew how to say it"?

A recognition doesn't usually feel like learning something new. It feels like finally putting words to something you already half-knew. Generate candidates from that feeling, not from explanation.

Express each candidate as a single complete sentence. No evidence, no explanation. Do not organize by domain or story.

**Stage 3 — Refine**

Apply the four editorial tests to each candidate. Merge candidates that are different expressions of the same underlying recognition. Split any candidate that requires two separate insights to be legible. Discard observations — a claim says *this is how things work*, not *this happened*.

Note the scale of each surviving candidate: perceptual, seasonal, institutional, technological, civilizational. A strong edition includes recognitions from more than one scale.

**Stage 4 — Return to Evidence**

Now and only now, return to the cabinet. For each surviving candidate, search for 3–4 items that show the recognition operating in distinct domains. Evidence is assigned to recognitions — recognitions are not generated from evidence.

If the cabinet cannot support a recognition with evidence from at least 3 distinct domains, the recognition is discarded — not because it is wrong, but because this edition is not the right moment for it. Evidence from outside the cabinet may be added if the recognition is strong but underserved.

---

## Structure

Each recognition has three parts:

**Title** — A complete sentence. A claim the reader can hold in memory and repeat. Short enough to be carried without the explanation.

**Explanation** — 100–250 words. Makes the recognition's insight legible before the evidence is read. Does not summarize the evidence; anticipates it.

**Evidence** — 3–4 source items from distinct domains. Dated. Each item shows the recognition operating in a different domain, making the cross-domain pattern visible.

---

## Schema

Recognitions are stored in `docs/patterns/data.json` under the `recognitions` array. Each recognition:

\`\`\`json
{
  "id": "kebab-case-identifier",
  "title": "A complete sentence expressing the recognition.",
  "explanation": "...",
  "momentum": "building | accelerating | peaking | fading | acute | persistent",
  "evidence": [
    {
      "domain": "Domain Name",
      "text": "One to three sentences describing the evidence.",
      "url": "https://...",
      "date": "YYYY-MM-DD",
      "is_new": false
    }
  ]
}
\`\`\`

Maximum 6 recognitions per edition. Minimum 3 evidence items per recognition, maximum 4.

---

## What Distinguishes Recognition from Pattern

The publication previously used "pattern" as the internal editorial unit. The rename to "recognition" is not cosmetic — it changes the question being asked.

**Pattern** asks: *What recurring structure do I observe in the world?*

**Recognition** asks: *What does the reader permanently gain?*

The subject of the sentence shifts from the world to the reader. Every editorial decision becomes sharper as a result: not "is this a pattern?" but "is this a recognition the reader can carry?"
