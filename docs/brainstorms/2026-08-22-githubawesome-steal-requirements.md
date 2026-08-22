---
date: 2026-08-22
topic: githubawesome-steal-hackathon
---

# GithubAwesome Steal Program — 7 Provenance & Trust Wins for UniHack

## Problem Frame

UniHack judges grade 40% on accuracy and 40% on verifiable quality — not marketing claims. ELIO holds `118/118 gold, 589/589 adversarial, 0 dual-pass fails, 2.156 attrs/row` and gauntlet `6/7` (P7 export syndication is honest single-CSV loss) via a frozen 9-stage DAG `38db2af` with 252-col `utf-8-sig` contract. The win is executable truth (`verify_everything.py` 12 gates), but the cockpit still shows aggregates not audit. Distributors upload cryptic `Mfg_Part_Num/Part_Desc/Part_Manuf + 3 Brand` rows; operators review 252k cells (252×1000) flat; brand noise forces honest abstention. Mining 200 GithubAwesome transcripts (308k words, `agent 2522, MCP 268, RAG 386, dashboard 265, markdown 309, PDF 251`) surfaces stealable open-source patterns that turn accuracy from number to inspectable proof — the only durable hackathon moat.

---

## Actors

- A1. Judge / evaluator: runs own upload, needs to see ≥85% provenance live in <90s, audits random cells.
- A2. Distributor operator: uploads cryptic CSV/PDF, triages Review queue, ships export.
- A3. Developer / maintainer: tunes `category_extractors.py` under freeze without breaking `0 dual-pass fails`.
- A4. Pipeline (9-stage DAG): deterministic extractor + dual-pass gate + 12-gate verifier.

---

## Key Flows

- F1. Judge provenance drill-down
  - **Trigger:** Judge clicks any verified cell in dashboard/export.
  - **Actors:** A1, A4
  - **Steps:** Click cell → drawer waterfall opens (1) verbatim `SourceEvidence` quote + char-span, (2) `MethodLineage` extractor name, (3) dual-pass verdict, (4) hash-linked receipt. Yellow highlight shows exact span in `Part_Desc`; hover shows `value+uom` conversion when applicable.
  - **Outcome:** Judge sees verbatim proof in <1s, trusts ≥85% claim without reading `metrics.json`.
  - **Covered by:** R1, R2, R3

- F2. Distributor upload healing
  - **Trigger:** A2 drops CSV/PDF in cockpit.
  - **Actors:** A2, A4
  - **Steps:** Doctor parses via `markitdown` → shows column mapping diff, `utf-8-sig`/BOM fix preview, truncated `Part_Desc` warnings, PDF markdown extraction preview → A2 confirms → `run_pipeline(raw_row)` → triage queue.
  - **Outcome:** Truncated/encoded rows never enter DAG; effective accuracy rises before pipeline.
  - **Covered by:** R4, R5

- F3. Operator triage & approval
  - **Trigger:** Pipeline emits Review cells (4 abstention classes).
  - **Actors:** A2, A4
  - **Steps:** Queue groups Review by abstention class, sorted by yield impact → A2 bulk Approves/Edits via `Cmd+K` → evidence promotes to `artifacts/evidence.json` → holdout metrics recompute.
  - **Outcome:** Operator clears 100 amber rows in <10min, shipped `attrs/row` rises without hallucinating.
  - **Covered by:** R6, R7

- F4. Developer lab optimization (Bar 5 guard)
  - **Trigger:** A3 proposes regex/prompt change in Lab tab.
  - **Actors:** A3, A4
  - **Steps:** Propose → run against `118 gold + 589 adversarial` inside Lab → dual-pass guard blocks if `>0 fails` → export candidate patch only if `gauntlet 7/7` + `metrics.json` improves.
  - **Outcome:** Future Bar 5 is measured artifact, not risky PR.
  - **Covered by:** R8, R9

---

## Requirements

