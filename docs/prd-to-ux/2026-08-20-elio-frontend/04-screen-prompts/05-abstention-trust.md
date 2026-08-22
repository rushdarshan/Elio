# Abstention / Trust — Screen Prompts

_Each block below is self-contained. Copy one block, paste into Stitch / Figma AI / Pencil / Claude Design._

---

## Abstention — Populated

````
**What this screen is for:**
The refuse-with-reason panel: the user sees every row the pipeline refused to guess, grouped by refusal reason, so the product's honesty is itself inspectable.

**What's visible:**
A dark console surface. At the top, a small segmented filter control with three options: All Refusals, Unsupported Category, Missing Evidence. Below, a list of refusal cards — each card shows the MPN in mono, the taxonomy path, the raw description, and the specific refusal reason as a prominent amber tag. Cards are grouped or filterable by reason type; every refusal is present, none are hidden.

**What the user can do:**
- Primary: filter refusals by reason (unsupported category vs missing evidence).
- Secondary: open a refusal's record in the Explorer to inspect the failed evidence; switch datasets.

**Feel:**
Dark ops-console tone, amber strictly for refusals, mono identifiers, hairline separators. This screen is the product's integrity display: calm, complete, nothing censored.

**State context:**
Populated state — refusals exist in the dataset.

**Critical affordances:**
Every refusal must show its reason on the card — the reason is the entire point. Filters must map to the real refusal categories the pipeline emits (unsupported category, missing evidence) and must always include an "all" view. The counts shown must match the dashboard's Abstention Summary exactly.
````

---

## Abstention — Empty (No Refusals)

````
**What this screen is for:**
The user came to inspect refusals and there are none — the panel should state the fact plainly.

**What's visible:**
The dark console shell with the filter control still visible but inert, and a plain statement that there are no refusals in the current dataset. No celebratory styling — zero refusals is a fact, not a trophy.

**What the user can do:**
- Primary: switch datasets to inspect another scope.
- Secondary: return to Explorer or Dashboard.

**Feel:**
Same calm dark console tone; consistent with the populated state minus the cards.

**State context:**
Empty state — no refusals in the current dataset.

**Critical affordances:**
The empty state must stay honest with the dashboard: if the dashboard shows abstained values, this screen must show them too — the two readouts can never contradict.
````