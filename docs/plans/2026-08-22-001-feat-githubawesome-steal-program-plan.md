---
title: "feat: GithubAwesome Steal Program — 7 Provenance & Trust Wins"
type: feat
status: active
date: 2026-08-22
origin: docs/brainstorms/2026-08-22-githubawesome-steal-requirements.md
---

# feat: GithubAwesome Steal Program — 7 Provenance & Trust Wins

## Overview

Ship the 7 stealable patterns mined from 200 GithubAwesome transcripts (308k words) as a single `githubawesome-steal` program that turns Bar-4's aggregate accuracy (118/118 gold, 589/589 adversarial @ 100% precision, 0 dual-pass fails, 2.156 attrs/row) into inspectable, triageable, judge-trustable provenance — without a single byte change under `unihack_catalog/` at `38db2af` (bar-4-freeze). All steals are proposal/evidence layers in `elio-frontend/` or `scripts/` + `artifacts/` static surfaces. The ranked #1 win is **Highlight-To-Prove** (verbatim yellow span + red-dashed attempted span in the custody drawer); the remaining 6 are sliced as vertical, shippable leaves that each read the single canonical evidence object. Frontend surfaces follow the High-Agency baseline `8,6,4` (DESIGN_VARIANCE 8 / MOTION 6 / VISUAL_DENSITY 4) — asymmetric bento, airy gallery spacing, spring-physics micro-interactions — reconciled with the Ledger palette (`#0a0a0d` glow, `#22c55e` verified, `#f59e0b` review, `#2563eb` interaction, mono for data).

---

## Problem Frame

Bar 4 is technically hardened but the cockpit still shows aggregates, not audit. A judge who clicks a verified cell cannot see *why* it is verified without reading `metrics.json`; a distributor who uploads a 5k-row CSV with a BOM or truncated `Part_Desc` (`IB7AIPO`) fails inside the DAG with no preview; an operator who must scan 252k cells (252×1000) cannot prioritize the 4 honest abstention classes; a developer who hand-tunes `category_extractors.py` has only `verify_everything.py (~90s)` as feedback and no guard that `0 dual-pass fails` holds. The 200-transcript corpus proves the market pattern: hackathon wins grade live provenance over coverage claims, and the stealable fix is to steal trace (Phoenix/Langfuse/Opik), highlight (LangExtract), doctor (markitdown/docling/Tiny PDF 3.3KB), triage (Evidently/promptfoo/Conductor palette), workbench (DSPy/instructor), offline explorer (GitAll/Gander Fuse.js), and live-brand graph (GraphRAG/cognee + Firecrawl/exa) — each as a thin, evidence-gated layer that makes accuracy inspectable in <2s. (see origin: docs/brainstorms/2026-08-22-githubawesome-steal-requirements.md Problem Frame)

---

## Requirements Trace

- R1. Cockpit drawer must show per-cell waterfall: `SourceEvidence` verbatim quote + char-span, `MethodLineage` extractor id, dual-pass verdict, SHA-256 receipt, confidence — Cockpit drawer only
- R2. Every filled cell must render yellow highlight at exact char-span in original `Part_Desc` (or `value+uom` literal conversion span) — verbatim source, not reconstructed text
- R3. Abstention cells must show both: yellow for proven values, red dashed for attempted-but-rejected spans, plus 4-class reason in plain English — Show both mode
- R4. Upload Doctor must preview before `run_pipeline`: column mapping diff (expected `Mfg_Part_Num,Part_Desc,Part_Manuf,E1_Brand,Unilog_Brand,DIB_Brand` vs actual), `utf-8-sig`/BOM fix, truncated `Part_Desc` detection, encoding issues — with Apply/Cancel
- R5. PDF/datasheet ingestion via `markitdown`-style markdown extraction must be previewable as source text span before it enters dual-pass, without weakening the gate (blank with reason if image-only)
- R6. Review queue must group Review cells by 4 abstention classes, sorted by enrichment-yield impact, showing mono snippet + source evidence, with bulk Approve/Edit and undo
- R7. `Cmd+K` palette must allow keyboard triage of Review queue (`j/k, x, Shift+A` bulk) inside single-file cockpit, no new dep beyond already-installed frontend stack
- R8. Lab tab must allow A3 to propose regex/prompt changes and test live against `118 gold + 589 adversarial` + `gauntlet_holdout_eval.py` holdout, showing `0 dual-pass fails` guard inline — all client-side before any `unihack_catalog/` edit
- R9. Lab must export candidate patch artifact only when gates pass and `metrics.json` provenance ≥ current; patch does not auto-apply (Bar 5 still requires human PR + full `verify_everything.py --full`)
- R10. `artifacts/explorer.html` static offline explorer (Fuse.js, no backend) must be generated: search over `transcripts.csv` + `metrics.json` + `evidence.json`, series filter, side-by-side transcript + evidence — opens via double-click, no `npm run dev`, `utf-8-sig` for Excel `®`
- R11. Brand resolver must build MPN-Brand-Category KG from `reference_loader.py` + `graph.json` and surface graph path in dashboard for `E1_Brand/Unilog_Brand/DIB_Brand` conflicts
- R12. Live brand verification via `Firecrawl`/`exa` must be opt-in (env key), cached via `tmp/` SHA-256 (existing `api/run/route.ts` pattern), and fed as `SourceEvidence` — abstention remains if offline/unreachable

**Origin actors:** A1 Judge/evaluator, A2 Distributor operator, A3 Developer/maintainer, A4 Pipeline 9-stage DAG
**Origin flows:** F1 Judge provenance drill-down (covers R1-R3), F2 Distributor upload healing (covers R4-R5), F3 Operator triage & approval (covers R6-R7), F4 Developer lab optimization (covers R8-R9)
**Origin acceptance examples:** AE1 (covers R1,R2 — verified Minimum Height waterfall + yellow `5 1/2"`), AE2 (covers R3 — mixed-unit tape red dashed + reason class 3), AE3 (covers R4 — `MPN→Mfg_Part_Num` + `\ufeff` fix preview), AE4 (covers R6,R7 — `Cmd+K` `j/x/Shift+A` bulk 50 rows), AE5 (covers R8,R9 — Lab `0 dpf, 118/118, 589/589, 2.156→2.21` gate + patch export guard), AE6 (covers R10 — air-gapped `explorer.html` search), AE7 (covers R11,R12 — `GE→GE Appliances` graph + `exa` or abstain)

---

## Scope Boundaries

- No edits to `unihack_catalog/` (stages, extractors, reference_loader) beyond proposal artifacts — Bar 5 requires full `verify_everything.py --full` rerun; Lab and Graph are proposal/evidence layers only
- No new backend service or cron — Doctor, Lab, Explorer, Graph are `elio-frontend/` or `scripts/` + `artifacts/` static surfaces; live Firecrawl is opt-in cache-only via `tmp/` SHA-256
- No hallucinated brand/datasheet values — dual-pass verbatim-or-abstain invariant holds (4 classes); synthetic fill is out of scope
- No breaking of single-file cockpit contract `PLAN.md:8` — chunks B-E append pattern stays; no monorepo tooling, no new deps beyond `dspy-ai` (Python) + `fuse.js` (vendored JS) + `markitdown` (Python, via `requirements.txt`/`scripts/requirements-doctor.txt`, not `elio-frontend/package.json`) — each justified per addition
- No ranking of 200 transcripts as product — transcripts remain `artifacts/githubawesome/` evidence corpus; mining is for steal lineage, not for shipping transcript search as primary product
- No new 252-col rendering — evidence-bearing columns first with reveal-remaining affordance; 252k-cell virtualization is fast-follow outside this plan
- No design-system fork — all surfaces reconcile High-Agency baseline `8,6,4` with existing Ledger palette/mono/flat rules; lime landing artifact does not propagate without decision

