# PRD — UniHack Catalog Intelligence Pipeline
**Owner:** Darshan K (rushdarshan) · **Deadline:** Aug 23, 2026, 11:59pm IST · **Team:** Solo, ~4 build days
**Status:** Scope locked. Reference files (200-item ground truth, LOVs, UOM standards, manufacturer/brand list) not yet fetched — see Open Dependencies.

---

## 1. Problem & Goal

Unilog needs an AI pipeline that turns a minimal product row (MPN + manufacturer name + short description) into a fully enriched, commerce-ready record across 252 output fields — sourced only from official manufacturer domains, with per-field provenance, and abstaining rather than guessing when evidence is missing.

**Win condition for this build:** a live, evaluator-uploadable app that runs the full pipeline end-to-end on any input, with **measured, on-screen accuracy numbers** that are genuinely strong on two categories (Kitchen Faucets, Fittings) and functionally correct (not necessarily high-accuracy) everywhere else.

## 2. Scope Decisions (locked)

| Axis | Decision |
|---|---|
| Pipeline breadth | Full 9-stage pipeline, always runs end-to-end |
| Accuracy depth | Deep, measured accuracy on **Kitchen Faucets + Fittings** only (strict LOV coverage exists for both) |
| Demo surface | Streamlit app, upload → results, hosted free-tier (HF Spaces / Streamlit Cloud) |
| Row volume | Capped at N (~50) rows/run with progress bar; excess rows skipped with on-screen notice |
| LLM strategy | Cascade — deterministic/rule-based first, paid model (Gemini Flash or GPT-4o-mini) only on ambiguity/high-value fields |
| Entity resolution | Alias table (76 observed `Part_Manuf` values) + RapidFuzz + 27k manufacturer/brand vocab. No embeddings, no Wikidata. |
| Research/sourcing | Cache-first (pre-crawled official-domain evidence for demo categories) with live fetch attempted first, graceful fallback to cache on timeout/block. Manufacturer-domain allowlist only; marketplaces hard-rejected at ingress. |
| Document parsing | Native-text + PDF layout parsing (Docling-style). OCR (PaddleOCR) stubbed as a routing hook only — not implemented in v1. |
| Verification | Dual independent extraction passes on high-value fields only (brand, MPN, dimensions, pack count). Single-pass + rule validation (LOV membership, UOM compatibility, span presence) elsewhere. |
| Orchestration | Plain Python DAG: typed dataclass state, ordered stage functions, retry decorator, one interrupt point for review. No LangGraph. |
| Review UX | Interactive panel: escalated rows listed → click row → see conflicting evidence spans/sources → accept/reject per field → decision persists to export. |
| Dashboard metrics | Field accuracy vs. gold set, LOV compliance %, char-limit compliance %, per-SKU cost, confidence/decision mix (auto_accept / review / reject counts) |
| Out of scope | Packaging (deck, video, repo README) — tracked separately, not a PRD deliverable |

## 3. Data Model

Canonical internal record (Pydantic), per the original build spec — richer than the flat CSV; CSV is a projection at export time.

```json
{
  "input": {"mpn": "...", "raw_text": "...", "raw_manufacturer": "..."},
  "identity": {
    "brand": {"id": "...", "label": "...", "parent": "..."},
    "manufacturer": {"id": "..."}
  },
  "classpath": {"dept": "...", "class": "...", "fine": "...", "candidate_ids": ["..."]},
  "attributes": [
    {"label": "...", "value": "...", "uom": "...",
     "source": {"url": "...", "page": null, "char_span": [0,0], "snippet": "..."},
     "confidence": 0.0, "verification": "supported|contradicted|not_found"}
  ],
  "descriptions": {"mobile": {"text": "...", "chars": 0, "valid": true}, "invoice": {}, "short": {}, "long": {}, "retail": {}, "marketing": {}},
  "quality": {"decision": "auto_accept|review|reject", "field_error_budget": 0.0, "review_reasons": []},
  "cost": {"llm_calls": 0, "estimated_usd": 0.0}
}
```

