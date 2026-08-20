# FREEZE — Bar 4 (adversarial-hardened pipeline)

Frozen at commit `<FILLED BY COMMIT>` (tag `bar-4-freeze`), superseding the
Bar 3 freeze intent (ticket #5). Every gate in the acceptance table passed
on the seed-7 holdout, the difficulty-stratified adversarial holdout, the
full-export diff vs `229ba70`, a blind critic A/B, and a fresh-upload
end-to-end run.

## Pipeline contract (do not change without a new bar)

1. **No pipeline changes** to `unihack_catalog/` after this freeze. The sole
   exception is the post-freeze generalization evaluation (ticket #8), which
   may reveal new evidence classes — any change it motivates becomes Bar 5
   and must re-run the full acceptance table.
2. Filled values must trace to the source text or a documented unit
   conversion (the dual-pass verification gate). Never weaken the gate.
3. If a value cannot be traced, the four abstention classes apply
   (gold-blessed blanks, pendant rows, dual-platform chargers, mixed-unit
   tape) — output blank, never invent.
4. Attribute count is a lagging metric; precision, provenance, and honest
   abstention are the contract. Do not chase counts at the cost of any of
   them.
5. Never describe the proposal layer as "LLM-assisted" in any submission
   artifact. It is "evidence-gated machine-generated proposals" — the
   verification gate (not the model) decides what ships.
6. Claims must be artifact-backed: exports, holdout CSVs, eval scripts, and
   this file are the evidence set and stay in-repo.

## Acceptance table — final Bar 4 numbers

| Gate | Bar 3 (`229ba70`) | Bar 4 (this freeze) | Status |
|---|---|---|---|
| attrs/row (seed-7 holdout, assisted) | 2.13 | 2.156 | PASS |
| Other % | 0.7% | 0.4% | PASS |
| Dual-pass fails | 0 | 0 | PASS |
| Gold exact (118 evaluated gold cells) | 118/118 | 118/118 | PASS |
| Untraceable accepted values (adversarial holdout, 277 rows / 589 values) | — | 0 | PASS |
| Precision on accepted (gate replay w/ full expansions) | — | 100% (589/589) | PASS |
| Provenance coverage on accepted | — | 100% | PASS |
| Regressions vs Bar 3 (correct-value losses) | — | 0 | PASS |
| 252-column export | PASS | PASS | PASS |
| Blind critic A/B (26 contested rows) | — | 17–1 (7 ties, 1 both-satisfied) | PASS |
| Fresh upload end-to-end (8 invented adversarial rows) | — | PASS | PASS |

## What Bar 4 changed vs Bar 3 (and why)

- **LG brand guard**: `\bLG\b` no longer fires on "Lg." (Large) or "BLK LG"
  (Black, Large); glove/holster/apparel words suppress LG. Removed 6 false
  LG-brand cells (3 rows) from the export.
- **Word-boundary taxonomy matching**: keyword substring traps killed —
  "Blue" from Blue**tooth**, "Red" from fissu**red**, "LED Bulbs" from
  **sled**, "Concrete Products" from pencil **lead**, "Trim" from hedge
  **trimmer**. Recovered fused product names with explicit keywords:
  `bandsaw`, `hardiepanel`, `plusosb`, `sub floor`, `raftersquare`,
  `drilling`, `battery mounts`.
- **Ceiling-tile unit swap**: `2x2`/`2x4` → feet convention; `24x24` stays
  inches (both numbers ≤ 6 ⇒ feet).
- **Taxonomy keywords**: jumpstart / jump starter / holster / pwr supply →
  Power Supplies / Tool Organizers; ceiling-tile → Ceiling Tiles.
- **Color extraction**: all colors word-bounded.

## Reproduce

```powershell
# assisted exports (proposal layer on):
$env:ELIO_ASSISTED="1"; python -B scripts\regen_exports.py
# seed-7 holdout (purge cache first):
Remove-Item scripts\.gauntlet_results.pkl; python -B scripts\gauntlet_holdout_eval.py
# adversarial holdout gate replay (real gate + expansions):
python -B scripts\adversarial_eval.py   # deterministic; assisted numbers in table above
```

Evidence set: `scripts/baseline_holdout*.csv`, `scripts/holdout_mpns.json`,
`scripts/adversarial_*.{py,csv,json,txt}`, `Unihack_Full_Export_1000.csv`,
`demo_export_50.csv`, `docs/gauntlet-progress.md` (Bar 3 + Bar 4 sections).