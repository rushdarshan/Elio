---
date: 2026-08-19
topic: unihack-win-ideation
focus: our main goal is to win this hackathon so do whatever it takes to make us win this hackathon
mode: repo-grounded
---

# Ideation: UniHack Win — 7 survivors

## Grounding Context

**Codebase context (condensed):** UniHack (Unilog) catalog intelligence pipeline in `C:\Users\rushd\Downloads\Jesus WIn`. Judges upload a file → Streamlit app enriches SKU rows (entity resolution → LLM cascade → LOV validation → char-limit compliance → provenance/source URLs) → 252-col export + dashboard. Judging: innovation/accuracy/quality/scalability ≈ equal (accuracy largest, ~40% per VP; portal adds Business Relevance). Solo, ~4 build days, deadline Aug 23 2026. Measured accuracy vs 200-item gold set on Faucets+Fittings, ≥85% target. No hard-coding; per-SKU cost tracked; manufacturer-first, no e-commerce sources. Three public competitor repos for this exact hackathon exist (CatalogIQ, product-enrichment-pipeline, UNI-Hack) — none ship per-value provenance, LOV validation, cost tracking, or char-limit compliance. First edition (no past winners). Cascade economics proven (FrugalGPT ~98%; structural verification > self-confidence). HF Spaces free tier: cache dies on restart, cold starts 30-90s, Streamlit SDK deprecated → Docker SDK. Gold set reference file still blocked (not downloaded from Resources tab).

## Ranked Ideas

