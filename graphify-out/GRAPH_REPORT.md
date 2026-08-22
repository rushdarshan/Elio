# Graph Report - Jesus WIn  (2026-08-23)

## Corpus Check
- 119 files · ~849,060 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1198 nodes · 1501 edges · 112 communities (87 shown, 25 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 42 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `93d9cf70`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- stages.py
- Tier1FeatureTests
- run_pipeline
- receipt_chain.py
- devDependencies
- category_extractors.py
- compilerOptions
- Gauntlet Loop — Live Progress
- dashboard/page.tsx
- UniHack Catalog Intelligence Pipeline (win-features integrated)
- Implementation Units
- feat: GithubAwesome Steal Program — 7 Provenance & Trust Wins
- 5. Components
- Q&A log — elio-frontend
- Q&A log — unihack-catalog-pipeline
- ELIO Judge-Proof Submission
- verify_everything.py
- ELIO Frontend — Lite PRD
- ELIO Frontend — Lite PRD
- 3. View Architectures & Layouts
- UniHack Win Features — Requirements (7 ideation survivors, ranked)
- GithubAwesome Steal Program — 7 Provenance & Trust Wins for UniHack
- PRD — UniHack Catalog Intelligence Pipeline
- ReferenceLoader
- fraction_lookup
- Ranked Ideas
- Acceptance Criteria
- Ranked Ideas
- Ranked Ideas
- Ranked Ideas
- Project: ELIO (UniHack Catalog Intelligence)
- PRD — UniHack Catalog Intelligence Pipeline
- build_deck.js
- CompetitorBaselineEnricher
- Screen: Custody Modal
- Screen: Dashboard
- Screen: Results Table
- Screen: Export Panel
- Screen: Run
- Screen: Source Index
- Screen: Identity Annex
- Screen: Review Panel
- Screen: Intake
- Gauntlet — ELIO vs Proton PIM (bar: https://www.proton.ai/pim)
- Product
- PLAN: ELIO Frontend — Judge-Ready Quality Pass
- AGENTS.md — ELIO (UniHack Catalog Intelligence)
- FREEZE — Bar 5 (Clean Genuine Extraction)
- DISCLOSURE — How ELIO Uses LLMs
- Screen: Intake
- Screen: Results Table
- Screen: Custody Modal
- Screen: Review
- Screen: Dashboard
- Screen: Export
- Screen: Run
- ELIO — Judge-Proof Catalog Intelligence (Pitch)
- Screen: Identity Annex
- Screen: Source Index
- Upload & Run — Screen Prompts
- Elio - UniHack Catalog Intelligence
- adversarial_eval.py
- 🧭 00-START_HERE.md — ELIO Cold-Start Walk Map & Judge Guide
- Evidence Explorer — Screen Prompts
- gauntlet_holdout_eval.py
- UX Philosophy — UniHack Catalog Demo
- UX Philosophy — ELIO Frontend
- Acceptance Dashboard — Screen Prompts
- Review Queue — Screen Prompts
- RED_TEAM — What Was Attacked, What Passed, What Remains Untested
- WALK_TEST — Fresh-Clone Acceptance Gate
- src/app/layout.tsx
- build_evidence.py
- fill_unihack_deck.py
- Features & States — UniHack Catalog Demo
- Abstention / Trust — Screen Prompts
- Export & Delivery — Screen Prompts
- elio-frontend/README.md
- check_freeze.py
- generate_deck_diagrams.py
- generate_stress_cases.py
- Developer / Architecture — Screen Prompts
- route.ts
- app/app/layout.tsx
- diff_exports.py
- export_slide_images.py
- elio-frontend/AGENTS.md
- eslint.config.mjs
- next.config.ts
- postcss.config.mjs
- GATES.md
- .test_f2_01_distributor_blacklist_appde
- .test_f3_03_sku_collision_independence
- .test_f3_05_no_hardcoded_gold_short_circuits
- .test_f4_01_longest_keyword_match_precedence
- .test_f4_02_power_tools_classification
- .test_f5_04_case_insensitive_boundary_matching
- .test_f8_01_absent_specification_clean_blank
- .test_f8_02_ambiguous_specification_abstention
- .test_f8_03_zero_hallucinated_features
- .test_f9_05_zero_unverified_leakage
- .test_f10_01_invoice_desc_bounds_and_casing
- .test_f10_04_retail_desc_bounds
- .test_f11_01_canonical_column_count
- .test_f11_04_item_features_and_unspsc_columns

## God Nodes (most connected - your core abstractions)
1. `Tier1FeatureTests` - 75 edges
2. `run_pipeline()` - 73 edges
3. `stage_intake_normalize()` - 23 edges
4. `Gauntlet Loop — Live Progress` - 21 edges
5. `verify_receipt()` - 18 edges
6. `ReferenceLoader` - 17 edges
7. `compilerOptions` - 16 edges
8. `build_receipt()` - 16 edges
9. `EnrichedRecord` - 16 edges
10. `ReceiptError` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Tier1FeatureTests` --uses--> `AttributeRecord`  [INFERRED]
  tests/test_tier1_features.py → unihack_catalog/models.py
- `Tier1FeatureTests` --uses--> `SourceProvenance`  [INFERRED]
  tests/test_tier1_features.py → unihack_catalog/models.py
- `GauntletCritic` --uses--> `CompetitorBaselineEnricher`  [INFERRED]
  scripts/gauntlet_critic.py → competitors/uni_hack/competitor_baseline.py
- `gold_check()` --calls--> `run_pipeline()`  [EXTRACTED]
  scripts/adversarial_eval.py → unihack_catalog/stages.py
- `run_all()` --calls--> `run_pipeline()`  [EXTRACTED]
  scripts/adversarial_eval.py → unihack_catalog/stages.py

## Import Cycles
- None detected.

## Communities (112 total, 25 thin omitted)

### Community 0 - "stages.py"
Cohesion: 0.07
Nodes (60): BaseModel, Exception, main(), process(), DataFrame, Tier 1: Feature Coverage E2E Tests for ELIO (UniHack Catalog Intelligence).…, F9.1: Verified attributes confirm verbatim or numeric presence in raw input., F9.3: Manually injected ungrounded attribute fails dual-pass verification. (+52 more)

### Community 1 - "Tier1FeatureTests"
Cohesion: 0.04
Nodes (30): Any, F1.5: Replaces newlines and carriage returns with clean single spaces., F3.2: Confirms no static MPN lookup — output adapts dynamically to description., F6.1: Normalizes \", inch, inches, in. to standard 'in'., F6.2: Normalizes voltage, amperage, wattage, hertz., F6.3: Normalizes GPM, PSI, CFM, dBA., F6.4: Normalizes feet, mm, cm, gallons, cu ft., F6.5: Normalizes package terms (ea, pk, pc, ct, dz). (+22 more)

### Community 2 - "run_pipeline"
Cohesion: 0.04
Nodes (26): evaluate_gold(), Dedicated Test-Only Gold Set Evaluator for ELIO. Evaluates pipeline performance…, main(), F2.2: Rejects Palmer Donavin (PALDO) distributor noise., F2.3: Correctly resolves Diablo to Freud Inc. parent manufacturer., F2.4: Resolves DEWALT brand to Stanley Black & Decker parent., F2.5: Gracefully falls back to Unbranded when no brand/manufacturer detected., F3.1: Completely unseen synthetic SKU executes through identical DAG. (+18 more)

### Community 3 - "receipt_chain.py"
Cohesion: 0.12
Nodes (37): Publish the minimal receipt index consumed by the offline cockpit drawer., main(), Generate the content-addressed receipt for the canonical demo artifacts., get(), live_walk(), load_json(), main(), Path (+29 more)

### Community 4 - "devDependencies"
Cohesion: 0.05
Nodes (40): dependencies, gsap, @gsap/react, lucide-react, next, pptxgenjs, react, react-dom (+32 more)

### Community 5 - "category_extractors.py"
Cohesion: 0.14
Nodes (29): _color(), _extract_adapters(), _extract_appliances(), _extract_belts(), _extract_blades(), _extract_ceiling_tiles(), _extract_discs(), _extract_drill_bits() (+21 more)

### Community 6 - "compilerOptions"
Cohesion: 0.07
Nodes (28): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+20 more)

### Community 7 - "Gauntlet Loop — Live Progress"
Cohesion: 0.07
Nodes (26): Bar 3: LLM-assisted long-tail enrichment (2026-08-20), Bar 4 — Adversarial-hardened pipeline (FROZEN, tag bar-4-freeze), Blind fresh-context critic (det vs assisted, cell-level diff), Design, Export audit vs committed Bar-2 export (08d72e3), Final state (Round 3, all checks green), Gauntlet Loop — Live Progress, Known honest limits (accepted, not hidden) (+18 more)

### Community 8 - "dashboard/page.tsx"
Cohesion: 0.08
Nodes (19): Attribute, canonicalJson(), DashboardPage(), DECISION_STYLES, DescriptionPack, ExportProjection, HashState, PipelineRecord (+11 more)

### Community 9 - "UniHack Catalog Intelligence Pipeline (win-features integrated)"
Cohesion: 0.08
Nodes (25): Context & Research, Deferred to Follow-Up Work, Deferred to Implementation, Documentation / Operational Notes, External References, High-Level Technical Design, Implementation Units, Institutional Learnings (+17 more)

### Community 10 - "Implementation Units"
Cohesion: 0.08
Nodes (25): Acceptance Examples, Assumptions, Dashboard & Performance, Definition of Done, Evidence Drawer & Custody Chain, Goal Capsule, Implementation Units, Key Decisions (+17 more)

### Community 11 - "feat: GithubAwesome Steal Program — 7 Provenance & Trust Wins"
Cohesion: 0.08
Nodes (25): Context & Research, Deferred to Follow-Up Work, Deferred to Implementation, Documentation / Operational Notes, External References, feat: GithubAwesome Steal Program — 7 Provenance & Trust Wins, High-Level Technical Design, Implementation Units (+17 more)

### Community 12 - "5. Components"
Cohesion: 0.08
Nodes (24): 1. Overview, 2. Colors, 3. Typography, 4. Elevation, 5. Components, 6. Do's and Don'ts, Buttons, Cards / Containers (+16 more)

### Community 13 - "Q&A log — elio-frontend"
Cohesion: 0.09
Nodes (21): Q&A log — elio-frontend, Q: Data volume — 50-row demo or 1000-row full export?, Q: Does the frontend need users/roles/permissions?, Q: How does the pipeline run — synchronous or async?, Q: How important are in-between states (empty, loading, error, permission-denied)?, Q: How important is offline/airgapped operation?, Q: How should the frontend be built?, Q: How should users move between the 6 surfaces? (+13 more)

### Community 14 - "Q&A log — unihack-catalog-pipeline"
Cohesion: 0.09
Nodes (21): Q&A log — unihack-catalog-pipeline, Q: Demo reliability vs. dynamic research: the pipeline must show live source fetching, but free-tier hosting + live crawls at judge time is where demos die. What research strategy?, Q: Evaluators must click a live link and upload their own dataset (no localhost, no hard-coded outputs). What demo surface do you want to ship?, Q: For the hybrid-depth demo, which 1-2 categories should the pipeline perfect first (where your accuracy numbers will be measured)?, Q: Ground truth and reference files: do you already have the 200-item Input-vs-Output file, LOV, UOM, and manufacturer/brand list downloaded from the Resources tab?, Q: Paid APIs are allowed but must be cost-effective per SKU. What LLM strategy should the pipeline use?, Q: Stage 2 (entity resolution) is your headline differentiator. How deep should the matcher go for this build?, Q: Stage 5 routes scanned/low-confidence pages to PaddleOCR PP-StructureV3. Given 4 solo days and free-tier hosting, is OCR in v1 scope? (+13 more)

### Community 15 - "ELIO Judge-Proof Submission"
Cohesion: 0.09
Nodes (21): Context & Research, Deferred to Follow-Up Work, Documentation / Operational Notes, ELIO Judge-Proof Submission, External References, High-Level Technical Design, Implementation Units, Institutional Learnings (+13 more)

### Community 16 - "verify_everything.py"
Cohesion: 0.17
Nodes (16): build(), replay(), sanity_check_rules(), acceptance_table(), gate(), gold_check(), header_ok(), main() (+8 more)

### Community 17 - "ELIO Frontend — Lite PRD"
Cohesion: 0.11
Nodes (17): Abstention / Trust, Acceptance Dashboard, Critical Questions or Clarifications, Developer — Architecture (out of main flow), Elevator Pitch, ELIO Frontend — Lite PRD, Evidence Explorer, Export & Delivery (+9 more)

### Community 18 - "ELIO Frontend — Lite PRD"
Cohesion: 0.11
Nodes (17): Abstention / Trust, Acceptance Dashboard, Critical Questions or Clarifications, Developer — Architecture (out of main flow), Elevator Pitch, ELIO Frontend — Lite PRD, Evidence Explorer, Export & Delivery (+9 more)

### Community 19 - "3. View Architectures & Layouts"
Cohesion: 0.12
Nodes (16): 1. The Design Read & Dial Configuration, 2.A Color Palette, 2.B Typography System, 2. Design System Map (Tailwind v4 & Radix Tokens), 3. View Architectures & Layouts, 4.A GSAP Sticky-Stack Walkthrough, 4.B Tabular Hover States, 4.C Skeletal Loaders (+8 more)

### Community 20 - "UniHack Win Features — Requirements (7 ideation survivors, ranked)"
Cohesion: 0.13
Nodes (14): Acceptance Examples, Actors, Deferred to Planning, Dependencies / Assumptions, Key Decisions, Key Flows, Next Steps, Outstanding Questions (+6 more)

### Community 21 - "GithubAwesome Steal Program — 7 Provenance & Trust Wins for UniHack"
Cohesion: 0.13
Nodes (14): Acceptance Examples, Actors, Deferred to Planning, Dependencies / Assumptions, GithubAwesome Steal Program — 7 Provenance & Trust Wins for UniHack, Key Decisions, Key Flows, Next Steps (+6 more)

### Community 22 - "PRD — UniHack Catalog Intelligence Pipeline"
Cohesion: 0.13
Nodes (14): 1. Problem & Goal, 2. Scope Decisions (locked), 3. Data Model, 4. Pipeline Stages, 5. Demo App (Streamlit), 6. Success Criteria, 7. Open Dependencies (block Day 1 work), 8. 4-Day Build Plan (+6 more)

### Community 23 - "ReferenceLoader"
Cohesion: 0.16
Nodes (3): _derive_brand_refs(), Any, ReferenceLoader

### Community 24 - "fraction_lookup"
Cohesion: 0.14
Nodes (9): F7.1: Converts standard binary decimals to irreducible fractions., F7.2: Converts sixteenth decimals accurately., F7.3: Converts 1/64-inch increments., F7.4: Converts mixed numbers like 7.25 -> 7-1/4, 4.5 -> 4-1/2., F7.5: Returns empty string for decimals not on 1/64 grid (e.g. 0.333, 0.7)., fraction_lookup(), load_all(), 0.5' -> '1/2', '50.25' -> '50-1/4'. '' if not a neat 1/64 fraction. (+1 more)

### Community 25 - "Ranked Ideas"
Cohesion: 0.15
Nodes (12): 1. Live Eval Harness — judge's own upload scored live, 2. Coverage / Abstention as the hero metric, 3. Chain-of-custody evidence graph, 4. Verified manufacturer knowledge base as primary source, 5. Self-built frozen gold set with published methodology, 6. Trust Engine — accuracy is structural, not model-based, 7. Judge-upload defense — column-mapping confidence + schema pre-flight, Grounding Context (+4 more)

### Community 26 - "Acceptance Criteria"
Cohesion: 0.15
Nodes (12): 2026-08-22T20:21:45Z, Acceptance Criteria, Generalization & Code Cleanliness, Grounded Provenance & Abstention Integrity, Live Runner & Test Verification, Original User Request, R1. Absolute Elimination of Hardcoded Overrides & Specialized Code Paths, R2. Strict Grounded Extraction, Controlled Vocabularies & Unit Normalization (+4 more)

### Community 27 - "Ranked Ideas"
Cohesion: 0.17
Nodes (11): 1. verify_everything.py + metrics.json — one command, live acceptance grid, 2. spot_check.py --mpn + why_blank.py — interrogable evidence probe, 3. demo.html — static offline row explorer, cell-to-evidence + abstention annotations, 4. Freeze hygiene: check_freeze.py + clean tree, 5. DISCLOSURE.md + corrections box, 6. Red-team dossier — "how we tried to break it", 7. PITCH.md — judge one-pager, Grounding Context (+3 more)

### Community 28 - "Ranked Ideas"
Cohesion: 0.17
Nodes (11): 1. Provenance Waterfall Drawer (per-cell trace), 2. Highlight-To-Prove — LangExtract Verbatim Map, 3. Upload Doctor & Healing Preview (markitdown/docling/Tiny PDF), 4. Abstention Triage Queue (Evidently/promptfoo), 5. DSPy Regex Workbench (with dual-pass guard), 6. Static Offline Explorer (GitAll/Gander — no backend), 7. Brand Conflict Graph Resolver (GraphRAG + Firecrawl live verify), Grounding Context (+3 more)

### Community 29 - "Ranked Ideas"
Cohesion: 0.17
Nodes (11): 1. Local-first one-command bulk extractor (hybrid yt-dlp + resume), 2. Provenance-anchored transcript store (ELIO-style ledger), 3. Timestamped repo-aware chunking → searchable catalog + RAG index, 4. Channel taxonomy preservation (series-aware grouping), 5. Hybrid cost ladder: local → API fallback → Whisper (with metrics), 6. Daily channel watch + diff + git-history dataset, 7. Offline transcript explorer (static HTML, no backend), Grounding Context (+3 more)

### Community 30 - "Project: ELIO (UniHack Catalog Intelligence)"
Cohesion: 0.17
Nodes (11): Architecture, `category_extractors.py` ↔ `reference_loader.py`, Code Layout, `description_engine.py` ↔ `stages.py`, Feature Inventory, Interface Contracts, Milestones, Project: ELIO (UniHack Catalog Intelligence) (+3 more)

### Community 31 - "PRD — UniHack Catalog Intelligence Pipeline"
Cohesion: 0.18
Nodes (10): 1. Problem & Goal, 2. Scope Decisions (locked), 3. Data Model, 4. Pipeline Stages, 5. Demo App (Streamlit), 6. Success Criteria, 7. Open Dependencies (block Day 1 work), 8. 4-Day Build Plan (+2 more)

### Community 32 - "build_deck.js"
Cohesion: 0.18
Nodes (3): C, PptxGenJS, pres

### Community 33 - "CompetitorBaselineEnricher"
Cohesion: 0.29
Nodes (5): CompetitorBaselineEnricher, A simple baseline enricher representing the competitor UNI-Hack. It does basic…, GauntletCritic, A harsh critic that compares our pipeline output against the competitor…, Returns (winner_label, score_our, score_comp, gaps_our)

### Community 34 - "Screen: Custody Modal"
Cohesion: 0.22
Nodes (8): Screen: Custody Modal, Screen Prompts — Custody Drill-Down (Audit Trail), State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 35 - "Screen: Dashboard"
Cohesion: 0.22
Nodes (8): Screen: Dashboard, Screen Prompts — Dashboard (Self-Score Front Page), State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 36 - "Screen: Results Table"
Cohesion: 0.22
Nodes (8): Screen Prompts — Enrich (Evidence-Led Results), Screen: Results Table, State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 37 - "Screen: Export Panel"
Cohesion: 0.22
Nodes (8): Screen: Export Panel, Screen Prompts — Export (Report Delivery), State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 38 - "Screen: Run"
Cohesion: 0.22
Nodes (8): Screen Prompts — Pipeline Run, Screen: Run, State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 39 - "Screen: Source Index"
Cohesion: 0.22
Nodes (8): Screen Prompts — Research (Source Index), Screen: Source Index, State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 40 - "Screen: Identity Annex"
Cohesion: 0.22
Nodes (8): Screen: Identity Annex, Screen Prompts — Resolve (Identity Annex), State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 41 - "Screen: Review Panel"
Cohesion: 0.22
Nodes (8): Screen Prompts — Review (Disputed Findings), Screen: Review Panel, State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 42 - "Screen: Intake"
Cohesion: 0.22
Nodes (8): Screen: Intake, Screen Prompts — Upload & Column Mapping, State: Edge cases, State: Empty, State: Error, State: Loading, State: Permission-denied, State: Populated

### Community 43 - "Gauntlet — ELIO vs Proton PIM (bar: https://www.proton.ai/pim)"
Cohesion: 0.22
Nodes (8): Bar snapshot (captured 2026-08-21), Blind critics (fresh context, harsh, labels stripped), Builders shipped (build ✓ each), Gauntlet — ELIO vs Proton PIM (bar: https://www.proton.ai/pim), Loop status, Measurable half, Piece slice (smallest judgeable), What was skipped (ponytail)

### Community 44 - "Product"
Cohesion: 0.22
Nodes (8): Accessibility & Inclusion, Anti-references, Brand Personality, Design Principles, Product, Product Purpose, Register, Users

### Community 45 - "PLAN: ELIO Frontend — Judge-Ready Quality Pass"
Cohesion: 0.22
Nodes (8): Contracts (shared surfaces), Integration contract, Judge-Proof Uni-Hack Execution, Leaves, PLAN: ELIO Frontend — Judge-Ready Quality Pass, Status log, Status log (append only), Work units

### Community 46 - "AGENTS.md — ELIO (UniHack Catalog Intelligence)"
Cohesion: 0.25
Nodes (7): AGENTS.md — ELIO (UniHack Catalog Intelligence), Commands (PowerShell; use `-B` to suppress `.pyc`), Frontend cockpit quirks, Gotchas, Pipeline freeze — do not violate without a new bar, Repo map, Stack

### Community 47 - "FREEZE — Bar 5 (Clean Genuine Extraction)"
Cohesion: 0.25
Nodes (6): Acceptance table — generated by scripts/verify_everything.py, Acceptance Table — Bar 5 Final Clean Metrics, FREEZE — Bar 5 (Clean Genuine Extraction), Pipeline Contract, Reproduce, What Bar 5 Changed vs Bar 4 (and why)

### Community 48 - "DISCLOSURE — How ELIO Uses LLMs"
Cohesion: 0.25
Nodes (7): Abstention, Audit trail, Commit-message reconciliation, DISCLOSURE — How ELIO Uses LLMs, The replay proof, What LLMs do, What LLMs never do

### Community 49 - "Screen: Intake"
Cohesion: 0.25
Nodes (8): Edge cases, Empty, Error, Feature: Upload & Column Mapping, Loading, Permission-denied, Populated, Screen: Intake

### Community 50 - "Screen: Results Table"
Cohesion: 0.25
Nodes (8): Edge cases, Empty, Error, Feature: Enrich (Evidence-Led Results), Loading, Permission-denied, Populated, Screen: Results Table

### Community 51 - "Screen: Custody Modal"
Cohesion: 0.25
Nodes (8): Edge cases, Empty, Error, Feature: Custody Drill-Down (Audit Trail), Loading, Permission-denied, Populated, Screen: Custody Modal

### Community 52 - "Screen: Review"
Cohesion: 0.25
Nodes (8): Edge cases, Empty, Error, Feature: Review (Disputed Findings), Loading, Permission-denied, Populated, Screen: Review

### Community 53 - "Screen: Dashboard"
Cohesion: 0.25
Nodes (8): Edge cases, Empty, Error, Feature: Dashboard (Self-Score Front Page), Loading, Permission-denied, Populated, Screen: Dashboard

### Community 54 - "Screen: Export"
Cohesion: 0.25
Nodes (8): Edge cases, Empty, Error, Feature: Export (Report Delivery), Loading, Permission-denied, Populated, Screen: Export

### Community 55 - "Screen: Run"
Cohesion: 0.25
Nodes (8): Edge cases, Empty, Error, Feature: Pipeline Run, Loading, Permission-denied, Populated, Screen: Run

### Community 57 - "ELIO — Judge-Proof Catalog Intelligence (Pitch)"
Cohesion: 0.29
Nodes (6): ELIO — Judge-Proof Catalog Intelligence (Pitch), Proof — run it yourself, The difference, The judge's 5-minute path, The problem, What ELIO does

### Community 58 - "Screen: Identity Annex"
Cohesion: 0.29
Nodes (7): Edge cases, Empty, Error, Loading, Permission-denied, Populated, Screen: Identity Annex

### Community 59 - "Screen: Source Index"
Cohesion: 0.29
Nodes (7): Edge cases, Empty, Error, Loading, Permission-denied, Populated, Screen: Source Index

### Community 60 - "Upload & Run — Screen Prompts"
Cohesion: 0.29
Nodes (6): Upload — Error (Validation / Execution Failed), Upload Landing — Drag-Over, Upload Landing — Empty State, Upload — Loading (Pipeline Running), Upload & Run — Screen Prompts, Upload — Success (Run Completed)

### Community 61 - "Elio - UniHack Catalog Intelligence"
Cohesion: 0.29
Nodes (6): Elio - UniHack Catalog Intelligence, Judge-facing docs, Layout, Pipeline, Plan, Verification

### Community 62 - "adversarial_eval.py"
Cohesion: 0.52
Nodes (6): adversarial_holdout(), gold_check(), main(), metrics(), run_all(), score_difficulty()

### Community 63 - "🧭 00-START_HERE.md — ELIO Cold-Start Walk Map & Judge Guide"
Cohesion: 0.33
Nodes (5): 🧭 00-START_HERE.md — ELIO Cold-Start Walk Map & Judge Guide, ⚡ 1-Minute Reproduction Quickstart, 📊 Canonical Headline Metrics Table, 🖥️ Launching the Web Cockpit Locally, 📁 Repository Structure & Domain Map

### Community 64 - "Evidence Explorer — Screen Prompts"
Cohesion: 0.33
Nodes (5): Evidence Explorer — Screen Prompts, Explorer — Empty (No Search Yet), Explorer — No Match / Untraceable (Edge), Explorer — Record Open (Custody Drawer), Explorer — Search Results (Populated)

### Community 65 - "gauntlet_holdout_eval.py"
Cohesion: 0.60
Nodes (5): gold_check(), main(), metrics(), run_all(), stratified_holdout()

### Community 66 - "UX Philosophy — UniHack Catalog Demo"
Cohesion: 0.40
Nodes (4): Chosen Philosophy: Self-Auditing Evidence Report (C+A blend), Rejected Alternative 1: Evidence Ledger (auditor's workbook), Rejected Alternative 2: Pipeline Cockpit (operator console), UX Philosophy — UniHack Catalog Demo

### Community 67 - "UX Philosophy — ELIO Frontend"
Cohesion: 0.40
Nodes (4): Chosen Philosophy: The Ops Console (hybrid of Production Line + Evidence Console + Record-First), Rejected Alternative 1: The Evidence Console (pure), Rejected Alternative 2: Record-First Explorer (pure), UX Philosophy — ELIO Frontend

### Community 68 - "Acceptance Dashboard — Screen Prompts"
Cohesion: 0.40
Nodes (4): Acceptance Dashboard — Screen Prompts, Dashboard — Dataset Switch (Demo / Full / Uploaded), Dashboard — Empty (No Run Yet), Dashboard — Populated

### Community 69 - "Review Queue — Screen Prompts"
Cohesion: 0.40
Nodes (4): Review Queue — Decision Made (Post-Action), Review Queue — Empty, Review Queue — Populated, Review Queue — Screen Prompts

### Community 70 - "RED_TEAM — What Was Attacked, What Passed, What Remains Untested"
Cohesion: 0.40
Nodes (4): Attack → outcome, Blind critic snapshot (reproducible-by-documentation), RED_TEAM — What Was Attacked, What Passed, What Remains Untested, What we still haven't proven

### Community 71 - "WALK_TEST — Fresh-Clone Acceptance Gate"
Cohesion: 0.40
Nodes (4): Checklist, Edge cases covered, Run log, WALK_TEST — Fresh-Clone Acceptance Gate

### Community 72 - "src/app/layout.tsx"
Cohesion: 0.40
Nodes (3): geistMono, geistSans, metadata

### Community 73 - "build_evidence.py"
Cohesion: 0.60
Nodes (4): locate(), main(), Dual-pass trace: value must appear in source text (or value+uom, or the unit-…, review_reason_for()

### Community 74 - "fill_unihack_deck.py"
Cohesion: 0.60
Nodes (4): add_bullet(), fill_deck(), Script to populate the official UniHack presentation template with ELIO project…, style_para()

### Community 75 - "Features & States — UniHack Catalog Demo"
Cohesion: 0.50
Nodes (3): Feature: Research (Source Index), Feature: Resolve (Identity Annex), Features & States — UniHack Catalog Demo

### Community 76 - "Abstention / Trust — Screen Prompts"
Cohesion: 0.50
Nodes (3): Abstention — Empty (No Refusals), Abstention — Populated, Abstention / Trust — Screen Prompts

### Community 77 - "Export & Delivery — Screen Prompts"
Cohesion: 0.50
Nodes (3): Export & Delivery — Screen Prompts, Export — Empty (No Run), Export — Ready for Import (Populated)

### Community 78 - "elio-frontend/README.md"
Cohesion: 0.50
Nodes (3): Deploy on Vercel, Getting Started, Learn More

### Community 79 - "check_freeze.py"
Cohesion: 0.83
Nodes (3): check(), git(), main()

### Community 81 - "generate_stress_cases.py"
Cohesion: 0.50
Nodes (3): generate_stress_cases(), DataFrame, ARC Task Gen-Style Adversarial & Distribution-Matched Stress Case Generator for…

## Knowledge Gaps
- **561 isolated node(s):** `PptxGenJS`, `pres`, `C`, `eslintConfig`, `nextConfig` (+556 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_pipeline()` connect `run_pipeline` to `stages.py`, `Tier1FeatureTests`, `verify_everything.py`, `CompetitorBaselineEnricher`, `adversarial_eval.py`, `gauntlet_holdout_eval.py`, `build_evidence.py`, `.test_f2_01_distributor_blacklist_appde`, `.test_f3_03_sku_collision_independence`, `.test_f3_05_no_hardcoded_gold_short_circuits`, `.test_f4_01_longest_keyword_match_precedence`, `.test_f4_02_power_tools_classification`, `.test_f5_04_case_insensitive_boundary_matching`, `.test_f8_01_absent_specification_clean_blank`, `.test_f8_02_ambiguous_specification_abstention`, `.test_f8_03_zero_hallucinated_features`, `.test_f9_05_zero_unverified_leakage`, `.test_f10_01_invoice_desc_bounds_and_casing`, `.test_f10_04_retail_desc_bounds`, `.test_f11_01_canonical_column_count`, `.test_f11_04_item_features_and_unspsc_columns`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `Tier1FeatureTests` connect `Tier1FeatureTests` to `stages.py`, `.test_f3_05_no_hardcoded_gold_short_circuits`, `run_pipeline`, `.test_f4_01_longest_keyword_match_precedence`, `.test_f4_02_power_tools_classification`, `.test_f5_04_case_insensitive_boundary_matching`, `.test_f8_01_absent_specification_clean_blank`, `.test_f8_02_ambiguous_specification_abstention`, `.test_f10_01_invoice_desc_bounds_and_casing`, `.test_f10_04_retail_desc_bounds`, `.test_f11_01_canonical_column_count`, `.test_f11_04_item_features_and_unspsc_columns`, `.test_f8_03_zero_hallucinated_features`, `.test_f9_05_zero_unverified_leakage`, `fraction_lookup`, `.test_f2_01_distributor_blacklist_appde`, `.test_f3_03_sku_collision_independence`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `extract_for()` connect `stages.py` to `category_extractors.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Tier1FeatureTests` (e.g. with `AttributeRecord` and `SourceProvenance`) actually correct?**
  _`Tier1FeatureTests` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `PptxGenJS`, `pres`, `C` to the rest of the system?**
  _561 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `stages.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06912280701754386 - nodes in this community are weakly interconnected._
- **Should `Tier1FeatureTests` be split into smaller, more focused modules?**
  _Cohesion score 0.03571428571428571 - nodes in this community are weakly interconnected._