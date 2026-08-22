# Developer / Architecture — Screen Prompts

_Each block below is self-contained. Copy one block, paste into Stitch / Figma AI / Pencil / Claude Design._

---

## Developer — Populated (Hidden Utility)

````
**What this screen is for:**
A hidden utility page, out of the judge journey: a technical readout of the pipeline's internals for a developer or an interviewer poking behind the curtain.

**What's visible:**
A sparse dark console page, reachable only through an unmarked debug affordance in the chrome (not visible in the main navigation). It shows the frozen pipeline contract: the stage list of the deterministic enrichment DAG, the verification ledger status, and references to the artifacts (evidence records, decision log) — all in mono, no marketing copy, no charts.

**What the user can do:**
- Primary: read the pipeline architecture facts.
- Secondary: nothing interactive of consequence — this is a reference surface, not a tool.

**Feel:**
The most austere surface in the product: near-black, mono-only, hairline rules, zero color accents. It should feel like reading the machine's own documentation.

**State context:**
Populated state — the pipeline contract is always present; this screen does not depend on a run.

**Critical affordances:**
Must remain reachable only through a deliberately hidden affordance — it must not appear in the judge-facing navigation. All facts stated here (stages, ledger, artifact references) must match the real pipeline exactly — this is the one screen a technical reviewer will fact-check.
````