### Deferred to Follow-Up Work

- Explorer/export highlight (outside drawer): deferred fast-follow after cockpit-drawer highlight proves span correctness
- 252k-cell virtualization for full flat scan: deferred (current queue/Explorer scope to filtered subsets)
- Transcript ranking as primary product surface: deferred — corpus stays evidence lineage
- Generalization evaluation ticket #8 (post-freeze holdout): separate tracked work, not part of this program

---

## Context & Research

### Relevant Code and Patterns

- `unihack_catalog/stages.py:1` 9-stage DAG `run_pipeline(raw_row) -> (EnrichedRecord, flat_252)` frozen `38db2af`; `unihack_catalog/models.py:44-122` `SourceEvidence{url,quote,sha256,char_span,hop_chain}` + `MethodLineage{model,extractor,pass_number}` + `ClaimRecord` + `EnrichedRecord.claims[]`; `unihack_catalog/category_extractors.py` + `unihack_catalog/reference_loader.py` longest-match taxonomy + `BRAND_VOCAB` + `TAXONOMY_KEYWORDS` word-boundaried; `unihack_catalog/verification_ledger.py` 6 UAT cases; `scripts/verify_everything.py:132-299` 12 gates -> `artifacts/metrics.json` + `artifacts/acceptance_table.md`; `scripts/build_evidence.py` -> `artifacts/evidence.json{freeze_commit,rows[row_order],rows[mpn]{accepted[evidence{snippet,char_span,kind}],abstained[reason]}}`; `scripts/build_decision_log.py` -> `artifacts/decision_log.jsonl` + `--replay`; `scripts/build_demo_html.py` `TEMPLATE %DATA%` offline inject with `no http://` invariant; `scripts/verify_manifest.py` + `submission_manifest.json` SHA256; `scripts/check_freeze.py` allowlist `verification_ledger.py`; `docs/FREEZE.md:9` freeze contract + dual-pass gate + 4 abstention classes
- `elio-frontend/src/app/app/dashboard/page.tsx:1` single-file cockpit (chunk A ends `// __CHUNK_A_END__`, chunks B-E appended), `VerifyChip:188` + `DecisionPill:166` + Custody Drawer `287-507` with GSAP `power4.out`, dual-pane (Confidence/URL/Page/Char Span left + `<span class='provenance-span'>` yellow highlight right), `reviewRecords:475`, `abstentionTypes:481`, `abstainedRecords:491`, `handleDecisionStatus:396` + `localStorage elio_overrides:342-354`, `ITEMS_PER_PAGE:69`, `handleFileUpload:403` + `handleExportCSV` formula-injection `'/^[=+\-@]/ -> ' +'`, `api/run/route.ts:10-93` `FormData(file) -> tmp/input_<id>.csv` SHA-256 -> `scripts/run_pipeline_cli.py` child_process; `elio-frontend/src/app/layout.tsx:5-13` `Geist` + `Geist_Mono`; `elio-frontend/src/app/globals.css:8-26` Ledger tokens `--accent-brand #2563eb` / `--accent-green #22c55e` / `--accent-amber #f59e0b` + `@import "tailwindcss"` v4
- `artifacts/githubawesome/transcripts.csv` 200 rows sha16 + `txt/*.txt` + `.en.vtt` frozen corpus; `artifacts/metrics.json` canonical 118/118 gold, 589/589 adversarial, 0 dpf, 2.156 attrs/row; prior plan `docs/plans/2026-08-20-002-feat-judge-proof-submission-plan.md` 10 units established canonical evidence object + metrics.json source + offline invariant

### Institutional Learnings

- `docs/solutions/` does not exist (verified absent) — this program is first compound-worthy work; capture with `/ce-compound` after landing the dual-pass char-span highlight nuance (`2x2 -> 2 ft x 2 ft` normalization) and `evidence.json as single source`
- Judge-proof submission surface plan established: one canonical `evidence.json` never re-extracted, `metrics.json` generated not hardcoded (kills 130/130 vs 118/118 drift), offline HTML via `%DATA%` inject with `no http://` test, `verify_everything.py` is truth, `check_freeze.py` asserts `git diff 38db2af HEAD -- unihack_catalog/` empty (allowlist `verification_ledger.py`)

### External References

- Phoenix / Langfuse / Opik — span-level trace waterfall pattern (per-value lineage, judge-clickable)
- google/langextract — highlight & verify each field in context + controlled generation schema (verbatim char-span)
- microsoft/markitdown + DS4SD/docling + Unstructured + Tiny PDF (400 lines, 3.3KB, zero-deps) — PDF->markdown minimal preview
- evidentlyai/evidently + promptfoo/promptfoo + Conductor/Ludas Fast MCP — eval triage + palette
- DSPy-ai/dspy + jxnl/instructor + dottxt-ai/outlines — constrained decoding + BootstrapFewShot optimizer
- GitAll/Gander — static offline site from repo, no DB (explorer.html lineage)
- microsoft/graphrag + anomalyco/cognee + Firecrawl/firecrawl + exa-labs/exa — MPN-Brand-Category KG + live verification as SourceEvidence
- High-Agency Frontend Skill v1 baseline `8,6,4` + Ledger `DESIGN.md` — asymmetric bento, spring physics, airy gallery spacing

---

## Key Technical Decisions

