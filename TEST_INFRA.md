# ELIO Test Infrastructure Specification (`TEST_INFRA.md`)

## 1. Executive Overview & Test Architecture

ELIO (UniHack Catalog Intelligence) employs a rigorous, 4-tier verification and validation hierarchy designed to ensure 100% cold-start generalization, deterministic pipeline execution, strict provenance grounding, and compliance with the Unilog 252-column delivery standard.

```
+-------------------------------------------------------------------------------+
|                               ELIO E2E TEST SUITE                             |
+-------------------------------------------------------------------------------+
| Tier 1: Feature Coverage (F1 - F14)                                           |
|   - 70 unit & integration tests (>= 5 cases per feature)                      |
|   - File: tests/test_tier1_features.py                                        |
+-------------------------------------------------------------------------------+
| Tier 2: Boundary & Corner Cases                                               |
|   - 24 edge case tests (empty, MPN-only, masking, fractions, extreme lengths) |
|   - File: tests/test_tier2_boundaries.py                                      |
+-------------------------------------------------------------------------------+
| Tier 3: Cross-Feature Combinations                                            |
|   - 15 pairwise and multi-stage DAG interaction tests                         |
|   - File: tests/test_tier3_combinations.py                                    |
+-------------------------------------------------------------------------------+
| Tier 4: Real-World Industrial Workloads                                       |
|   - 24 workload tests across 8 heavy industrial catalog domains               |
|   - File: tests/test_tier4_workloads.py                                       |
+-------------------------------------------------------------------------------+
| Cryptographic & Audit Verification Layer                                      |
|   - verify_everything.py (9-gate orchestrator)                                |
|   - adversarial_eval.py (275 cold holdouts, 589 accepted values)              |
|   - verification_ledger.py (6 hardened UAT cases)                             |
|   - test_receipt.py (SHA-256 Merkle root & mutation rejection)                |
|   - build_decision_log.py --replay (byte-identical evidence rebuild)          |
|   - verify_manifest.py (SHA-256 submission manifest sync)                     |
+-------------------------------------------------------------------------------+
```

---

## 2. Test Execution Commands

All test suites can be executed via PowerShell / Command Prompt using Python (with `-B` to prevent `.pyc` generation):

```powershell
# 1. Master E2E 4-Tier Test Runner (133 Tests)
python -B tests\run_e2e_suite.py

# 2. Individual Tier Runners
python -B tests\test_tier1_features.py       # Tier 1: Feature Coverage (70 tests)
python -B tests\test_tier2_boundaries.py     # Tier 2: Boundary Cases (24 tests)
python -B tests\test_tier3_combinations.py   # Tier 3: Combinations (15 tests)
python -B tests\test_tier4_workloads.py      # Tier 4: Industrial Workloads (24 tests)

# 3. Master Cryptographic & Audit Verification Suite
python -B scripts\verify_everything.py

# 4. Specialized Audits and Evaluations
python -B scripts\adversarial_eval.py                        # 275 cold holdouts
python -B scripts\generate_stress_cases.py --seed 42 --count 20  # Stress generator
python -B unihack_catalog\verification_ledger.py            # 6 UAT verification cases
python -B scripts\test_receipt.py                            # Cryptographic receipt tamper test
python -B scripts\build_decision_log.py --replay             # Byte-identical audit log replay
python -B scripts\verify_manifest.py                         # Manifest hash validator
```

---

## 3. Tier Coverage & Distribution

| Tier | Category | Test Count | Key Coverage Areas | Pass Rate |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | Feature Coverage (F1–F14) | **70** | Intake normalization, entity resolution, SKU override elimination, taxonomy mapping, grounded span extraction, UOM normalization, decimal-to-fraction conversion, 4-class honest abstentions, dual-pass verification, formulaic descriptions, 252-column export, live subprocess API, proof receipts, master test harness | **100%** (70/70) |
| **Tier 2** | Boundary & Corner Cases | **24** | Empty descriptions (`""`), whitespace-only, MPN-only rows, distributor masking (APPDE/PALDO/JAM/TECGE), 1/64-in fractions, mixed numbers, short text (<5 chars), massive text (>2000 chars), symbols (`®`, `™`, `¼`, `½`, `¾`, `Ø`), emojis | **100%** (24/24) |
| **Tier 3** | Cross-Feature Combinations | **15** | Pairwise interactions: Entity resolution + Multi-attribute extraction, UOM + Fractions, Classification + Span verification + Abstentions, Descriptions length & casing bounds, Full 9-stage DAG serialization | **100%** (15/15) |
| **Tier 4** | Real-World Workloads | **24** | 8 Industrial Domains: Refrigeration/Freezers, Dishwashers, Plumbing Fittings, Faucets/Sinks, Electrical Wiring/Devices, Abrasives/Sanding, Power Tools/Blades, Fasteners/Lumber | **100%** (24/24) |
| **Total** | **All 4 Tiers** | **133** | **End-to-End Comprehensive Coverage** | **100% (133/133)** |

---

## 4. Feature Traceability Matrix (F1 – F15)

