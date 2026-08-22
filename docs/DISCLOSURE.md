# DISCLOSURE — How ELIO Uses LLMs

**One-line truth:** Elio's frozen enrichment pipeline does not require an
external LLM call. No emitted attribute is accepted solely because a
generative model proposed it.

## What LLMs do

- **Evidence-gated machine-generated proposals only.** An LLM may *propose*
candidate values during enrichment (the proposal layer), but a proposal is
never emitted unless the deterministic dual-pass verification gate can trace
it to the source text or a documented unit conversion.
- The gate, not the model, decides what ships.

## What LLMs never do

| Function | Owned by |
|---|---|
| Verify values (dual-pass trace) | Deterministic gate (`unihack_catalog/stages.py`) |
| Decide acceptance vs abstention | Deterministic gate + quality layer |
| Taxonomy / classification | Word-boundary keyword matcher, closed tree |
| Export logic (252-column projection) | Deterministic code |
| URL / reference resolution | Frozen reference loader |

## The replay proof

The pipeline runs with the proposal layer on (`ELIO_ASSISTED=1`) or off
(`ELIO_ASSISTED=0`). The full acceptance table is reproduced by
`python -B scripts\verify_everything.py` (see `docs/FREEZE.md`). Any
judge can flip the flag and observe that the deterministic gates hold
identically — because they are deterministic.

## Commit-message reconciliation

Commit `229ba70` ("llm-assisted long-tail enrichment") used the phrase
"LLM-assisted". The approved framing is **"evidence-gated machine-generated
proposals"** — see `docs/FREEZE.md` rule 5. The pipeline behavior is
unchanged; only the wording was corrected so history and docs agree under
audit. The proposal layer was present at Bar 4 freeze (`38db2af`) and is
covered by the freeze manifest.

## Abstention

Where a value cannot be traced, ELIO abstains — it does not invent. The four
abstention classes are documented in `docs/FREEZE.md` (gold-blessed blanks,
pendant rows, dual-platform chargers, mixed-unit tape). Abstentions are
visible in `demo.html` as `[ABSTAINED]` cells with reasons, and in
`artifacts/evidence.json` as `status: "abstained"` records.

## Audit trail

- Frozen commit: `bar-5-clean` (tag `bar-5-clean`)
- Manifest: `submission_manifest.json` (SHA256-bound evidence set, verified
  by `python -B scripts\verify_manifest.py`)
- Reproduce: `python -B scripts\verify_everything.py`
- Evidence explorer: `demo.html` (offline)
