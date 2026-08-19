---
date: 2026-08-19
topic: unihack-win-features
---

# UniHack Win Features — Requirements (7 ideation survivors, ranked)

## Problem Frame

The locked PRD (docs/lite-prd/unihack-catalog-pipeline/lite-prd.md) defines a 9-stage catalog intelligence pipeline with measured accuracy vs a 200-item gold set. The win condition is judged on innovation/accuracy/quality/scalability, with accuracy the largest single share (~40%). The accuracy claim is currently asserted, not observed: judges cannot verify it on their own upload, the gold set is not yet available, and 3 public competitor repos already target this exact hackathon. This brainstorm ranks 7 ideation survivors (docs/ideation/2026-08-19-unihack-win-ideation.md) into must/should/could tiers so the 4-day solo build commits only to the highest-leverage work: making the accuracy number an observable, reproducible artifact of the judge's own run.

---

## Actors

- A1. Judge: uploads an arbitrary file to the live app, watches the run, spot-checks values
- A2. Solo builder (us): builds, calibrates, and runs the offline eval; also the demo operator
- A3. Catalog-ops persona: the buyer perspective the demo addresses (Unilog catalog team doing the same enrichment manually)

---

## Key Flows

- F1. Judge upload → run
  - **Trigger:** A1 uploads a file
  - **Actors:** A1, A2
  - **Steps:** Upload → column-mapping step shows per-column confidence (ambiguous mappings refused with manual fallback) → schema dry-run vs 252-col contract → pipeline run with progress → dashboard renders
  - **Outcome:** A file that would silently corrupt is refused up front; a valid file produces enriched output plus live self-score
  - **Covered by:** R1, R17, R18
- F2. Spot-check audit
  - **Trigger:** A1 clicks a score cell or an enriched value
  - **Actors:** A1
  - **Steps:** Click → custody chain renders (search result → page → content hash → region/span → re-fetchable snippet) → field changelog shows what changed and why
  - **Outcome:** The judge verifies any claim in ~1 click; every enriched value has a traceable source
  - **Covered by:** R6, R7, R8
- F3. Flight-critical uncertainty
  - **Trigger:** A value for brand/MPN/dimensions/pack-count is supported by only one source
  - **Actors:** A2, A3
  - **Steps:** Single-source value is held (not accepted) → escalated to the review panel → evidence is added or the value abstains
  - **Outcome:** No flight-critical value ships on one source alone; the review-panel moment still fires
  - **Covered by:** R11, R12
- F4. Gold-set audit
  - **Trigger:** A2 runs the offline eval, or the judge's upload overlaps the frozen gold set
  - **Actors:** A2, A1
  - **Steps:** Same harness scores the run → exact field match rate shown where rows overlap the gold set; otherwise evidence-support index shown with an "estimate" label
  - **Outcome:** The headline accuracy claim is reproducible in 30 seconds; the offline and demo scoring paths are identical
  - **Covered by:** R2, R3, R14

---

## Requirements

**Priority tiers: Must = M, Should = S, Could = C. Planning commits to all M; S/C are cut candidates.**