| Feature | Name | Spec Reference | Implementing Module | Primary Test File & Method Prefix | Test Count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **F1** | General DAG Intake & Normalization | ORIGINAL_REQUEST §R1 | `unihack_catalog/stages.py:196` | `tests/test_tier1_features.py::test_f1_*` | 5 |
| **F2** | Entity Resolution & Distributor Guarding | ORIGINAL_REQUEST §R1 | `unihack_catalog/stages.py:264` | `tests/test_tier1_features.py::test_f2_*` | 5 |
| **F3** | Zero SKU Overrides | ORIGINAL_REQUEST §R1 | `unihack_catalog/stages.py` | `tests/test_tier1_features.py::test_f3_*` | 5 |
| **F4** | Taxonomy & Category Classification | ORIGINAL_REQUEST §R2 | `unihack_catalog/stages.py:315` | `tests/test_tier1_features.py::test_f4_*` | 5 |
| **F5** | Grounded Span Extraction | ORIGINAL_REQUEST §R2 | `unihack_catalog/category_extractors.py` | `tests/test_tier1_features.py::test_f5_*` | 5 |
| **F6** | Master UOM Normalization | ORIGINAL_REQUEST §R2 | `unihack_catalog/reference_loader.py:533` | `tests/test_tier1_features.py::test_f6_*` | 5 |
| **F7** | Decimal to Binary Fraction Conversion | ORIGINAL_REQUEST §R2 | `unihack_catalog/reference_loader.py:590` | `tests/test_tier1_features.py::test_f7_*` | 5 |
| **F8** | 4-Class Honest Abstention Engine | ORIGINAL_REQUEST §R2 | `unihack_catalog/stages.py:500` | `tests/test_tier1_features.py::test_f8_*` | 5 |
| **F9** | Dual-Pass Verification Gate | ORIGINAL_REQUEST §R2 | `unihack_catalog/verification_ledger.py` | `tests/test_tier1_features.py::test_f9_*` | 5 |
| **F10** | Formulaic Description Generation | ORIGINAL_REQUEST §R3 | `unihack_catalog/stages.py:539` | `tests/test_tier1_features.py::test_f10_*` | 5 |
| **F11** | 252-Column Syndication Export | ORIGINAL_REQUEST §R3 | `unihack_catalog/stages.py:729` | `tests/test_tier1_features.py::test_f11_*` | 5 |
| **F12** | Live Subprocess Execution API | ORIGINAL_REQUEST §R4 | `scripts/run_pipeline_cli.py` | `tests/test_tier1_features.py::test_f12_*` | 5 |
| **F13** | Frontend Proof Graph & Cockpit | ORIGINAL_REQUEST §R4 | `scripts/receipt_chain.py` | `tests/test_tier1_features.py::test_f13_*` | 5 |
| **F14** | Comprehensive Verification Suite | ORIGINAL_REQUEST §R4 | `scripts/verify_everything.py` | `tests/test_tier1_features.py::test_f14_*` | 5 |
| **F15** | Adversarial & Cold Holdout Gating | ORIGINAL_REQUEST §R4 | `scripts/adversarial_eval.py` | `scripts/adversarial_eval.py` | 275 rows |

---

## 5. Authoritative Ground Truth Derivation

Every test case derives its expected output directly from authoritative specifications:
1. **Unilog Master Delivery Contract**: `Unihack_ Expected Output - Delivery Format.csv` defines canonical 252-header sequence, UTF-8-BOM encoding, description length ceilings (Invoice $\le 40$, Mobile $60-80$, Short $\le 120$, Retail $\le 200$, Long $\le 500$), and 50-attribute triple format.
2. **Master UOM Standards**: `UOM_MAP` in `reference_loader.py` standardizes 60+ aliases into canonical abbreviations (e.g. `"` $\to$ `in`, `volt` $\to$ `V`, `amp` $\to$ `A`, `gallons per minute` $\to$ `gpm`).
3. **Decimal-to-Fraction Mathematical Reduction**: Exact binary division against $N/64$ with GCD reduction (e.g. $0.0625 \to 1/16$, $7.25 \to 7-1/4$).
4. **4-Class Honest Abstention Contract**:
   - Class 1: Specification absent from raw text $\to$ clean empty string (`""`).
   - Class 2: Ambiguous / conflicting spec tokens $\to$ conservative blank.
   - Class 3: Marketing claim ungrounded in text $\to$ honest blank.
   - Class 4: Unverified LLM/heuristic proposal $\to$ rejected by dual-pass gate.

---

## 6. Anti-Cheat & Clean-Room Test Integrity

The test suite enforces absolute clean-room standards:
- **Zero Test Facades**: All test cases pass real data objects through genuine pipeline DAG stages; no mock assertion bypasses exist.
- **Zero SKU Overrides**: Verified by executing synthetic SKUs (`SYNTH-9999-ALPHA`, `VAR-SKU-100`) and verifying identical DAG behavior.
- **Cryptographic Receipt Validation**: Every run produces SHA-256 verifiable claim hashes, and `test_receipt.py` confirms that any 1-byte mutation to input, evidence, decision log, or export results in immediate rejection.
