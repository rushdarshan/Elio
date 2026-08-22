# Review Queue — Screen Prompts

_Each block below is self-contained. Copy one block, paste into Stitch / Figma AI / Pencil / Claude Design._

---

## Review Queue — Empty

````
**What this screen is for:**
The sign-off station with nothing to sign off — the user should see that the queue is clean without any ceremony.

**What's visible:**
The dark console shell. The main area shows a quiet, plain statement that there are no rows awaiting review right now, with a small hint that escalated rows from the pipeline will appear here. No confetti, no trophy — a clean station.

**What the user can do:**
- Primary: return to the Dashboard or Explorer.
- Secondary: change datasets, in case another dataset has escalations.

**Feel:**
Dark ops-console tone; the empty queue is calm and factual, the same voice as the rest of the console.

**State context:**
Empty state — no rows have been escalated for review.

**Critical affordances:**
The empty state must not look like an error. The path back to populated screens must be obvious via the sidebar.
````

---

## Review Queue — Populated

````
**What this screen is for:**
The sign-off station: the user works through the rows the pipeline escalated, deciding each one's fate so it can flow to the export.

**What's visible:**
A list of escalated rows. Each row card shows: the MPN in mono, the brand label, the taxonomy path, the raw description, the primary refusal reason as a prominent tag (e.g., evidence blocker), and the pipeline's extracted attributes with their evidence state. Each card carries a clear decision control — accept or reject — with the current decision state visible.

**What the user can do:**
- Primary: accept or reject each row; the decision is recorded and the row leaves the queue.
- Secondary: open the record's custody drawer to inspect evidence before deciding; edit an attribute value before accepting.

**Feel:**
Dark ops-console tone, hairline separators, mono identifiers, amber reserved for the refusal tags. The decision control should feel like a physical sign-off — deliberate, not a toggle. Dense enough to work through quickly, quiet enough to read carefully.

**State context:**
Populated state — rows escalated by the pipeline are awaiting sign-off.

**Critical affordances:**
The refusal reason must be visible on every card without opening anything — the user decides on the evidence, so the reason is the card's headline detail. Decisions must feel final (a deliberate act), and the queue must visibly shrink as rows are signed off.
````

---

## Review Queue — Decision Made (Post-Action)

````
**What this screen is for:**
The user just signed off a row — the queue must reflect the decision instantly and the row must flow onward toward export.

**What's visible:**
The signed-off row leaves the queue list (or moves to a completed section), and the queue count updates. If the user edits an attribute before accepting, the corrected value is visible in the row's attribute list and carries a "reviewed override" marker distinct from pipeline values. A quiet confirmation of the decision appears briefly — no modal dance, no confetti.

**What the user can do:**
- Primary: continue to the next escalated row.
- Secondary: undo a decision if the flow supports it; export now includes the signed-off decision.

**Feel:**
The action lands with finality: one short confirmation, list updates, count drops. Dark console tone, decisions recorded in mono type.

**State context:**
Post-action state — a decision (accept/reject/edit) has been applied to a row.

**Critical affordances:**
Every decision must be recorded in the decision log and reflected in the Export counts — accept/reject/edit states must be distinguishable in any subsequent readout. Overrides must be visually distinct from pipeline values so the judge sees human intervention clearly.
````