- **Evidence is read, not re-derived** (R1-R3): drawer waterfall + highlight consume canonical `artifacts/evidence.json` (`rows[mpn]{accepted[evidence{text,char_span,kind}, verification, export_column], abstained[reason]}`) plus `EnrichedRecord.claims[]` (`SourceEvidence{url,quote,sha256,char_span,hop_chain}` + `MethodLineage{extractor}` + confidence) read via `/data/demo_results.json` + `evidence.json` — never re-run extraction in the frontend. Verbatim `char_span` highlight prefers `Part_Desc` span when present; otherwise surfaces workbook snippet span (evidence `kind: workbook`) with explicit "source: workbook, not Part_Desc" label. `value+uom` conversion shows original span + tooltip (origin LFG: Converted span + original middle path)
- **Cockpit drawer only for highlight** (scope): explorer/export highlight deferred fast-follow — fastest win is extending the existing Custody Drawer (already dual-pane + `provenance-span`) to waterfall + dual-color, avoiding 252k virtualization in this cut
- **Upload Doctor is preview, not mutation** (R4-R5): Doctor runs before `handleFileUpload -> /api/run -> run_pipeline` but renders **only when a diff is detected** (header mismatch, BOM, truncated rows, or PDF); clean CSVs auto-apply with a one-line `utf-8-sig fix: removed \ufeff` toast, no extra click. When shown, it diffs `headers` vs required `Mfg_Part_Num,Part_Desc,Part_Manuf,E1_Brand,Unilog_Brand,DIB_Brand` + fallback `MPN,Description,Manufacturer`, strips `\ufeff` (`utf-8-sig`), flags truncated `IB7AIPO`-class `Part_Desc` via heuristic (`raw length < 12 and no verifiable attribute span` — threshold to be validated on 50-row sample), previews PDF->markdown char-span without weakening `stage_verification`; Apply/Cancel is the gate — pipeline is never fed raw truncated rows
- **markitdown as doctor's PDF engine** (R5): `microsoft/markitdown` (Python dep, `requirements.txt`/`scripts/requirements-doctor.txt`) is the justify-per-addition dep — minimal, markdown-char_span preserving, matches Tiny PDF zero-deps philosophy (3.3KB episode-15 reference). `docling/Unstructured` are heavier fallbacks only if markitdown misses image-only tables; OCR remains stubbed (blank with reason). Not added to `elio-frontend/package.json` (JS deps are `fuse.js` only)
- **Triage groups by 4-class yield impact** (R6): queue groups `abstainedRecords` by `QualityDecision.review_reasons` / `FREEZE.md:17-19` (pendant / dual-platform / mixed-unit / gold-blessed) sorted by `attrs/row` lift; bulk Approve/Edit writes `localStorage elio_overrides` (existing pattern `342-354`) and recomputes `metrics.json`-displayed yield — no hallucination, just promotion of evidence-backed edits
- **`Cmd+K` palette is in-file, zero new dep** (R7): `j/k` nav, `x` toggle, `Shift+A` bulk — uses existing `lucide-react` + GSAP, respects `globals.css:84` `prefers-reduced-motion`, stays inside chunk contract `PLAN.md:8`
- **DSPy Lab is proposal-only, guard-blocked** (R8-R9): Lab tab adds `lab` to cockpit enum, client proposes regex/prompt, server reuses `clean_room_evaluator.py` + `gauntlet_holdout_eval.py` (purge `scripts/.gauntlet_results.pkl` first) + `adversarial_eval.py`; gate shows `0 dual-pass fails, 118/118, 589/589, holdout 2.156 -> X` inline; export patch enables only if `gauntlet 7/7` + `provenance >= current`; patch does NOT auto-apply — Bar 5 PR still requires `verify_everything.py --full`
- **DSPy optimizer: BootstrapFewShot over COPRO** (deferred R8 resolved): BFS minimizes gold overfit on 118-row gold set by bootstrapping from Phoenix traces as reward (provenance pass/fail, not LLM judge); COPRO's prompt-rewriting is too aggressive for dual-pass verbatim constraint
- **Explorer.html is vendored Fuse.js, not CDN** (R10): clone `scripts/build_demo_html.py` -> `scripts/build_explorer.py` -> `artifacts/explorer.html`; `fuse.js` vendored into the HTML bundle (no `https://`, SRI-checked), `utf-8-sig` write for `®`, search over `transcripts.csv + metrics.json + evidence.json` with series filter, paginated 50 hits (not worker) for 308k words (~2-3MB budget) — keeps offline `file://` invariant greppable (`no http://`). Implementer measures bundle; if >3MB split to `artifacts/explorer/` with shared vendored `fuse.js`


- **Brand Graph is KG view + opt-in live verify, cached SHA-256 only** (R11-R12): build KG from `reference_loader.py` + `graphify-out/graph.json` via `scripts/kg_brand_resolver.py` (MPN-brand-category edges, longest-match), surface `E1/Unilog/DIB` conflict path in dashboard; live `exa`/`Firecrawl` is opt-in env key, cached `tmp/live_brand/<sha256>.json` (isolated from `tmp/input_<id>.csv` which is deleted post-run; live cache excluded from `verify_manifest.py` hashing), emitted as `ClaimRecord/SourceEvidence` (domain-allowlisted to `mfr_url` domains only) or `abstain (offline)` — never hallucinates; cache invalidation is SHA-256 only (no TTL) for reproducibility, env key absent -> abstention path exercised in demo
- **High-Agency 8,6,4 reconciled with Ledger** (design): DESIGN_VARIANCE 8 -> landing uses asymmetric bento (split hero, masonry where data allows, massive empty zones); cockpit keeps asymmetric `2fr 1fr` **data-density exception** to `DESIGN.md` (middle band `2fr 1fr` for Evidence/Pipeline legibility) but otherwise flat-by-default, no boxed bento grid in queue/explorer (uses `border-t`/`divide-y` per Ledger). MOTION 6 -> fluid `cubic-bezier(0.16,1,0.3,1)` + premium spring `stiffness 100 damping 20`, `layout`/`layoutId` on drawer/queue reorders, `staggerChildren` capped at 100ms (no infinite loops in data rows), JS-guarded by `prefers-reduced-motion` (in addition to `globals.css:78`); VISUAL_DENSITY 4 -> gallery airy on landing, **dense on cockpit** (triage/explorer rows): cards `rounded-[2.5rem]` `p-8`/`p-10` only on landing shell, data rows use `rounded-[10px]` ledger cards + generous section gaps, mono only for numbers/MPN/hash/span — resolves prior `c8d84a` vs `2563eb` variance by using Ledger `#2563eb` interaction. Semantic: Verified `#22c55e` solid yellow? No — highlight uses `f59e0b` amber tint `bg-amber-500/15` solid for proven, **amber dashed** `border-amber-500/50 border-dashed` for attempted (not red — red is reject/error per `DESIGN.md`); lime `c8d84a` stays landing-only.



---

## Open Questions

### Resolved During Planning

- Which DSPy optimizer minimizes gold overfit while keeping `0 dual-pass`? BootstrapFewShot (reward = provenance pass/fail from Phoenix trace), not COPRO — lower overfit on 118 gold rows, respects verbatim constraint
- Fuse.js index size for 308k words (~2-3MB HTML) — pagination vs worker? Pagination 50 hits, no worker — simpler, keeps HTML under budget, deterministic offline
- Firecrawl cache invalidation policy in `tmp/` (TTL vs SHA-256 only)? SHA-256 only, no TTL — reproducibility trumps freshness; manual purge is the invalidation
- Highlight scope and abstention display? Cockpit drawer only + Show both (amber solid proven `bg-amber-500/15` + amber dashed attempted `border-amber-500/50`) per origin LFG — explorer/export deferred; red reserved for reject/error per Ledger
- Value+uom conversion highlight? Original span + tooltip (middle path) — provenance is verbatim source, conversion is derived

### Deferred to Implementation

- Exact Fuse.js vendor version and chunk split threshold if explorer.html exceeds 3MB on real transcripts — implementer measures during `build_explorer.py` and splits to `artifacts/explorer/` if needed
- Tiny PDF 3.3KB as fallback for markitdown on specific PDF layouts — measure markitdown hit rate on the 50-row doctor sample first; add only if needed
- GraphRAG vs cognee KG builder for MPN-Brand-Category edges — implementer prototypes both against `reference_loader.py` BRAND_VOCAB on 50 rows and picks the one that preserves longest-match + word-boundary invariants

---

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

