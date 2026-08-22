# Project: ELIO (UniHack Catalog Intelligence)

## Architecture
ELIO is an enterprise-grade, cold-row industrial catalog enrichment pipeline transforming raw product rows (MPN, Description, Manufacturer/Brand) into standardized 252-column commerce-ready records following Unilog Content Guidelines, Master UOM Standards, and LOV taxonomies.

### System Architecture
1. **Core Pipeline DAG (`unihack_catalog/`)**:
   - `stages.py`: 9-stage deterministic DAG (`stage_intake_normalize` -> `stage_entity_resolution` -> `stage_taxonomy_classification` -> `stage_research_planning` -> `stage_document_fetch` -> `stage_extraction` -> `stage_verification` -> `stage_description_generation` -> `stage_export`).
   - `models.py`: Pydantic data models (`RawInputRow`, `ClaimRecord`, `SourceEvidence`, `EnrichedRecord`).
   - `category_extractors.py`: 17 specialized category extraction routines with exact character span tracking (`_locate`).
   - `reference_loader.py`: Authoritative reference data dictionaries (`BRAND_VOCAB`, `TAXONOMY_KEYWORDS`, `UOM_MAP`, `fraction_lookup`).
   - `description_engine.py`: Deterministic description generators for Invoice (<=40 UPPERCASE), Mobile (60-80 chars), Short (<=120 chars), Retail (<=200 chars), and Long (<=500 chars).
   - `verification_ledger.py`: Dual-pass verification engine ensuring 100% verbatim/numeric provenance or honest abstentions across 4 documented classes.

2. **Verification & Cryptographic Harness (`scripts/`)**:
   - `verify_everything.py`: Master 9-gate verification orchestrator.
   - `verify_manifest.py`: SHA-256 manifest integrity validator with cross-platform CRLF normalization.
   - `adversarial_eval.py`: Holdout evaluation on 275 unseen cold rows with 5-factor difficulty scoring.
   - `test_receipt.py`: Cryptographic receipt tamper-rejection suite.
   - `build_decision_log.py`: Event-sourced decision audit log builder and byte-identical replay validator.
   - `rules_linter.py`: Static analysis of regexes, triggers, and distributor filters.
   - `judge_walk.py`: Multi-surface verification covering artifacts, code contracts, and provenance graphs.

3. **Live Cockpit & API (`elio-frontend/`)**:
   - `src/app/api/run/route.ts`: Subprocess API streaming enrichment results on arbitrary user-uploaded CSVs.
   - `src/app/app/dashboard/page.tsx`: Single-file cockpit with in-browser Web Crypto SHA-256 lineage verification, reviewer overrides, and 252-column CSV downloads.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | General DAG Intake & Normalization | Cleanse raw input rows, strip encoding artifacts, normalize whitespace | M1 | ORIGINAL_REQUEST §R1 |
| F2 | Entity Resolution & Distributor Guarding | Resolve brand/manufacturer against UniCat references; filter distributor noise | M1 | ORIGINAL_REQUEST §R1 |
| F3 | Zero SKU Overrides | Eliminate all hardcoded MPN if-branches, answer-key lookup dicts, or SKU special-casing | M1 | ORIGINAL_REQUEST §R1 |
| F4 | Taxonomy & Category Classification | Longest-match keyword hierarchy mapping across 150+ categories | M2 | ORIGINAL_REQUEST §R2 |
| F5 | Grounded Span Extraction | 17 domain extractors with 0-indexed character slice boundaries and SHA-256 hashing | M2 | ORIGINAL_REQUEST §R2 |
| F6 | Master UOM Normalization | Map 60+ unit aliases against Unilog Master UOM standards | M2 | ORIGINAL_REQUEST §R2 |
| F7 | Decimal to Binary Fraction Conversion | Convert decimal measurements up to 1/64-inch increments with GCD reduction | M2 | ORIGINAL_REQUEST §R2 |
| F8 | 4-Class Honest Abstention Engine | Emit clean blanks with standard reason codes for unverified or ambiguous specs | M2 | ORIGINAL_REQUEST §R2 |
| F9 | Dual-Pass Verification Gate | Enforce strict verbatim/numeric provenance auditing before syndication | M2 | ORIGINAL_REQUEST §R2 |
| F10 | Formulaic Description Generation | Synthesize Invoice (<=40 CAPS), Mobile (60-80), Short, Retail, Long descriptions | M3 | ORIGINAL_REQUEST §R3 |
| F11 | 252-Column Syndication Export | Canonical 252-header sequence formatted with `utf-8-sig` (UTF-8 BOM) | M3 | ORIGINAL_REQUEST §R3 |
| F12 | Live Subprocess Execution API | Async CSV upload processing in `api/run/route.ts` with temp cleanup | M4 | ORIGINAL_REQUEST §R4 |
| F13 | Frontend Proof Graph & Cockpit | In-browser SHA-256 lineage verification, reviewer overrides, multi-view exports | M4 | ORIGINAL_REQUEST §R4 |
| F14 | Comprehensive Verification Suite | 9-gate master verification harness generating genuine `artifacts/metrics.json` | M4 | ORIGINAL_REQUEST §R4 |
| F15 | Adversarial & Cold Holdout Gating | Stress testing on unseen cold rows and cryptographic mutation rejection | Final | ORIGINAL_REQUEST §R4 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Overrides Elimination & Entity Resolution | Audit `unihack_catalog/` and `scripts/` to confirm zero hardcoded SKU overrides; verify general DAG intake and entity resolution | None | DONE |
| M2 | Grounded Extraction, UOM & Abstentions | Verify 17 category extractors, exact character span provenance, Master UOM/fractions, and 4-class abstention dual-pass gate | M1 | DONE |
| M3 | 252-Column Schema & Formulaic Descriptions | Verify 252-column export ordering, `utf-8-sig` encoding, description length/casing bounds | M2 | DONE |
| M4 | Live Subprocess API, Frontend Cockpit & Master Harness | Verify live frontend API file processing, sync submission manifest, run master verification suite | M3 | DONE |
| M5 | Final E2E Verification & Adversarial Hardening | Execute full test tiers 1-5 (including cold holdouts, mutation tests, and adversarial evaluation) to confirm 100% gate pass | M4 | DONE |

