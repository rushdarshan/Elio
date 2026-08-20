---
date: 2026-08-20
topic: submission-surface-ideation
focus: judge-facing submission improvements (freeze 38db2af, deadline Aug 23)
mode: repo-grounded
---

# Ideation: Judge-Facing Submission Surface

## Grounding Context

**Codebase context:** Elio normalizes messy B2B industrial product rows into a 252-column catalog (brand/OEM/distributor typed edges, closed taxonomy, evidence-grounded attributes, 4 abstention classes). Pipeline frozen at `38db2af`. Bar-4: attrs/row 2.156, gold 118/118, dpf 0, adversarial 589 values 100% precision, blind critic 17-1. Artifacts: exports, holdouts, FREEZE.md, gauntlet-progress.md, verification_ledger.py (6 UAT), rules_linter.py, export_rules_map.py → rules_map.html.

**External context (judging research):** reproducibility is a scored rubric category; judges spend 5-8 min on code+README after a 4-min video; "evidence vs assumption" is an explicit dimension; judges check git history for authenticity; LLM disclosure is mandatory and scored; only reliable working features count; post-award AI-slop scrutiny is a real risk (DeepMind $25K controversy). Abstention literature: report abstention rate + error-on-answered rate; provenance links per field; signed manifest + audit bundle = standard pattern.

**Known gaps:** README "130/130" vs FREEZE.md "118/118" inconsistency; README "0.74" vs FREEZE "2.156" attrs/row; `.gauntlet_results.pkl` dirty in git; untracked clutter; 2 post-freeze commits (7be141a, cf70946); no interactive demo surface (app.py disavowed legacy); commit 229ba70 says "llm-assisted" vs FREEZE rule 5 phrasing.

**Constraints:** NO changes to `unihack_catalog/`; tasks ~30-60 min; tactical quick-win scope.

## Ranked Ideas

### 1. verify_everything.py + metrics.json — one command, live acceptance grid
**Description:** One cross-platform script re-runs every acceptance gate (gold, dual-pass, adversarial, UAT ledger, rules linter), prints the FREEZE.md acceptance table with live PASS/FAIL per row, and emits `metrics.json` — the single canonical source of headline numbers that README/PITCH/video all read from. Kills the 130/130 vs 118/118 and 0.74 vs 2.156 drift structurally.
**Warrant:** `direct:` FREEZE.md:64-77 lists six disjoint reproduce commands a judge must reconcile with the table at FREEZE.md:29-43; README.md:8/43 contradicts FREEZE.md:36/33, proving prose drift is real. `external:` HF eval-harness "one command reproduces the leaderboard" trust standard.
**Rationale:** Reproducibility is a scored rubric category; one green table buys trust in 60 seconds, and a single metrics source prevents every downstream surface from drifting.
**Downsides:** ~1-1.5h build; must wrap existing scripts and capture live outputs; metrics.json needs a render step for README.
**Confidence:** 90%
**Complexity:** Medium
**Status:** Unexplored

### 2. spot_check.py --mpn + why_blank.py — interrogable evidence probe
**Description:** `spot_check.py --mpn <X>` prints the raw input row, every emitted value, and the exact evidence substring each value traced to (replaying the dual-pass gate) plus the abstention class for blanks. `why_blank.py <csv> <row> <col>` replays the pipeline for one cell and prints which of the 4 refusal classes fired and the evidence that led there.
**Warrant:** `direct:` README.md:6 "every emitted value traces to source text" is the core claim with no queryable surface; verification is otherwise inspectable only inside pipeline code.
**Rationale:** "Evidence vs assumption" is a scored dimension; converts a 30-min audit into a 30-second command and answers the exact rows a skeptic attacks first (blanks).
**Downsides:** Must replay pipeline logic per-row (moderate wiring); keep read-only.
**Confidence:** 85%
**Complexity:** Low-Medium
**Status:** Unexplored

### 3. demo.html — static offline row explorer, cell-to-evidence + abstention annotations
**Description:** Self-contained HTML embedding the 50-row demo input+export: search an MPN, click a row, see raw input text → emitted values side-by-side, blanks annotated with their refusal class. Opens in any browser offline, zero install. Extends `export_rules_map.py` pattern.
**Warrant:** `direct:` README.md:33 disavows app.py as legacy with no replacement frontend; the only interactive artifact is the internal rules_map.html.
**Rationale:** Gives the 5-8-min judge a hands-on surface that works offline; abstention annotations make blanks read as rigor, not failure — the differentiator made visible.
**Downsides:** ~1-2h; must be genuinely static (no CDN) per offline constraint.
**Confidence:** 85%
**Complexity:** Medium
**Status:** Unexplored

