# Knowledge Architecture

*A design document for the institutional memory of Why Today? Written before implementation. The goal is to think clearly about what we're building before building it. Challenge assumptions, discuss tradeoffs, design for decades.*

*Status: Design proposal. Not yet implemented. Every section is a recommendation, not a decision.*

---

## The Core Problem

After 500 editions, the publication faces four failure modes:

1. **Repetition** — asking a hidden question it already explored, without knowing it
2. **Forgetting** — failing to leverage previous research when a related topic reappears
3. **Fragmentation** — 500 articles with no connective tissue, no compounding value
4. **Entropy** — institutional knowledge that lives only in article prose, not in any retrievable form

The goal of this architecture is not to prevent these failures by accumulating more information. It is to accumulate *the right kind of information* — specifically, perspective — in a form that makes Edition 500 noticeably smarter than Edition 5.

The question that should guide every architectural decision: **would this help a new editor or a new AI model understand why Edition 200 made the choices it made?**

---

## The Wikipedia Distinction

Wikipedia accumulates facts. This means the atomic unit is the **statement**: "July 4th is the date the Declaration of Independence was approved by Congress."

We are accumulating perspective. This means the atomic unit is different. A perspective is always a relationship between a thing, a question, and a broader concept:

> "The question 'Why is July 4th the wrong date?' produced the surprising sentence about Adams predicting July 2nd, which opened toward the concept: *national identities are built through accumulated commemoration, not through historical accuracy.*"

The components of a perspective:
- A question (the angle of approach)
- An **object** (the concrete, specific thing through which the concept becomes tangible)
- A surprising sentence (the specific claim that made the concept felt)
- A concept (the generalizable idea the question instantiated)

Concepts are what compound. Objects are the handles that carry concepts into conversation. Surprising sentences are the editorial expression of the relationship between object and concept. The architecture must be built around **concepts as the primary accumulating entity** and **objects as the primary carrier entity**.

---

## The Full Editorial Chain

The publication operates on a four-layer chain, not two:

```
Shared Moment        America turns 250
        ↓
Object of Attention  The date printed on the Declaration
        ↓
Surprising Sentence  "Adams predicted July 2nd — he got everything right except the date"
        ↓
Concept              Collective memory is constructed through repetition, not found in events
```

Each layer does different work:

- The **Shared Moment** creates relevance — why today
- The **Object** creates memorability — what the reader carries
- The **Surprising Sentence** creates the stop — the moment of "I never knew that"
- The **Concept** creates durability — what the reader thinks about later

Objects are especially important because they are *reusable lenses*. The same Object can access different Concepts across different editions. "A penalty kick" could access performance under pressure in one edition, the arbitrariness of tiebreakers in another, and the gap between practice and performance in a third. Tracking which Objects prove generative across multiple Concepts is one of the most valuable things the knowledge architecture can do.

**The craft of Why Today? is finding the Object that makes the Concept tangible without reducing it.** Concepts without Objects are a philosophy journal. Objects without Concepts are trivia. The Object is the bridge.

---

## Two Systems, Not One

The knowledge architecture must support two fundamentally different modes of intelligence. These are not two features — they are two different postures toward the same corpus, requiring different structures and different access patterns.

### The Memory Layer
*Optimized for retrieval. Answers: "What do we already know about this?"*

Structured, indexed, queryable. Concept files with explicit relationships. Source credibility records. Rejected questions with reasons. Edition postmortems with cross-references. You query the Memory Layer with a known term and get organized knowledge back.

**What it protects against:** Repetition, wasted research, forgetting what worked.
**Its failure mode:** Over-structure suppresses surprise. A publication with only Memory becomes safer and safer — it knows everything it's done and avoids doing it again. Eventually it stops discovering.

### The Curiosity Layer
*Optimized for discovery. Answers: "What haven't we wondered about yet?"*

Unstructured, browsable, driftable. Research residue. Objects that appeared during research but didn't fit the current edition. Surprising sentences that were found but not used. Unresolved questions raised by every edition. Unexpected adjacencies between concepts. You don't query the Curiosity Layer — you move through it, looking for collisions.

**What it protects against:** Sameness. The gradual narrowing of editorial range that comes from only doing what has worked before.
**Its failure mode:** Without structure, the Curiosity Layer becomes noise. Residue accumulates without any mechanism for surfacing what's worth revisiting.

### The Balance
The two layers must be maintained in conscious tension. The Memory Layer answers "have we been here before?" The Curiosity Layer answers "where haven't we been yet?" A publication that privileges Memory becomes competent but predictable. A publication that privileges Curiosity becomes surprising but inconsistent. Both are needed.

