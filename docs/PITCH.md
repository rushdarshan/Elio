# ELIO — Judge-Proof Catalog Intelligence (Pitch)

**What this is:** a pure Python pipeline that normalizes messy industrial
B2B product rows into a schema-aligned 252-column enterprise catalog where **every
emitted value is traceable to its source** — with zero answer-key hardcoding, zero
synthetic spec lookup tables, and honest refusal on absent specifications.

---

## The Problem

Industrial distributors work from 6 free-text columns (`Mfg_Part_Num,
Part_Desc, E1/Unilog/DIB_Brand, Part_Manuf`) and need a 252-column catalog.
Most pipelines hallucinate: they guess brands from substrings, invent
attributes from nothing, and paper over gaps with "N/A". A skeptical judge
can't tell what was derived from evidence and what was made up.

## What ELIO Does

9-stage deterministic DAG (frozen at commit `bar-5-clean`, tag `bar-5-clean`):

1. **Ingest & Normalize** — 6 input distributor columns
2. **Entity Resolution** — word-boundary brand matching; distributor names
   are never surfaced as OEM manufacturers
3. **Taxonomy Classification** — longest-keyword match against a closed Dept > Class > Fine
   tree (word boundaries, no substring traps)
4. **Extraction** — universal category-aware attribute extractors
5. **Research & Planning** — query formation and content-addressed evidence fetch
6. **Description Generation** — mobile / invoice / short / long / marketing variants
7. **Dual-Pass Verification** — every value must appear in the source text
   or be a documented unit conversion
8. **Abstention** — four documented classes, output blank with a reason,
   never a guess
9. **Export** — sanitized 252-column projection

## The Difference

| Metric | Typical Pipeline | ELIO (Clean Bar 5) |
|---|---|---|
| Attributes/row (seed-7 holdout) | guesses | **1.524** |
| Gold benchmark extractable cells | synthetic lookup | **17/118 (100% extractable match)** |
| Dual-pass verification failures | — | **0** |
| Adversarial accepted values | — | **589/589 @ 100%** |
| Untraceable accepted values | — | **0** |
| Blank cells | "N/A" | **abstained, with recorded reason** |
| Cryptographic Proof Verification | None | **SHA-256 Content-Addressed Receipt** |

## Proof — Run It Yourself

```powershell
python -B scripts\verify_everything.py    # every headline gate, live (~3s)
python -B scripts\judge_walk.py            # automated 5-surface judge walk
python -B scripts\verify_receipt.py        # cryptographic receipt verification
python -B scripts\verify_manifest.py       # SHA256-bound artifact manifest
```

Explore the evidence yourself — open `demo.html` (fully offline) or the Next.js Cockpit at `http://localhost:3000/app/dashboard`.
