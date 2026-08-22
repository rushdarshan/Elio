# Elio - UniHack Catalog Intelligence

Normalize messy industrial B2B product rows into a schema-aligned, auditable
catalog: brand / OEM / distributor kept as distinct typed edges, closed-taxonomy
classpath, evidence-grounded attributes, constrained descriptions, and an honest
abstention decision - every emitted value traces to the source text.

Built for UniHack 2026. Gold-bar: **118/118 evaluated gold cells byte-exact**
against the official delivery-format workbook (2 rows x 252 cols; 134 populated
cells, 16 excluded = the 8 input columns x 2 gold rows: `Mfg_Part_Num`,
`Part_Desc`, `E1_Brand`, `Unilog_Brand`, `DIB_Brand`, `Part_Manuf`,
`PART_NUMBER`, `SKU - MY_PART_NUMBER`), verified with a dual-pass (value must
appear in source text or be a literal unit conversion). All headline numbers
are regenerated live by one command - see **Verification** below.

## Pipeline

9-stage plain-Python DAG (`unihack_catalog/stages.py`), frozen at commit
`bar-5-clean` (tag `bar-5-clean`):

1. Ingest - 6 input columns (`Mfg_Part_Num, Part_Desc, E1/Unilog/DIB_Brand, Part_Manuf`)
2. Entity resolution - word-boundary brand matching, MPN-prefix map, supplier-aware
   (`Part_Manuf` is a supplier field; distributor names are never surfaced as OEM)
3. Taxonomy - longest-keyword match against a closed Dept>Class>Fine tree
4. Extraction - per-category extractors (discs, blades, belts, bits, adapters,
   fasteners, lighting, lumber, wire, electrical) + generic fallback
5. Description generation - mobile / invoice / short / long variants with char
   limits and validity flags
6. Verification - dual-pass: every value must trace to raw text; failures escalate
7. Quality - auto_accept only on gold-exempt evidence; everything else goes to review
8. Abstention - explicit refusal reasons for unsupported or ungrounded values
9. Export - 252-column projection with UTF-8-sig encoding (Excel-safe)

The four abstention classes (gold-blessed blanks, pendant rows, dual-platform
chargers, mixed-unit tape) are documented in `docs/FREEZE.md`; blank cells are
refused-with-reason, never guesses.

## Layout

- `unihack_catalog/` - pipeline package (stages, extractors, reference loader, models)
- `scripts/` - verification + generation tooling (see **Verification**)
- `docs/` - FREEZE (bar + acceptance table), PITCH, DISCLOSURE, RED_TEAM, walk test, plan
- `artifacts/` - generated canonical numbers: `metrics.json`, `evidence.json`
- `demo.html` - offline interactive evidence explorer (open directly, no network)
- `submission_manifest.json` - SHA256-bound evidence set
- `*.csv` - 1000-row full export and 50-row balanced demo export (both gold rows included)
- `app.py` - legacy Streamlit demo app; superseded by `demo.html` (offline evidence explorer)

## Verification

Every headline metric is generated or asserted live by one command:

```powershell
python -B scripts\verify_everything.py    # 16-gate acceptance grid + artifacts\metrics.json
python -B scripts\verify_everything.py --full   # + reruns the heavy holdout evals
python -B scripts\verify_manifest.py      # SHA256-bound manifest; fails on any byte drift
python -B scripts\verify_receipt.py       # content-addressed evidence receipt
python -B scripts\judge_walk.py --live    # artifact walk + live cockpit/API smoke test
```

| Gate | Result (Bar 4) |
|---|---|
| Gold exact (118 evaluated gold cells) | 118/118 |
| Dual-pass verification failures | 0 |
| attrs/row (seed-7 holdout, assisted) | 2.156 |
| Other % | 0.4% |
| Adversarial accepted values (277 rows / 589 values) | 589/589 @ 100% precision |
| Untraceable accepted values | 0 |
| Provenance coverage on accepted | 100% |
| Regressions vs Bar 3 | 0 |
| 252-column export | PASS |
| Blind critic A/B (26 contested rows) | 17-1 (7 ties) |
| Fresh upload end-to-end (8 invented adversarial rows) | PASS |
| UAT ledger (6 cases) + rules linter | PASS |
| Content-addressed receipt | 106/106 claims verified |
| Judge walk | PASS (artifact walk; `--live` checks cockpit/API) |

All numbers and their generating commands live in `artifacts/metrics.json`
- the single source README, FREEZE.md, PITCH.md, and the video read from.

The frozen Bar-4 holdout numbers are bound to the input snapshot used at freeze
time. The current organizer sample CSV is a separate evaluator fixture; its
live upload is checked by `scripts/judge_walk.py --live --input` and must not be
presented as the frozen holdout benchmark.

## Judge-facing docs

- `docs/PITCH.md` - the 5-minute story with provable numbers
- `docs/DISCLOSURE.md` - precise LLM-usage disclosure (evidence-gated
  machine-generated proposals; the gate, not the model, decides what ships)
- `docs/RED_TEAM.md` - what was attacked, what passed, what remains untested
- `docs/FREEZE.md` - pipeline contract, acceptance table, reproduce commands
- `demo.html` - offline evidence explorer: search an MPN, see every value's
  source trace and every abstention's reason

## Plan

Implemented per `docs/plans/...unihack-catalog-pipeline-plan.md`:

- Phase 1 Foundation - core model, entity resolution, taxonomy
- Phase 2 Trust & Evidence - extraction + dual-pass verification
- Phase 3 Measurability - gold set, byte-exact harness, critic loop
- Phase 4 Submission surface - freeze, manifest, verify_everything, demo.html,
  evidence explorer, honesty docs (this repo's current state)
