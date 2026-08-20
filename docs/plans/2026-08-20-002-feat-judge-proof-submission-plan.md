---
title: ELIO Judge-Proof Submission
type: feat
status: active
date: 2026-08-20
origin: docs/ideation/2026-08-20-submission-surface-ideation.md
---

# ELIO Judge-Proof Submission

## Overview

Transform the frozen Elio pipeline (Bar 4, commit `38db2af`, tag `bar-4-freeze`) from an engineering artifact into a submission a skeptical judge can understand, verify, interrogate, and trust in under 5 minutes. All work is submission-support: verification tooling, a signed artifact manifest, a canonical metrics source, an offline interactive evidence explorer, and honesty docs. **Zero changes under `unihack_catalog/`** (sole exception: `unihack_catalog/verification_ledger.py`, the UAT gate script added in post-freeze commit `cf70946` — allowlisted everywhere the freeze boundary is asserted).

## Problem Frame

The pipeline is technically strong (gold 118/118, dual-pass fails 0, adversarial 589/589 @ 100% precision, blind critic 17-1) but the judge-facing surface is self-contradictory and unverifiable:

- README claims **130/130** byte-exact (README.md:8, 39) while FREEZE.md:36 says **118/118 evaluated gold cells**; README.md:43 claims attrs/row **0.74** while FREEZE.md:33 says **2.156** — the two documents a judge reads first contradict each other.
- The gold check is a dense one-liner (README.md:48-53); reproduce commands are PowerShell-specific with a manual cache-purge ritual (FREEZE.md:64-77).
- `scripts/.gauntlet_results.pkl` is modified post-freeze (evidence drift optics); commit `229ba70` says "llm-assisted" while FREEZE.md rule 5 forbids that phrasing — a history-vs-framing contradiction AI-slop audits are built to catch.
- The differentiator — 4-class honest abstention — is invisible in the export (blank cells read as "unfinished," not "refused").
- No interactive surface exists (`app.py` is disavowed as legacy, README.md:33).

Judging research (ideation run): reproducibility is a scored rubric category; judges spend 5-8 min on code+README; "evidence vs assumption" is an explicit dimension; git history is checked for authenticity; LLM disclosure is mandatory and scored; post-award AI-slop scrutiny is real.

## Requirements Trace

- R1. One command verifies every headline metric (acceptance bar 1)
- R2. Every headline metric comes from one canonical `metrics.json` (bar 2)
- R3. Frozen submission artifacts are SHA256-bound; `verify_manifest.py` fails loudly on any byte drift (bar 3)
- R4. A judge can open `demo.html` offline and inspect raw input, enriched output, evidence for accepted values, and reasons for abstained values (bar 4)
- R5. README, FREEZE.md, PITCH.md, and the video contain zero contradictory metrics (bar 5)
- R6. LLM usage is explicitly and honestly disclosed (bar 6)
- R7. A red-team document shows what was attacked, what passed, what failed, what remains untested (bar 7)
- R8. `git status` is clean (bar 8)
- R9. No changes under `unihack_catalog/` except the allowlisted `unihack_catalog/verification_ledger.py` (UAT gate tooling added post-freeze in `cf70946`, not pipeline code) (bar 9)
- R10. A fresh agent with no project context can clone → run verification → understand the claim → inspect evidence (bar 10)
- R11. P0 priority: freeze hygiene, manifest, verify_everything, metrics.json before any demo work (feature description priority order)
- R12. P1 priority: demo.html + abstention annotations, then DISCLOSURE.md (feature description priority order)
- R13. One canonical evidence object consumed by demo.html, spot_check (later), and red-team report — never implement evidence extraction three times (feature description verdict)

## Scope Boundaries

- **No pipeline changes**: `unihack_catalog/` stays byte-identical to `38db2af`. No Bar 5 — extraction work stops; another improvement loop reads as "you never finished."
- **No new dashboards**: one excellent static evidence explorer beats five surfaces; no knowledge-graph visualization; no fake scale claims (10M rows, enterprise-ready) — unmeasured.
- **No `spot_check.py` / `why_blank.py` standalone tools now**: folded into the canonical evidence object + demo.html (R13); `spot_check.py` may come later consuming the same evidence.
- **No prose linter**: manual README cleanup (inflated claims, buzzwords, contradictions) wins over a detector; user judgment applies.
- **No blind-critic re-run harness**: the critic snapshot (prompt + 17-1 judgments) is documented, not re-executed — it requires an external LLM and adds no gate value.

### Deferred to Follow-Up Work

- `scripts/spot_check.py --mpn` (engineering-facing evidence probe): separate later task consuming `artifacts/evidence.json` (R13).
- Freeze-boundary verification of ticket #8 artifacts (generalization evaluation): separate tracked work, not part of the submission surface.

## Context & Research

### Relevant Code and Patterns

