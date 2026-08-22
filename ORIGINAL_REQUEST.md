# Original User Request

## 2026-08-22T20:21:45Z

Build and verify a fully generalized, cold-row industrial catalog enrichment pipeline (ELIO) that transforms raw product rows (MPN, Description, Manufacturer / Brand) into standardized 252-column commerce-ready records following Unilog Content Guidelines, Master UOM Standards, and LOV taxonomies, with 100% verifiable source provenance or honest blanks, zero hardcoded product overrides, and a working live dashboard.

Working directory: C:\Users\rushd\Downloads\Jesus WIn
Integrity mode: development

## Requirements

### R1. Absolute Elimination of Hardcoded Overrides & Specialized Code Paths
Audit all pipeline and script files (`unihack_catalog/`, `scripts/`, `elio-frontend/`) and remove every single special-case branch, hardcoded lookup, or pre-written answer tied to specific part numbers (such as `PDSH4816AF`, `WDTS7024RZ`, or any specific catalog SKU). All products—known or unknown—must execute through the exact same deterministic enrichment DAG.

### R2. Strict Grounded Extraction, Controlled Vocabularies & Unit Normalization
All extracted attributes, taxonomy leaf nodes, and brand/manufacturer resolutions must be strictly derived from the raw input text, manufacturer reference tables (`UniCat_Manufacturer_and_Brand_List`, `Unicat_Lov_v1_0`, `FAUCETS_LOV`, `Fittings_LOV`), and authorized web/spec sources. 
- Units of measure must strictly normalize against `Unilog_Master_UOM_Standards_Abbreviations_and_Terms` and `Decimal_Fraction`.
- When an attribute or spec cannot be verified with high confidence, the pipeline must output a clean, honest blank (with standard abstention reason codes), never hallucinating or filling placeholder text.

### R3. Standardized 252-Column Schema and Formulaic Descriptions
Generate the required 252-column delivery schema per Unilog Content Guidelines:
- Construct deterministic descriptions (Invoice ≤40 char CAPS, Mobile 60-80 char, Product Title/Short Desc, Long Desc) solely using verified attributes.
- Ensure exact header sequence, utf-8-sig encoding, and export compatibility with the official evaluation schema.

### R4. End-to-End Live Execution and Verification Harness
Ensure the live frontend cockpit (`elio-frontend/src/app/api/run/route.ts` and dashboard) processes arbitrary user-uploaded CSV files cleanly via the pipeline, streaming verifiable source citations and structured exports. Provide a repeatable programmatic verification harness that evaluates unseen cold holdouts and computes genuine accuracy metrics.

## Acceptance Criteria

### Generalization & Code Cleanliness
- [ ] Codebase audit verifies zero instances of hardcoded MPN special-casing or lookup tables in `unihack_catalog/` and `scripts/`.
- [ ] Any cold, unseen product row executes through the identical pipeline DAG without error.

### Grounded Provenance & Abstention Integrity
- [ ] 100% of emitted attribute claims trace back to exact source spans or authorized reference loaders.
- [ ] Missing, ambiguous, or unconfirmed attributes cleanly output blanks rather than fabricated guesses.
- [ ] Unit conversions conform strictly to the master UOM and fraction lookup rules.

### Schema & Export Compliance
- [ ] Emitted CSV/JSON exports adhere exactly to the canonical 252-header delivery format with `utf-8-sig` encoding.
- [ ] Character length limits and casing formulas (Invoice Description, Mobile Description, Product Title) are strictly enforced.

### Live Runner & Test Verification
- [ ] `python -B scripts\verify_everything.py` (and cold holdout benchmarks) run cleanly and generate genuine, non-faked verification metrics in `artifacts/metrics.json`.
- [ ] `elio-frontend` API and UI live-test on a cold sample row cleanly from upload to export download with verifiable source citations.
