# Screen Prompts — Dashboard (Self-Score Front Page)

## Screen: Dashboard

### State: Empty

**What this screen is for:** The pre-run state — the report has not been generated.

**What's visible:** "No report yet — upload a file to generate one." (Reachable only before a run; the flow normally leads here from upload.)

**What the user can do:** Return to upload.

**Feel:** Honest-report calm — a quiet statement, not a void.

**State context:** Empty state — no run yet.

**Critical affordances:** The path back to upload must be one step.

---

### State: Loading

**What this screen is for:** The recompute moment after review verdicts.

**What's visible:** A subtle "recomputing…" indicator on the affected metrics only — seconds-class, never a full-screen spinner.

**What the user can do:** Continue reading the report.

**Feel:** Calm precision — the report is live, not fragile.

**State context:** Loading state — post-verdict recompute.

**Critical affordances:** Only the affected numbers must show the indicator; the rest of the report stays readable.

---

### State: Populated

**What this screen is for:** The hero moment — headline accuracy and its evidence basis on one front page.

**What's visible:** (1) the headline number — field accuracy vs gold when the upload overlaps the frozen gold set, or evidence-support rate labeled "estimate" when it doesn't — the single biggest element; (2) persistent stamps for "estimate" and "deterministic-only" modes with one-line explanations; (3) the metric cluster — field accuracy vs gold, evidence-support rate, abstention coverage, LOV compliance, char-limit compliance, per-SKU cost, decision mix, and a per-row verified-vs-blank coverage bar; (4) the methods section — the 1%/2%/5% field-error-budget curve; (5) every score cell and value clickable into its custody chain.

**What the user can do:** Click any score cell into its custody chain; expand the curve; export.

**Feel:** The report's cover — editorial, confident, breathable; the headline number is unmissable, the stamps read as footnotes of a serious publication, the curve as the methodology page. The whole thing must feel like a document, not a dashboard.

**State context:** Populated state — the post-run report front page.

**Critical affordances:** The estimate/degraded stamps must persist visibly — a labeled number is the honesty story, never hidden; the "estimate" one-liner ("your file doesn't overlap the frozen gold set — showing evidence-support instead; abstention = engineered honesty") must survive; every metric cell must be clickable into custody; the headline must state its scope (exact vs estimate).

---

### State: Error

**What this screen is for:** No error path of its own — metrics come from the run; a failed run never reaches the dashboard. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state.

**Critical affordances:** None.

---

### State: Permission-denied

**What this screen is for:** Not applicable. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state.

**Critical affordances:** None.

---

### State: Edge cases

**What this screen is for:** The front page under unusual runs.

**What's visible:** Partial gold overlap (e.g., 12 of 30 rows) shows the exact rate scoped to those rows with the rest labeled estimate — the scope is stated, never hidden; a fully abstained run shows "0% enriched" with the honest-stamp framing; clicking a score cell mid-recompute still opens its chain from stored evidence.

**What the user can do:** Click through; read the scope notes.

**Feel:** Same report gravity — even zero is stated with confidence.

**State context:** Edge-case variations of the dashboard.

**Critical affordances:** The exact-rate scope must name the row count it covers; the 0% headline must not be dressed up; chains must open from stored evidence during recompute.