- `scripts/regen_exports.py` — the canonical pattern for running the frozen pipeline over CSVs (`run_pipeline` → `stage_export`); `verify_everything.py` wraps its gate variants.
- `unihack_catalog/verification_ledger.py` — 6 UAT cases, exit code 0/1, print-based output; the model for gate scripts.
- `scripts/export_rules_map.py` — static-HTML generation pattern; **note: it uses Vis.js + Google Fonts CDNs — demo.html must NOT copy that; offline self-containment is required**.
- `unihack_catalog/models.py` — `AttributeRecord` (label/value/uom/source/confidence/verification), `SourceProvenance` (url/page/char_span/snippet), `QualityDecision.review_reasons` — the evidence object's source fields.
- `docs/FREEZE.md` — acceptance table (lines 29-43) and reproduce commands (lines 64-77); the numbers `verify_everything.py` replays.
- `scripts/adversarial_eval.py`, `scripts/gauntlet_holdout_eval.py` — deterministic gate scripts (per FREEZE.md:70).
- `demo_input_50.csv` / `demo_export_50.csv` — PDSH4816AF confirmed present in both (row 2); the demo explorer's seed rows.

### Institutional Learnings

- None in `docs/solutions/` (verified: no learnings store exists). Capture with `/ce-compound` after landing.

### External References

- Coalition for Secure AI, *Signing ML Artifacts* — signed manifest = signed collection of per-artifact hashes (the manifest pattern).
- PaperTrail (CHI 2026) — supported/unsupported/omitted claim classes (the abstention-annotation pattern).
- arXiv:2506.00694 — abstention ratio + error-on-answered rate as the honest framing.
- Judging rubrics (CBB 2026, Opportunity Hack, NYU Vibe Coding): reproducibility scored; 5-8 min code+README; evidence-vs-assumption dimension; mandatory LLM disclosure.

## Key Technical Decisions

- **One canonical evidence object** (R13): `artifacts/evidence.json` — per-cell `{mpn, attribute, value, evidence, status: accepted|abstained, reason}` — built once by an evidence-builder script, consumed by demo.html now and spot_check later. Evidence span = the dual-pass trace: the value string located within the raw input text (the same check the verification gate performs), or the reference-workbook snippet where applicable.
- **`verify_everything.py` regenerates `metrics.json` from live runs** (R1+R2): the script runs each gate, captures the numbers, writes `artifacts/metrics.json`, and prints the acceptance table with live PASS/FAIL. README/FREEZE/PITCH never hardcode headline numbers again — they render from (or link to) `metrics.json`. Number contradictions become structurally impossible.
- **Manifest hashes the evidence set, not the working tree**: exports, holdouts, adversarial artifacts, FREEZE.md, eval scripts, ledger, rules_map.html, demo.html. `verify_manifest.py` recomputes SHA256 and fails on any mismatch. The manifest records the freeze commit + tag + Python/dependency versions.
- **demo.html is fully offline**: data embedded at build time by the generator script (injected JSON, `export_rules_map.py`-style), no CDN, no fonts, no API. Works from a file:// URL on any judge laptop.
- **`metrics.json` number source**: the acceptance table values (attrs/row 2.156, Other 0.4%, gold 118/118, dpf 0, adversarial 589/589, provenance 100%, regressions 0, blind critic 17-1, 252-col export PASS). Where a number is a committed deterministic run (adversarial eval, blind critic), it is read from the committed artifact or stated as a fixed recorded value with the generating command recorded in the manifest.
- **PowerShell-only reproduce commands are kept in FREEZE.md but superseded**: `verify_everything.py` is the cross-platform single entry point; `ELIO_ASSISTED=1` and the cache purge become internal concerns of the script (env var set programmatically where needed, purge before holdout eval).

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

```
scripts/verify_everything.py
  ├── gate: freeze integrity   (git diff 38db2af HEAD -- unihack_catalog/ == empty, allowlisted: verification_ledger.py)
  ├── gate: UAT ledger         (import verification_ledger, run 6 cases)
  ├── gate: rules linter       (import rules_linter check)
  ├── gate: gold exact         (run_pipeline on the 2 gold rows vs delivery workbook)
  ├── gate: adversarial replay (adversarial_eval.py determinism / committed result)
  ├── gate: export columns     (252-col contract check on both exports)
  ├── gate: manifest           (verify_manifest SHA256 check)
  └── writes artifacts/metrics.json  ← single source of truth
        README / FREEZE / PITCH / video script all read from here

scripts/build_evidence.py
  └── runs frozen pipeline over demo_input_50.csv (+ selected adversarial rows)
      └── artifacts/evidence.json   {mpn, attribute, value, evidence, status, reason}

scripts/build_demo_html.py
  └── embeds evidence.json + raw input rows + export rows
      └── demo.html  (offline, file:// safe, cell → evidence / abstention reason)

submission_manifest.json + scripts/verify_manifest.py
  └── SHA256 of every frozen evidence artifact → FAIL on any byte drift
```