### 4. Freeze hygiene: check_freeze.py + clean tree
**Description:** `check_freeze.py` asserts `git diff 38db2af HEAD -- unihack_catalog/` is empty and prints a freeze-status certificate; `.gitignore` additions (`.gauntlet_results.pkl`, clutter) so `git status` is clean-or-intentional. Optional CUSTODY.md evidence-log narrative.
**Warrant:** `direct:` git status shows `M scripts/.gauntlet_results.pkl` (post-freeze modified evidence = "retroactive tuning" optics), untracked `.agents/`, `graphify-out/`, `skills-lock.json`, and 2 post-freeze commits that don't self-label as docs-only.
**Rationale:** The freeze is the submission's integrity claim; judges check git history and post-award AI-slop audits scan the same surface. One command converts a suspicion trigger into a proof point.
**Downsides:** None meaningful; pure hygiene.
**Confidence:** 90%
**Complexity:** Low
**Status:** Unexplored

### 5. DISCLOSURE.md + corrections box
**Description:** Precise LLM-usage disclosure: where LLMs were used (evidence-gated proposal layer only) vs not (verification gate, taxonomy, extractors, export logic), with the `ELIO_ASSISTED=0` vs `=1` replay proof. Plus a pre-published corrections box stating the 130/130 → 118/118 relationship plainly.
**Warrant:** `direct:` commit 229ba70 says "llm-assisted long-tail enrichment" while FREEZE.md rule 5 forbids calling the proposal layer LLM-assisted — a contradiction between history and framing is exactly what post-award AI audits catch. Disclosure is mandatory and scored (NYU, WeMakeDevs).
**Rationale:** Converts disclosure from a defensive footnote into a designed declaration; the pre-published correction turns a found defect into proof of honesty discipline.
**Downsides:** None meaningful.
**Confidence:** 90%
**Complexity:** Low
**Status:** Unexplored

### 6. Red-team dossier — "how we tried to break it"
**Description:** One page documenting documented attacks (duplicate rows, corrupt brands, contradictory specs, adversarial receipts), what the pipeline did, what slipped through (dpf 0, 589/589, blind critic 17-1), and what remains untested, stated plainly. Includes a snapshot of the blind-critic prompt + all judgments for judge re-run.
**Warrant:** `external:` OpenAI adversarial-evals writeup + model-card "limitations" sections are the credibility standard; Zheng et al. LLM-as-judge methodology; all numbers already measured in-repo.
**Rationale:** Rather than assert honesty, expose the pipeline to documented attack; re-runnable evaluation is more persuasive than re-runnable pipeline and preempts slop scrutiny.
**Downsides:** Small; needs packaging + critic prompt snapshot.
**Confidence:** 80%
**Complexity:** Low-Medium
**Status:** Unexplored

### 7. PITCH.md — judge one-pager
**Description:** A single-page narrative: what Elio does, headline numbers (from metrics.json), bar progression (0.21 → 1.368 → 2.13 → 2.156 attrs/row), freeze discipline, and the mandated disclosure phrasing verbatim. Includes a 30-second card: one reproduce command + four verdict lines.
**Warrant:** `direct:` gauntlet-progress.md is a 273-line engineering log — the wrong shape for a 5-8 min judge read; no judge-shaped doc exists.
**Rationale:** The one artifact designed for the judge's actual read time; sets the narrative once so every copied surface inherits it.
**Downsides:** Writing discipline only; must be tied to metrics.json to avoid drift.
**Confidence:** 85%
**Complexity:** Low
**Status:** Unexplored

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Silent demo screencast | Video budget already fixed; demo.html covers interactivity cheaper |
| 2 | Boss-fight tutorial demo | Gimmick; 1h for a 20s beat; demo.html already interactive |
| 3 | CONSORT flow diagram | Overlaps verify_everything table; extra doc burden |
| 4 | Honest-ceiling 10M-row page | No measured data; scaling not scored; risks undermining |
| 5 | Summit plan (turn-around time) | Internal planning, not judge-facing; below subject floor |
| 6 | Pre-flight checklist | Duplicates verify_everything + PITCH |
| 7 | Nutrition-label disclosure block | Duplicates DISCLOSURE + metrics.json |
| 8 | Sample-6 audit workpaper trace | Duplicates demo.html/spot_check |
| 9 | Evidence-chain appendix | Duplicates demo.html; depth beyond judge budget |
| 10 | Refusal tradeoff plot | Presentation choice; folds into PITCH |
| 11 | Refusal gallery standalone | Folds into demo.html annotations |
| 12 | Subtraction-only (ship fewer things) | Hygiene covered by survivor 4 |
| 13 | Blind-critic standalone publish | Folds into red-team dossier |
| 14 | Claims manifest table | Folds into verify_everything |
| 15 | Strip-root + MANIFEST.txt | Folds into survivor 4 |
| 16 | Judge's Brief mega-HTML | Folds into one-pager + demo.html |
| 17 | Cross-platform reproduce runner | Folded into verify_everything requirement (single cross-platform python runner) |