Every attribute/edge carries provenance (`source URL, snippet/span, confidence, status`). Manufacturer and brand are resolved as **separate typed edges** — never collapsed into one string (e.g. `brand=Diablo`, `manufacturer=Freud Inc.`, distributor code kept separate).

## 4. Pipeline Stages

Plain Python DAG, typed state object passed through ordered stages, retry decorator per stage, cost-cascade throughout (deterministic/cheap first, paid model only on ambiguity).

1. **Intake & normalize** — parse CSV/XLSX, preserve raw input, build expanded text view (tokenized MPN, dims, UOMs, brand mentions).
2. **Entity resolution** — alias table → RapidFuzz → 27k manufacturer/brand vocab match. Resolve `brand_of` / `manufactured_by` as separate edges. No merge without evidence.
3. **Taxonomy classification** — retrieval over Dept/Class/Fine index (built from LOV files), rank/pick only from retrieved candidates; low-confidence → review flag, never invent a classpath.
4. **Research planning** — per-record allowlist from resolved manufacturer's official domain(s); MPN + product-family search; hard-reject marketplaces at ingress.
5. **Document fetch** — cache-first fetch of HTML/PDF, content-hashed; live fetch attempted, cache fallback on failure. Faucets/Fittings pre-crawled during build week.
6. **Extraction** — native-text + PDF layout parsing. One record per attribute with exact span. **Reject any value without evidence span** — missing stays missing.
7. **Verification** — dual-pass on brand/MPN/dimensions/pack-count; LOV/UOM rule checks elsewhere. Calibrated accept/review/reject bands from the 200-item gold set.
8. **Description generation** — freeze verified facts, generate 5 variants (mobile/invoice/short/long/retail/marketing) against fixed char limits and field order as executable tests, not prompt hope. Repair ladder on overflow.
9. **Export** — JSON (full record) + 252-column CSV projection, provenance and compliance flags attached.

## 5. Demo App (Streamlit)

- **Upload** → row count + input hash shown, row cap enforced with progress bar.
- **Resolve** → entity graph shown (brand/manufacturer/distributor edges + match scores).
- **Research** → source timeline (cache hit vs. live fetch vs. fallback), allowlist decisions visible.
- **Enrich** → attributes populate with label/value/UOM + citation; unsupported fields visibly blank.
- **Review** → interactive panel for escalated rows (Faucets/Fittings-tuned to surface at least one hard case reliably).
- **Export** → CSV/JSON download + dashboard: accuracy, LOV compliance, char compliance, per-SKU cost, confidence mix.

## 6. Success Criteria

- App runs on a public live link, no localhost, no hard-coded outputs.
- Evaluator can upload an arbitrary file and get real output within the row cap.
- Faucets + Fittings: field accuracy vs. 200-item gold set is the headline number and must be defensible (target ≥85%, stretch ≥90%).
- All 9 stages execute for every row, even outside the two deep categories (degraded quality acceptable, silent failure not).
- At least one row in the demo run predictably escalates to interactive review.
- Dashboard shows all 5 committed metrics on every run.

## 7. Open Dependencies (block Day 1 work)

Must be fetched from the UniHack Resources tab before Stage 3/6/7 work starts:
- `Unilog-Sample_200_Items-Input-vs-Output.xlsx` — the actual labeled ground truth (not yet in repo; current `Expected_Output` CSV is header-template + 1 example only)
- `Unicat_Lov_v1_0_Updated_With_Remarks.xlsx` — cross-category LOV
- `FAUCETS_LOV.xlsx`, `Fittings_LOV.xlsx` — category-specific specs
- `UniCat_Manufacturer_and_Brand_List.xlsx` — 27k canonical vocab
- `Unilog_Master_UOM_Standards_Abbreviations_and_Terms.xlsx`
- `Decimal_Fraction.xlsx`
- `UNILOG_INTERNAL_CONTENT_GUIDELINES.docx`