## Implementation Units

- U1. **[Freeze hygiene — clean tree + `check_freeze.py`]**

**Goal:** `git status` clean-or-intentional; the freeze boundary is provable with one command; the post-freeze commits self-label as docs/tooling.

**Requirements:** R8, R9, R10

**Dependencies:** None

**Files:**
- Create: `scripts/check_freeze.py`
- Modify: `.gitignore`
- Delete (untracked clutter, if confirmed safe): `.agents/`, `graphify-out/`, `skills-lock.json`, `scripts/search_inspected.py`, `docs/ideation/antigravity_hardening.html` (or gitignore them — implementer judgment, prefer deletion of agent-tool clutter that must not ship)
- Test: `scripts/check_freeze.py` self-check (no separate test file needed; the script asserts its own invariants and exits non-zero on failure)

**Approach:**
- `check_freeze.py`: asserts `git diff 38db2af HEAD -- unihack_catalog/` contains only the allowlisted `verification_ledger.py` (exit 0), asserts tag `bar-4-freeze` points at `38db2af`, prints what the two post-freeze commits (7be141a, cf70946) actually changed (docs + tooling only — note `cf70946` added `unihack_catalog/verification_ledger.py`, UAT tooling allowlisted here, not pipeline code), and prints `git status --porcelain` as an audit line. Read-only, print-based, mirrors `verification_ledger.py` style.
- First untrack the evidence cache: `git rm --cached scripts/.gauntlet_results.pkl` (it is currently tracked — `.gitignore` alone cannot untrack it). Then `.gitignore`: add `scripts/.gauntlet_results.pkl` (evidence cache — regenerable, was only dirty because eval runs rewrite it), `__pycache__/`, `.pkl` caches.
- Untracked clutter: remove `.agents/`, `graphify-out/`, `skills-lock.json`, `scripts/search_inspected.py` from the working tree (untracked — safe to delete; they are session/agent artifacts, not submission evidence). Keep `docs/ideation/` (it is the origin doc for this plan).
- Do NOT commit `unihack_catalog/` changes; do not rebase/amend history — judges read the commit graph; leave `38db2af` → `7be141a` → `cf70946` visible and labeled in the commit messages of this plan's work.

**Patterns to follow:** `verification_ledger.py` (print-based gate, exit code contract).

**Test scenarios:**
- Happy path: with the tree clean, `check_freeze.py` exits 0 and prints all-PASS lines.
- Edge case: `.gitignore` entry for `.gauntlet_results.pkl` — `git status --porcelain` no longer lists it after a cache rewrite.
- Error path: if `unihack_catalog/` is ever touched (simulate with a temp edit), `check_freeze.py` exits non-zero and names the offending file.
- Integration: `git status --porcelain` shows only intentional entries (new scripts/docs committed by this plan; nothing else).

**Verification:** `git status` is clean-or-intentional; `check_freeze.py` passes; untracked agent clutter is gone from the working tree.

---

- U2. **[Submission manifest + verifier]**

**Goal:** Every frozen artifact is SHA256-bound; `verify_manifest.py` proves "the exact artifacts you're looking at are the frozen ones" in one command.

**Requirements:** R3, R10

**Dependencies:** None (runs standalone; U3 calls into it)

**Files:**
- Create: `submission_manifest.json`
- Create: `scripts/verify_manifest.py`
- Test: `scripts/verify_manifest.py` self-check (exit-code contract; no separate test file)

**Approach:**
- Manifest entries (path → SHA256 + size + role label): `Unihack_Full_Export_1000.csv`, `demo_export_50.csv`, `demo_input_50.csv`, `docs/FREEZE.md`, `docs/gauntlet-progress.md`, `unihack_catalog/verification_ledger.py`, `scripts/adversarial_*.{py,csv,json}`, `scripts/gauntlet_holdout_eval.py`, `scripts/baseline_holdout*.csv`, `scripts/holdout_round2.csv`, `scripts/holdout_mpns.json`, `scripts/rules_linter.py`, `scripts/export_rules_map.py`, `rules_map.html`, `docs/ideation/2026-08-20-submission-surface-ideation.md`, plus `scripts/verify_everything.py`, `scripts/build_evidence.py`, `scripts/build_demo_html.py`, `demo.html`, `artifacts/metrics.json`, `artifacts/evidence.json`, `docs/DISCLOSURE.md`, `docs/RED_TEAM.md`, `docs/PITCH.md`, and the video script (added when U3 resyncs it). U2 lists paths for the frozen set; U3-U8 add their outputs to the manifest.
- Manifest header: `{freeze_commit: 38db2af, freeze_tag: bar-4-freeze, generated: date, python: version, deps: versions}` — regenerated by a `--update` flag, never hand-edited hashes.
- `verify_manifest.py`: recompute SHA256 per entry, print `PASS/FAIL: <path>` per line, exit non-zero on any mismatch. A mismatch must name the file and the expected-vs-actual hash (the "if one byte changes" contract).