---

## Interface Contracts

### `stages.py` ↔ `models.py`
- `RawInputRow`: `Mfg_Part_Num: str`, `Part_Desc: str`, `Part_Manuf: str`, `E1_Brand: Optional[str]`, `Unilog_Brand: Optional[str]`, `DIB_Brand: Optional[str]`
- `ClaimRecord`: `attribute_name: str`, `value: str`, `uom: Optional[str]`, `confidence: float`, `provenance_type: str`, `source_span: Optional[Tuple[int, int]]`, `source_text_hash: str`
- `EnrichedRecord`: Complete structured representation with all 50 attribute triples, features, descriptions, and audit metadata.

### `category_extractors.py` ↔ `reference_loader.py`
- Function signatures: `_extract_<category>(text: str, brand: str) -> List[ClaimRecord]`
- Helper: `_locate(text: str, value: str) -> Tuple[Optional[Tuple[int, int]], str]`
- Helper: `fraction_lookup(val_str: str) -> Optional[str]`
- Helper: `normalize_uom(raw_uom: str) -> str`

### `description_engine.py` ↔ `stages.py`
- `generate_invoice_desc(brand: str, item_type: str, mpn: str, specs: List[str]) -> str` (Len <= 40, UPPERCASE)
- `generate_mobile_desc(brand: str, item_type: str, series: str, mpn: str, specs: List[str]) -> str` (Len 60-80)
- `generate_short_desc(...) -> str` (Len <= 120)
- `generate_long_desc(...) -> str` (Len <= 500)

### `scripts/run_pipeline_cli.py` ↔ `elio-frontend/src/app/api/run/route.ts`
- Command: `python scripts/run_pipeline_cli.py --input <input_csv> --output <output_json>`
- Standard output progress format: `PROGRESS:<current>/<total>:<mpn>`
- Return payload JSON: `[{"input": {...}, "record": {...}, "flat_export": {...}}, ...]`

---

## Code Layout
- `unihack_catalog/`:
  - `stages.py` (DAG runner)
  - `models.py` (Pydantic models)
  - `category_extractors.py` (17 domain extractors)
  - `reference_loader.py` (Reference vocabularies & fraction conversion)
  - `description_engine.py` (Formulaic descriptions)
  - `verification_ledger.py` (UAT ledger & dual-pass engine)
- `scripts/`:
  - `verify_everything.py` (Master runner)
  - `verify_manifest.py` (Manifest sync & hash validation)
  - `adversarial_eval.py` (275 cold holdouts)
  - `test_receipt.py` (Cryptographic tamper rejection)
  - `build_decision_log.py` (Event log builder & replay)
  - `rules_linter.py` (Rule linting)
  - `judge_walk.py` (Surface contract checker)
  - `run_pipeline_cli.py` (CLI entry point for frontend API)
- `elio-frontend/`:
  - `src/app/api/run/route.ts` (API route)
  - `src/app/app/dashboard/page.tsx` (Cockpit dashboard)
- `artifacts/`:
  - `metrics.json`, `evidence.json`, `decision_log.jsonl`, `receipt.json`, `acceptance_table.md`