### 1. Live Eval Harness — judge's own upload scored live
**Description:** The app scores the judge's uploaded file as it runs: internal-consistency (LOV membership, char limits, dual-pass agreement), evidence-support rate, and — where the upload overlaps it — the frozen gold set. A "predicted accuracy" gauge renders per category in the dashboard. The same harness used in development is shipped, so the 85%+ claim becomes reproducible in 30 seconds, not asserted.
**Warrant:** [`external:` — "Teams optimise for whatever you score on day one" (ai-beavers.com rubric guide); judging rubrics reward measured claims over theatre. `reasoned:` — accuracy is the largest single share (~40%); the only way to defend it live is to make the score an observed artifact of the judge's own run.]
**Rationale:** Converts the headline number from claim → demo. No competitor ships any scoring harness; CatalogIQ/UNI-Hack assert accuracy.
**Downsides:** Scorer must not be gameable (self-score could read as vanity); overlap with gold set may be small on arbitrary uploads — internal-consistency metrics carry the load.
**Confidence:** 85%
**Complexity:** Medium — scorer reuses gold-set eval code; internal-consistency metrics are already computed per row.
**Status:** Explored

### 2. Coverage / Abstention as the hero metric
**Description:** Lead the accuracy story with what the pipeline refuses to fill: coverage reported at 1%/2%/5% field-error budgets (the PRD's risk-coverage curve), abstention treated as a valid clinical result ("inconclusive"), and a per-row verified-vs-blank coverage bar.
**Warrant:** [`direct:` — PRD research HTML: "missing stays missing", "never invent classpath"; the benchmark spec already mandates abstention coverage and error-budget curves; the delta is surfacing them as the headline, not a footnote.]
**Rationale:** Publishing fewer, evidence-backed cells raises measured accuracy more than guessing; the curve is a defensible accuracy story before any gold-set scoring and reads as engineered honesty to quality judges.
**Downsides:** A judge primed on "fill 252 columns" may read blanks as incompleteness — the framing must be explicit and rehearsed.
**Confidence:** 80%
**Complexity:** Low-Medium — curve + gauge UI over existing risk-coverage logic.
**Status:** Explored

### 3. Chain-of-custody evidence graph
**Description:** Every enriched value carries a custody chain — search result → page → content hash → region/span → re-fetchable snippet — rendered as a per-SKU custody report with per-cell drill-down and a field changelog (git-style "what changed and why" with reasons).
**Warrant:** [`external:` — Provenance is a named enterprise pattern; B2B buyers demand provenance metadata and source weighting (jobspikr 2025 B2B guide; webcite grounding survey). `direct:` — PRD research HTML: "a source URL alone is not evidence"; URL + content hash + page/region + snippet is the PRD's own definition.]
**Rationale:** No competitor ships per-value provenance chains — this is simultaneously the innovation story and the quality/accuracy credibility engine.
**Downsides:** UI surface grows; needs disciplined evidence capture from stages 5-6 onward (already in PRD data model).
**Confidence:** 85%
**Complexity:** Medium — evidence graph UI + field-history persistence.
**Status:** Explored

### 4. Verified manufacturer knowledge base as primary source
**Description:** Pre-crawl the official manufacturer domains for the deep categories during build week into a content-hashed evidence index; the live demo's default path is deterministic index lookup with web fetch as secondary repair. Every value carries a citation that was crawled once, not flaked live.
**Warrant:** [`reasoned:` — Provenance, not liveness, is the PRD's evidence definition; a re-fetchable, content-hashed KB satisfies it better than a live crawl that can block/timeout mid-demo. `external:` — HF Spaces free tier kills the cache on restart and cold-starts (30-90s); a pre-built KB survives both.]
**Rationale:** Removes the flakiest stage from the demo's critical path; accuracy improves because verification is against stable, re-fetchable artifacts.
**Downsides:** Pre-crawl is build-week work on top of everything else; scope must stay limited to the two deep categories + top manufacturers.
**Confidence:** 80%
**Complexity:** Medium — crawl + index + hash verification, bounded by category scope.
**Status:** Explored

### 5. Self-built frozen gold set with published methodology
**Description:** If Unilog's 200-item file stays blocked, build our own gold set from the sample rows' real manufacturer documents — frozen BEFORE tuning, double-labeled on hard rows — and publish the labeling methodology. Unilog's file, when it arrives, becomes an external audit of the same harness.
**Warrant:** [`reasoned:` — The eval is the single highest-leverage asset (accuracy ~40%) and is currently blocked on an un-downloaded file; the PRD's own benchmark spec demands freeze-before-tuning discipline, which a self-built set satisfies. `external:` — Judges reward honest self-evaluation methodology over borrowed benchmarks.]
**Rationale:** Unblocks Day 1 of the build plan (stages 3/6/7 calibration) without waiting on the dependency; the methodology document is itself a credibility artifact.
**Downsides:** Labeling effort (~200 rows from manufacturer docs); risk of gold-set bias if built by the same pipeline's assumptions — mitigated by double-labeling and publishing errors.
**Confidence:** 75%
**Complexity:** Medium — labeling effort, not code.
**Status:** Explored

### 6. Trust Engine — accuracy is structural, not model-based
**Description:** Three sub-moves as one thesis: (a) the LLM becomes a query-answerer — the deterministic pipeline poses narrow questions ("does page X state flow rate in L/min?") and the LLM returns evidence spans that rules validate; (b) flight-critical fields (brand/MPN/dims/pack-count) require TWO INDEPENDENT sources (manufacturer page + datasheet PDF), upgrading the PRD's dual-pass; (c) an evidence-repair loop — values lacking evidence are returned to the extractor with a reviewer note until sourced or abstained (capped retries). Plus cheap guards: alias-conflict detector (one alias → two brands flagged) and `-- Unbranded --` never brand-inferred.
**Warrant:** [`external:` — Cascade research: self-confidence gating fails when the cheap model is overconfident-and-wrong; structural verification (JSON parse, LOV membership) is the fix; verifier must cost ≤10-20% of the next stage (generalcompute.com; llm-model-routing-benchmark). `direct:` — PRD: dual-pass on brand/MPN/dims/pack-count only; wrong brand merge costed worse than missed alias; ensemble judges on disagreements.]
**Rationale:** This is where the accuracy score is actually won; it also feeds the model-swap demo (swap the LLM, accuracy holds — verifier-is-the-product).
**Downsides:** Reframes stage 6 extraction; dual-source fetching doubles fetches for 4 fields; repair loop adds iteration cycles.
**Confidence:** 85%
**Complexity:** Medium — refactor of stage 6 + fetch policy + retry loop.
**Status:** Explored

### 7. Judge-upload defense — column-mapping confidence + schema pre-flight
**Description:** Arbitrary judge uploads get a mapping step that shows per-column confidence and REFUSES ambiguous mappings (no silent guessing); a day-one schema dry-run against the gold set's header validates the 252-col contract before any enrichment.
**Warrant:** [`reasoned:` — A silent wrong column mapping corrupts every downstream value — the single biggest silent accuracy killer on a judge's own file; no competitor addresses upload robustness. `direct:` — PRD: judges upload arbitrary files within a 50-row cap; the gold set header is the contract.]
**Rationale:** Protects the accuracy number at the exact point of judge interaction; the refusal UX itself reads as engineering rigor.
**Downsides:** Mapping UI adds surface; refusal must offer manual mapping so judges aren't stuck.
**Confidence:** 80%
**Complexity:** Low — mapping confidence + refusal + header dry-run.
**Status:** Explored

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Live cost dashboard savings-line / $0.00 framing | Duplicates PRD dashboard per-SKU cost metric; delta is presentation framing |
| 2 | Before/after diff per SKU | Merged into #3 (field changelog) |
| 3 | Verifier-is-the-product (model-swap demo) | Folded into #6 as evidence angle |
| 4 | Automation-ceiling page | Tension with locked PRD review panel; brainstorm variant of the panel |
| 5 | Try-with-our-data default state | Demo choreography; app default tweak, not product improvement |
| 6 | Trust propagation graph (page-rank) | Too expensive relative to value for 4-day solo; allowlist policy already covers |
| 7 | Per-field verification budget | Duplicates PRD decision 9 + risk-coverage framing |
| 8 | Gold set as red/green failing-test UX | Merged into #1 (same harness, UX variant) |
| 9 | Engineered escalation moment | Already a PRD success criterion (≥1 predictable escalation) |
| 10 | Completeness map over full 1,000 rows | Breadth story secondary to depth; stretch only |
| 11 | Cold-start restart beat | Demo script beat, not product improvement |
| 12 | Export-readiness N/252 gauge | Folded into #3's evidence chain |
| 13 | Alias-conflict + unbranded flags | Folded into #6 as cheap accuracy guards |
| 14 | Schema dry-run as standalone | Process hygiene; folded into #7 |
| 15 | Char-limit pre-flight gauge | Duplicates PRD char-limit compliance metric |
| 16 | Deep-40 lead framing | Presentation choice, not product improvement |
| 17 | Judge-runnable CLI | Implementation detail of #1's harness |
| 18 | Manufacturer allowlist panel | PRD has allowlist; panel is presentation |

## Tensions noted
- T1: PRD review panel stays (locked); #2's coverage framing and #6's abstention must not look like failure to fill columns — rehearse the framing.
- T2: #4 pre-crawl must stay scoped to deep categories; it is the riskiest build-week addition.
- T3: If Unilog's gold file arrives, #5 becomes an audit of the same harness, not a replacement.