**Patterns to follow:** `verification_ledger.py` exit-code contract; `export_rules_map.py` ROOT-path bootstrap.

**Test scenarios:**
- Happy path: `verify_manifest.py` exits 0, all entries PASS.
- Error path: append a byte to `demo_export_50.csv` (temp copy scenario) → `FAIL: demo_export_50.csv hash mismatch` + non-zero exit.
- Edge case: missing file (rename a holdout temporarily) → explicit `MISSING` line, non-zero exit.
- Edge case: `--update` regenerates hashes and the manifest stays parseable JSON.
- Integration: U3's `verify_everything.py` invokes the verifier and reports its gate as PASS only when it exits 0.

**Verification:** Touching any manifest-bound file makes `verify_manifest.py` fail loudly with the offending path; restoring it passes again.

---

- U3. **[`verify_everything.py` — one command, live acceptance grid + `metrics.json`]**

**Goal:** One cross-platform command replays every headline gate, prints the acceptance table with live PASS/FAIL, and writes `artifacts/metrics.json` — the canonical source every doc reads from.

**Requirements:** R1, R2, R5, R10, R11

**Dependencies:** U1, U2 (freeze check + manifest gates), existing gate scripts

**Files:**
- Create: `scripts/verify_everything.py`
- Create: `artifacts/metrics.json` (generated)
- Modify: `docs/FREEZE.md` (Reproduce section: add `verify_everything.py` as the single entry point; keep existing commands as fallback detail)
- Test: `scripts/verify_everything.py` self-check + one temp-dir smoke test (no separate test file)

**Approach:**
- Gate list (each prints `[PASS]/[FAIL] <label>` and contributes to exit code):
  1. Freeze integrity — invoke U1 check
  2. Manifest — invoke U2 verifier
  3. 252-column export — header contract check on both exports
  4. Gold exact 118/118 — run the 2 gold rows through the frozen pipeline vs the delivery workbook (reuse the gold-check logic from README.md:48-53, cleaned into a callable function rather than the inline one-liner). **Count like `adversarial_eval.py`'s gold_check: 118 evaluated of 130 populated cells — the 12 excluded are the 6 input columns × 2 gold rows (Mfg_Part_Num, Part_Desc, E1_Brand, Unilog_Brand, DIB_Brand, Part_Manuf), not "URLs/unverifiable literals". The README one-liner's 130/130 framing must not leak into the gate: the live gate and `metrics.json` must agree on 118.**
  5. Dual-pass failures 0 — committed result from adversarial/gauntlet runs, or rerun of `adversarial_eval.py` (deterministic per FREEZE.md:70)
  6. Other % 0.4 — read from committed holdout result
  7. attrs/row 2.156 — read from committed seed-7 holdout result
  8. Adversarial precision 589/589 — committed result
  9. Provenance coverage 100% — committed result
  10. Bar-3 regressions 0 — committed result
  11. UAT ledger — invoke `verification_ledger.run_ledger_tests()`
  12. Rules linter — invoke rules_linter check
- **Runtime policy**: deterministic committed numbers (6-10) are read from the committed artifacts/records with the generating command recorded; live-runnable gates (1-5, 11, 12) execute. A `--full` flag reruns the heavy evals. Rationale: judges get a 60-90s one-command experience; the heavy evals are documented and rerunnable via FREEZE.md.
- **README quick-fix (R5)**: as soon as `metrics.json` exists, correct README's two headline contradictions (the 130/130 vs 118/118 relationship at README.md:8/39; attrs/row 0.74 → 2.156 at README.md:43). The full rewrite stays in U8; the numbers stop lying today — README is the second artifact judges open after the video.
- **Video resync (R5)**: after `metrics.json` is written, diff the 4-min video script's metric mentions against `metrics.json` and update them (plus any on-screen numbers if re-rendered) — the video is the judge's first touchpoint and must show zero-contradictory metrics. Add the video script to the manifest (U2 `--update`) as a hashed artifact.
- `metrics.json` shape: `{generated, freeze_commit, gates: {gold: "118/118", dpf: 0, other_pct: 0.4, attrs_per_row: 2.156, adversarial: "589/589 @ 100%", provenance: 1.0, regressions: 0, blind_critic: "17-1 (7 ties)", export_252: true}, sources: {<metric>: <generating command or artifact>}}` — every value carries its source so README/PITCH can cite it.
- Verdict line: `VERDICT: ACCEPTED` (exit 0) or `VERDICT: FAILED` (exit non-zero) — the exact output sketch from the feature description.
- Set `ELIO_ASSISTED=1` programmatically for assisted gates; purge `.gauntlet_results.pkl` before holdout eval (internal, not a documented manual ritual).

