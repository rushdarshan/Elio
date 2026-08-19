# UX Philosophy — UniHack Catalog Demo

## Chosen Philosophy: Self-Auditing Evidence Report (C+A blend)

**Organizing metaphor / mental model:**
A quality report that audits itself — the self-score is the front page, every number carries its own cited evidence footnote, and abstention reads as "not tested," never as failure.

**How the PRD features map into this structure:**
- Upload → Intake QA: column-mapping confidence shown like a lab intake form; ambiguous columns refused up front, manual mapping offered.
- Resolve → Identity annex: entity graph rendered as a compact identity footnote (brand/manufacturer edges + scores) under each row, not a standalone spectacle.
- Research → Source index: timeline (cache hit / live / fallback) rendered as the report's bibliography — per value, per row, all sources listed.
- Enrich → Evidence-led results: attributes as labeled, cited line items (value + UOM + citation); unsupported fields render as explicit "not tested" rows, never blank voids.
- Review → Disputed findings: held rows as contested claims with both sources shown side-by-side; accept/reject is the auditor's verdict; decision lands in the changelog.
- Export → Report delivery: CSV/JSON download plus the self-scoring dashboard; formula-sanitized.
- Dashboard → Front page: the headline number (field accuracy vs gold, or "estimate") is the hero; the 8 metrics sit as a footnote cluster under it; the 1%/2%/5% curve and per-row coverage bar are the report's methods section; every score cell clickable → custody chain (the report's appendix).
- Custody chain → Appendix: search result → page → content hash → span → re-fetchable snippet, per value, one click from any score cell.
- Changelog → Audit trail: git-style record of what changed and why, replayable per field.
- Degraded modes → Honest labels: "deterministic-only" and "estimate" are persistent report stamps with explanatory footnotes, never bare badges.

**Trade-offs:**
- Good at: making the headline accuracy number (the largest single judging share, ~40%) the unmissable moment; making trust verification (F2) a one-click appendix read; making abstention legible as engineered honesty — the plan's own success criterion is "the remembered moment is the self-scoring run," and this philosophy manufactures exactly that moment.
- Sacrifices: pipeline machinery (entity graph, source timeline) becomes secondary appendices rather than stage-lit features; the flow is calmer than a cockpit — acceptable because the judge's job is to verify, not to operate.

**Why the user chose this:**
User directed "focus on what can make us win." Chosen because it optimizes the judging rubric: accuracy share (~40%) demands the number be the hero; innovation (provenance/custody — the competitor gap) must be provable in one click; quality reads as report-grade polish; and the mandatory escalation beat lands as "disputed findings." The cockpit alternative's theater dilutes the headline number; the pure ledger's self-score is a summary row instead of a moment.

---

## Rejected Alternative 1: Evidence Ledger (auditor's workbook)

**Metaphor:** Every enriched value is a ledger line item — value, source, hash, span, status; the dashboard is the summary sheet.
**Feature mapping summary:** Enrich = ledger entries with citation columns; Review = flagged entries awaiting the auditor; custody chain = entry audit trail; changelog = ledger history.
**Trade-offs:** Native fit for F2 spot-checks and trust; but the self-score is a summary row, not a moment — the winning moment (judge watches their upload get scored) is underplayed.
**Why rejected:** The win condition needs the scoring moment front and center; a ledger foregrounds verification over the number.

## Rejected Alternative 2: Pipeline Cockpit (operator console)

**Metaphor:** A flight deck — stage lamps, instrument cluster, throttle (cost), flight-critical alarms (held rows).
**Feature mapping summary:** Run = flight; progress = stage lamps; metrics = instrument cluster; Review = alarm queue; evidence = black-box recorder.
**Trade-offs:** Best demo theater for a live run; matches the plan's operational language; but the headline accuracy number becomes one gauge among many — diluting the ~40% scoring share, and the tool-read risks reading as machinery rather than measured results.
**Why rejected:** On the rubric, legibility of the accuracy number and the trust drill-down beat instrument theater.