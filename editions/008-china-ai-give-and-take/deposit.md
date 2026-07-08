# Edition 008 Deposit — china-ai-give-and-take

What this edition added to the compounding knowledge base.

---

## Concept confirmed

**Openness is a phase, not a value.**

A strategy of giving something away makes sense exactly as long as giving it away buys more than keeping it would. China's AI labs gave away frontier models while they needed the world's attention — DeepSeek in January 2025, then Qwen, then Hy3 on July 6, 2026. Eighteen months later, Chinese models hold 45% of traffic on OpenRouter, up from under 2%. The attention has been bought. Reuters reports that Beijing is now discussing whether the *next* generation of models should leave the country at all — not because the openness strategy failed, but because it succeeded completely enough to change what it needs to protect.

This is a durable idea, not a China-specific one. It should recur anywhere a party gives something away to win an argument or capture a market, then reconsiders generosity once the win is banked — open betas that go proprietary once dominant, free tiers that get metered once the user base is locked in, "we're building in the open" claims that quietly stop being true. Watch for it in future editions about any strategic reversal that looks like a betrayal but is actually a phase transition.

**Related but distinct — not the concept, the mechanism underneath it:** Joel Spolsky's 2002 "commoditize your complement" (give away the product, capture the layer above or below it) explains *why* the strategy made sense in the first place. It is the tool; "openness is a phase" is the insight about what happens after the tool has finished working. Future editions using Spolsky's framework should treat it as mechanism, not as the reusable concept itself.

---

## Object studied

**Tencent's Hy3 license — the clause that was there in April and gone in July.**

The April preview excluded the EU, UK, and South Korea from using the model at all. The July 6 official release, under Apache 2.0, dropped the exclusion entirely — a single clause's disappearance functioning as a small, legible instrument reading out a much larger strategic decision. One day later, Reuters reported Beijing weighing whether that kind of decision should still be possible for the *next* model. The object is small (one license clause) but it's the whole edition in miniature: the exact moment a door was propped fully open, one day before someone started drafting the sign that might shut it.

---

## Visual format that earned its place

**The vertical timeline, four markers one color, the fifth breaking it.**

Sequential dated events (Jan 2025 → Jul 7, 2026) don't compress well into a grid or a bar chart — the point is the *order* and the *break in the pattern*, not a distribution across categories. A simple vertical timeline with a color change on the last marker let the reader see the reversal before reading the caption that explains it. Lesson for future editions: when the discovery is "this had been going one direction, then didn't," a timeline that visually breaks its own pattern does more work than prose stating "then it changed."

---

## Human voice — a technique worth naming

No named, on-record source was reacting to *this week's* news — only anonymous Reuters sourcing and an unnamed X post. Rather than force a weak quote, the edition used Joel Spolsky's 2002 "Strategy Letter V," a genuinely on-record, attributed quote that is the actual theoretical origin of the mechanism being argued, not a contemporary reaction. Edition 006 did something similar with Christophe's 1919 quote. **Emerging technique, two instances:** when no clean contemporary human voice exists, a historical or foundational on-record quote that the edition's argument is actually built on can satisfy the human-voice requirement more honestly than reaching for a thin, anonymous, or manufactured-sounding contemporary one. Worth watching for a third instance before naming this in PATTERNS.md.

---

## Forks saved for future editions

**Fork A — JadePuffer, the "agentic ransomware."** Surfaced at Step 2 alongside the China AI thread, dropped when this one showed more momentum. The hidden question ("at what point does malware stop being a program and start being a decision-maker?") is unresolved and the underlying story — AI agents automating extortion end-to-end — hasn't gone away. Candidate for a future edition on agentic AI risk, once public technical detail is less thin than a single write-up.

**Fork B — Qwen's billion downloads as its own edition.** Used here only as "One More Thing." The question it deserves on its own: what does it mean for one company's model weights to become the most-downloaded software artifact in history, faster than anything before it — and does "downloads" even measure what we think it measures (many are automated pipelines, not individual developers)?

**Fork C — The sequel this edition is explicitly waiting on.** Reuters' reporting describes discussions, not decisions. If Beijing's Ministry of Commerce actually enacts (or explicitly abandons) the tiered restriction regime, that resolution is a strong future edition: did the door actually close, and what happened to the world's dependence on Chinese open models in the meantime?

**Fork D — Open-source as industrial policy, beyond AI.** The USCC's "Two Loops" framing (open models + manufacturing dominance as a reinforcing feedback loop) suggests this isn't really an AI story. It's a nation using open-source software as a lever the way earlier powers used tariffs or subsidies. Worth a future edition that starts from that frame rather than from AI specifically.

---

## Research residue and sourcing notes

- **The 45% OpenRouter figure** is scoped to one marketplace that skews toward coding/agentic workloads, not "global AI usage." Sources disagreed anywhere from ~30% (broad 100-trillion-token study) to 61% (a single peak week, narrowly defined). Future editions citing this stat should keep it scoped, not average conflicting methodologies into a false-precision number.
- **DeepSeek's $5.576 million training-cost figure** is real but partial — the company's own disclosure, covering one training run only. SemiAnalysis's independent estimate of ~$1.3 billion total GPU capital expenditure is the more honest total-cost figure. Both are now on record for future editions that need either the "cheap headline" number or the "real total" number.
- **The gwern.net link** ("commoditize your complement") returned an HTTP 403 to an automated fetch attempt used to verify the Spolsky quote. Likely bot-detection rather than the page being down, but not confirmed with a real browser. Flag for a manual check before the next edition links to that domain again.
- **Reuters exclusive sourcing**: three people "not authorised to speak," declining to be identified; nothing decided; reported to apply to future models only. This caveat is load-bearing for the edition's honesty and should travel with the story if it's referenced again.