**Patterns to follow:** `verification_ledger.py` (gate contract); FREEZE.md:64-77 command list (the six commands this replaces).

**Test scenarios:**
- Happy path: on the frozen tree, script prints the full grid, all PASS, `VERDICT: ACCEPTED`, exit 0, `artifacts/metrics.json` written with correct values.
- Error path: break a manifest file → its gate FAILs, exit non-zero, verdict FAILED.
- Error path: simulated gold mismatch (temp-modified workbook copy) → gold gate FAILs with the exact count.
- Edge case: missing `artifacts/` dir → created; missing `.gauntlet_results.pkl` → not an error (purge tolerates absence).
- Integration: `metrics.json` values match FREEZE.md acceptance table exactly (U5's README rewrite and U8's PITCH consume this file — a mismatch here re-opens the contradiction it must close).

**Verification:** Running the script on the committed tree yields the acceptance table from FREEZE.md with all-PASS, and `metrics.json` values agree with FREEZE.md:29-43.

---

- U4. **[`build_evidence.py` — canonical evidence object]**

**Goal:** One evidence builder produces `artifacts/evidence.json` — per-cell accepted/abstained records with evidence spans — consumed by demo.html (U5) now and spot_check later (R13). Never implement evidence extraction twice.

**Requirements:** R4, R13

**Dependencies:** None (reads frozen pipeline outputs)

**Files:**
- Create: `scripts/build_evidence.py`
- Create: `artifacts/evidence.json` (generated)
- Test: `scripts/build_evidence.py` self-check (asserts schema + coverage invariants)

**Approach:**
- Run the frozen pipeline over `demo_input_50.csv` (50 rows; PDSH4816AF confirmed present) plus the 8 invented fresh-upload rows (adversarial input set) for abstention coverage.
- Per row, per attribute cell, emit:
  - Accepted: `{mpn, attribute, value, uom, evidence: <source snippet or located raw-text span>, confidence, status: "accepted"}`
  - Abstained: `{attribute, value: null, status: "abstained", reason: <one of the 4 abstention classes or review_reason text>}`
- Evidence span construction: locate the value string within the row's raw input text (the dual-pass trace — value must appear in source text or be a documented unit conversion); fall back to the reference-workbook snippet where the dual-pass cites it. Where the model exposes `AttributeRecord.source.snippet`/`char_span`, prefer those fields (models.py:38-49).
- Abstention reasons come from `QualityDecision.review_reasons` (models.py:68) and the 4 documented abstention classes (FREEZE.md:17-19: gold-blessed blanks, pendant rows, dual-platform chargers, mixed-unit tape).
- The exporter stays read-only over the pipeline: `run_pipeline` on inputs, serialize outputs. No pipeline modification.

**Patterns to follow:** `regen_exports.py` (pipeline invocation + ROOT path bootstrap); `models.py` field names.

**Test scenarios:**
- Happy path: evidence.json contains ≥1 accepted record with a non-empty evidence span for PDSH4816AF (e.g., Amperage "15 A" traced to "15A" in source).
- Happy path: abstained records present with a reason string from the known class set.
- Edge case: a value absent from raw text but accepted via unit conversion is labeled with the conversion (not an empty evidence field).
- Error path: pipeline raises on a row → builder reports the row, continues, and fails at the end with a non-zero exit (no silent partial write).
- Integration: every `attribute` in evidence.json maps to a real export column in `demo_export_50.csv` (or is explicitly abstained).

**Verification:** `artifacts/evidence.json` parses, every record has `status` ∈ {accepted, abstained}, accepted records have evidence, abstained records have reasons; PDSH4816AF shows the feature-description behavior (values with evidence, abstentions with reasons).

---

- U5. **[`build_demo_html.py` — offline interactive evidence explorer]**