```
artifacts/evidence.json (canonical, from build_evidence.py) + /data/demo_results.json (EnrichedRecord.claims[])
  |  per-cell {mpn, attribute, value, uom, evidence{text,char_span,kind}, verification, export_column} + ClaimRecord{SourceEvidence+MethodLineage+confidence}
  |
  +--> elio-frontend/src/app/app/dashboard/page.tsx (single-file, chunk B-E)
  |      Cockpit Drawer (R1-R3): extend existing Custody Drawer
  |        left pane: Confidence / URL / Page / Char Span / SHA receipt / dual-pass verdict / extractor id (from claims[] when available, else evidence.json)
  |        right pane: Part_Desc with amber <span class='provenance-span'> at char_span (verbatim) + amber dashed attempted + tooltip value+uom; fallback workbook snippet when Part_Desc span absent
  |      Upload Doctor (R4-R5): conditional pre-handleFileUpload preview — header diff + utf-8-sig fix + truncated flag + PDF markdown span — Apply/Cancel -> /api/run; clean files auto-apply
  |      Triage Queue (R6-R7): group abstainedRecords by 4 classes, sorted by yield, bulk Approve/Edit -> localStorage elio_overrides -> metrics recompute
  |      Cmd+K palette: j/k, x, Shift+A, palette overlay, GSAP spring, JS-guarded prefers-reduced-motion
  |      Lab tab (R8-R9): propose regex/prompt -> reuse clean_room_evaluator + gauntlet_holdout_eval + adversarial_eval -> guard 0 dpf -> patch artifact
  |      Brand Graph view (R11): KG path for E1/Unilog/DIB conflicts, opt-in exa/Firecrawl -> allowlisted SourceEvidence or abstain
  |      High-Agency 8,6,4: landing bento; cockpit 2fr 1fr data exception (border-t/divide-y, not bento grid), spring 100/20 + cubic-bezier(0.16,1,0.3,1), stagger 100ms
  |
  +--> scripts/build_explorer.py -> artifacts/explorer.html (R10)
  |      OFFLINE: %DATA% inject (no CDN, no http://), Fuse.js vendored, utf-8-sig, double-click file://
  |      data: transcripts.csv + metrics.json + evidence.json, series filter, paginated 50, side-by-side transcript + evidence (split to artifacts/explorer/ if >3MB)
  |
  +--> scripts/kg_brand_resolver.py + tmp/live_brand/<sha256>.json cache (R11-R12, excluded from manifest hash)
  |      KG from reference_loader.py + graphify-out/graph.json, longest-match, word-boundaried
  |      live exa/Firecrawl opt-in env key -> domain-allowlisted SourceEvidence or abstain(offline), SHA-256 only (no TTL)
  |
  +--> scripts/verify_everything.py (12 gates -> 15 after) + scripts/verify_manifest.py + submission_manifest.json
         add: explorer.html, kg artifacts, lab patch guard to gates; metrics.json stays canonical (regenerate to clear 38/118 drift)

All surfaces: no edits to unihack_catalog/ (frozen 38db2af); dual-pass invariant holds; verify_everything remains truth.
```

---

## Implementation Units

- U1. **Provenance Waterfall Drawer + Highlight-To-Prove — cockpit drawer (R1,R2,R3, AE1,AE2)**

**Goal:** Judge clicks any verified cell and in <1s sees verbatim proof: waterfall (quote+char-span, extractor id, dual-pass verdict, SHA receipt, confidence) plus yellow highlight at exact `Part_Desc` span (or original span + `value+uom` tooltip), and for abstained cells red-dashed attempted span + 4-class plain-English reason — Show both, Cockpit drawer only.

**Requirements:** R1, R2, R3 (covers F1, AE1, AE2)

**Dependencies:** None (reads canonical `artifacts/evidence.json` + `artifacts/decision_log.jsonl`; no pipeline edit)

**Files:**
- Modify: `elio-frontend/src/app/app/dashboard/page.tsx` (extend Custody Drawer `287-507`; add waterfall pane + `provenance-span` yellow + `attempted-span` red dashed + `value+uom` tooltip)
- Modify: `elio-frontend/src/app/globals.css` (highlight tokens: `--provenance-yellow`, `--attempted-red-dashed`, tooltip motion)
- Create: `scripts/build_decision_log.py` (if not present — emits per-value waterfall data as `decision_log.jsonl` — or extend existing)
- Modify: `artifacts/evidence.json` (ensure per-cell `method{extractor}` + `receipt{sha256}` + dual-pass verdict surfaced; `scripts/build_evidence.py` already canonical)
- Test: `scripts/verify_everything.py` (add gate: every accepted evidence has non-empty char_span + snippet)

**Approach:**
- Extend the existing dual-pane drawer (already Confidence/URL/Page/Char Span + `provenance-span` right pane) to render `ClaimRecord.method.extractor` (e.g., `category_extractors.py:ExtractHeight`), dual-pass `supported|not_found` verdict, SHA-256 receipt, and confidence. Right pane overlays yellow on `Part_Desc` at `char_span` (verbatim, not reconstructed); abstained cells render both yellow proven spans and red-dashed attempted spans with 4-class reason (`pendant row / dual-platform charger / mixed-unit tape / gold-blessed`) in plain English. Unit conversion cells show original span + tooltip with converted `value+uom` (middle path). Design: asymmetric bento card `rounded-[2.5rem]` `p-8` diffusion shadow, mono for MPN/hash/span, spring `stiffness 100 damping 20` on open, `staggerChildren 100ms` for waterfall rows, respects `prefers-reduced-motion`.

**Patterns to follow:**
- `dashboard/page.tsx:287-507` Custody Drawer + GSAP `power4.out`; `VerifyChip:188`/`DecisionPill:166` semantic colors `#22c55e`/`#f59e0b`; `models.py:44-122` evidence lineage; `demo.html:87` `WHY?` toggle; `DESIGN.md` Ledger + High-Agency 8,6,4 (airy gallery, asymmetric, spring physics)

**Test scenarios:**
- Happy path: Covers AE1 — click verified `Minimum Height` for PDSH4816AF -> waterfall shows verbatim quote + char-span, yellow highlight exactly over `5 1/2"` in `Part_Desc`, extractor `category_extractors.py:ExtractHeight`, `dual-pass: pass`, SHA receipt present — completes in <1s (Covers F1/AE1)
- Happy path: abstained `Diameter` on mixed-unit tape row -> no yellow; red dashed attempted span + reason `mixed-unit tape — honest blank (class 3)` + attempted `SourceEvidence` (Covers AE2)
- Happy path: `value+uom` conversion (e.g., `2x2` -> `2 ft x 2 ft` ceiling-tile) -> original `2x2` span highlighted + tooltip `2 ft x 2 ft` (not reconstructed text)
- Edge case: `Part_Desc` with no verbatim span (gold-blessed blank) -> waterfall shows `abstained` + reason, no highlight — never fabricates span
- Edge case: `prefers-reduced-motion` enabled -> drawer opens without spring/stagger, no animation
- Integration: Every accepted cell's evidence round-trips through `artifacts/evidence.json` and drawer highlight without re-extraction in frontend

