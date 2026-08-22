# ELIO Frontend — Lite PRD

## Elevator Pitch

A hosted Next.js web app that turns ELIO's frozen, evidence-gated catalog results into a working catalog-operations product: upload a CSV, watch the pipeline run, explore every extracted value down to its source trace, approve or reject decisions, and export a review-complete catalog — with acceptance numbers and abstention honesty front and center.

## Problem Statement

Today the ELIO evidence lives in static artifacts (`demo.html`, `evidence.json`, `decision_log.jsonl`, `acceptance_table.md`). A judge can open `demo.html` and trace values, but there is no product-shaped surface: you can't upload your own file, work a review queue, or export a corrected catalog. The pipeline is proven; the delivery is a folder of files, not a product. For a UNIHACK demo and for any future ops use, that gap is the difference between "a proven pipeline" and "a working product."

## Target Audience

- **Judges (load-bearing)**: want the 5-minute demo — upload, evidence traceability, headline acceptance numbers, and honest abstentions, without engineering noise.
- **Ops reviewers (later)**: want to work a decision queue and produce a corrected export at speed.

## USP

Evidence-gated trust as a usable workflow, not a report: every value the pipeline emits is traceable to a source span or honestly abstained, and the frontend makes that traceability the core interaction — explore, review, decide, export. It is a data-ops layer over a deterministic 9-stage DAG (frozen at `bar-4-freeze`), not another enrichment tool that guesses.

## Target Platforms

- Web (hosted Next.js app, deployed on Render or Railway)
- Single operator, no auth

## Features List

### Upload & Run

- [ ] As a judge, I want to upload a CSV with the 6 required columns (`Mfg_Part_Num`, `Part_Desc`, `Part_Manuf`, `E1_Brand`/`Unilog_Brand`/`DIB_Brand`) so that the pipeline processes my own data.
  - [ ] Strict validation: refuse upload with clear per-column error messages if required columns are missing.
  - [ ] Row cap enforced with a progress bar; synchronous run for demo rows so results appear fast.
  - [ ] Input hash + row count shown after upload (matches the original PRD F1 behavior).
  - [ ] Schema dry-run against the 252-column contract before enrichment (fast fail).

### Acceptance Dashboard

- [ ] As a judge, I want to see the headline metrics so that I can verify ELIO's claims at a glance.
  - [ ] Metrics grid from `metrics.json`: attrs/row (2.156), gold cells byte-exact (118/118), dual-pass verification failures (0), adversarial accepted (589/589 @ 100%), untraceable accepted (0), abstention coverage.
  - [ ] Evidence-support rate and abstention coverage displayed as first-class results, never as failure.
  - [ ] Size toggle: demo (50 rows) default, full (1000 rows) opt-in.
  - [ ] Persistent banner + footnotes labeling "deterministic-only" runs and "estimate" scores when there is no gold overlap — never bare badges.

### Evidence Explorer

- [ ] As a judge, I want to search a part/MPN and see each extracted value with its source trace so that I can verify nothing was invented.
  - [ ] Per-value custody chain: search result → page → content hash → region/span → re-fetchable snippet (R7).
  - [ ] Click any score cell or enriched value to open its custody chain (R6).
  - [ ] Each value shows verification state (supported/contradicted/not_found), source URL, span, snippet, confidence.
  - [ ] Abstained cells show their reason (missing evidence, conflicting evidence, unsupported category, validation failure), never a blank "N/A".
  - [ ] Placeholder semantics (`-- Unbranded --` etc.) visible, never brand-inferred.
  - [ ] Size toggle: demo (50 rows) default, full (1000 rows) opt-in with paginated/virtualized table.

### Review Queue

- [ ] As an ops reviewer, I want to work a queue of escalated decisions so that I can accept, reject, or edit extraction results before export.
  - [ ] Approved/rejected/edited values override the export; changed cells are visibly marked.
  - [ ] Decisions written back to a decision log file (extends the existing `decision_log.jsonl` pattern).
  - [ ] Review is post-run: run completes → review panel → export + scoring recompute.

### Abstention / Trust

- [ ] As a judge, I want a dedicated view of where the system refuses to guess so that I can trust the places it does emit values.
  - [ ] Focused view grouped by refusal reason: evidence missing, conflicting evidence, unsupported category, validation failure.
  - [ ] Abstention is first-class — rendered as a deliberate, explained result, not a gap.

### Export & Delivery

- [ ] As an ops reviewer, I want to export the reviewed catalog so that it is ready for import.
  - [ ] 252-column schema validation status shown.
  - [ ] Rows processed + accepted / reviewed / abstained counts shown.
  - [ ] CSV/JSON download of the review-complete catalog.
  - [ ] "Ready for import" status indicator.
  - [ ] Formula-injection sanitization on export.

### Developer — Architecture (out of main flow)

- [ ] As a developer, I want the codebase graph view (from `graphify-out/graph.html`) available so that I can inspect the pipeline internals.
  - [ ] Hidden from the judge journey; reached via "Developer → Architecture" only.

## UX/UI Considerations

- **Navigation:** persistent sidebar, free navigation between all surfaces — no forced wizard, works as a daily ops tool and a demo walkthrough.
- **Aesthetic:** two-tone — dark app surfaces (engineering-tool feel, matches `demo.html`), light landing/pitch surface.
- **Surfaces:** Upload & Run → Acceptance Dashboard → Evidence Explorer → Review Queue → Abstention/Trust → Export & Delivery; Developer/Architecture separate.
- **States:** every surface handles empty, loading, populated, and error states; upload errors are first-class UI with recovery paths.
- **No generic Home/About/How-it-works/Settings screens** — the product is the workflow.
- **Data:** static bundled artifacts (`evidence.json`, `metrics.json`, `decision_log.jsonl`, `acceptance_table.md`) for demo surfaces; API backend (calling the Python pipeline) only for Upload & Run.

## Non-Functional Requirements

- [ ] **Performance:** fast render of the demo dataset; 1000-row full-export table paginated or virtualized.
- [ ] **Scalability:** demo rows (≤50) run synchronously; full export (1000 rows) supported via size toggle; async queue out of scope for v1.
- [ ] **Security:** single-operator, no auth; formula-injection sanitization on export; no secrets in the bundle.
- [ ] **Accessibility:** baseline — keyboard nav, focus states, sufficient contrast, semantic HTML.

## Critical Questions or Clarifications

- [ ] **Pipeline execution on upload:** the synchronous run calls the real Python pipeline via an API route. How long is acceptable for a 50-row run before the judge's attention wanders? (demo target is "seconds")
- [ ] **Review decision persistence scope:** decisions written back to the log — do they persist server-side per deployment, or reset each deploy? (no DB chosen; likely file-backed on the host)
- [ ] **Rendering source snippets offline:** the custody chain re-fetches source snippets — should snippets be cached in the artifacts so the demo works with no network for the demo surfaces?
- [ ] **Exact branding/name in the app chrome:** "ELIO" confirmed in docs — confirm the app title/logo treatment (light landing surface content).