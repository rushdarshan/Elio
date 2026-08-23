# ELIO — Industrial Catalog Intelligence

<div align="center">

[![Live Web Cockpit](https://img.shields.io/badge/Live%20Cockpit-Demo%20Online-2563eb?style=for-the-badge&logo=render)](https://elio-lwxr.onrender.com/app/dashboard)
[![Verification Gates](https://img.shields.io/badge/Verification%20Gates-16%2F16%20PASSED-22c55e?style=for-the-badge&logo=githubactions)](https://github.com/rushdarshan/Elio)
[![E2E Test Suite](https://img.shields.io/badge/E2E%20Tests-133%2F133%20PASSED-22c55e?style=for-the-badge)](https://github.com/rushdarshan/Elio)
[![Delivery Schema](https://img.shields.io/badge/Delivery%20Schema-252%20Columns%20Exact-blue?style=for-the-badge)](https://github.com/rushdarshan/Elio)
[![Pipeline Freeze](https://img.shields.io/badge/Pipeline%20Tag-bar--5--clean-orange?style=for-the-badge)](https://github.com/rushdarshan/Elio/tree/bar-5-clean)

**Transform sparse, noisy B2B distributor feeds into schema-certified, 252-column master catalog records with 100% cryptographic provenance and honest abstentions.**

[Live Operations Cockpit](https://elio-lwxr.onrender.com/app/dashboard) • [Competitive Benchmark](docs/COMPETITIVE_RESEARCH.md) • [Freeze Contract](docs/FREEZE.md) • [Submission Guide](docs/SUBMISSION_PPT_GUIDE.md)

</div>

---

## 📌 Executive Summary

Industrial e-commerce onboarding starts with minimal, unstructured distributor feeds (often only 6 sparse columns: `Mfg_Part_Num`, `Part_Desc`, `Part_Manuf`, `E1_Brand`, `Unilog_Brand`, `DIB_Brand`). Syndication targets (ERP, e-commerce marketplaces) demand certified **252-column records**, strict **Master UOM normalization**, taxonomy classification (Dept > Class > Fine), and multi-tier formulaic descriptions.

Existing solutions fall into two fatal traps:
1. **Brittle Overfitting:** Hardcoded keyword rules and sample part-number overrides that crash on unseen cold catalogs.
2. **Generative Hallucination:** Zero-shot LLMs that fabricate ungrounded technical specs (voltage, dimensions, tolerances) when values are missing, taking 30–60 minutes per 1,000 rows at high API cost.

**ELIO** solves this with a **deterministic 9-stage DAG pipeline** backed by **Dual-Pass Verification Invariance**: every single emitted value is anchored to verbatim character spans in raw source text or formal unit conversions. When specs are absent, ELIO generates machine-readable **honest abstentions** rather than fabricated data.

---

## 🏗️ System Architecture & Workflow

```mermaid
flowchart TD
    subgraph INTAKE ["1. Distributor Intake (6 Sparse Columns)"]
        Raw["Raw Product Row\n(MPN, Description, Masked Manufacturer, Brand Fields)"]
    end

    subgraph DAG ["2. Deterministic 9-Stage Pipeline DAG (bar-5-clean)"]
        S1["Stage 1: Ingest & Normalize\n• Schema sanitation\n• Unicode & fraction cleanup"]
        S2["Stage 2: Entity Resolution\n• Word-boundary brand lookup\n• Distributor vs OEM masking"]
        S3["Stage 3: Taxonomy Classification\n• Longest-keyword match\n• Closed Dept > Class > Fine taxonomy"]
        S4["Stage 4: Research & Planning\n• Query formation\n• Spec sheet retrieval"]
        S5["Stage 5: Category Extraction\n• 10 Category extractors\n• Master UOM standardization"]
        S6["Stage 6: Description Engine\n• Invoice (<=40 char CAPS)\n• Mobile, Short, Retail titles"]
        S7["Stage 7: Dual-Pass Verification\n• Verbatim character span anchor\n• Zero ungrounded claims"]
        S8["Stage 8: Abstention Engine\n• 4 Formal refusal classes\n• Honest blank with reason"]
        S9["Stage 9: 252-Column Syndication\n• Canonical schema sequence\n• UTF-8-SIG export"]
        
        Raw --> S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7 --> S8 --> S9
    end

    subgraph PROVENANCE ["3. Verification & Governance Ledger"]
        V1{"Verification Gate"}
        S7 --> V1
        V1 -- "100% Verbatim Span" --> Acc["Auto Accepted\n(SHA-256 Content-Addressed Receipt)"]
        V1 -- "Missing Evidence / Ambiguity" --> Esc["Review Queue\n(Human-in-the-Loop Cockpit)"]
        S8 --> Abs["Abstentions & Refusals Ledger\n(4 Machine-Readable Classes)"]
    end

    subgraph DELIVERY ["4. Multi-Surface Output & Syndication"]
        Acc --> OutCSV["252-Column Delivery CSV / XLSX\n(Unilog Master Delivery Contract)"]
        Esc --> Cockpit["Interactive Web Cockpit\n(Next.js App Router)"]
        Abs --> Ledger["Audit & Replay Log\n(decision_log.jsonl)"]
    end
```

---

## 🔄 Dual-Pass Verification & Cryptographic Provenance

ELIO guarantees that no hallucinations enter your enterprise catalog through a content-addressed SHA-256 receipt chain:

```mermaid
sequenceDiagram
    autonumber
    participant Input as Raw Distributor Row
    participant Extractor as Category Extractor & UOM
    participant Verifier as Dual-Pass Gate
    participant Receipt as SHA-256 Receipt Chain
    participant Export as 252-Column Export

    Input->>Extractor: Raw Text (e.g. "DEWALT DCG402B 20V MAX 4-1/2 in Grinder")
    Extractor->>Extractor: Standardize Units ("20 V", "4-1/2 in")
    Extractor->>Verifier: Proposed Attribute Claim (Label, Value, UOM)
    Verifier->>Verifier: Check verbatim span in source text: [22, 25] -> "20V"
    alt Verbatim Match or Formal Conversion
        Verifier->>Receipt: Record Claim Hash + Source Span + SHA-256
        Receipt->>Export: Emit into ATTRIBUTE_LABEL/VALUE/UOM 1..50
    else Value Absent from Source Text
        Verifier->>Receipt: Refuse Fabrication (Code: not_found)
        Receipt->>Export: Emit Honest Blank (No Fake Specs)
    end
```

---

## ⚡ Competitive Matrix

| Judging Dimension | Archetype 1: Regex / Rule Maps | Archetype 2: Zero-Shot LLMs | Archetype 3: Agentic Search / RAG | Archetype 5: **ELIO (`bar-5-clean`)** |
|:---|:---:|:---:|:---:|:---:|
| **Generalization & Cold Rows** | ❌ Fails on unseen SKUs | ⚠️ Unstable / Hallucinates | ⚠️ Fragile (Web scrapers timeout) | ✅ **100% Universal category DAG (0 MPN shortcuts)** |
| **Provenance & Verifiability** | ❌ None (Opaque string splits) | ❌ None (Black box output) | ⚠️ Low (Fuzzy search summaries) | ✅ **100% Verbatim Span Anchoring + SHA-256 Receipts** |
| **252-Column Schema Exactness** | ❌ Header drift / unpadded CSV | ⚠️ Unstable JSON formatting | ⚠️ Partial column subsets | ✅ **252/252 Sequence Exact, UTF-8-SIG, Length Bounded** |
| **Master UOM Normalization** | ⚠️ Ad-hoc string replacement | ⚠️ Inconsistent output units | ⚠️ Inconsistent formatting | ✅ **Deterministic Master UOM Standardization Engine** |
| **Abstention vs. Fabrication** | ❌ Emits fake defaults / blanks | ❌ Hallucinates plausible numbers | ❌ Injects unverified third-party specs | ✅ **4 Formal Abstention Classes with Audit Ledger** |
| **Throughput (per 1,000 Rows)** | $\sim 0.5\text{s}$ | $\sim 1,800\text{s} - 3,600\text{s}$ | $\sim 600\text{s} - 1,200\text{s}$ | ✅ **$\sim 3.0\text{s}$ (Sub-second Python DAG)** |
| **Cost (per 1,000 Rows)** | $\$0.00$ | $\$15.00 - \$50.00$ | $\$20.00 - \$75.00$ | ✅ **$\$0.00$ (Zero runtime API dependency)** |
| **Review & Audit Governance** | ❌ None | ❌ None | ❌ None | ✅ **Append-Only Decision Log (100% Replayable) + Cockpit** |

---

## 📂 Repository Organization

```
├── unihack_catalog/              # Core 9-Stage DAG Pipeline
│   ├── stages.py                 # Pipeline DAG runner & 252-column exporter
│   ├── category_extractors.py   # High-precision category extractors
│   ├── description_engine.py    # Multi-tier formulaic description generator
│   ├── reference_loader.py       # Master UOM, LOV, and brand taxonomy reference loaders
│   ├── verification_ledger.py    # Dual-pass verification rules & UAT test suite
│   └── models.py                 # Pydantic data schemas (EnrichedRecord, ClaimRecord)
├── elio-frontend/                # Next.js 16 App Router Operations Cockpit
│   ├── src/app/app/dashboard/   # Single-file operations cockpit & inspection drawer
│   ├── src/app/api/run/          # High-capacity streaming pipeline API endpoint
│   └── public/data/              # Pre-computed verification ledgers & receipts
├── scripts/                      # Verification, Audit & Gate Tooling
│   ├── verify_everything.py      # Executable single source of truth (16 acceptance gates)
│   ├── verify_manifest.py        # SHA-256 bound file integrity checker
│   ├── verify_receipt.py         # Content-addressed receipt verification harness
│   └── judge_walk.py             # Automated 5-surface judge smoke test
├── tests/                        # Comprehensive End-to-End Test Suite
│   └── run_e2e_suite.py          # 133 automated unit, edge, and integration tests
├── artifacts/                    # Canonical Generated Metrics & Proof Ledgers
│   ├── metrics.json              # Canonical acceptance numbers
│   ├── evidence.json             # Character span evidence mapping
│   └── decision_log.jsonl        # Immutable append-only audit trail
└── docs/                         # Architecture, Pitch & Freeze Documentation
    ├── FREEZE.md                 # Pipeline contract & acceptance criteria
    ├── PITCH.md                  # Executive pitch & proof numbers
    ├── COMPETITIVE_RESEARCH.md   # Primary research & benchmark analysis
    └── SUBMISSION_PPT_GUIDE.md   # Slide-by-slide prototype presentation guide
```

---

## 🚀 Quick Start & Verification

### 1. Run Complete Verification (Single Source of Truth)
Every metric is executable and verified live by a single script:

```powershell
# Run the 16-gate acceptance suite (~3s)
python -B scripts\verify_everything.py

# Run complete 133-test E2E test suite
python -B tests\run_e2e_suite.py

# Verify cryptographic receipt chain
python -B scripts\verify_receipt.py

# Verify SHA-256 repository manifest
python -B scripts\verify_manifest.py
```

### 2. Run the Next.js Operations Cockpit Locally

```powershell
cd elio-frontend
npm install
npm run dev
```
Open [http://localhost:3000/app/dashboard](http://localhost:3000/app/dashboard) to upload custom catalog CSVs, inspect verbatim character spans, verify cryptographic SHA-256 receipts, and export certified 252-column files.

---

## 🛡️ The Four Formal Abstention Classes

When product descriptions lack information, ELIO does not guess. It records one of four formalized refusal codes:

1. **`not_found`** — Specification absent from source description.
2. **`unverified_tolerance`** — Ambiguous numerical values failing exact unit or boundary constraints.
3. **`missing_oem_spec`** — Manufacturer technical data omitted in distributor-masked feeds.
4. **`cross_category_absence`** — Attributes invalid for the identified product taxonomy class.

All refusals are surfaced in the **Abstentions & Refusals** ledger with full audit reasons.

---

<div align="center">
<b>ELIO — Evidence-Gated Catalog Intelligence</b><br>
<i>Built for UniHack 2026 • Verified at commit <code>bar-5-clean</code></i>
</div>
