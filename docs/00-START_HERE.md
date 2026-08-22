# 🧭 00-START_HERE.md — ELIO Cold-Start Walk Map & Judge Guide

> **Frozen Pipeline Commit:** `bar-5-clean` (tag `bar-5-clean`)  
> **Mission:** Immutable, falsifiable catalog intelligence engine transforming messy distributor rows into verified 252-column product records with 100% provenance coverage on accepted values and zero answer-key hardcoding.  
> **No Conversation Context Needed:** Any fresh coding agent or hackathon judge can reproduce all claims, metrics, and surfaces directly using this guide.

---

## ⚡ 1-Minute Reproduction Quickstart

Run these executable commands in PowerShell from the repository root:

```powershell
# 1. Master verification (16 gates; generates metrics.json & acceptance_table.md)
python -B scripts/verify_everything.py --full

# 2. Artifact judge walk (add --live when the cockpit is running)
python -B scripts/judge_walk.py --live
# 2b. Dynamic evaluator upload against the organizer sample
python -B scripts/judge_walk.py --live --input "Unihack_ Sample Dataset - Input.csv"

# 3. Cryptographic Proof Chain Verifier (Recomputes SHA-256 hashes across evidence spans)
python -B scripts/verify_receipt.py

# 4. Decision Log Deterministic Replay (Proves byte-identical state reconstruction from event stream)
python -B scripts/build_decision_log.py --replay

# 5. Receipt mutation checks (input/source/decision/output tamper rejection)
python -B scripts/test_receipt.py
```

---

## 📁 Repository Structure & Domain Map

```text
├── unihack_catalog/             # Frozen Python 9-stage DAG engine (commit 38db2af)
│   ├── stages.py                # 252-column projection & main pipeline entry
│   ├── models.py                # Pydantic schema: ClaimRecord, SourceEvidence, EnrichedRecord
│   ├── description_engine.py    # Universal 5-variant description builder (Invoice, Mobile, Short, Long, Mkt)
│   └── verification_ledger.py   # Executable UAT verification ledger (6 hardened test cases)
│
├── scripts/                     # Executable verification & evaluation test harness
│   ├── verify_everything.py     # Master 16-gate runner (single source of truth)
│   ├── judge_walk.py            # Artifact walk plus optional live upload/API smoke test
│   ├── verify_receipt.py        # Cryptographic receipt & SHA-256 hash recomputation verifier
│   ├── build_decision_log.py    # Event-sourced decision logger & byte-identical replay engine
│   ├── test_receipt.py          # Mutation checks for the content-addressed receipt
│   └── adversarial_eval.py      # Difficulty-stratified holdout test
│
├── elio-frontend/               # Next.js 16.3 / React 19 App Router Frontend
│   ├── src/app/landing/         # Landing page
│   ├── src/app/app/dashboard/   # 5-surface Dark Operations Cockpit & Proof Graph
│   └── public/data/             # Demo (50 rows) & Full (1,000 rows) JSON results
│
├── artifacts/                   # Canonical generated evidence artifacts
│   ├── metrics.json             # Canonical metrics snapshot
│   ├── acceptance_table.md      # Generated acceptance table
│   ├── evidence.json            # Structured claim evidence with character spans
│   └── decision_log.jsonl       # Append-only governance decision stream
│
└── docs/                        # Specifications, freeze contracts, and pitch decks
    ├── 00-START_HERE.md         # This cold-start walk map
    ├── FREEZE.md                # Frozen pipeline contract and acceptance invariants
    ├── GATES.md                 # executable judge-proof gate definitions
    └── PITCH.md                 # Pitch narrative and value proposition
```

---

## 📊 Canonical Headline Metrics Table

| Metric | Measured Value | Verification Command | Artifact Source |
|---|---:|---|---|
| **252-Column Header Sequence** | **252 / 252** | `python -B scripts/verify_manifest.py` | `Unihack_ Expected Output - Delivery Format.csv` |
| **Gold Benchmark Extractable Cells** | **17 / 118 (100% extractable match, 0 hallucinations)** | `python -B scripts/gold_evaluator.py` | `artifacts/metrics.json` |
| **Dual-Pass Verification Failures** | **0** | `python -B scripts/verify_everything.py` | `artifacts/metrics.json` |
| **Adversarial Accepted Precision** | **589 / 589 (100%)** | `python -B scripts/verify_everything.py` | `artifacts/metrics.json` |
| **Provenance Coverage on Accepted** | **100%** | `python -B unihack_catalog/verification_ledger.py` | `artifacts/evidence.json` |
| **Decision Log Replay Fidelity** | **100% Byte-Identical** | `python -B scripts/build_decision_log.py --replay` | `artifacts/decision_log.jsonl` |
| **Content-Addressed Receipt Claims** | **91 / 91 verified** | `python -B scripts/verify_receipt.py` | `artifacts/receipt.json` |
| **Abstentions with recorded reasons** | **112 (demo) / 2,494 (full)** | `python -B scripts/judge_walk.py` | `artifacts/evidence.json` |

---

The adversarial headline is the Bar-4 frozen snapshot. The current organizer
sample is a different input snapshot; use the live `judge_walk.py --input`
command above for evaluator-upload behavior rather than treating its holdout
recompute as the frozen benchmark.

## 🖥️ Launching the Web Cockpit Locally

```powershell
cd elio-frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) for the landing page, and navigate to `/app/dashboard` for the 5-surface Cockpit:
1. **Pipeline Overview:** Live DAG stage counts, completeness metrics, and flow analytics.
2. **Evidence Explorer:** Click any attribute card to open the **Custody Drawer** and interact with the live **Proof Graph**.
3. **Review Queue:** High-throughput escalation management with instant Accept / Reject and local overrides.
4. **Abstentions & Refusals:** Transparent audit ledger explaining why ungrounded fields were deliberately refused.
5. **Export:** Instant sanitized 252-column CSV download.
