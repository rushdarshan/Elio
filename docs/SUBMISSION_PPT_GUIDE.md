# UniHack 2026 — Prototype Submission & Evaluation Guide
**Project:** ELIO (Evidence-Gated Industrial Catalog Intelligence)  
**Evaluation Flow:** PPT ➔ Demo Video ➔ Live Prototype ➔ GitHub Repository  

---

## 🎯 Evaluation Stage 1: PPT (Prototype Deck Content)

Use this slide-by-slide breakdown to fill out the mandatory presentation template:

### **Slide 1: Title & Team**
* **Project Name:** ELIO — Evidence-Gated Industrial Catalog Intelligence
* **Tagline:** Deterministic, Provenance-Backed 252-Column Catalog Syndication with Zero Answer-Key Dependency.
* **Live App URL:** [https://elio-lwxr.onrender.com/app/dashboard](https://elio-lwxr.onrender.com/app/dashboard)
* **GitHub Repository:** [https://github.com/rushdarshan/Elio](https://github.com/rushdarshan/Elio)

### **Slide 2: Problem Statement & Context**
* **The Input Challenge:** Distributor feeds provide only 6 sparse, noisy columns (`Mfg_Part_Num`, `Part_Desc`, `Part_Manuf`, `E1_Brand`, `Unilog_Brand`, `DIB_Brand`).
* **The 252-Column Requirement:** Enterprise syndication requires 252 structured columns, normalized Master UOM standards, taxonomy hierarchy (Dept > Class > Fine), and multi-tier descriptions.
* **Why Competitors Fail:**
  * *Brittle Regex:* Hardcodes sample part numbers (`PDSH4816AF`), breaking on cold-start items.
  * *Generative LLMs:* Hallucinate missing electrical/mechanical specs, taking 30–60 minutes per 1,000 items with zero cryptographic auditability.

### **Slide 3: Proposed Solution & Key Innovations**
* **Deterministic 9-Stage DAG:** Pure Python pipeline (`bar-5-clean`) that extracts, classifies, normalizes, and verifies attributes in milliseconds.
* **Dual-Pass Verification Invariance:** Every single emitted attribute must anchor to verbatim character spans in raw source text or formal Master UOM conversions.
* **Honest Abstentions (Zero Guessing):** When specs are absent, ELIO refuses to fabricate numbers—recording machine-readable refusal codes (`not_found`, `missing_oem_spec`, `cross_category_absence`).
* **Cryptographic Provenance Receipts:** Content-addressed SHA-256 hashes linking raw source spans $\rightarrow$ extraction $\rightarrow$ decision logs $\rightarrow$ delivery exports.

### **Slide 4: Technical Architecture & Workflow**
* **9-Stage Processing DAG:**
  1. `Intake & Normalize` (6 sparse distributor headers)
  2. `Entity Resolution` (Word-boundary brand recognition, OEM disambiguation)
  3. `Taxonomy Classification` (Longest-keyword match against Dept > Class > Fine taxonomy)
  4. `Research & Planning` (Document query & retrieval)
  5. `Category-Aware Extraction` (Master UOM standardization & decimal conversions)
  6. `Dual-Pass Verification` (Verbatim source character span anchoring)
  7. `Refusal & Abstention Ledger` (Formal rejection codes for ungrounded specs)
  8. `Description Engine` (Invoice $\le 40$ chars uppercase, Mobile, Short, Retail)
  9. `252-Column Delivery Export` (Exact static header sequence with UTF-8-SIG)
* **Interactive Operations Cockpit:** Next.js App Router frontend with real-time CSV uploads, custody drawers, and instant projection exports.

### **Slide 5: Compliance with Hackathon Criteria**
* **Zero Hardcoded Overrides:** 100% dynamic pipeline running the identical DAG on known and unknown cold-start catalogs.
* **Exact 252-Column Schema:** Populates all canonical static delivery headers without modifying, removing, or reordering any column.
* **Master UOM & Fraction Standards:** Full normalization of fractions (`7-1/4 in`, `2 ft x 2 ft`) and units (`V`, `A`, `gpm`, `cu ft`, `AWG`).
* **Sub-Second Latency:** $\sim 3\text{ms/row}$ ($\sim 3\text{s}$ per 1,000 rows) with $\$0.00$ runtime API dependency.

### **Slide 6: Live Results & Benchmark Verification**
* **Verification Gates:** 16/16 verification gates passed (`python -B scripts/verify_everything.py`).
* **E2E Test Suite:** 133/133 automated unit and integration tests passed (100%).
* **Adversarial Holdout Accuracy:** 100% precision on accepted values with 0 dual-pass verification failures.

---

## 🎥 Evaluation Stage 2: Demo Video Script (2–3 Minutes)

1. **Introduction (0:00 - 0:30):**
   * State the challenge: turning sparse 6-column distributor data into a certified 252-column enterprise catalog.
   * State the core principle: **100% Grounded Provenance or Honest Abstention — Never Hallucinate.**
2. **Live Upload & Real-Time Processing (0:30 - 1:15):**
   * Open [`https://elio-lwxr.onrender.com/app/dashboard`](https://elio-lwxr.onrender.com/app/dashboard).
   * Click **Upload CSV** and upload a cold sample file (`sample_test_minimal_3cols.csv`).
   * Show that processing completes in sub-seconds and populates the live table.
3. **Evidence Explorer & Proof Drawer (1:15 - 1:55):**
   * Click on a row (e.g. `DCG402B` Angle Grinders or `PDSH4816AF` Dishwashers).
   * Demonstrate the **Record Custody Drawer**: verbatim source character spans, normalized Master UOMs (`20 V`, `4-1/2 in`), and description formulas (Invoice $\le 40$ chars uppercase).
   * Click **Recompute & Verify Hash** to showcase the live SHA-256 cryptographic proof.
4. **Abstentions & Governance (1:55 - 2:30):**
   * Click on the **Review Queue** tab to show human-in-the-loop escalations (`Accept` / `Reject`).
   * Click on the **Abstentions & Refusals** tab to show honest refusals for missing specs with machine-readable reasons instead of AI hallucinations.
5. **252-Column Delivery Export (2:30 - 3:00):**
   * Click **Export CSV** and download `elio_export.csv`.
   * Open the file or show the audit: 100% exact 252-column delivery schema match with UTF-8-SIG encoding.

---

## 💻 Evaluation Stage 3: Live Prototype Checklist

* [x] **Live Deployed URL:** `https://elio-lwxr.onrender.com/app/dashboard`
* [x] **Dynamic & Un-Mocked:** Processes cold CSV uploads live via `/api/run`.
* [x] **252 Delivery Headers:** Exports all 252 static headers matching `Unihack_ Expected Output - Delivery Format.csv`.
* [x] **Downloadable Output:** Generates downloadable CSV / XLSX formatted files with UTF-8-SIG.

---

## 📂 Evaluation Stage 4: GitHub Repository Verification

* [x] **Repository URL:** `https://github.com/rushdarshan/Elio`
* [x] **Release Tag:** `bar-5-clean`
* [x] **Run Single Source of Truth:**
  ```powershell
  python -B scripts\verify_everything.py
  ```
  *(16/16 gates pass, VERDICT: ACCEPTED)*
* [x] **Run Complete E2E Suite:**
  ```powershell
  python -B tests\run_e2e_suite.py
  ```
  *(133/133 tests pass, 100%)*