**Verification:**
- All 3 acceptance examples for this unit (AE1/AE2 + conversion tooltip) pass; `verify_everything.py` gate confirms every accepted evidence has char_span + snippet; manual drawer open <1s on desktop + mobile fallback single-column

---

- U2. **Upload Doctor & Healing Preview — pre-pipeline (R4,R5, AE3)**

**Goal:** Distributor drops a 5k-row CSV/PDF and before any `run_pipeline` call sees a healing console: column mapping diff, `utf-8-sig` BOM fix, truncated `Part_Desc` warnings, encoding issues, and PDF markdown extraction preview — with Apply/Cancel — so truncated/encoded rows never enter the DAG.

**Requirements:** R4, R5 (covers F2, AE3)

**Dependencies:** None (pre-`handleFileUpload`; independent of U1)

**Files:**
- Modify: `elio-frontend/src/app/app/dashboard/page.tsx` (add Doctor preview layer before `handleFileUpload:403` -> `/api/run`; state `doctorPreview{headerDiff,bomFix,truncatedRows,encodingIssues,pdfMarkdown}`)
- Modify: `elio-frontend/src/app/api/run/route.ts` (keep 6-col contract `Mfg_Part_Num,Part_Desc,Part_Manuf,E1_Brand,Unilog_Brand,DIB_Brand` + fallback `MPN,Description,Manufacturer:28-38`; add Doctor validation hook `validateHeaders` + BOM strip)
- Create: `scripts/doctor_preview.py` (optional helper — header diff + BOM detection + truncation heuristic)
- Modify: `elio-frontend/package.json` (add `markitdown` dep — justify: markdown char-span preview without weakening dual-pass; Tiny PDF 400-line reference as minimal alternative; docling/unstructured are deferred fallbacks)
- Test: `elio-frontend/src/app/app/dashboard/page.test.tsx` (new) or `scripts/doctor_preview.test.py` if helper script route

**Approach:**
- Doctor parses `File` via `TextDecoder utf-8-sig` (strip `\ufeff`), diffs `headers` vs required 6 cols + fallback, detects truncated `Part_Desc` (e.g., `IB7AIPO` class — heuristic: no verbatim extractable attribute + suspicious short length), flags encoding issues, and for PDF/datasheet runs `markitdown` -> markdown char_span preview. Preview shows mapping `MPN -> Mfg_Part_Num` etc., `utf-8-sig fix: removed \ufeff`, per-row warnings. PDF extraction is previewable as source text span; if image-only, gate stays blank with reason (dual-pass never weakened). Apply writes healed CSV to `tmp/input_<id>.csv` SHA-256 and proceeds to `/api/run`; Cancel aborts. Design: airy card `rounded-[2.5rem]` `p-8`, asymmetric `2fr 1fr` (preview left, diff right), mono for headers/hashes.

**Patterns to follow:**
- `api/run/route.ts:10-93` FormData->tmp SHA-256->child_process->cleanup; `handleFileUpload:403`; `build_evidence.py:54` `utf-8-sig`; `AGENTS.md` BOM/CRLF gotcha; Tiny PDF zero-deps philosophy

**Test scenarios:**
- Happy path: Covers AE3 — drop CSV with headers `MPN,Description,Manufacturer` + `\ufeffMfg_Part_Num` BOM -> Doctor shows `MPN -> Mfg_Part_Num` etc. + `utf-8-sig fix: removed \ufeff`, preview before pipeline (Apply proceeds, healed file has no BOM)
- Happy path: PDF datasheet dropped -> markdown extraction preview shows first table as text span; Apply feeds that span as source for dual-pass
- Edge case: truncated `IB7AIPO` `Part_Desc` -> row flagged `truncated — no extractable span (will abstain)`; effective accuracy rises because operator sees it before DAG
- Edge case: 5k-row CSV -> Doctor lists only first 20 truncated rows + count `+ 47 more`; no full 5k render
- Error path: image-only PDF -> preview shows `no text span — image-only (dual-pass will abstain with reason)`; pipeline still fed but correctly blanks
- Integration: healed CSV after Apply produces identical `evidence.json` char_spans as if BOM had never been present

**Verification:**
- AE3 passes; `verify_everything.py` still 0 dpf after Doctor path; 5k-row file enters pipeline clean after Apply; image-only PDF correctly abstains

---

- U3. **Abstention Triage Queue + Cmd+K Palette — operator throughput (R6,R7, AE4)**

**Goal:** Operator clears 100 amber rows in <10min: queue groups Review cells by 4 abstention classes, sorted by enrichment-yield impact, mono snippet + source evidence, bulk Approve/Edit + undo via `Cmd+K` palette (`j/k, x, Shift+A`).

**Requirements:** R6, R7 (covers F3, AE4)

**Dependencies:** U1 (reuses abstention reason taxonomy + evidence wiring)

**Files:**
- Modify: `elio-frontend/src/app/app/dashboard/page.tsx` (extend `reviewRecords:475` + `abstentionTypes:481` + `abstainedRecords:491` — group by 4 classes `FREEZE.md:17-19` + `models.py:QualityDecision.review_reasons`, sorted by yield impact, paginated; add palette overlay + keyboard handlers + `localStorage elio_overrides:342-354` + undo stack)
- Modify: `elio-frontend/src/app/globals.css` (palette `layoutId` spring, `Cmd+K` focus ring, mono queue rows, `prefers-reduced-motion` guard)
- Test: `elio-frontend/src/app/app/dashboard/triage.test.tsx` (new — grouped queue + palette keyboard)

**Approach:**
- Group `abstainedRecords` by 4 classes (pendant rows / dual-platform chargers / mixed-unit tape / gold-blessed blanks from `FREEZE.md:17-19` + `GOLD_BLESSED_COLS` from `build_decision_log.py:20`), compute yield impact = `attrs gained if class resolved`, sort groups descending impact. Each group shows count, mono snippet, source evidence, and per-row checkbox. Palette `Cmd+K` (no new dep — `lucide-react` + GSAP existing) handles `j/k` nav, `x` toggle, `Shift+A` bulk approve, `u` undo. Bulk writes `localStorage elio_overrides`, recomputes displayed `metrics.reviewCount`/`attrs/row` lift. Design: airy list with `border-t`/`divide-y` (not boxed cards) for VISUAL_DENSITY 4, `rounded-[2.5rem]` palette modal, diffusion shadow, spring `100/20`, `staggerChildren` on group reveal.

**Patterns to follow:**
- `dashboard/page.tsx:342-354` localStorage overrides, `396` handleDecisionStatus; `Evidently/promptfoo` triage + `Conductor` palette; `AGENTS.md` cockpit chunk contract; High-Agency airy (no boxed cards for dense queue), mono for data

**Test scenarios:**
- Happy path: Covers AE4 — 100 amber Review rows grouped by 4 classes, sorted by yield impact; `Cmd+K` -> `j, x, Shift+A` bulk-approves 50 rows, queue count drops, `u` undo restores
- Happy path: bulk Edit changes a value -> override stored in `localStorage`, evidence promoted to `evidence.json` shape, holdout metrics recomputed
- Edge case: single-row group -> still shows group header with reason in plain English
- Edge case: `prefers-reduced-motion` -> palette opens without spring
- Integration: bulk Approve writes overrides that survive page reload and `handleExportCSV` includes promoted values (until manifest re-hashes)

