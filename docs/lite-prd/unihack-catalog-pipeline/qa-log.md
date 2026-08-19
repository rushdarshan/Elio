# Q&A log — unihack-catalog-pipeline

**Raw ask:** UniHack Build Spec — Catalog Intelligence Pipeline. Synthesized from `unihack_product_enrichment_research.html` into an executable plan. Target: `rushdarshan/` UniHack submission. Deadline: Aug 23, 11:59pm IST. Key spec points: (0) ground-truth-first — get `Unilog-Sample_200_Items-Input-vs-Output.xlsx` from Resources tab; (1) Pydantic data model with typed entity graph, provenance on every edge/attribute; (2) 9 pipeline stages: intake → entity resolution (brand/manufacturer as typed edges, Splink-style fusion) → taxonomy retrieval (BM25+embedding, constrained candidate selection) → manufacturer-only research planner (Navigator/Extractor/Aggregator) → document ensemble (PDF/OCR, PaddleOCR PP-StructureV3) → evidence-grounded extraction (Instructor, span-cited, reject unsupported values) → verification (dual-pass, calibrated accept/review/reject on gold set) → description compiler (5 descriptions, char limits as tests) → export (JSON + 252-column CSV projection); (3) LangGraph-style orchestration, cascade cost model; (4) demo sequence: upload → resolve → research → enrich → verify (one escalated row) → export; (5) build order: entity resolution first, evaluate against 200-item ground truth continuously. Input files present in repo: `Unihack_ Sample Dataset - Input.csv`, `Unihack_ Expected Output - Delivery Format.csv`, `unihack_product_enrichment_research.html`. Also pasted: UniHack intro/FAQ transcripts (manufacturer sites first, no e-commerce sources, source URL required per value, accuracy/innovation/quality/scalability judged equally, working MVP sufficient, cost-effective APIs OK) and Solution Guide summary (depth beats breadth, LOV-constrained output, 252-col Delivery Format, placeholders are not data, show measured field-level accuracy).

**Mode:** default

## Round 1 — Root (Problem & Core Behavior)

### Q: The Solution Guide says depth beats breadth (one category done fully beats a thin pass over 1,000 rows), but your spec outlines the full 9-stage pipeline. Which scope strategy should the PRD commit to?
- **Chosen:** Full pipeline, hybrid depth
- **Notes:** Build all 9 stages end-to-end, but demo/evaluate deeply on one or two categories (e.g. dishwashers/fittings) where the LOVs are complete.

### Q: Evaluators must click a live link and upload their own dataset (no localhost, no hard-coded outputs). What demo surface do you want to ship?
- **Chosen:** Web app, upload→results
- **Notes:** Streamlit/FastAPI app: upload CSV/XLSX, run pipeline, show resolution graph, source timeline, per-field citations, download CSV/JSON.

### Q: Paid APIs are allowed but must be cost-effective per SKU. What LLM strategy should the pipeline use?
- **Chosen:** Cascade: free/cheap first, paid only on ambiguity
- **Notes:** Deterministic parsing + local open models for obvious rows; paid model only on conflicts, low-confidence retrievals, high-value fields.

### Q: Ground truth and reference files: do you already have the 200-item Input-vs-Output file, LOV, UOM, and manufacturer/brand list downloaded from the Resources tab?
- **Chosen:** Only what's in this folder
- **Notes:** Has Sample-1000 CSV + Expected Output CSV + research HTML. Must fetch 200-item labeled set + reference files from Resources tab before building evals.

## Round 2 — Scope boundaries & constraints

### Q: For the hybrid-depth demo, which 1-2 categories should the pipeline perfect first (where your accuracy numbers will be measured)?
- **Chosen:** Kitchen faucets + fittings
- **Notes:** Faucets have strict LOV spec (build order, attribute sequence, permitted values); fittings has 390 types + 1,472→515 connection normalization — entity-resolution showcase. Both in sample data.

### Q: Where will the live demo link live? Judges must be able to run a real upload end-to-end — the pipeline does web research, so it needs egress + reasonable CPU.
- **Chosen:** Free tier: HF Spaces/Streamlit Cloud
- **Notes:** Zero cost, persistent live link, handles uploads.

### Q: The spec says 'LangGraph-style' orchestration. Do you want actual LangGraph, or a plain-Python DAG with the same properties?
- **Chosen:** Plain Python DAG
- **Notes:** Typed dataclass state, idempotent nodes, retries, interrupt for review — without LangGraph dependency.

### Q: Who's building this and how much time do you actually have between now and Aug 23?
- **Chosen:** Solo, full-time push
- **Notes:** ~4 days to deadline. Prioritize stages 1-2 (entity resolution) + demo harness as the floor.

## Round 3 — Architecture & verification

### Q: Stage 2 (entity resolution) is your headline differentiator. How deep should the matcher go for this build?
- **Chosen:** Alias + fuzzy + vocab
- **Notes:** Alias table from observed Part_Manuf values + RapidFuzz + 27k controlled vocab; no embeddings, no Wikidata. Fully explainable at demo, no infra.

### Q: Demo reliability vs. dynamic research: the pipeline must show live source fetching, but free-tier hosting + live crawls at judge time is where demos die. What research strategy?
- **Chosen:** Cache-first with live fallback
- **Notes:** Pre-crawl/cache official-domain evidence for demo categories; live research runs but hits cache first and degrades gracefully on block/timeout.

### Q: Stage 7 verification runs two independent extraction passes. On which fields should the dual-pass actually run?
- **Chosen:** High-value dual-pass
- **Notes:** Dual-pass on brand, MPN, dimensions, pack count; single-pass + LOV-membership rules elsewhere. Bands calibrated on gold set.

### Q: The submission needs: prototype deck, 3-min demo video, public GitHub repo, live link. Should the PRD scope the packaging or just the software?
- **Chosen:** Software only; deck/video separate
- **Notes:** PRD covers the pipeline + demo app only.

## Round 4 — UX, scale & metrics

### Q: The live app must handle evaluator-uploaded data on free-tier hosting. How should upload volume be handled?
- **Chosen:** Cap rows, show progress
- **Notes:** Process first N rows (e.g. 25-50) per run with progress bar; skip beyond N with a notice.

### Q: Stage 5 routes scanned/low-confidence pages to PaddleOCR PP-StructureV3. Given 4 solo days and free-tier hosting, is OCR in v1 scope?
- **Chosen:** OCR as stretch goal
- **Notes:** v1 = native-text + PDF layout parsing; route to OCR only if time allows. PaddleOCR is heavy for free tier.

### Q: Which numbers should the results dashboard show on screen (multi-select)?
- **Chosen:** Field accuracy vs gold set, LOV compliance %, Char-limit compliance, Per-SKU cost, Confidence/decision mix
- **Notes:** All five selected.

### Q: The demo sequence includes one deliberately-hard row escalated to review. Should that review be an interactive screen or just a flag in the export?
- **Chosen:** Interactive review panel
- **Notes:** Escalated rows → select row → see conflicting evidence spans → accept/reject field → then export.
