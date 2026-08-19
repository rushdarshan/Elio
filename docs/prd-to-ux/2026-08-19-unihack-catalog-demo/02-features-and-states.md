# Features & States — UniHack Catalog Demo

_Scoped by the chosen UX philosophy in `01b-ux-philosophy.md` (Self-Auditing Evidence Report)._

---

## Feature: Upload & Column Mapping

**User Stories:**
- As a judge, I want to upload my own file and have the app tell me honestly how confident it is about each column, so that I trust the run before it starts.
- As a judge, I want ambiguous mappings refused up front with a manual fallback, so that a file that would silently corrupt is never run.

**Screens this feature spans:**
- Intake screen — file drop + column-mapping confidence + schema dry-run (F1's opening beat)

### Screen: Intake

**States:**

#### Empty
The landing state. App title, one-line promise ("Upload any product file — every value will carry its own cited evidence"), a single file dropzone (CSV/XLSX, ≤25MB), and a note about the row cap (~50) and demo-mode framing. No chrome beyond the dropzone — the report's cover page. Secondary: "View sample format" link (downloads the 6-column sample template).

#### Loading
File accepted → parsing with a size/type check (magic bytes, decompression caps). Brief progress line: "Reading file… rows detected, hash computing". If the file fails the type/size checks, this state hands off to Error.

#### Populated
Mapping review: the table of detected columns, each with a confidence chip (high/medium/low) and a suggested mapping to the 6 known input columns. Low/ambiguous columns are refused — a manual mapping control appears inline (dropdown per refused column). The 252-col schema dry-run result shows as a status line ("Output contract: 252 columns ✓"). Input hash + row count displayed. Primary action: "Run pipeline" (enabled only when no column is unmapped). Busy flag: if a run is already in progress, the run button is disabled with "A run is in progress" — the operator drives uploads.

#### Error
Rejection states, each with an explicit reason and a recovery path: file too large (>25MB) → "File exceeds 25MB — split or reduce"; wrong type (magic bytes don't match extension) → "Not a valid CSV/XLSX"; unparseable content → "Could not read rows — check encoding"; zip-bomb / decompression overrun → "File structure rejected". All recover by re-uploading. Never a bare exception.

#### Permission-denied
Not applicable — public demo Space, no auth. State recorded as inapplicable.

#### Edge cases
- Empty file / all-placeholder rows → graceful empty-state on run (see Run feature), not a crash
- Renamed input column (e.g., "Part Number") → confidence shown low, manual mapping offered (AE4)
- Output-shaped file uploaded (252-col) → mapping vs the 6 input columns only; it will not be accepted as input — refusal with explanation
- >50 rows → "First 50 processed (deep-category rows prioritized)" notice on the cap

**Interaction notes:**
- Progressive disclosure: the mapping table appears only after the file passes type/size checks; the manual-mapping control appears only for refused columns
- Key affordances: Run pipeline (primary, gated on full mapping); re-upload (secondary, always available)
- What changes between states: Empty → Loading (dropzone becomes progress line) → Populated (mapping table + Run) or Error (reason + re-upload); a mid-state refresh preserves the mapping via session state (processed flag), so a rerun never reprocesses the file

---

## Feature: Pipeline Run

**User Stories:**
- As a judge, I want to watch the 9 stages complete in visible order with a live-fetch indicator, so that the run never reads as a hang and I can see the pipeline working.

**Screens this feature spans:**
- Run view — per-stage progress, row counts, live-fetch indicator, completion banner (the report being assembled)

### Screen: Run

**States:**

#### Empty
Not reachable as a standalone state — the run only starts from a mapped upload. Recorded as inapplicable.

#### Loading
The run in progress: a 9-stage tracker (Intake → Resolve → Classify → Research → Fetch → Extract → Verify → Describe → Export), stages lighting up as they complete, current stage's row count ticking, and a live-fetch indicator ("Fetching 3 sources…" with per-URL status). A run is 30s-class; the tracker must move within the first seconds. If degraded mode engages (LLM unavailable), a banner appears immediately: "Running in deterministic-only mode — no LLM. Scores will be labeled accordingly." (Honest label, not failure.)

#### Populated
Not a resting state — the run transitions to the Dashboard the moment Export completes. Completion banner: "Run complete — 30 rows enriched in 24s. See the report." Auto-advance to dashboard.

#### Error
Per-row failures never abort the run — a row counter shows "2 rows abstained (reasons logged)" while the run continues. Hard failures (cache/LLM entirely dead → whole-run degradation) show the deterministic-only banner and complete with labeled scores. Mid-run Space restart: progress state restores or the run restarts cleanly, with a notice — never a frozen spinner.

#### Permission-denied
Not applicable — no auth.

#### Edge cases
- Judge's file not fully pre-warmed → pre-run notice in the operator flow ("N rows will fetch live — expect a longer run"); the in-demo run is pre-fetched so this is the exception, not the default
- 0 rows enriched (all-placeholder input) → completes with an explicit "no enrichable rows found" result rather than a dashboard of zeros

**Interaction notes:**
- Progressive disclosure: stage detail (per-URL fetch status) collapses by default; expandable via the stage tracker
- Key affordances: none needed mid-run — the only action is watching; the completion banner auto-advances
- What changes between states: Loading → (banner on degradation) → completion banner → auto-advance to Dashboard; error rows never pause the tracker

---

## Feature: Resolve (Identity Annex)

**User Stories:**
- As a judge, I want to see how the pipeline resolved brand vs manufacturer, so that I can audit identity claims without reading raw output.

**Screens this feature spans:**
- Identity annex panel — entity graph per row (brand/manufacturer/distributor edges + match scores)

### Screen: Identity Annex

**States:**

#### Empty
Reachable when a run produced no resolvable identities: "No identity claims were resolvable for these rows — see the changelog for why." (Placeholder values like `-- Unbranded --` are never inferred — the empty state is honest.)

#### Loading
Not a standalone state — the annex is part of the post-run report and renders with the dashboard. Recorded as inapplicable.

#### Populated
Per-row identity card: resolved brand, manufacturer, and distributor as separate typed edges with match scores and the alias/evidence that produced them. Conflicts (alias→two brands) render flagged, never silently picked (R13).

#### Error
Resolution failures appear as abstained edges with reasons — no crash, no fabrication.

#### Permission-denied
Not applicable.

#### Edge cases
- Unknown manufacturer → abstained edge with "no vocab match — not guessed"
- 1,000-row upload (capped) → only the first 50 rows appear; the annex notes the cap

**Interaction notes:**
- Progressive disclosure: identity cards collapse to a summary line per row; expand for edges + scores
- Key affordances: click an edge → its custody chain (shared drill-down)
- What changes between states: Empty vs Populated differ by content; errors inline per row, never a full-screen failure

---

## Feature: Research (Source Index)

**User Stories:**
- As a judge, I want to see every source the pipeline consulted — cache hit, live fetch, or fallback — so that sourcing is auditable and no marketplace ever appears.

**Screens this feature spans:**
- Source index panel — per-row source timeline and allowlist decisions

### Screen: Source Index

**States:**

#### Empty
Reachable when a run fetched nothing (all rows abstained pre-fetch): "No sources were consulted — rows abstained earlier (see changelog)."

#### Loading
Not a standalone state — renders with the dashboard post-run. Recorded as inapplicable.

#### Populated
Per-row source timeline: each consulted URL tagged cache hit / live / fallback / rejected, with the allowlist decision shown for rejected hosts (e.g., "amazon.com — rejected: marketplace"). Only official manufacturer domains appear; a rejected marketplace is shown as evidence of the guard, not hidden.

#### Error
Fetch failures render as timeline entries with the failure reason ("timeout — 3 retries") rather than as an app error.

#### Permission-denied
Not applicable.

#### Edge cases
- Allowlisted site unreachable → fallback entry with reason; the run continues
- No datasheet PDF found for a flight-critical field → visible as a missing second source in the timeline (why the value is held)

**Interaction notes:**
- Progressive disclosure: timeline collapses to a count per row ("4 sources"); expand for full list
- Key affordances: click a source → its fetched content snippet + hash
- What changes between states: content only; the panel is read-only post-run

---

## Feature: Enrich (Evidence-Led Results)

**User Stories:**
- As a judge, I want every enriched value to carry its citation visibly, so that I can verify any claim in one glance.
- As a judge, I want unsupported fields to read as "not tested," never as missing data holes.

**Screens this feature spans:**
- Results table — per-row attribute list (label/value/UOM + citation); unsupported fields rendered explicitly

### Screen: Results Table

**States:**

#### Empty
All rows abstained: "No values could be enriched with evidence — full abstention. See the changelog for per-field reasons." (The empty state is the honesty narrative, not a failure wall.)

#### Loading
Not a standalone state — renders post-run with the dashboard. Recorded as inapplicable.

#### Populated
Per-row attribute lines: label, value, UOM, and a citation chip (source host + span). Unsupported fields render as "— not tested —" rows with a reason link. Placeholder semantics preserved (`-- Unbranded --` renders as the placeholder, never as a brand). Score cells and values are clickable → custody chain. Verified vs held vs abstained values are visually distinguishable at a glance (status chip per value).

#### Error
Extraction failures → abstained values with reasons inline; never invented values (R9 enforced).

#### Permission-denied
Not applicable.

#### Edge cases
- Contradicted values (two sources disagree) → shown with both citations and a "disputed" chip, routed to Review
- Long values (descriptions) → truncated with expand, never clipped silently
- 252-col parity: values map to their columns; anything unmapped is dropped with an explicit reason, never silently

**Interaction notes:**
- Progressive disclosure: citation chips expand to span + snippet on hover/click; the full custody chain is one click away
- Key affordances: click value → custody chain (F2); disputed values → jump to Review
- What changes between states: populated vs empty differ by honesty of content; the table is read-only post-run except for review links

---

## Feature: Custody Drill-Down (Audit Trail)

**User Stories:**
- As a judge, I want to open any value and see its full custody chain — search result → page → content hash → region/span → re-fetchable snippet — so that I can verify any claim in about one click.

**Screens this feature spans:**
- Custody modal — per-value chain (F2), per-field changelog

### Screen: Custody Modal

**States:**

#### Empty
Reachable only from an abstained cell, where "no evidence exists" is the point: "No evidence — this value abstained by design (R9). See the changelog for the attempt history." Never a dead click.

#### Loading
Hash verification spinner when a snippet is re-fetched from cache ("Verifying content hash…"). Seconds-class.

#### Populated
The chain as an ordered hop list: search result → product page → (linked) datasheet → content hash → page region/span → snippet, each hop with its own evidence fields (URL, fetched time, hash). The field changelog renders below: what changed, why, and by which stage (git-style, replayable).

#### Error
Re-fetch of a snippet fails → the chain renders from stored evidence with a "cached copy (hash verified at capture)" note; never a broken modal.

#### Permission-denied
Not applicable.

#### Edge cases
- Image-only PDF datasheet (no text layer) → the hop renders "no text layer — abstained (OCR out of scope)" — honest, not a broken link
- Long snippets → scrollable within the modal, hash + region shown pinned at top

**Interaction notes:**
- Progressive disclosure: hops render collapsed (one line each); expand per hop for full fields
- Key affordances: close (Escape / backdrop); hop expand; "re-fetch" only where cache holds the content
- What changes between states: empty (abstained cell) vs populated (chain) vs loading (hash verify) — every click lands somewhere meaningful

---

## Feature: Review (Disputed Findings)

**User Stories:**
- As a judge, I want held and disputed values gathered in one post-run panel where I can accept or reject each with both sources visible, so that the escalation beat is legible and my verdict lands in the report.

**Screens this feature spans:**
- Review panel — post-run queue of held/disputed values; verdicts feed the changelog + scoring recompute

### Screen: Review

**States:**

#### Empty
"No values held for review — every flight-critical value had two independent sources." (This is a good-looking state; it is also the exception, since the demo deliberately escalates ≥1 row.) Shown as a positive confirmation, never as an empty void.

#### Loading
Not a standalone state — the panel appears post-run. Recorded as inapplicable.

#### Populated
Held values grouped by field type. Each entry: both sources side-by-side with their evidence hops (or "single source" note), value(s), and per-value Accept/Reject controls. Verdict feedback is immediate: the value's status chip updates, scoring recomputes visibly ("Score updated: 1 accepted, 1 rejected"), and the changelog records the verdict. Judge rejections are recorded as judge disagreement — never folded into abstention (honesty preserved).

#### Error
Panel state is derived from the run — no error path of its own beyond the run's; recorded as inapplicable.

#### Permission-denied
Not applicable.

#### Edge cases
- Two sources disagree → both values + reasons shown; reject is the expected verdict
- Judge runs out of time → unreviewed held values export blank with a "held — unreviewed" flag; the run's numbers stay honest
- Many held rows (review flood) → grouped by field, paginated; bulk accept is NOT offered (per-value verdicts keep the audit trail clean)

**Interaction notes:**
- Progressive disclosure: per-field groups; each entry expands to full source evidence
- Key affordances: Accept / Reject per value (primary); "show custody chain" per source; return-to-results (secondary)
- What changes between states: verdict → status chip change + scoring recompute notice + changelog entry; panel clears items as they're decided

---

## Feature: Dashboard (Self-Score Front Page)

**User Stories:**
- As a judge, I want the headline score and its evidence basis on one front page, so that the accuracy claim is the unmissable moment.
- As a judge, I want to know what the score means — exact, estimate, or deterministic-only — so that I never read a labeled number as a failure.

**Screens this feature spans:**
- Report front page — headline score, 8 metrics, error-budget curve, per-row coverage bar, estimate/degraded stamps

### Screen: Dashboard

**States:**

#### Empty
Pre-run: "No report yet — upload a file to generate one." (The landing → upload flow covers this; the dashboard is not reachable before a run.)

#### Loading
Post-run recompute on review verdicts: metrics refresh with a subtle "recomputing…" indicator on the affected numbers — seconds-class, never a full-screen spinner.

#### Populated
Front page hierarchy:
1. Headline number — field accuracy vs gold (exact, when the upload overlaps the frozen gold set) OR evidence-support rate labeled "estimate" (no overlap) — the single biggest element
2. Stamps — persistent banners/footnotes for "estimate" and "deterministic-only" modes with one-line explanations ("estimate: your file doesn't overlap the frozen gold set — showing evidence-support instead; abstention = engineered honesty")
3. Metric cluster — the 8 metrics: field accuracy vs gold, evidence-support rate, abstention coverage, LOV compliance %, char-limit compliance %, per-SKU cost, decision mix, per-row verified-vs-blank coverage bar
4. Methods section — the 1%/2%/5% field-error-budget curve (risk-coverage), rendered as the report's methodology
5. Every score cell and value clickable → custody chain (F2)

#### Error
No error path of its own — metrics come from the run; a failed run never reaches the dashboard. Recorded as inapplicable.

#### Permission-denied
Not applicable.

#### Edge cases
- Gold overlap of only 12/30 rows → exact rate shown scoped to those 12, rest labeled estimate; the scope is stated, never hidden
- Full 100% abstention run → headline shows "0% enriched" with the honest-stamp framing; the number is never dressed up
- Judge clicks a score cell mid-recompute → chain still opens from stored evidence (never stale-blocked)

**Interaction notes:**
- Progressive disclosure: the 8 metrics collapse under the headline; the curve is expandable; custody chains open from any cell
- Key affordances: click any score cell (primary); expand curve; export (secondary, shared with Export)
- What changes between states: recompute notices on verdict; score scope (exact vs estimate) decided by gold overlap; stamps persist until the run changes

---

## Feature: Export (Report Delivery)

**User Stories:**
- As a judge, I want to download the enriched 252-column CSV (or full JSON) exactly matching the contract, so that the demo ends with a real artifact.

**Screens this feature spans:**
- Export panel — download controls + contract verification status

### Screen: Export

**States:**

#### Empty
Pre-run: "Nothing to export yet — run the pipeline first." (Reachable only by direct navigation pre-run; the stepper normally prevents it.)

#### Loading
Export generation on click: brief "Assembling 252-column contract…" (sanitization + projection run here). Seconds-class.

#### Populated
Two download controls (CSV / JSON) plus a verification line: "252 columns, contract order ✓ — formula-injection sanitized." Per-row compliance flags (char-limit/LOV) attach to the file. The dashboard's headline number is repeated here as the file's cover note.

#### Error
Export fails → "Could not assemble export — see the changelog" with retry; the contract check failing blocks download with a reason (never a silently-wrong file).

#### Permission-denied
Not applicable.

#### Edge cases
- Held-but-unreviewed values at export → exported blank with a "held — unreviewed" flag column, never guessed values
- Huge run (50 rows × 252 cols) → download is a local file; no size issue; JSON includes full evidence (large by design, noted in the download label)

**Interaction notes:**
- Progressive disclosure: contract verification line appears after first successful generation
- Key affordances: Download CSV (primary), Download JSON (secondary), re-verify (tertiary)
- What changes between states: empty (pre-run) → loading (assembling) → populated (downloads + verification); errors keep the panel usable with retry

---