**Provenance waterfall & highlight (steals: Phoenix/Langfuse/Opik + LangExtract — Highlight #1)**

- R1. Cockpit drawer must show per-cell waterfall: `SourceEvidence` verbatim quote + char-span, `MethodLineage` extractor id, dual-pass verdict (pass/fail + reason), SHA-256 receipt, and confidence — for every filled cell in `Cockpit drawer only` (not explorer/export).
- R2. Every filled cell must render yellow highlight at exact char-span in original `Part_Desc` (or `value+uom` literal conversion span). Highlight is verbatim source, not reconstructed text.
- R3. Abstention cells must show both: yellow for proven values, red dashed for attempted-but-rejected spans, plus 4-class reason in plain English (`pendant row / dual-platform charger / mixed-unit tape / gold-blessed`) — `Show both` mode.

**Upload healing (steals: markitdown/docling/Unstructured + Tiny PDF)**

- R4. Upload Doctor must preview before `run_pipeline`: column mapping diff (expected `Mfg_Part_Num,Part_Desc,Part_Manuf,E1_Brand,Unilog_Brand,DIB_Brand` vs actual), `utf-8-sig`/BOM fix, truncated `Part_Desc` detection (e.g., `IB7AIPO`), encoding issues — with Apply/Cancel.
- R5. PDF/datasheet ingestion via `markitdown`-style markdown extraction must be previewable as source text span before it enters dual-pass, without weakening the gate (blank with reason if image-only).

**Review triage (steals: Evidently/promptfoo + Conductor palette)**

- R6. Review queue must group Review cells by 4 abstention classes, sorted by enrichment-yield impact, showing mono snippet + source evidence, with bulk Approve/Edit and undo.
- R7. `Cmd+K` palette must allow keyboard triage of Review queue (`j/k, x, Shift+A` bulk) inside single-file cockpit, no new dep beyond already-installed frontend stack.

**DSPy Lab (steals: DSPy/instructor/outlines)**

- R8. Lab tab must allow A3 to propose regex/prompt changes and test live against `118 gold + 589 adversarial` + `gauntlet_holdout_eval.py` holdout, showing `0 dual-pass fails` guard inline — all client-side before any `unihack_catalog/` edit.
- R9. Lab must export candidate patch artifact only when gates pass and `metrics.json` provenance ≥ current; patch does not auto-apply (Bar 5 still requires human PR + full `verify_everything.py --full`).

**Offline explorer (steals: GitAll / Gander)**

- R10. `artifacts/explorer.html` static offline explorer (Fuse.js, no backend) must be generated: search over `transcripts.csv` + `metrics.json` + `evidence.json`, series filter, side-by-side transcript + evidence — opens via double-click, no `npm run dev`, `utf-8-sig` for Excel `®`.

**Brand graph resolver (steals: GraphRAG/cognee + Firecrawl/exa)**

- R11. Brand resolver must build MPN-Brand-Category KG from `reference_loader.py` + `graph.json` and surface graph path in dashboard for `E1_Brand/Unilog_Brand/DIB_Brand` conflicts.
- R12. Live brand verification via `Firecrawl`/`exa` must be opt-in (env key), cached via `tmp/` SHA-256 (existing `api/run/route.ts` pattern), and fed as `SourceEvidence` — abstention remains if offline/unreachable (never hallucinate brand).

---

## Acceptance Examples

- AE1. **Covers R1, R2.** Given a verified `Minimum Height` cell, when Judge clicks it, waterfall shows verbatim quote + char-span and yellow highlight appears exactly over `5 1/2"` in `Part_Desc` with extractor `category_extractors.py:ExtractHeight` and `dual-pass: pass`.
- AE2. **Covers R3.** Given a mixed-unit tape `Part_Desc` that is blank, when Operator opens it, drawer shows no yellow highlight but red dashed attempted span + reason `mixed-unit tape — honest blank (class 3)` and `SourceEvidence` of attempted match.
- AE3. **Covers R4.** Given CSV with header `MPN,Description,Manufacturer` and `\ufeffMfg_Part_Num` BOM, when Distributor drops file, Doctor shows mapping `MPN → Mfg_Part_Num` etc. and `utf-8-sig fix: removed \ufeff`, preview before pipeline.
- AE4. **Covers R6, R7.** Given 100 Review rows (amber `#f59e0b`), when Operator presses `Cmd+K` then `j, x, Shift+A`, 50 rows bulk-approve and queue count drops, undo restores.
- AE5. **Covers R8, R9.** Given proposed regex change, when Lab runs `118 gold + 589 adversarial`, gate shows `0 dual-pass fails, 118/118, 589/589, holdout 2.156 → 2.21 attrs/row`, patch export enables; if `1 dual-pass fail`, export stays disabled.
- AE6. **Covers R10.** Given air-gapped laptop, when double-clicking `artifacts/explorer.html`, search for `Hacker News Show #10` loads transcript + evidence without network.
- AE7. **Covers R11, R12.** Given row where `E1_Brand=GE, Unilog_Brand=GE Appliances`, when resolver runs, graph shows `GE → GE Appliances` edge + live `exa` source snippet as `ClaimRecord`, or `abstain (offline)` if no key.

---

## Success Criteria

- Judge can audit any random filled cell to verbatim source highlight in <2s and trusts ≥85% live provenance without reading `metrics.json`.
- Distributor self-corrects truncated/encoded upload via Doctor preview without emailing operator; 5k-row CSV enters pipeline clean.
- Operator clears 100 amber rows in <10min via grouped triage + keyboard, and shipped `attrs/row` rises without new abstention violations.
- Developer proposes extractor change in Lab with measured `0 dual-pass fails` artifact; planning never invents Bar 5 behavior — this doc is the handoff to `/ce-plan`.

---

## Scope Boundaries

- No edits to `unihack_catalog/` (stages, extractors, reference_loader) beyond proposal artifacts — Bar 5 requires full `verify_everything.py --full` rerun; Lab and graph are proposal/evidence layers.
- No new backend service or cron — Doctor, Lab, Explorer, Graph are frontend (`elio-frontend/`) or `scripts/` + `artifacts/` static surfaces; live Firecrawl is opt-in cache-only.
- No hallucinated brand/datasheet values — dual-pass verbatim-or-abstain invariant holds (4 classes); synthetic fill is out of scope.
- No breaking of single-file cockpit contract `PLAN.md:8` — chunks B-E append pattern stays; no monorepo tooling, no new deps beyond DSPy/Fuse.js/markitdown (justify per addition).
- No ranking of 200 transcripts as product — transcripts remain `artifacts/githubawesome/` evidence corpus; mining is for steal ideas, not for shipping transcript search as primary product.

---

## Key Decisions

- Highlight scope: `Cockpit drawer only` — fastest win; explorer/export highlight deferred to fast-follow (explicitly not in R10).
- Abstention display: `Show both` (yellow proven + red dashed attempted) — makes dual-pass pedagogy visible, per judge feedback.
- Unit conversion highlight: original text span with tooltip for `value+uom` conversion (LFG default: `Converted span + original` middle path) — provenance is verbatim source, conversion is derived.
- LFG on remaining 6: apply sensible defaults (Doctor = markitdown preview, Triage = grouped + palette, Lab = guard-blocked patch export, Explorer = static Fuse.js, Graph = KG view + opt-in live verify) — avoids further brainstorm dilution.
- All 7 as one program: ship as single release `githubawesome-steal` program; `/ce-plan` will slice into vertical leaves.

---

## Dependencies / Assumptions

- `artifacts/githubawesome/transcripts.csv` 200/200 + `.en.vtt` + `txt/*.txt` remain frozen corpus for steal lineage (sha16).
- `verify_everything.py` 12 gates + `metrics.json` remain executable truth; Lab reuses `clean_room_evaluator.py` + `gauntlet_holdout_eval.py` with cache purge discipline.
- `DESIGN.md` "Ledger" palette (`#0a0a0d` glow, `#22c55e` verified, `#f59e0b` review) governs highlight/drawer styling.
- Firecrawl/exa keys are optional env; offline demo must still pass via abstention path.

---

## Outstanding Questions

### Resolve Before Planning

- None — LFG defaults cover open decisions; planning can proceed.

### Deferred to Planning

- Affects R8 [Technical] Which DSPy optimizer (bootstrap few-shot vs COPRO) minimizes `gold` overfit while keeping `0 dual-pass`?
- Affects R10 [Needs research] Fuse.js index size for 308k words (~2–3MB HTML) — pagination vs worker?
- Affects R12 [Technical] Firecrawl cache invalidation policy in `tmp/` (TTL vs SHA-256 only)?

---

## Next Steps

-> /ce-plan for structured implementation planning — slice 7 steals into vertical leaves (waterfall + highlight first, as ranked #1 by user), each with goal-backward verification against `verify_everything.py` gates.

