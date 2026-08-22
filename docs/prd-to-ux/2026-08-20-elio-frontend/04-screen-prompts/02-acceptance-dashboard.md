# Acceptance Dashboard — Screen Prompts

_Each block below is self-contained. Copy one block, paste into Stitch / Figma AI / Pencil / Claude Design._

---

## Dashboard — Populated

````
**What this screen is for:**
The headline readout of the console: every number on this screen answers "did the pipeline do its job on my catalog?" and every metric is a drillable instrument, never a bare badge.

**What's visible:**
A dark console surface. A grid of metric instruments, each a quiet panel with a large mono numeral and a small uppercase label:
- An asymmetric hero instrument spanning more width: Attributes per Row — a precise mono value with a "PER ROW" tag and a mono footnote of the extraction scope.
- Evidence Support — a percentage with a "TRACEABLE" tag; green denotes values that carry a source span.
- Char Limit Compliance — a percentage.
- Escalated Reviews — a count of rows sent to the Review queue.
- Abstained Values — a count in amber; values the pipeline refused to guess.
Below the instruments, a status banner stating the abstention pipeline is active, with mono chips for "Dual-Pass: active" and "Gold overlap: byte-exact." Then a two-column readout: on the left, a Processing Stage list — mono rows for each stage (Intake Normalize, Entity Resolution, Taxonomy Classification, Dual-Pass Verification) each with a real derived count (rows parsed, manufacturers resolved, categories classified, rows escalated) — and on the right, an Abstention Summary listing refusal categories (Category Not Supported, Evidence Deficient) each with a real row count.

**What the user can do:**
- Primary: click any metric instrument to drill into the Explorer at the corresponding evidence.
- Secondary: switch dataset size from the chrome; jump to the Review queue for escalated rows.

**Feel:**
Dark operations console: deep near-black surfaces, hairline borders, mono numerals for all data, one blue accent for interactive elements, green only for verified status, amber only for review/escalation. Quiet, dense, trustworthy — a control room, not a marketing page. No decorative motion.

**State context:**
Populated state — a run exists (demo, full, or uploaded dataset).

**Critical affordances:**
Every number must trace to a real derivation from the loaded data — no static or invented values. The hero metric (Attributes per Row) is the headline instrument and should read as the strongest card on the grid. Numbers must feel clickable (drill-to-evidence), so affordance is visible without being loud.
````

---

## Dashboard — Empty (No Run Yet)

````
**What this screen is for:**
The user opened the console but nothing has been processed — the screen must say so plainly and point to the intake step.

**What's visible:**
The dark console shell with the sidebar navigation visible. The dashboard area shows an honest empty readout: a brief message that no run has been completed yet, and a single forward action toward the Upload step. No zero-filled instrument grid — zeros pretend a run happened.

**What the user can do:**
- Primary: navigate to Upload & Run to start.
- Secondary: switch to the built-in Demo dataset if one is available to load.

**Feel:**
Same dark ops-console tone; the empty state is calm and directional, not broken. No skeleton shimmer, no fake loading.

**State context:**
Empty state — no records loaded yet.

**Critical affordances:**
Do not render a populated-looking dashboard with zeros. The path forward (upload or load demo) must be the visual focus.
````

---

## Dashboard — Dataset Switch (Demo / Full / Uploaded)

````
**What this screen is for:**
The user changed the dataset scope — the entire readout recomputes and the instruments must visibly re-derive without a full reload feel.

**What's visible:**
The same instrument grid, but every numeral and count now reflects the newly selected dataset (Demo 50, Full 1000, or the user's uploaded file). The scope is echoed in each instrument's footnote (e.g., "across N rows"). The active dataset is marked in the chrome toggle.

**What the user can do:**
- Primary: switch dataset size from the toggle and re-read the headline numbers.
- Secondary: drill into the Explorer, which now operates on the same dataset.

**Feel:**
One continuous console; the switch is a scope change, not a screen change. Numbers update crisply, no reload flash, no celebration.

**State context:**
Edge state — dataset scope changed after a populated run.

**Critical affordances:**
The counts shown must be derived from the selected dataset's records, and the "across N rows" footnotes must match. The dashboard and the Explorer must always be on the same dataset.
````