**Verification:**
- AE4 passes; 100-row bulk flow <10min manual; grouped queue + palette keyboard all work in single-file cockpit (no new dep), `verify_everything.py` still PASS (triage never writes to `unihack_catalog/`)

---

- U4. **DSPy Regex Workbench (Lab tab) — developer velocity with guard (R8,R9, AE5)**

**Goal:** Developer proposes a regex/prompt change in Lab tab, tests live against `118 gold + 589 adversarial + holdout`, sees `0 dual-pass fails` guard inline, and exports a candidate patch artifact only if `gauntlet 7/7` + `provenance >= current` — patch never auto-applies.

**Requirements:** R8, R9 (covers F4, AE5)

**Dependencies:** U1 (reuses evidence/decision artifacts as ground truth)

**Files:**
- Modify: `elio-frontend/src/app/app/dashboard/page.tsx` (add `lab` to cockpit tab enum `62` — new pane; proposal editor (regex + prompt), live gate run button, guard badge `0 dpf`/`FAIL`, metrics delta `2.156 -> X`, patch export button disabled until `7/7`)
- Create: `scripts/dspy_workbench.py` (or `scripts/dspy_optimizer.py` — DSPy BootstrapFewShot harness wrapping `category_extractors.py` as program, reward = provenance pass/fail from Phoenix trace)
- Create: `scripts/lab_guard.py` (reuses `clean_room_evaluator.py` + `gauntlet_holdout_eval.py` + `adversarial_eval.py` with `scripts/.gauntlet_results.pkl` purge discipline `AGENTS.md:56`)
- Modify: `scripts/verify_everything.py` (add Lab guard gate: Lab patch candidate must be 0 dpf before export)
- Modify: `artifacts/metrics.json` (read-only reference for guard comparison)
- Test: `scripts/lab_guard.test.py` (new — guard blocks on `>0 dpf`, enables on `7/7`)

**Approach:**
- Lab tab: left editor (regex + optional prompt), center live gate output (gold 118/118, adversarial 589/589, holdout attrs/row, dpf), right patch preview (unified diff). Propose -> server invokes `lab_guard.py` which purges `.gauntlet_results.pkl`, runs `clean_room_evaluator` + `gauntlet_holdout_eval` + `adversarial_eval` (deterministic per `FREEZE.md:70`), shows guard inline. DSPy layer (new dep `dspy-ai` justified per addition) wraps frozen extractors as DSPy programs where Phoenix trace is reward (provenance pass/fail, not LLM judge); optimizer is BootstrapFewShot. Export writes `artifacts/lab_patch_<sha>.json` only if `7/7` + `provenance >= current`; Bar 5 PR still requires human + `verify_everything.py --full`.

**Patterns to follow:**
- `verify_everything.py` 12-gate pattern + `FREEZE.md:70` deterministic eval; `PHOENIX/Langfuse` trace as reward; `PLAN.md:8` chunk contract; High-Agency spring on guard badge reveal

**Test scenarios:**
- Happy path: Covers AE5 — propose regex that lifts holdout `2.156 -> 2.21` with `0 dpf, 118/118, 589/589` -> patch export enables, artifact written
- Happy path: BFS optimizer bootstraps from 118 gold traces -> few-shot program passes `7/7` on holdout subset
- Error path: proposed regex causes `1 dual-pass fail` -> guard shows `FAIL: 1 dual-pass fail`, export stays disabled, no artifact
- Edge case: no API key / offline -> Lab still runs deterministic gates (no live LLM needed); patch export still gated by `0 dpf`
- Integration: Lab patch does NOT mutate `unihack_catalog/` until human PR; `verify_everything.py` without patch still ACCEPTED

**Verification:**
- AE5 passes; Lab with `>0 dpf` always blocks export; `7/7` patch artifact only writes when `provenance >= current`; zero `unihack_catalog/` writes from Lab path

---

- U5. **Static Offline Explorer — `artifacts/explorer.html` (R10, AE6)**

**Goal:** Double-click `artifacts/explorer.html` on an air-gapped laptop and search the 200-transcript corpus + `metrics.json` + `evidence.json` (series filter, paginated 50, side-by-side transcript + evidence) with zero `npm run dev`, `utf-8-sig` for Excel `®`.

**Requirements:** R10 (covers AE6)

**Dependencies:** U1 (evidence.json) — reads evidence but otherwise standalone static artifact

**Files:**
- Create: `scripts/build_explorer.py`
- Create: `artifacts/explorer.html` (generated, offline, vendored Fuse.js)
- Modify: `elio-frontend/package.json` (add `fuse.js` devDep — vendored into HTML, not CDN; justify: 308k-word client search, GitAll/Gander lineage)
- Modify: `scripts/verify_everything.py` (add gate: explorer.html exists + `no http://` invariant)
- Modify: `submission_manifest.json` (hash explorer.html)
- Test: `scripts/build_explorer.test.py` (new — offline invariant + search smoke)

**Approach:**
- Clone `scripts/build_demo_html.py:20` `TEMPLATE %DATA%` offline inject (embedded JSON, not CDN — hard constraint: `rules_map.html` uses Vis.js + Google Fonts as anti-pattern; explorer.html must have zero external refs). At build time embed `transcripts.csv` (200 rows sha16) + selected `txt` snippets + `metrics.json` + `evidence.json` (or summary). Vendor `fuse.js` source into the HTML bundle (no `<script src="https://">`). Write with `encoding="utf-8-sig"` for `®`. Search: Fuse over `transcripts.csv` + `metrics.json` + provider labels, series filter, click row -> side-by-side left transcript + right evidence with repo links highlighted and `?t=` timestamp jump. Paginate 50 hits, not worker (308k words ~2-3MB budget). Design: airy gallery `rounded-[2.5rem]` cards, asymmetric `2fr 1fr` (results left, detail right), diffusion shadow, spring on detail reveal.

**Patterns to follow:**
- `build_demo_html.py` offline inject + `no http://` test `193-196`; `export_rules_map.py` static-gen structure; `AGENTS.md` `utf-8-sig`; GitAll/Gander static-offline lineage

**Test scenarios:**
- Happy path: Covers AE6 — air-gapped (network disabled) double-click `artifacts/explorer.html` -> search `Hacker News Show #10` loads transcript + evidence without network
- Happy path: series filter -> results narrow to series; click row -> side-by-side transcript + evidence with repo links, timestamp `?t=` anchor
- Happy path: search `evidence` term -> hits `evidence.json` rows, shows MPN + attribute
- Edge case: query with no hits -> beautiful empty state (High-Agency: not generic spinner) with how-to-populate hint
- Error path: generated HTML contains no `http://`/`https://`/`src=` to external hosts (grep-able invariant) — gate fails if CDN leaked
- Integration: `artifacts/metrics.json` numbers shown in explorer match `verify_everything.py` live values

**Verification:**
- AE6 passes; `explorer.html` opens via `file://` offline and searches; `no http://` holds; search over 308k words paginates under 3MB

---

- U6. **Brand Conflict Graph Resolver — KG + opt-in live verify (R11,R12, AE7)**

