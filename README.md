# Elio — UniHack Catalog Intelligence

Normalize messy industrial B2B product rows into a schema-aligned, auditable
catalog: brand / OEM / distributor kept as distinct typed edges, closed-taxonomy
classpath, evidence-grounded attributes, constrained descriptions, and an honest
abstention decision — every emitted value traces to the source text.

Built for UniHack 2026. Gold-bar: **118/118 evaluated gold cells byte-exact**
against the official delivery-format workbook (2 rows × 252 cols; 134 populated
cells, 16 excluded as the 8 input columns × 2 rows), verified with a
dual-pass (value must appear in source text or be a literal unit conversion).

## Pipeline

9-stage plain-Python DAG (`unihack_catalog/stages.py`):

1. Ingest — 6 input columns (`Mfg_Part_Num, Part_Desc, E1/Unilog/DIB_Brand, Part_Manuf`)
2. Entity resolution — word-boundary brand matching, MPN-prefix map, supplier-aware
   (`Part_Manuf` is a supplier field; distributor names are never surfaced as OEM)
3. Taxonomy — longest-keyword match against a closed Dept>Class>Fine tree
4. Extraction — per-category extractors (discs, blades, belts, bits, adapters,
   fasteners, lighting, lumber, wire, electrical) + generic fallback
5. Description generation — mobile / invoice / short / long variants with char
   limits and validity flags
6. Verification — dual-pass: every value must trace to raw text; failures escalate
7. Quality — auto_accept only on gold-exempt evidence; everything else goes to review
8. Export — 252-column projection with UTF-8-sig encoding (Excel-safe ®)

## Layout

- `unihack_catalog/` — pipeline package (stages, extractors, reference loader, models)
- `docs/` — research brief, PRD, plan, demo UX spec, gauntlet progress log
- `*.csv` — 1000-row full export and 50-row balanced demo export (both gold rows included)
- `app.py` — Streamlit demo app (legacy; superseded by the frontend)

## Verification

| Check | Result |
|---|---|
| Gold byte-exact (incl. MFR URLs) | 118/118 evaluated (16 excluded = 8 input cols × 2 rows) |
| Dual-pass verification failures | 0 |
| Brand resolved (1000-row sample) | 866/1000 |
| Unknown Manufacturer (honest abstention) | 134 (distributors / no-signal / blacklisted) |
| Avg attributes/row (seed-7 holdout, assisted) | 2.156 |

Run the gold check (and every headline gate):

```bash
python -B scripts\verify_everything.py   # live gold gate: 118 evaluated, 16 excluded = 8 input cols x 2 rows
```

## Plan

Implemented per `docs/plans/...unihack-catalog-pipeline-plan.md`:

- Phase 1 Foundation — core model, entity resolution, taxonomy
- Phase 2 Trust & Evidence — extraction + dual-pass verification
- Phase 3 Measurability — gold set, byte-exact harness, critic loop
- Phase 4 Demo & Ship — exports, demo app, submission