**Goal:** A judge opens `demo.html` (file://, offline, zero install) and in 30 seconds: searches an MPN, sees raw input → enriched output side-by-side, clicks a value to see its evidence, and sees abstentions with explicit reasons.

**Requirements:** R4, R12

**Dependencies:** U4 (evidence.json)

**Files:**
- Create: `scripts/build_demo_html.py`
- Create: `demo.html` (generated)
- Modify: `submission_manifest.json` (add demo.html + builder, via U2's `--update`)
- Test: `scripts/build_demo_html.py` self-check (schema/embedding assertions); manual browser smoke test

**Approach:**
- Generator embeds the raw input rows (from `demo_input_50.csv`), the enriched export rows (from `demo_export_50.csv`), and `artifacts/evidence.json` directly into the HTML at build time — the `export_rules_map.py` injection pattern (`%DATA%` placeholder replace).
- **Offline requirement (differs from `export_rules_map.py`):** no Vis.js CDN, no Google Fonts, no external anything. Vanilla JS + embedded JSON only. Test by opening via `file://` with network disabled.
- **252-column scoping:** the export row is 252 columns — never render all of them. Render evidence-bearing columns first (columns carrying accepted values with evidence or abstained values with reasons, per `evidence.json`), with a reveal-remaining affordance for the rest. The 30-second demo goal depends on this scoping, not on rendering the full row.
- UI: MPN search box; row view with RAW INPUT panel and ELIO OUTPUT panel; each accepted value renders a `WHY?` affordance revealing the evidence span + confidence; each abstained value renders `[ABSTAINED]` with the reason (the feature-description killer feature).
- Add the "how this works" footer: one line on dual-pass verification, link to FREEZE.md, and the verify command.

**Patterns to follow:** `export_rules_map.py` HTML-generation structure; feature-description UI sketch (search → RAW INPUT → ELIO OUTPUT → WHY? / ABSTAINED).

**Test scenarios:**
- Happy path: `demo.html` contains embedded evidence for PDSH4816AF; searching the MPN renders the row with both accepted (evidence shown) and abstained (reason shown) cells.
- Edge case: file has zero external network references — assert the generated HTML contains no `http://`/`https://`/`src=` to external hosts; grep-able invariant.
- Edge case: an abstained cell renders the reason string, never an empty cell or "N/A".
- Error path: missing evidence.json → builder fails loudly with a clear message (no half-built HTML).
- Integration: opening the file from a temp dir with network disabled still renders and searches.

**Verification:** `demo.html` opens offline from a file:// path; MPN search works; every value cell has either evidence or an abstention reason; no external network references in the HTML.

---

- U6. **[DISCLOSURE.md — precise LLM-usage disclosure]**

**Goal:** Kill the "LLM-assisted" ambiguity before a judge finds it; make disclosure a designed strength, not a confession.

**Requirements:** R6

**Dependencies:** None

**Files:**
- Create: `docs/DISCLOSURE.md`
- Modify: `submission_manifest.json` (add file via U2 `--update`)

**Approach:**
- Structure: what LLMs do (evidence-gated machine-generated proposals only — never free-form output), what they never do (verify, decide acceptance, taxonomy, export logic), and the mechanism: `ELIO_ASSISTED=0` vs `=1` replay proof that the gate, not the model, decides what ships (FREEZE.md rule 5 wording used verbatim).
- Use the feature-description disclosure text as the core statement: "Elio's frozen enrichment pipeline does not require an external LLM call… No emitted attribute is accepted solely because a generative model proposed it."
- Commit-message reconciliation: explicitly note commit `229ba70` ("llm-assisted long-tail enrichment") and re-state it in the approved phrasing, so history and docs agree under audit.
- Content-only artifact; no code.

**Patterns to follow:** FREEZE.md rule 5 phrasing (lines 23-25); feature-description disclosure block.

**Test scenarios:**
- `Test expectation: none` — content-only artifact. Verification is a consistency grep: the words "LLM-assisted" appear in DISCLOSURE.md only inside the reconciliation note; README and PITCH use the approved phrasing.

**Verification:** A skeptical auditor can write a one-page summary of LLM usage from the repo alone that matches reality; no README/PITCH surface calls the proposal layer "LLM-assisted."

---

- U7. **[RED_TEAM.md — the self-attack dossier]**

**Goal:** Package the existing adversarial work into a judge-readable attack log: what was attacked, what passed, what failed, what remains untested.

**Requirements:** R7

**Dependencies:** None (numbers already measured)

**Files:**
- Create: `docs/RED_TEAM.md`
- Modify: `submission_manifest.json` (add file via U2 `--update`)

**Approach:**
- Table from the feature description: attack → outcome (Amperage false positive: blocked; LG substring brand collision: blocked; Bluetooth→Blue: blocked; mixed-unit dimensions: abstained; dual-platform charger: abstained; adversarial 589 values: 589 accepted correctly; untraceable values: 0), plus blind critic 17-1, fresh-upload 8/8.
- Snapshot the blind-critic prompt + judgment summary into the doc (or a referenced file) so the evaluation is reproducible-by-documentation without re-running an LLM.
- "What we still haven't proven" section — the honest ceiling: no demonstrated generalization outside the evaluated distribution (e.g., arbitrary industrial catalogs, other verticals); single-threaded, 1000-row scale; no claims about 10M rows.

**Patterns to follow:** feature-description RED_TEAM table; FREEZE.md adversarial numbers (lines 37-43).

**Test scenarios:**
- `Test expectation: none` — content-only artifact. Verification: every number in RED_TEAM.md matches FREEZE.md's acceptance table; the "untested" section exists and names at least the generalization boundary.

**Verification:** A judge reads the doc and can list what was attacked, what passed, what failed, what remains untested — in 90 seconds.

---

- U8. **[PITCH.md + README rewrite from canonical metrics]**

**Goal:** The judge's 5-8 minute read: one page that tells the story with numbers that provably come from `metrics.json`, and a README that no longer contradicts anything.

**Requirements:** R5, R6

**Dependencies:** U3 (metrics.json)

**Files:**
- Create: `docs/PITCH.md`
- Modify: `README.md`
- Modify: `submission_manifest.json` (add PITCH.md via U2 `--update`)

**Approach:**
- PITCH.md follows the feature-description structure verbatim: The problem / What Elio does / The difference (more correct fields + traceable evidence + explicit abstention) / Proof (2.156 attrs/row, 118/118 gold, 0 dual-pass fails, 589/589 @ 100%, 0 untraceable, 17-1 blind critic) / The judge action (`python scripts/verify_everything.py`). Every number sourced from `artifacts/metrics.json` (R5).
- README rewrite:
  - Reconcile the number contradiction: "130/130 populated cells byte-exact" (README.md:8, 39) vs FREEZE.md's "118 evaluated gold cells 118/118" → state the relationship once: 130 populated cells; 118 evaluated (12 excluded: the 6 input columns — Mfg_Part_Num, Part_Desc, E1_Brand, Unilog_Brand, DIB_Brand, Part_Manuf — across the 2 gold rows); both exact.
  - Fix attrs/row 0.74 → 2.156 (README.md:43; the 0.74 is pre-Bar-1 stale).
  - Replace the dense gold-check one-liner (README.md:48-53) with `python scripts/verify_everything.py` + link to FREEZE.md and PITCH.md.
  - Fix "app.py — legacy; superseded by the frontend" (README.md:33) → "legacy; see demo.html (offline evidence explorer)".
  - Use approved LLM phrasing (FREEZE.md rule 5); add a Verification section pointing at `verify_everything.py`, `verify_manifest.py`, `demo.html`, DISCLOSURE.md, RED_TEAM.md.

**Patterns to follow:** feature-description PITCH structure; FREEZE.md rule 5 phrasing; metrics.json as the only numeric source.

**Test scenarios:**
- Happy path: every numeric claim in README.md and PITCH.md matches `artifacts/metrics.json` (grep-able invariant — script one-liner in verification).
- Edge case: "130/130" appears nowhere as a standalone claim — the reconciled 130-populated / 118-evaluated relationship is stated with both numbers explained.
- Edge case: "LLM-assisted" absent from README/PITCH (approved phrasing only).
- Integration: README's verification section commands exist and run (verify_everything.py, verify_manifest.py).

**Verification:** A repo-wide grep shows zero contradictory headline numbers across README, FREEZE, PITCH, and metrics.json; the judge-action command is a real, working entry point.

---

- U9. **[Walk-test acceptance gate]**

**Goal:** Prove acceptance bar 10: a fresh agent with no project context can clone → run verification → understand the claim → inspect evidence.

**Requirements:** R10

**Dependencies:** U1-U8 (everything it tests)

**Files:**
- Create: `docs/WALK_TEST.md`
- Modify: `submission_manifest.json` (add file via U2 `--update`)

**Approach:**
- A checklist doc, not a script: (1) clone the repo; (2) read README; (3) run `python scripts/verify_everything.py` → ACCEPTED; (4) run `python scripts/verify_manifest.py` → all PASS; (5) open `demo.html`, search PDSH4816AF, inspect one accepted value's evidence and one abstention's reason; (6) read PITCH.md and confirm the numbers match the verification output; (7) time the whole thing — target under 10 minutes from a clean clone.
- The walk test itself is executed as the final acceptance gate before submission (run by this agent at plan completion or by the user); WALK_TEST.md records the run date + outcome + timing.

**Patterns to follow:** feature-description acceptance bar 10; FREEZE.md evidence-set discipline.

**Test scenarios:**
- Happy path: checklist steps 1-6 all pass on a fresh clone in a temp dir.
- Edge case: machine without PowerShell — verify_everything.py is the cross-platform path (no PowerShell required).
- Edge case: offline machine — demo.html opens, manifests verify (no network needed).

**Verification:** A clean-clone run of the walk test completes in under 10 minutes with every checklist item passed; outcome recorded in WALK_TEST.md.

---

- U10. **[Final integration: regenerate manifest, full verify, commit the surface]**

**Goal:** The submission surface is complete, hashed, verified, and committed with a history that self-labels.

**Requirements:** R3, R8, R9, R10

**Dependencies:** U1-U9

**Files:**
- Modify: `submission_manifest.json` (final `--update` — all artifacts hashed)
- Modify: `.gitignore` (final pass)
- Commit: all plan outputs (new scripts, docs, artifacts, generated HTML) as labeled commits; no `unihack_catalog/` changes

**Approach:**
- Regenerate every artifact in dependency order (U1-U9), run `verify_manifest.py --update` then `verify_manifest.py` (clean), run `verify_everything.py` (all PASS), run the walk test (U9), then commit with commit messages that self-label as submission-support (the "docs-only / evidence-only; zero pipeline changes" convention from the ideation findings).
- Do not touch git history: `38db2af` → `7be141a` → `cf70946` stay as-is; the new commits sit on top with clear labels.

**Patterns to follow:** commit hygiene from FREEZE.md (rule 6: evidence set stays in-repo); bar-4-freeze tag convention.

**Test scenarios:**
- Integration: full sequence from clean tree — regenerate → verify → walk test → commit — every gate passes at each stage.
- Edge case: `git status --porcelain` post-commit is empty (everything intentional is committed; nothing untracked remains).
- Error path: if any gate fails during the sequence, fix the artifact (not the pipeline) and re-run — the plan's scope boundary holds.

**Verification:** Clean `git status`; `verify_everything.py` ACCEPTED; `verify_manifest.py` all PASS; walk test recorded; zero diffs under `unihack_catalog/` vs `38db2af` (verification_ledger.py allowlisted).

---

## Phased Delivery

### Phase 1 — P0 (tonight, U1-U3)
Freeze hygiene → manifest + verifier → verify_everything + metrics.json. The credibility landmine (contradictory numbers, dirty evidence, unverifiable claims) is defused first — including the README headline-number quick-fix and the video-script resync against the fresh metrics.json (the two surfaces a judge sees before the repo).

### Phase 2 — P0/P1 (U4-U5)
Evidence builder → demo.html. The judge-facing differentiator: inspectable evidence + explicit abstention.

### Phase 3 — P1/P2 (U6-U10)
DISCLOSURE.md → RED_TEAM.md → PITCH.md + README rewrite → walk test → final integration commit.

## System-Wide Impact

- **Interaction graph:** `verify_everything.py` invokes `verification_ledger.run_ledger_tests()`, `rules_linter`, `adversarial_eval.py`, and U1/U2 checks — it is a supervisor over existing gates, not a new gate. `build_evidence.py` and `build_demo_html.py` read pipeline outputs read-only.
- **Error propagation:** every script follows the ledger contract — print `[PASS]/[FAIL]`, exit 0/1. `verify_everything.py` aggregates gate exit codes into one verdict; no gate failure is swallowed.
- **State lifecycle risks:** `.gauntlet_results.pkl` is regenerable cache — gitignored (U1) so post-freeze rewrites stop appearing as dirty evidence. Evidence/metrics artifacts are generated (never hand-edited) — regeneration is the recovery path.
- **API surface parity:** no public API/CLI contract changes. The six FREEZE.md reproduce commands remain valid; `verify_everything.py` supersedes them as the entry point without removing them.
- **Integration coverage:** the walk test (U9) is the cross-layer scenario — clone, verify, inspect, understand — proving all surfaces agree.
- **Unchanged invariants:** `unihack_catalog/` byte-identical to `38db2af`; dual-pass verification gate untouched; 4 abstention classes untouched; FREEZE.md rule 5 phrasing respected everywhere; git history unmodified (no rebase/amend).

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| `verify_everything.py` runtime too long for judge patience | Default path reads committed deterministic numbers (60-90s); `--full` flag reruns heavy evals |
| Generated metrics.json drifts from FREEZE.md prose | U3 emits the table; U8 (README/PITCH) reads metrics.json — FREEZE.md is the reference the script asserts against |
| demo.html accidentally pulls CDN resources (copied pattern from `export_rules_map.py`) | Offline invariant is an explicit test scenario: no external URLs in generated HTML |
| Evidence span construction differs from dual-pass semantics | Prefer `AttributeRecord.source` fields; fall back to value-in-raw-text location — same check the gate performs |
| Post-freeze commits read as "numbers moved" | U1 labels all new commits submission-support; freeze check + manifest make the boundary provable |
| Walk test fails on clean clone (env drift) | U9 checklist includes env setup; verify_everything is cross-platform Python; pandas/pydantic are declared in requirements |

## Documentation / Operational Notes

- `docs/FREEZE.md` Reproduce section gains `verify_everything.py` as the single entry point (U3).
- `README.md` Verification section is rewritten (U8); PITCH.md becomes the judge-facing summary.
- No deployment, monitoring, or runtime operations — all artifacts are static, offline, and regenerable.

## Sources & References

- **Origin document:** [docs/ideation/2026-08-20-submission-surface-ideation.md](docs/ideation/2026-08-20-submission-surface-ideation.md) (feature description = the ideation verdict; this plan implements its P0/P1/P2 order and acceptance bar)
- Related code: `scripts/regen_exports.py`, `unihack_catalog/verification_ledger.py`, `scripts/export_rules_map.py`, `unihack_catalog/models.py`, `docs/FREEZE.md`
- External docs: Coalition for Secure AI *Signing ML Artifacts*; PaperTrail (CHI 2026); arXiv:2506.00694 (abstention measurement)