**Goal:** Brand conflicts `E1_Brand vs Unilog_Brand vs DIB_Brand` (e.g., `GE` vs `GE Appliances`) show a graph path from MPN-Brand-Category KG and, when env key present, an `exa`/`Firecrawl` live snippet as `SourceEvidence` — or `abstain (offline)` if no key/unreachable — raising `attrs/row` without violating freeze.

**Requirements:** R11, R12 (covers AE7)

**Dependencies:** U1 (evidence wiring) + U5 explorer manifest discipline (shares `graph.json` + `tmp/` cache pattern)

**Files:**
- Create: `scripts/kg_brand_resolver.py` (builds MPN-Brand-Category KG from `unihack_catalog/reference_loader.py` + `graphify-out/graph.json`; longest-match + word-boundaried)
- Create: `scripts/live_brand_verify.py` (opt-in `exa`/`Firecrawl` via env key, `tmp/<sha256>.json` cache, emits `ClaimRecord/SourceEvidence` or abstention)
- Modify: `elio-frontend/src/app/app/dashboard/page.tsx` (dashboard graph view pane for `E1/Unilog/DIB` conflicts — KG path edges `GE -> GE Appliances`, live snippet card or `abstain (offline)` badge)
- Modify: `elio-frontend/src/app/globals.css` (graph edge + verified/offline tokens)
- Test: `scripts/kg_brand_resolver.test.py` (new — longest-match + word-boundary + abstention)

**Approach:**
- KG builder reads `reference_loader.py:BRAND_VOCAB{manufacturer,mfr_url,alias_of}` + `TAXONOMY_KEYWORDS` + `graphify-out/graph.json` (regenerate via `graphify update .` after any reference change — derived, not hand-edited), builds MPN-brand-category edges with longest-match precedence + word-boundary (same invariants as `FREEZE.md` Bar 4 word-boundary fixes). Dashboard graph view surfaces conflict path for `E1_Brand/Unilog_Brand/DIB_Brand` rows. Live layer: `live_brand_verify.py` reads env `EXA_API_KEY`/`FIRECRAWL_KEY`, fetches brand page, caches `tmp/<sha256>.json` (same as `api/run/route.ts:43-55`), emits as `SourceEvidence{url,quote,sha256,char_span}` feeding `ClaimRecord`, or returns `abstain (offline)` if no key/unreachable — dual-pass invariant holds (never hallucinate brand). Cache invalidation: SHA-256 only, no TTL (manual purge is invalidation). Design: graph as asymmetric bento panel `rounded-[2.5rem]`, verified edge `#22c55e`, offline `#f59e0b`, mono for MPN/brand.

**Patterns to follow:**
- `reference_loader.py` longest-match + `BRAND_VOCAB` + word-boundaried taxonomy; `run_store.py` + `research_engine.py` hop_chain; `api/run/route.ts` tmp SHA-256 cache; `graphify-out/` derived; High-Agency airy (graph breathes, not cockpit-packed)

**Test scenarios:**
- Happy path: Covers AE7 — row `E1_Brand=GE, Unilog_Brand=GE Appliances` -> graph shows `GE -> GE Appliances` edge + live `exa` snippet as `ClaimRecord` when key present
- Happy path: `tmp/<sha256>.json` hit -> no network call, snippet served from cache, still `SourceEvidence`
- Edge case: offline / no env key -> shows `abstain (offline)` badge, `attrs/row` not inflated, drawer still shows `abstained` reason — no hallucinated brand
- Edge case: word-boundary trap `fissuRed` vs `Red` -> KG does NOT emit `Red` edge (same fix as Bar 4 `fissuRed` case)
- Error path: live fetch hits 403/timeout -> `attempted SourceEvidence` logged with `pointer_status="unavailable_live"` but `abstain` remains (honest blank)
- Integration: promoted brand resolves via localStorage override raise `attrs/row` without `unihack_catalog/` edit; `verify_everything.py` still 0 dpf

**Verification:**
- AE7 passes in both modes (key present -> snippet, no key -> abstain); word-boundary invariants hold (no `Red` from `fissuRed`); `tmp/` cache SHA-256 only, no hallucinated brand

---

- U7. **Final integration — manifest, gates, walk-test, freeze assertion (program closeout)**

**Goal:** All 7 steals are hashed, gated, and provable in one command; `git status` clean; freeze boundary holds; a fresh agent can clone -> verify -> inspect evidence in <10min.

**Requirements:** R1-R12 (program acceptance); originates walk-test from `docs/plans/2026-08-20-002-feat-judge-proof-submission-plan.md:U9` hygiene

**Dependencies:** U1-U6