**[Self-scoring harness — M (core of #1) + S (coverage framing of #2)]**
- R1. Every completed run displays a live evidence-support rate: % of enriched values with a traceable source span (URL + content hash + page region + re-fetchable snippet) and abstention coverage (fields deliberately left un-enriched). [M]
- R2. Where the uploaded file overlaps the frozen gold set (row key = MPN), the harness also displays exact field match rate, scoped to the overlapping rows; with no overlap, the evidence-support index is shown with an explicit "estimate" label. [M]
- R3. The live harness uses the same scoring code path as the offline development eval — no demo-only scoring path. [M]
- R4. Coverage is displayed as the 1%/2%/5% field-error-budget curve (risk-coverage) plus a per-row verified-vs-blank coverage bar; abstention is a first-class result, never rendered as failure. [S]
- R5. The dashboard gains evidence-support rate and abstention coverage alongside the locked 5 metrics (field accuracy vs gold, LOV compliance %, char-limit compliance %, per-SKU cost, decision mix). [S]

**[Chain-of-custody evidence graph — M (#3)]**
- R6. Any score cell or enriched value is clickable and opens its custody chain. [M]
- R7. Every enriched value carries a custody chain: search result → page → content hash → page region/span → re-fetchable snippet, rendered as a per-SKU custody report with per-cell drill-down. [M]
- R8. A field changelog records what changed and why (reasons retained, git-style), replayable per field. [M]
- R9. Evidence capture is enforced at extraction: a value without an evidence span is not emitted — it abstains. [M]

**[Trust Engine — M (#6, v1 scope)]**
- R10. The LLM operates as a query-answerer: the deterministic pipeline poses narrow questions (e.g., "does page X state flow rate in L/min?") and the LLM returns evidence spans that rules validate; no free-form enrichment output. [M]
- R11. Flight-critical fields (brand, MPN, dimensions, pack count) require two independent sources (e.g., manufacturer page + datasheet PDF); single-source values are held/escalated, never accepted. [M]
- R12. Evidence repair folds into the existing LOV repair ladder (generate → validate → repair → cap 2-3 retries → abstain), extended to evidence presence; no new cross-field repair loop. [M]
- R13. Cheap guards: alias-conflict detector (one alias mapping to two+ brands is flagged, never silently picked) and `-- Unbranded --` / `-- No Unilog Brand --` / `-- No DIB Brand --` placeholders never brand-inferred. [M]

**[Self-built frozen gold set — M (#5)]**
- R14. A 100-row gold set (50 Kitchen Faucets / 50 Fittings) is built from manufacturer documents, double-labeled on hard rows, and frozen before tuning. [M]
- R15. The labeling methodology is published: how labels were derived, which sources, and the double-label resolution rule. [M]
- R16. If Unilog's 200-item file arrives, it is used as an external audit of the same harness — not a replacement for the frozen set. [M]

**[Judge-upload defense — S (#7)]**
- R17. The upload mapping step shows per-column confidence and refuses ambiguous mappings with a manual-mapping fallback; no silent guessing. [S]
- R18. A schema dry-run against the 252-column header contract runs before enrichment (fast fail, not mid-run corruption). [S]

**[Verified manufacturer knowledge base — C (#4)]**
- R19. Official manufacturer domains for the two deep categories are pre-crawled into a content-hashed evidence index; the live demo's default path is index lookup with web fetch as secondary repair; scope bounded to deep categories + top manufacturers. [C]

---

## Acceptance Examples

- AE1. **Covers R1, R3, R5.** Given a 30-row judge upload, when the run completes, the dashboard shows evidence-support 91% and abstention coverage 12%, with a 1%/2%/5% curve; clicking a value opens its custody chain; the number comes from the same code path as the offline eval.
- AE2. **Covers R2.** Given an upload with zero gold-set overlap, when the run completes, the score is labeled "estimate"; given a 12-row overlap, exact match rate is shown for those 12 rows only.
- AE3. **Covers R11.** Given a brand value found on the manufacturer page only, when extraction completes, the value is held for review; when a datasheet PDF confirms it, the value is accepted with both sources in the chain.
- AE4. **Covers R17, R18.** Given a judge upload with a renamed "Part Number" column, the mapping step shows confidence for each column; a column matching nothing is refused with a manual mapping prompt before any enrichment runs.
- AE5. **Covers R10, R12.** Given a flow-rate question, when the LLM returns a span failing the LOV check, the repair ladder runs and abstains after the retry cap — no free-form value is emitted.

---

## Success Criteria

- A judge can reproduce the accuracy claim in 30 seconds on their own file; 5 minutes after the demo, the remembered moment is the self-scoring run.
- No flight-critical value ships on a single source; no ambiguous column mapping is silently guessed; abstention reads as engineered honesty, not missing data.
- The 100-row frozen gold set with published methodology exists and drives calibration (Unilog's file, when it arrives, audits the same harness).
- Handoff: a planner can derive the build plan from the M/S/C tiers alone; the must tier has no hidden product decisions.

---

## Scope Boundaries

- No dedicated cross-field evidence-repair loop — repair lives inside the existing LOV ladder (R12).
- No trust-propagation graph / page-rank source weighting — the manufacturer allowlist policy covers source trust.
- No automation-ceiling page — the locked PRD review panel stays; the coverage framing (R4) is its summary view.
- No live-cost-dashboard theatrics beyond the locked per-SKU cost metric.
- No OCR; no 252-column contract changes; 50-row cap and free-tier host per locked PRD.
- R19 (pre-crawl) is the only tier-C item; it must be droppable without touching any M requirement.

---

## Key Decisions

- **Centerpiece = the self-scoring moment**: the judge watches their own upload get scored; accuracy claim becomes an observed artifact. (User choice)
- **Self-score basis = evidence-support rate + abstention coverage**: honest, cheap, spot-checkable; gold-overlap exact rate shown only when the upload actually overlaps. (User choice)
- **Tiers: Must = #1+#3+#5+#6; Should = #7+#2; Could = #4** — coupling acknowledged: the score (R1) requires custody chains (R7), so #1 and #3 ship together. (User choice)
- **Trust Engine v1 = query-answerer + dual-source**; repair folds into LOV repair; cheap guards included. (User choice)
- **Gold set = 100 rows double-labeled** (50/50 categories), frozen before tuning. (User choice)

---

## Dependencies / Assumptions

- Unilog's 200-item gold file may or may not arrive from the Resources tab; R14-R16 make the eval independent of it. (Assumption: if it arrives mid-build, it audits rather than replaces.)
- The PRD data model already carries source url/page/char_span/snippet per attribute — assumed present; verify during planning.
- Gold-set rows may need to be drawn from real manufacturer SKUs in the deep categories if the 1,000-row sample lacks enough Faucets/Fittings rows (the sample is mostly abrasives). (Unverified — count in planning.)
- HF Spaces free tier: cache is ephemeral; R19's index persists as a repo artifact, not Spaces disk. LLM API keys live in Space secrets, never in the repo.

---

## Outstanding Questions

### Resolve Before Planning

(none — all product decisions resolved)

### Deferred to Planning

- [Affects R14][Needs research] How many of the 1,000 sample rows actually fall in Kitchen Faucets/Fittings, and which MPNs; if too few, select gold rows from manufacturer-published SKUs in the deep categories.
- [Affects R11][Technical] Exact field list for dual-source confirmation (which dimension fields beyond L×W×H, and pack-count definition from the LOV/UOM files).
- [Affects R19][Technical] Manufacturer domain list + crawl scope for the deep categories; whether the Unilog LOV/brand list arrives in time to bound it.

---

## Next Steps

-> /ce-plan for structured implementation planning (tiers M first; S/C as cut candidates)