*Implementation note:* The two layers are not separate corpora — they are two different access modes to the same material. The same knowledge deposit can feed both layers depending on how it's tagged and how it's accessed.

---

## Knowledge vs. Curiosity as Accumulating Assets

This is the deepest distinction in the architecture.

A **knowledge base** is a record of answers. It gets more complete over time. It is finished when it knows everything.

A **curiosity base** is a record of *better questions* — questions raised by editions that weren't answered, questions the surprising sentence opened without resolving, questions the reader is left wondering when the edition ends. It gets richer over time, but it is never finished. It should not be finished.

After Edition 001, here is what we now know:
- National memory is constructed through accumulated commemoration, not through historical events
- July 4th became the date because it appeared on the printed document; the decisive act was July 2nd

After Edition 001, here is what we are still wondering:
- Has any country successfully changed its official founding date? What was required?
- Is the gap between decisive act and commemorated date a universal property of founding stories, or is America unusual?
- What would it take to shift American commemoration from July 4th to July 2nd? Is it even theoretically possible?
- Is national memory always constructed accidentally, or is it sometimes deliberately engineered?
- Are there other Objects like "the date on the document" — administrative accidents that became cultural facts?

None of these unresolved questions appear in the edition. All of them are more generative than what the edition answered. They are the intellectual exhaust of good editorial work — the questions raised by answering a different one.

**The publication becomes more curious by accumulating the questions it doesn't answer.** Answers are terminal. Questions compound. An edition that deposits five unresolved questions contributes more to future editorial intelligence than an edition that resolves five known questions — because the unresolved questions open territory that hasn't been mapped yet.

Every knowledge deposit must include both layers: what this edition now knows (Memory), and what this edition is now wondering (Curiosity).

---

## First-Class Entities

These are the objects that deserve their own persistent records in the system.

### 1. Objects of Attention
The concrete, specific, memorable things through which Concepts become tangible and portable.

*Examples from imagined editions:* The grass at Wimbledon. A penalty kick. The date printed on the Declaration. Shade. Hinges. A tall ship. Fireworks. A postmark.

Objects are first-class entities because they are **reusable lenses** — the same Object can access different Concepts across different editions. Tracking which Objects prove generative across multiple Concepts is one of the most valuable things the architecture can do.

Each Object record should contain:
- The object (as concrete and specific as possible — not "dates" but "a date printed on an official document")
- The editions that have used it, and which Concept each edition accessed through it
- Concepts not yet accessed through this Object (the unexplored angles)
- The Object's "carry" quality: how naturally does a reader hold this in mind? How naturally do they bring it into conversation?

Objects are *not* topics. A topic is an entry point into the publication. An Object is what the publication holds up to the light to reveal a Concept. Topics recur in the news. Objects recur in the mind.

*Pruning rule:* Objects that have only been used once and don't suggest obvious further Concepts are probably topics in disguise. Let them live in the edition record rather than as standalone entities.

---

### 2. Concepts
The most important entity. A concept is a generalizable idea that appeared in at least one edition and may appear again in different forms.

*Examples:* National memory, invisible disasters, performance under pressure, the gap between official history and lived experience, things that persist because they're entrenched not optimal, the power of a named date.

Concepts are *not* topics. "July 4th" is a topic. "Nations remember what they decided to celebrate" is a concept. Topics are entry points. Concepts are what we're actually accumulating.

Each concept record should contain:
- The concept (stated as a transferable idea, not as a topic)
- The editions that have instantiated it, and what angle each used
- Angles not yet explored
- The surprising sentences that best expressed this concept
- Sources most valuable for this concept
- Adjacent concepts (the edges in the concept graph)

### 2. Surprising Sentences
The publication's most valuable atomic editorial units. A surprising sentence is not just a good line — it is a specific, verifiable claim that stopped a reader and changed how they experienced something familiar.

Surprising sentences are reusable: the same sentence might be relevant in a future edition approaching the same concept from a different angle. They are also measurable: they are the unit most likely to be repeated in conversation, shared, or remembered.

Each surprising sentence record should contain:
- The sentence itself
- The edition it appeared in
- The concept it expressed
- The source where the underlying fact was found
- Source credibility assessment
- Whether it was used as the primary surprising sentence or as supporting material

### 3. Rejected Questions
This is counterintuitive but important. Rejected questions are not failures — they are editorial judgments about *why* a question wasn't strong enough, at a given moment, given a specific shared moment. That judgment has value.