**Files:**
- Modify: `scripts/verify_everything.py` (extend 12 gates -> 15: add U1 waterfall char_span gate, U5 offline `no http://` gate, U6 graph abstention gate)
- Modify: `scripts/verify_manifest.py` + `submission_manifest.json` (hash `artifacts/explorer.html`, `artifacts/decision_log.jsonl`, `scripts/kg_brand_resolver.py`, `scripts/dspy_workbench.py`, `tmp/` cache is not hashed)
- Create: `docs/WALK_TEST.md` (update or create — checklist: clone -> `python -B scripts/verify_everything.py` -> `python -B scripts/build_explorer.py` -> open `artifacts/explorer.html` file:// -> audit waterfall highlight -> heal a BOM CSV -> triage 50 rows -> verify manifest)
- Test: `scripts/verify_everything.py` self-check + temp-dir clean-clone walk-test

**Approach:**
- Regenerate artifacts in dependency order (evidence -> explorer -> graph cache), run `verify_manifest.py --update` then `verify_manifest.py` (clean), run `verify_everything.py` (all 15 gates PASS), run check_freeze `git diff 38db2af HEAD -- unihack_catalog/` empty (allowlist `verification_ledger.py`), run walk-test on temp dir clone (air-gapped explorer + BOM heal + bulk triage + waterfall <1s). Commit with labeled commits `feat: steal-<id>` + `docs:` prefix, never amend `38db2af` history.

**Patterns to follow:**
- `docs/FREEZE.md` reproduce block; `docs/plans/2026-08-20-002-feat-judge-proof-submission-plan.md:U10` final integration; commit hygiene from FREEZE rule 6

**Test scenarios:**
- Happy path: clean tree `verify_everything.py` -> `VERDICT: ACCEPTED (ALL 15 GATES PASSED)`, exit 0, `metrics.json` matches `acceptance_table.md`
- Happy path: `verify_manifest.py` all PASS; `check_freeze.py` PASS (allowlist only)
- Happy path: walk-test on temp cloned dir completes in <10min with every checklist item passed (air-gapped explorer + BOM heal + palette bulk + waterfall highlight)
- Edge case: `artifacts/explorer.html` >3MB -> implementer splits to `artifacts/explorer/` chunk per deferred question resolution
- Error path: any gate fails -> fix artifact, not pipeline; re-run — scope boundary holds
- Integration: `git status --porcelain` post-commit empty; zero diffs under `unihack_catalog/` vs `38db2af` beyond allowlist

**Verification:**
- `verify_everything.py` ACCEPTED, `verify_manifest.py` all PASS, `check_freeze.py` PASS, walk-test recorded in `WALK_TEST.md` with date + timing + outcome, zero `unihack_catalog/` diff beyond allowlist

---

## System-Wide Impact

- **Interaction graph:** `verify_everything.py` invokes `verification_ledger.run_ledger_tests()`, `rules_linter`, `adversarial_eval.py`, `gauntlet_holdout_eval.py`, `build_decision_log.py` replay — it is supervisor over existing gates; `build_evidence.py`/`build_explorer.py`/`kg_brand_resolver.py`/`lab_guard.py` are read-only over pipeline outputs; Doctor sits pre-`handleFileUpload` before child_process `run_pipeline`; Triage writes `localStorage elio_overrides` (frontend-only promotion); Lab never writes `unihack_catalog/`
- **Error propagation:** every script follows ledger contract — print `[PASS]/[FAIL]`, exit 0/1; `verify_everything.py` aggregates gate exit codes into one verdict; no gate failure swallowed; Doctor Apply/Cancel is the explicit gate — pipeline never receives raw truncated rows on silent fail
- **State lifecycle risks:** `scripts/.gauntlet_results.pkl` is regenerable cache — gitignored, purge before holdout eval; `tmp/<sha256>.json` live-brand cache is SHA-256 only, manual purge is invalidation, not hashed in manifest; `localStorage elio_overrides` is ephemeral (proposal promotion), not canonical evidence — canonical is `artifacts/evidence.json` regenerated via `build_evidence.py`
- **API surface parity:** no public API/CLI contract changes; 6 FREEZE.md reproduce commands remain valid; `verify_everything.py` supersedes as entry point without removing them; `api/run/route.ts` 6-col contract unchanged (Doctor is pre-validation layer)
- **Integration coverage:** walk-test (U7) is the cross-layer scenario — clone, verify, inspect waterfall highlight, heal BOM CSV, triage 50 rows, open offline explorer, prove abstention — proving all surfaces agree; High-Agency motion respects `prefers-reduced-motion` globally
- **Unchanged invariants:** `unihack_catalog/` byte-identical to `38db2af`; dual-pass verification gate untouched; 4 abstention classes untouched; `FREEZE.md` rule 5 phrasing respected everywhere (`evidence-gated machine-generated proposals`, never `LLM-assisted`); git history unmodified (no rebase/amend); `utf-8-sig` + `\ufeff` handling preserved

---

## Risks & Dependencies

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Lab `dspy-ai` dep inflates install + `0 dpf` still broken by proposed regex | Medium | High | Gate blocks export unless `7/7` + `provenance >= current`; BFS reward is provenance pass/fail, not LLM judge; no auto-apply — human PR + `verify_everything.py --full` required |
| `markitdown` misses a PDF table layout | Medium | Medium | Doctor still shows `no text span — will abstain` (honest blank, not hallucinated); deferred fallback to `docling` only if measured miss rate > threshold on 50-row sample |
| Explorer.html exceeds 3MB (308k words + evidence) | Medium | Low | Pagination 50 hits keeps budget; implementer splits to `artifacts/explorer/` chunk if measured >3MB (deferred question) |
| Live brand verify rate-limited or 403 during demo | High | Low | Opt-in only; offline `abstain (offline)` path is the demo default — abstention remains honest blank, never hallucinated; `tmp/` SHA-256 cache proves prior success |
| High-Agency 8,6,4 motion hurts dense cockpit legibility | Low | Medium | MOTION 6 is fluid CSR only (not `8-10` choreography), VISUAL_DENSITY 4 is gallery airy (cards `p-8` diffusion shadow), palette respects Ledger `#2563eb`/`#22c55e`/`#f59e0b`; `prefers-reduced-motion` guard on every animated surface |
| Single-file cockpit chunk contract broken by 7 steals landing together | Medium | High | All frontend edits are `PLAN.md:8` chunk B-E appends — no file split; each unit patches inside the contract, verified by `check_freeze.py` + `verify_everything.py` |
| `Fuse.js` vendor bloat breaks `no http://` | Low | Medium | Vendor source is inlined, not CDN; gate asserts `no http://`/`https://`/`src=` to external hosts |

---

## Documentation / Operational Notes

- `docs/FREEZE.md` Reproduce section gains `verify_everything.py` 15-gate table (extends 12 -> 15) plus Doctor/Lab/Explorer/Graph commands; `artifacts/acceptance_table.md` remains generated canonical
- `README.md` Verification section rewritten to point at `verify_everything.py` + `artifacts/explorer.html` offline explorer + `docs/DISCLOSURE.md` phrasing (`evidence-gated machine-generated proposals`)
- No deployment, monitoring, or runtime operations — all artifacts static, offline, regenerable via `scripts/`; live exa/Firecrawl is opt-in and never required for gates
- Post-landing `/ce-compound` to capture first `docs/solutions/` entry: `dual-pass char_span highlight` + `evidence.json as single source`

---

## Phased Delivery

### Phase 1 — Provenance as product (U1 + U3 foundation, longest judge leverage)
U1 Waterfall+Highlight + U2 Doctor — judge can audit any cell in <1s and distributor never feeds truncated CSV into DAG; ships the 2 steals with highest rubric leverage first

### Phase 2 — Operator throughput (U3 Triage)
U3 Triage+Palette — 100 amber rows in <10min via grouped queue + `Cmd+K` bulk; reuses U1's abstention taxonomy

### Phase 3 — Developer velocity + offline proof (U4 Lab + U5 Explorer)
U4 Lab (proposal-only, guard-blocked) + U5 Offline Explorer (vendored Fuse.js, air-gapped) — future Bar 5 is measured artifact, transcript corpus is browsable evidence

### Phase 4 — Graph raise + program closeout (U6 + U7)
U6 Brand Graph (KG + opt-in live verify) raises `attrs/row` without freeze violation; U7 Final integration hashes everything, extends gates to 15, runs walk-test, asserts freeze

---

## Sources & References

- **Origin document:** [docs/brainstorms/2026-08-22-githubawesome-steal-requirements.md](docs/brainstorms/2026-08-22-githubawesome-steal-requirements.md)
- Related code: `elio-frontend/src/app/app/dashboard/page.tsx`, `elio-frontend/src/app/api/run/route.ts`, `elio-frontend/src/app/globals.css`, `elio-frontend/src/app/layout.tsx`, `unihack_catalog/models.py`, `unihack_catalog/stages.py`, `unihack_catalog/category_extractors.py`, `unihack_catalog/reference_loader.py`, `scripts/verify_everything.py`, `scripts/build_evidence.py`, `scripts/build_decision_log.py`, `scripts/build_demo_html.py`, `scripts/verify_manifest.py`, `scripts/check_freeze.py`, `docs/FREEZE.md`, `artifacts/metrics.json`, `artifacts/evidence.json`
- Prior plan: [docs/plans/2026-08-20-002-feat-judge-proof-submission-plan.md](docs/plans/2026-08-20-002-feat-judge-proof-submission-plan.md) (10 units, canonical evidence + metrics + offline invariants — reused here)
- External docs: Phoenix/Langfuse/Opik waterfall, google/langextract highlight, microsoft/markitdown, Tiny PDF 3.3KB, Evidently/promptfoo, DSPy/instructor, GitAll/Gander, GraphRAG/cognee, Firecrawl/exa, High-Agency Frontend Skill v1 (8,6,4)
