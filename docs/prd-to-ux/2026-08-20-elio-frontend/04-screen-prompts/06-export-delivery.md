# Export & Delivery — Screen Prompts

_Each block below is self-contained. Copy one block, paste into Stitch / Figma AI / Pencil / Claude Design._

---

## Export — Empty (No Run)

````
**What this screen is for:**
The shipping dock with nothing shipped yet — the user needs a clear, honest "nothing to export" readout.

**What's visible:**
The dark console shell. The main area states plainly that no run has been completed yet, so there is nothing to export, with a forward action toward the Upload step. No zero-filled export summary — zeros would pretend a run happened.

**What the user can do:**
- Primary: navigate to Upload & Run to produce exportable results.
- Secondary: load a built-in dataset if available.

**Feel:**
Dark ops-console tone; the empty dock is calm and directional, consistent with the Dashboard's empty state.

**State context:**
Empty state — no run exists.

**Critical affordances:**
Never show a populated-looking export readout with zeros. The forward path must be obvious.
````

---

## Export — Ready for Import (Populated)

````
**What this screen is for:**
The shipping dock: the user verifies the export is schema-clean and downloads the enriched catalog for import into their system.

**What's visible:**
A centered panel on the dark console surface with three stacked facts, each in mono: the export schema status (252-column standard, verified), the row counts by decision class (accepted / reviewed / abstained, matching the dashboard exactly), and the delivery format options. Two quiet download actions: the full enriched export and the sanitized variant (row-level decisions applied, refusal cells handled). A closing status line marks the deliverable as ready for import.

**What the user can do:**
- Primary: download the enriched export (and the sanitized variant).
- Secondary: return to the Review queue if any rows remain unresolved; re-check counts against the Dashboard.

**Feel:**
Dark ops-console tone: mono facts, hairline separators, blue only on the download actions, green only for the schema-verified status. The dock reads like a manifest — complete, precise, final.

**State context:**
Populated state — a run exists and is ready to export.

**Critical affordances:**
The export summary counts (accepted / reviewed / abstained) must match the dashboard and abstention readouts exactly — cross-screen consistency is the trust contract. The schema check (252-column standard) is the headline guarantee and must be stated as verified. The sanitized variant must exist as a distinct, clearly explained option — judges must understand the difference between raw and sanitized deliverables.
````