## 8. 4-Day Build Plan

- **Day 1**: Fetch reference files. Data model. Stage 1–2 (intake, entity resolution) against full 1000-row sample.
- **Day 2**: Stage 3 (classify) + Stage 4–6 (research/extract) scoped to Faucets+Fittings. Streamlit skeleton wired to stub pipeline. Begin pre-crawl cache for demo categories.
- **Day 3**: Stage 7–9 (verify/generate/export) for the two deep categories, measured against gold set. Full pipeline stitched end-to-end, dashboard live.
- **Day 4**: Review panel polish, evaluator-upload edge cases (dead site, unknown category, oversized file), buffer, deploy to public link.

## 9. Explicit Non-Goals (v1)

- OCR / scanned-document extraction
- Embedding-based / Wikidata entity resolution
- Async background job queue for large uploads
- LangGraph or any heavyweight orchestration runtime
- Accuracy guarantees outside Faucets + Fittings

---

# UX-Facing Addendum (from requirements + plan)

## Key Flows (judge-facing)

- **F1. Judge upload → run:** Upload → column-mapping step shows per-column confidence (ambiguous mappings refused with manual fallback) → schema dry-run vs 252-col contract → pipeline run with progress → dashboard renders.
- **F2. Spot-check audit:** Click a score cell or enriched value → custody chain renders (search result → page → content hash → region/span → re-fetchable snippet) → field changelog shows what changed and why.
- **F3. Flight-critical uncertainty:** A brand/MPN/dimensions/pack-count value supported by only one source is held (not accepted) → escalated to the review panel → evidence added or the value abstains.
- **F4. Gold-set audit:** Same harness scores the run → exact field match rate shown where rows overlap the frozen gold set; otherwise evidence-support index with an "estimate" label.

## Win-feature requirements (dashboard-facing)

- R1. Every completed run displays live evidence-support rate (% of enriched values with traceable source span) and abstention coverage (fields deliberately left un-enriched).
- R2. Where upload overlaps the frozen gold set (row key = MPN), exact field match rate scoped to overlapping rows; with no overlap, evidence-support index with explicit "estimate" label.
- R4. Coverage displayed as the 1%/2%/5% field-error-budget curve plus a per-row verified-vs-blank coverage bar; abstention is a first-class result, never rendered as failure.
- R5. Dashboard: evidence-support rate + abstention coverage alongside locked 5 metrics (field accuracy vs gold, LOV compliance %, char-limit compliance %, per-SKU cost, decision mix).
- R6. Any score cell or enriched value is clickable → opens custody chain.
- R7. Every enriched value carries a custody chain: search result → page → content hash → page region/span → re-fetchable snippet.
- R8. Field changelog records what changed and why (reasons retained, git-style), replayable per field.
- R13. Placeholder semantics (`-- Unbranded --` etc.) are visible, never brand-inferred.
- R17. Upload mapping step shows per-column confidence; ambiguous mappings refused with manual-mapping fallback; no silent guessing.
- R18. Schema dry-run against the 252-column header contract runs before enrichment (fast fail).

## Demo constraints (plan U9)

- Single-replica: busy flag refuses a second upload during a run; operator drives the upload.
- Warm-up beat: judge's file is pre-fetched before the demo so the in-demo run is cache hits within the 30s window; live fetch = "live run" mode, labeled.
- Dashboard labels runs "deterministic-only" (degraded LLM mode) and scores "estimate" (no gold overlap) — persistent banner + footnotes, never bare badges.
- Upload limits: 25MB max, magic-byte type check, row cap before full parse, deep-category-first row selection.
- Review is post-run: run completes → review panel → export + scoring recompute.
- Export: formula-injection sanitization; 252-col contract check.