A rejected question might be:
- Wrong for this shared moment but right for a different one
- Right question, wrong day (the world wasn't ready for it)
- Right question, no surprising sentence available yet (but research may change that)
- Genuinely wrong (and the reason why is the editorial insight)

Storing rejected questions with their rejection reasons creates an asset: a library of editorial decisions that teaches future editors and future AI models why some questions die and others survive.

Each rejected question record should contain:
- The question
- The shared moment it was rejected from
- Why it was rejected (specifically: which failure mode, or which specific weakness)
- Whether it might work in a different context
- Date of rejection

### 4. Sources
Not a bibliography. A living record of sources that proved valuable, with assessments of what they're reliable for.

Each source record should contain:
- The source (book, archive, researcher, institution, publication)
- What concept families it's reliable for
- What it's been used for in previous editions
- Credibility assessment
- Direct links to the surprising sentences it produced

### 5. Shared Moment Types
Not individual events, but categories of shared moments that consistently produce strong or weak editorial results.

*Examples:* National holidays, sporting upset moments, annual seasonal events (solstices, seasons), technological announcements, natural weather events, cultural anniversaries.

Tracking which types of shared moments consistently yield strong editions is how we refine the selection algorithm over time. After 50 editions, we should have data.

### 6. Editions
The outputs. But treated as evidence rather than endpoints — each edition is a data point for understanding the algorithms, not the final accumulation target.

---

## Key Relationships

These are the edges in the concept graph that matter most.

| Relationship | From | To | Why it matters |
|---|---|---|---|
| **entered through** | Edition | Shared Moment | What event made the edition relevant today |
| **focused on** | Edition | Object | The concrete thing the edition held up to the light |
| **instantiates** | Edition | Concept | The generalizable idea the edition accessed |
| **approaches via** | Edition | Angle | Which angle of the concept was used |
| **contains** | Edition | Surprising Sentence | The primary editorial unit, Memory Layer |
| **deposited** | Edition | Unresolved Question | What the edition is still wondering, Curiosity Layer |
| **rejected** | Editorial Meeting | Question | With reason — a library of editorial judgment |
| **expresses** | Surprising Sentence | Concept | What concept the sentence makes felt |
| **accesses** | Object | Concept | Which concept this Object was used to reach |
| **could access** | Object | Concept | Concepts not yet explored through this Object |
| **found in** | Surprising Sentence | Source | For credibility and future retrieval |
| **connects** | Concept | Concept | The graph edges — what concepts appear together |
| **raises** | Concept | Unresolved Question | Questions opened by exploring this concept |
| **entered via** | Edition | Shared Moment Type | Category of shared moment — for pattern analysis |
| **angles available** | Concept | Angle | Approaches to this concept not yet taken |

---

## Three Architectural Options

### Option A: Flat Tagged Corpus

Every edition produces a structured "knowledge deposit" markdown file with rich YAML frontmatter. Tags create implicit relationships. A concept is just a tag. The corpus is searched rather than traversed.

```yaml
---
edition: 001
shared_moment_type: national_holiday
concepts: [national_memory, founding_myth, constructed_dates]
surprising_sentence: "John Adams predicted July 2nd forever..."
angles_used: [constructed_commemoration]
sources_used: [adams_letter_to_abigail_1776]
rejected_questions:
  - question: "How does a country choose its birthday?"
    reason: universal_without_anchor
---
```

**Pros:** Simple. Durable. Human-readable. No tooling required. Can be parsed into any future system.

**Cons:** Relationships are implicit (tags), not explicit (edges). "national_memory" in Edition 001 and "national_memory" in Edition 087 are connected only by sharing a string. No concept records that accumulate depth over time. The graph is potential, not actual.

**Best for:** Getting started. Years 1–2.

---

### Option B: Entity Files + Relationship Files

Separate markdown files for each first-class entity. Concept files accumulate depth across editions. Relationship files connect entities. Editions are thin — they reference entities by ID rather than duplicating content.

```
/knowledge/
  /concepts/
    national-memory.md
    founding-myth.md
    invisible-disasters.md
  /surprising-sentences/
    adams-july-2nd-prediction.md
    heat-kills-more-than-tornadoes.md
  /sources/
    adams-letter-abigail-1776.md
    national-archives-declaration.md
  /rejected-questions/
    2026-06-30-how-does-country-choose-birthday.md
  /shared-moment-types/
    national-holiday.md
    sporting-upset.md
```

Each concept file contains not just metadata but an *evolving record of the publication's understanding* — updated with each new edition that touches the concept.

**Pros:** Concepts genuinely accumulate depth. A concept file read at Edition 200 tells you everything the publication has learned about that concept across 200 editions. Explicit rather than implicit relationships. Enables genuine editorial intelligence retrieval.

**Cons:** Overhead. Every edition requires updating potentially multiple entity files. Risk of stale records if the update discipline fails. The corpus can fragment if concepts multiply without pruning.

**Best for:** After 10–20 editions, when patterns are clearer and discipline is established. Years 2–4.

---

### Option C: Semantic Knowledge Graph

A proper graph structure — nodes for all first-class entities, typed edges for all relationships, queryable. Could be JSON-LD, a simple custom format, or eventually a real graph database. The corpus of articles is separate from the knowledge graph; the graph indexes the knowledge extracted from the articles.

```json
{
  "nodes": [
    {"id": "concept:national-memory", "type": "Concept", 
     "description": "Nations remember what they decided to celebrate, not what actually happened"},
    {"id": "edition:001", "type": "Edition"},
    {"id": "ss:adams-july-2nd", "type": "SurprisingSentence",
     "text": "John Adams predicted July 2nd forever..."}
  ],
  "edges": [
    {"from": "edition:001", "to": "concept:national-memory", "relation": "instantiates"},
    {"from": "edition:001", "to": "ss:adams-july-2nd", "relation": "contains"},
    {"from": "ss:adams-july-2nd", "to": "concept:national-memory", "relation": "expresses"},
    {"from": "concept:national-memory", "to": "concept:founding-myth", "relation": "connects"}
  ]
}
```

**Pros:** True graph traversal. Enables powerful queries: "find all editions that touched national-memory and haven't used the angle of contested monuments." Concept evolution trackable. Supports eventual AI-native retrieval.

**Cons:** Requires tooling. Harder for humans to maintain by hand. Risk of over-engineering before we know what the graph actually needs to contain.

**Best for:** Year 4+, when the concept graph has meaningful density and the patterns are well-understood.

---

### Recommendation: Option B Now, Option C Eventually, Option A as the Bridge

The architecture should evolve in phases:

**Phase 1 (Editions 1–20):** Option A. Rich YAML frontmatter on knowledge deposit files. Design the frontmatter structure so it can be parsed into a graph later. Focus on establishing the discipline of depositing knowledge after every edition. Don't prematurely optimize.

**Phase 2 (Editions 20–100):** Option B. Once patterns are clear and entity categories are well-understood, migrate to explicit entity files. Concepts accumulate depth. The surprising sentence library becomes a genuine editorial asset.

**Phase 3 (Editions 100+):** Option C. Once the concept graph has meaningful density, build the actual graph layer. At this point, the editorial meeting can start with: "what concepts does today's shared moment touch?" and the system returns the full history of how the publication has approached those concepts.

The key is that the frontmatter designed in Phase 1 must be graph-ready — structured so Phase 3 can parse it without re-annotating 100 editions.

---

## The Knowledge Deposit

After every edition, the publication deposits the following across both layers. This is what makes the system compound rather than merely accumulate.

### Memory Layer Deposits

**1. Object Record**
The Object of Attention: what concrete thing did the edition hold up? Which Concept did it access through this Object? What other Concepts could this Object access that haven't been explored?

**2. Concept Assertions**
Which concepts did this edition instantiate? Which angle did it use? What angles remain unexplored for this concept?

**3. Surprising Sentence Record**
The primary surprising sentence: text, source, Concept expressed. Any secondary surprising sentences found during research but not used. These are among the most valuable deposits — a library of editorial expression that can inform future editions approaching the same Concept.

**4. Rejected Questions (with reasons)**
Every finalist that didn't make the cut. Specifically: which failure mode killed it, or which specific weakness. This is not bookkeeping — it is editorial judgment made explicit and retrievable. A rejected question from Edition 001 might be exactly right for Edition 087.

**5. Source Assessment**
Every source used: what was it reliable for, what was its quality? Over time this builds a source map — which sources are trustworthy for which concept families.

### Curiosity Layer Deposits

**6. Unresolved Questions**
What is the edition still wondering? Not rhetorical questions, not questions the edition answered — questions the research raised without resolving. These are the most generative deposit. They are the questions Edition 001 opened that future editions may answer.

*Format:* State the question as precisely as possible. Note which Concept it belongs to. Note what shared moment type might make it newly relevant.

**7. Research Residue**
Facts, connections, and Objects that appeared during research but didn't fit this edition. Rabbit holes opened but not explored. These feed the Curiosity Layer — they are what the edition discovered on its way to what it published.

**8. Adjacent Objects**
Objects that appeared during research and were interesting but weren't the right lens for this edition. Stored here so future editions can find them when approaching the same Concept from a different angle.

**9. New Concepts**
If the edition introduced a concept not yet in the system, add it — with this edition marked as the "founding edition" for that concept and the first Unresolved Questions it generated.

---

## How Edition 500 Differs from Edition 5

In Edition 5, the editorial process is:
- Survey shared moments
- Generate hidden questions
- Select by instinct
- Research from scratch
- Write

In Edition 500, with a mature knowledge graph, the editorial process becomes:
- Survey shared moments
- **Cross-reference against concept graph: what concepts does each shared moment touch?**
- **Retrieve: how has the publication approached these concepts before?**
- **Ask: which angles of these concepts haven't been used?**
- Generate hidden questions *informed by what's been done*
- Select — now with explicit knowledge of the editorial history
- **Retrieve: what sources proved valuable for this concept family?**
- **Retrieve: what surprising sentences were found but not used in previous editions on this concept?**
- Research — with a head start from previous residue
- Write — with knowledge of what the publication has already said and what it hasn't

The selection algorithm improves because it has data. The construction algorithm improves because it can retrieve previous research. The edition is better not because the editors are smarter, but because the *system is smarter*.

---

## The Angle Problem

The deepest challenge in avoiding repetition without becoming stale. Once we've covered a concept, how do we return to it without repeating ourselves?

The answer is **angle tracking**. A concept is not a topic — it can be approached from many angles. "National memory" has been approached through: *constructed dates* (Edition 001). Future editions might approach it through: *contested monuments*, *the gap between founding stories and founding events*, *how national anthems get written*, *why some historical events become holidays and others don't*.

The concept record must track not just "this concept has been used" but "this concept has been used from *this angle*." A returning concept approached from a new angle is not repetition — it is deepening.

---

## The Anti-Clutter Rule

Every knowledge system accumulates clutter. The discipline of adding must be matched by a discipline of pruning.

**Rule: Concepts must be broad enough to recur.** If a concept file has only one edition in its history after 50 editions, it may be too specific. Consider merging it into a parent concept or reclassifying it as a topic (a one-time entry point) rather than a concept (a recurring idea).

**Rule: Connections must be typed and meaningful.** Not every entity connects to every other entity. Relationships should only be added when they carry editorial intelligence — when knowing the connection would actually change how a future editor approaches a problem.

**Rule: Periodic graph tending.** Every 50 editions, review the concept graph. Merge over-specific concepts. Split over-crowded concepts. Retire concepts that consistently produce weak editions. Promote "Patterns Under Watch" that have proven out.

---

## What This Architecture Cannot Do

It cannot replace editorial judgment in the selection step. The selection algorithm is currently the least explicit part of the process. Richer knowledge retrieval will inform it, but the final choice — which question survives — requires something the knowledge graph cannot provide: a feeling for what the reader is ready to be surprised by today, given what is in the air, given what has come before. That is editorial taste. It may be the permanent human contribution.

It cannot prevent all repetition. Concepts are wide enough to recur; the same concept approached from the same angle twice is still repetition. The angle tracking system mitigates this but does not eliminate it. Human review remains necessary.

It cannot make the knowledge useful if the deposit discipline fails. A knowledge graph that isn't updated after every edition quickly becomes stale and misleading — worse than no system, because it creates false confidence. The deposit must be treated as mandatory, not optional.

---

## If We Started Today Knowing Everything We've Learned

*Brett's question, applied to this architecture.*

We would design the knowledge deposit format first, before writing a single edition. We would decide what concepts are — specifically, that they are not topics — before creating any concept records. We would build the rejected-questions library from Day 1, not as an afterthought. We would create a single consistent frontmatter schema for all knowledge files before writing any content, so the graph can be parsed without re-annotating.

We did not do those things in Phase 1. That is appropriate — we needed Edition 001 to understand what kind of knowledge we were accumulating before we could design a system to accumulate it. But now we know. And that knowledge should shape Phase 2.

---

## Proposed Immediate Next Steps

Before building anything:

1. **Agree on the concept definition.** Write down, in one sentence, what distinguishes a concept from a topic. Test it against five examples. The architecture depends on this distinction.

2. **Design the knowledge deposit frontmatter.** Create a draft schema for the YAML frontmatter that will annotate every edition going forward. Design it to be graph-parseable.

3. **Retroactively deposit Edition 001.** Apply the knowledge deposit process to the edition we've already built. This is both a test of the schema and the beginning of the knowledge base.

4. **Create the first concept record.** Choose one concept from Edition 001 (probably "national memory") and write its first concept file. This will reveal whether the entity design is right before we commit to it.

None of this is software. All of it is intellectual infrastructure. The software comes when the intellectual infrastructure is stable enough to express.
