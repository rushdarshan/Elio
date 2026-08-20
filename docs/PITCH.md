# ELIO — Judge-Proof Catalog Intelligence (Pitch)

**What this is:** a plain-Python pipeline that normalizes messy industrial
B2B product rows into a schema-aligned 252-column catalog where **every
emitted value is traceable to its source** — and every cell that can't be
traced is honestly abstained, never invented.

---

## The problem

Industrial distributors work from 6 free-text columns (`Mfg_Part_Num,
Part_Desc, E1/Unilog/DIB_Brand, Part_Manuf`) and need a 252-column catalog.
Most pipelines hallucinate: they guess brands from substrings, invent
attributes from nothing, and paper over gaps with "N/A". A skeptical judge
can't tell what was derived from evidence and what was made up.

## What ELIO does

9-stage deterministic DAG (frozen at commit `38db2af`, tag `bar-4-freeze`):

1. **Ingest** — 6 input columns
2. **Entity resolution** — word-boundary brand matching; distributor names
   are never surfaced as OEM
3. **Taxonomy** — longest-keyword match against a closed Dept > Class > Fine
   tree (word boundaries, no substring traps)
4. **Extraction** — per-category attribute extractors
5. **Description generation** — mobile / invoice / short / long variants
6. **Verification** — dual-pass: every value must appear in the source text
   or be a documented unit conversion
7. **Quality** — auto-accept only on gold-exempt evidence; everything else
   goes to review
8. **Abstention** — four documented classes, output blank with a reason,
   never a guess
9. **Export** — 252-column projection

## The difference

| | Typical pipeline | ELIO |
|---|---|---|
| Attributes/row (seed-7 holdout, assisted) | guesses | **2.156** |
| Gold cells byte-exact | some | **118/118 evaluated** |
| Dual-pass verification failures | — | **0** |
| Adversarial accepted values | — | **589/589 @ 100%** |
| Untraceable accepted values | — | **0** |
| Blank cells | "N/A" | **abstained, with a reason** |

## Proof — run it yourself

```powershell
python -B scripts\verify_everything.py    # every headline gate, live, ~90s
python -B scripts\verify_manifest.py      # SHA256-bound artifact manifest
```

- **Gold:** 118/118 evaluated cells byte-exact (134 populated in the
  delivery workbook; 16 excluded = the 8 input columns × 2 gold rows)
- **Adversarial:** 277 difficulty-stratified rows, 589 accepted values —
  100% precision, 100% provenance, 0 untraceable
- **Blind critic A/B:** 17–1 (7 ties) — fresh-context judge preferred ELIO
- **Fresh-upload end-to-end:** 8/8 invented adversarial rows, no leakage
- **Honesty:** `docs/DISCLOSURE.md` (LLM usage), `docs/RED_TEAM.md`
  (what we attacked, what passed, what remains untested)

Explore the evidence yourself — open `demo.html` (fully offline) and search
an MPN: every accepted value shows its source trace; every abstained cell
shows its reason.

## The judge's 5-minute path

1. Open `demo.html` — see values with evidence, blanks with reasons
2. Run `python -B scripts\verify_everything.py` — watch every headline
   metric pass live
3. Read `docs/RED_TEAM.md` — see what was attacked and what remains untested
4. Check `docs/DISCLOSURE.md` — see exactly what the LLM does and doesn't do
5. `git log` — clean history: freeze at `38db2af`, everything after is
   submission surface only (freeze gate enforces this)
