# Screen Prompts — Upload & Column Mapping

## Screen: Intake

### State: Empty

**What this screen is for:** The judge's first contact — land, understand the promise in one line, and drop in their file.

**What's visible:** The report's cover page: app title, a one-line promise ("Upload any product file — every value will carry its own cited evidence"), a single generous file dropzone for CSV/XLSX, a quiet note about the row cap and demo framing, and a secondary "view sample format" link.

**What the user can do:** Drop or browse-select a file; open the sample-format reference.

**Feel:** Neutral, modern, trustworthy. Quietly utilitarian — content-first, generous whitespace, the dropzone is the only loud thing. Black/white/gray palette with one understated accent reserved for the primary action. No ornament, no gradients.

**State context:** Empty state — no file has been uploaded yet; this is also the pre-run landing for the whole app.

**Critical affordances:** The upload affordance must be unmistakably primary; the one-line promise must survive verbatim; the row-cap/demo-mode note must be visible but not alarming.

---

### State: Loading

**What this screen is for:** Show the judge the file is being vetted (size, type, structure) before any mapping appears.

**What's visible:** The dropzone replaced by a brief progress line — "Reading file… rows detected, hash computing" — plus a subtle size/type check indicator.

**What the user can do:** Wait; cancel back to the empty dropzone.

**Feel:** Calm and legible — a quiet progress line, no spinners theater. Consistent with the neutral utilitarian palette.

**State context:** Loading state — file accepted, parsing in progress (magic-byte type check, decompression caps, row/hash computation).

**Critical affordances:** The transition must read as "vetting," not "uploading" — the judge should feel the app is being careful, which is the trust story.

---

### State: Populated

**What this screen is for:** Let the judge confirm how the app read their file before anything runs — the intake-QA moment.

**What's visible:** A mapping-review table: each detected column with a confidence chip (high/medium/low) and its suggested mapping to the six known input columns; refused columns show an inline manual-mapping control; a status line for the 252-column output-contract dry-run; the input hash and row count; a primary "Run pipeline" action, disabled if any column is unmapped or a run is in progress.

**What the user can do:** Accept suggested mappings; manually map refused columns; re-upload; run the pipeline.

**Feel:** Report-grade, editorial calm — a clean table, confident chips, the primary action distinct but not loud. The mapping table feels like a lab intake form: precise, legible, honest.

**State context:** Populated state — the judge's file has passed vetting and every column is accounted for.

**Critical affordances:** The confidence chips and the "refused → manual mapping" path must survive — no silent guessing is the point; the Run action must be gated on complete mapping.

---

### State: Error

**What this screen is for:** Reject a bad file with an explicit reason and an immediate recovery path.

**What's visible:** A rejection message with the specific reason — file too large (with a size hint), wrong type (magic bytes don't match), unparseable content, or rejected structure — and a re-upload affordance. Never a bare exception.

**What the user can do:** Read the reason; re-upload a corrected file.

**Feel:** Honest and unalarming — a clear, plain-spoken rejection line in the same calm palette; no error-page drama.

**State context:** Error state — the file failed one of the intake checks.

**Critical affordances:** The specific reason must be stated (never generic); re-upload must be one step away.

---

### State: Permission-denied

**What this screen is for:** Not applicable in this product — public demo, no auth. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state — no authentication gates exist in this app.

**Critical affordances:** None.

---

### State: Edge cases

**What this screen is for:** The populated state's variations when the judge's file is unusual.

**What's visible:** Behaviors per case — renamed input columns show low confidence with manual mapping offered; an output-shaped 252-column file is refused with an explanation that input mapping targets the six input columns only; files over fifty rows show a "first 50 processed (deep-category rows prioritized)" notice; an empty file is accepted and defers to the run's graceful empty result.

**What the user can do:** Map refused columns; proceed knowing the cap is applied; re-upload.

**Feel:** Same intake-QA calm — every variation reads as care, not friction.

**State context:** Edge-case variations of the populated mapping state.

**Critical affordances:** The cap notice must state "deep-category rows prioritized," never "first 50 by luck"; the input-vs-output schema distinction must be explicit when refusing output-shaped files.