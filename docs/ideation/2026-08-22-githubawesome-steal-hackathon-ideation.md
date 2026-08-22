---
date: 2026-08-22
topic: githubawesome-steal-hackathon
focus: mine 200 GithubAwesome transcripts (308k words) for best GitHub projects to steal to win UniHack hackathon — 200 videos artifacts/githubawesome/transcripts.csv + txt
mode: repo-grounded
---

# Ideation: Steal From GithubAwesome To Win UniHack

## Grounding Context

**Codebase context:**
- Shape: Python 9-stage DAG `unihack_catalog/stages.py:1` frozen `38db2af` → `EnrichedRecord` + 252-col export via `_canonical_252_headers()` (utf-8-sig, Excel `®`), verification is executable truth `scripts/verify_everything.py:1` (12 gates → `artifacts/metrics.json` + `artifacts/acceptance_table.md`). Frontend: Next.js 16.3 `elio-frontend/` App Router, single-file cockpit `app/dashboard/page.tsx:1` (double-nested `app/app` is route grouping, chunk A ends `// __CHUNK_A_END__`), Design System `DESIGN.md` "The Ledger" (paper/zinc, blue #2563eb interaction, green #22c55e verified, amber #f59e0b review, mono for data, flat-by-default).
- Patterns: Freeze contract `docs/FREEZE.md:9` + dual-pass gate (every emitted value must appear verbatim in source text or literal `value+uom`, blanks are 4 abstention classes with reason, never guesses) + hash-linked receipts `run_store.py` + claim ledger `models.py:ClaimRecord/SourceEvidence(url,quote,sha256)/MethodLineage/ReviewAudit`. Derived `graphify-out/` + `artifacts/` never hand-edit; `scripts/.gauntlet_results.pkl` untracked cache purged before seed-7 holdout.
- Pain/gaps: `unihack_catalog/` edits require Bar 5 + full acceptance rerun; cockpit single-file maintainability cap `PLAN.md:8`; no pytest/jest — only `verify_everything.py`/`verification_ledger.py` (6 UAT cases); Windows utf-8-sig/BOM + CRLF gotchas; `tmp/` + `.next` noise; win bar is live provenance `118/118 gold, 589/589 adversarial, 0 dual-pass fails, 2.156 attrs/row, gauntlet 6/7 wins` (P7 export syndication is honest loss: single CSV vs Salsify network, picker preview only).
- Likely leverage: (a) pipeline accuracy/provenance before touching frozen DAG (ingestion + verification UX), (b) dashboard trust/freshness (ledger/receipt/replay, evidence drawer, per-cell highlight), (c) verification story (12-gate + gauntlet + critic), (d) frontend polish (React motion/micro-interactions) without breaking frozen DAG.

**Transcript corpus context (200/200 fetched 2026-08-22, 308k words, avg 1540/video, files `artifacts/githubawesome/transcripts.csv` + `transcripts.jsonl` + `txt/*.txt` + `.en.vtt` + `fetch.log` 99.5% coverage via `yt-dlp player_client=android`):**
- Buckets from keyword scan: `agent 2522, MCP 268, RAG 386, dashboard 265, markdown 309, OCR 95, schema 63, self-hosted 347, offline 103, trace 84, eval 112, provenance 7, PDF 251, crawl 28, verif 148, ledger 6, knowledge graph 19, vector 88, embedding 50, chat 305, stream 273`.
- Sample episode 15 (29 projects): Tiny PDF (400 lines, 3.3KB, zero-deps PDF), Conductor (Gemini CLI extension, context-driven), Quen image layered (RGBA layers), OIM (Mac Vim bindings), Lightron (4D parallelism <1k LOC), History LLMs, Fuzzy Canary (anti-scraping), Nitrogen (pixel→gamepad BC), Claudebar (menu-bar quota), GitHub U Log, Tailwind SQL, GSD, Poof (non-blocking rm), Coverflow Finder, GitStory, DVGT (3D point maps), Particulate (3D articulation), Design OS, Ludas Fast MCP (157 tools), Jellyfin Bazaar, Keden, World Canvas, Just J HTML, Gaziteer (offline reverse geocode), Video→robot, Mac Persistence Checker, LLM Tradebot, Luminina, plus 170 other videos' trending projects.

**Past learnings:**
- `docs/solutions/` does not exist (zero files). Reuse ELIO provenance ledger pattern `models.py:ClaimRecord` as warrant for per-transcript lineage (sha16/word_count) — already noted in `docs/ideation/2026-08-22-githubawesome-transcripts-ideation.md:21`.
- Win condition is live accuracy with provenance: judges run their own upload via self-scoring harness (R1-R3) — stolen ideas must raise measured `metrics.json` provenance live, not demo theater.

**External context (mid-2026 trending, proxy webresearch):**
- Ingestion: `microsoft/markitdown` + `DS4SD/docling` + `Unstructured-IO/unstructured` (datasheet→markdown before extraction; your SourceEvidence is text-only, datasheets are PDF/image).
- Optimization: `DSPy-ai/dspy` / `jxnl/instructor` / `dottxt-ai/outlines` (constrained decoding + bootstrapped optimizers vs hand-tuned `category_extractors.py`; auto-optimize prompts with eval sets).
- Live grounding: `Firecrawl/firecrawl` + `unclecode/crawl4ai` + `exa-labs/exa` (live web grounding for brand/MFG verification beyond frozen `reference_loader.py`).
- Trace: `langfuse/langfuse` / `Arize-ai/phoenix` / `comet-ml/opik` (span-level trace waterfall: per-value lineage, judge-clickable).
- Graph: `microsoft/graphrag` / `anomalyco/cognee` (MPN-Brand-Category KG for long-tail where 252 export is sparse).
- Streaming: `vercel/ai` + `CopilotKit/CopilotKit` (streaming reason+evidence chat-over-table vs static cockpit).
- Eval: `promptfoo/promptfoo` / `confident-ai/deepeval` / `evidentlyai/evidently` (eval harness generating `metrics.json` judges trust live; you have 12 gates but not adversarial live eval).
- Market signal: Hackathon wins in 2026 = live hostile input + visible abstention, not 95% claim; provenance > coverage; MCP servers dominant — judges expect `MCP tool: run_pipeline` + citations, not just CSV download.

## Ranked Ideas

### 1. Provenance Waterfall Drawer (per-cell trace)
**Description:** Steal `Arize Phoenix / Langfuse / Opik` span-level trace waterfall. For every enriched cell in the 252-col export, render an expandable drawer in `app/dashboard/page.tsx` showing `ClaimRecord/SourceEvidence + MethodLineage` — verbatim source snippet `value+uom`, extractor name (`category_extractors.py` line), dual-pass pass/fail, confidence, and abstention reason. Backed by `scripts/build_decision_log.py → artifacts/decision_log.jsonl` + `artifacts/evidence.json`. Zero `unihack_catalog/` edit; pure frontend + existing artifact wiring.
**Warrant:** `external:` `phoenix/langfuse/opik` — dominant span-level trace waterfall for LLM decisions mid-2026 (`trace 84, eval 112` mentions in corpus, trending top 20); maps 1:1 to ELIO's `MethodLineage`. `direct:` `models.py:88` defines `SourceEvidence(url,quote,sha256)` + `verification_ledger.py:1` 6 UAT cases but no UI.
**Rationale:** Bar is `118/118 gold, 589/589 adversarial, 0 dual-pass` — judges currently see aggregates (`2.156 attrs/row`) but cannot audit a single claim live; waterfall converts trust from number to inspectable warrant, the exact dimension hackathon rubric scores as innovation+accuracy.
**Downsides:** Trace UI over 252k cells (252×1000) needs virtualization; large evidence payload may bloat `decision_log.jsonl`.
**Confidence:** 90%
**Complexity:** Low-Medium
**Status:** Unexplored

### 2. Highlight-To-Prove — LangExtract Verbatim Map
**Description:** Ship source-anchored highlight map: every filled value must appear verbatim char-span in `Part_Desc` (or literal `value+uom` unit conversion), rendered as yellow highlight in original text inside drawer. Steal `google/langextract` pattern (every extraction grounded, traceable, auditable, highlight & verify each field in context + controlled generation schema). Toggle shows dual-pass gate literally rejecting non-verbatim values. Pure frontend highlight + `stages.py` span already emitted.
**Warrant:** `external:` `LangExtract` (`yrqyYO0XIp4` transcript pattern: highlight & verify each field in context) + `direct:` dual-pass gate `docs/FREEZE.md:9` already implements this but hides it; corpus shows `provenance 7` hits — judges haven't seen pattern pitched as headline.
**Rationale:** Turns abstract `0 dual-pass fails` into visceral 5-second demo: judge clicks any cell → sees it lit up in source. Memory-shots beat metrics tables for ≥85% live claim.
**Downsides:** Mixed-unit tape and image-only `Part_Desc` legitimately have no span — must show honest blank with reason (4 classes) or highlight fails.
**Confidence:** 85%
**Complexity:** Low
**Status:** Unexplored

### 3. Upload Doctor & Healing Preview (markitdown/docling/Tiny PDF)
**Description:** Steal `microsoft/markitdown` / `DS4SD/docling` / `Unstructured` PDF→markdown + `Tiny PDF` (episode 15: 400 lines, 3.3KB, zero-deps) minimal preview. `api/run/route.ts` validates `Mfg_Part_Num,Part_Desc,Part_Manuf,E1_Brand,Unilog_Brand,DIB_Brand` with fallback `MPN,Description,Manufacturer`, hashes to `tmp/input_<id>.csv` via SHA-256 and silently fails on `utf-8-sig \ufeff`, truncated `Part_Desc` like `IB7AIPO`, wrong encodings. Add pre-run healing console: column-mapping diff, `utf-8-sig` fix preview, row-level cryptic-desc warnings, PDF/datasheet markdown extraction preview before `run_pipeline(raw_row)`.
**Warrant:** `external:` `markitdown/docling/Unstructured` — `PDF 251, markdown 309` mentions across 200 transcripts = most requested ingestion pattern. `direct:` `AGENTS.md` notes `encoding="utf-8-sig"` + `\ufeff` stripping; `app/dashboard/page.tsx` already does `FormData(file) → tmp/` but has no doctor.
**Rationale:** Distributor friction is top of funnel — if `Part_Desc` truncated before DAG, 9-stage accuracy capped regardless of extractor quality; healing preview raises effective accuracy before pipeline and is the only place to win on PDF datasheets competitors ignore.
**Downsides:** Adds PDF/image parsing scope (OCR stub today); title regex for series `Hacker News Show #` brittle if channel renames.
**Confidence:** 85%
**Complexity:** Low-Medium
**Status:** Unexplored

### 4. Abstention Triage Queue (Evidently/promptfoo)
**Description:** Steal `evidentlyai/evidently` / `promptfoo/promptfoo` eval triage. Single-file cockpit currently flat-renders 252 cols × 1000 rows = 252k cells. Add `Review` queue panel in `app/dashboard/page.tsx` grouped by 4 allowed abstention classes, sorted by enrichment-yield impact, with mono snippet, source evidence, and bulk Approve/Abstain/Edit + `Cmd+K` palette (from `Conductor/Ludas Fast MCP` pattern `MCP 268, dashboard 265`). Backed by `artifacts/evidence.json`. Zero pipeline edit.
**Warrant:** `direct:` `docs/FREEZE.md:9` "Four abstention classes are the only allowed blanks" + `stages.py:_canonical_252_headers()` 252 contract makes flat scan impossible. `external:` `Evidently/promptfoo` — standard triage for eval failures mid-2026.
**Rationale:** Operator pain is throughput, not intelligence: finding 20 ambiguous Brand conflicts in 252k cells. Prioritized queue turns 90s verification into minutes-saved triage and directly raises shipped `attrs/row` without violating freeze.
**Downsides:** Queue grouping heuristics need tuning; bulk actions risk approving false positives if operator rushes.
**Confidence:** 85%
**Complexity:** Medium
**Status:** Unexplored

### 5. DSPy Regex Workbench (with dual-pass guard)
**Description:** Steal `DSPy-ai/dspy` / `jxnl/instructor` / `dottxt-ai/outlines` constrained decoding. Ship `scripts/dspy_optimizer.py` + dashboard `Lab` tab: propose/compile regex, test against `118 gold + 589 adversarial` live in browser, show `0 dual-pass fails` guard, export candidate patch for future Bar 5 only if `gauntlet 6/7 → 7/7`. Developers hand-tune `category_extractors.py` today with only `verify_everything.py (~90s)` feedback. Wrap frozen extractors as DSPy programs where Phoenix trace is reward (provenance pass/fail, not LLM judge).
**Warrant:** `direct:` `unihack_catalog/stages.py` frozen `38db2af` — `docs/FREEZE.md` forbids `unihack_catalog/` edits without Bar 5. `external:` `DSPy/instructor` — mid-2026 standard is auto-optimizing prompts with eval sets, not hand-regex; 308k words of transcripts = few-shot bank.
**Rationale:** Freezes accuracy at `2.156 attrs/row` if tuning stays manual; workbench proves `+0.1 attrs/row` with provably `0 dual-pass` regressions as verification artifact before unfreezing — turns future Bar 5 from risky PR into measured artifact.
**Downsides:** DSPy optimization needs `gold set` held-out discipline; optimizer itself adds `dspy-ai` dep and Prompt tuning complexity.
**Confidence:** 78%
**Complexity:** Medium
**Status:** Unexplored

### 6. Static Offline Explorer (GitAll/Gander — no backend)
**Description:** Generate `artifacts/explorer.html` self-contained static explorer (like existing `demo.html` / `rules_map.html` pattern already in repo) — search box over `transcripts.csv` + `metrics.json` via client-side Fuse.js, series filter, click row → side-by-side transcript + evidence with repo links highlighted and timestamp jump to `?t=` anchor. Opens offline double-click, zero `npm run dev`, shareable via USB stick. Ship `artifacts/githubawesome/explorer.html` using same static-artifact distribution constraint.
**Warrant:** `direct:` repo already ships `demo.html` (1MB static explorer) and `rules_map.html` as zero-backend surfaces per `README.md:43`. `external:` `GitAll (v0DqrkkW13w: static site from repo, no DB)` + `Gander (e6hcbgyuZAw: no internet permission, lockdown webview)` + `Dory (ZotwULorjwI: shared VM 122MB)` — all win by removing backend dependence; 5–10% videos lack captions — static handles offline fallback.
**Rationale:** Judges skim 60s; `npx next dev` failure = loss. Static artifact survives air-gapped judging and demonstrates the transcript corpus (308k words) is not vapor — it's browsable evidence, mirroring ELIO's provenance story.
**Downsides:** Client-side search over 850k words needs indexing; large HTML payload (~2–3MB) needs pagination; not live-updating.
**Confidence:** 80%
**Complexity:** Medium
**Status:** Unexplored

### 7. Brand Conflict Graph Resolver (GraphRAG + Firecrawl live verify)
**Description:** Steal `microsoft/graphrag` / `cognee` MPN-Brand-Category KG + `Firecrawl/firecrawl` / `exa-labs/exa` live verification. Pain: `E1_Brand vs Unilog_Brand vs DIB_Brand` conflicts via `reference_loader.py` cause abstentions; `rules_map.html` is static. Build `scripts/kg_brand_resolver.py` (MPN-brand-category edges) + dashboard graph view to resolve conflicts interactively and launch `exa` live brand check as `SourceEvidence`, feeding `ClaimRecord` provenance. Raises `attrs/row` at data layer without touching frozen extractors.
**Warrant:** `reasoned:` Brand is highest-cardinality noisy input (3 brand columns + `Part_Manuf`) — without entity resolution, dual-pass gate must abstain (correct per freeze) leaving yield stuck at 2.156; `external:` `graphrag/cognee` is first-principles fix for alias resolution, `Firecrawl/exa` provides live warrant beyond frozen `reference_loader.py`. `direct:` corpus `knowledge graph 19, crawl 28` + brand columns documented in `api/run/route.ts`.
**Rationale:** Raises `attrs/row` without violating freeze — resolves abstention at graph layer and upgrades trust from "frozen rules said so" to "live web verifies brand → provenance link" — the only honest path to beat long-tail where 252 export is sparse.
**Downsides:** KG needs maintenance; live Firecrawl adds latency + API cost and risks rate-limit during demo; requires caching via `tmp/` SHA-256 already in route.
**Confidence:** 75%
**Complexity:** Medium
**Status:** Unexplored

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Pure browser DOM scrape via extension for transcripts | Too vague/brittle — yt-dlp subtitle endpoint is maintained API, dominates corpus |
| 2 | Always-paid API (Apify 437 credits, no local fallback) | Too expensive — 90% achievable at $0 via yt-dlp hybrid ladder, econ violation |
| 3 | Download full MP4s then Whisper everything | Duplicates stronger idea 5 hybrid ladder; wastes bandwidth |
| 4 | Transcript-Optional Pipeline (remove transcripts) | Not grounded — transcripts are separate artifact, not pipeline input; not actionable for win |
| 5 | Delete category_extractors.py entirely (synthesized) | Duplicates stronger 5 DSPy Workbench; too expensive vs measured Bar 5 |
| 6 | Kill 252-Column Export (narrow table only) | Subject-replacement — abandons `_canonical_252_headers()` contract; breaks `acceptance_table.md` |
| 7 | Span-Locked Dual Pass (type invariant) | Interesting but better as brainstorm variant for type-system hardening, not product improvement |
| 8 | No-Cockpit Operations (exception-only cron) | Too expensive — judges need cockpit to see trust; removes demo surface |
| 9 | Self-Bootstrapping References (auto-bootstrap) | Duplicates stronger 7 Graph Resolver + 4a Flywheel; risks dual-pass silently drifting |
| 10 | Steal-to-PR Robot (ELIO_ASSISTED auto-PR) | Already covered — `ELIO_ASSISTED=1` proposal layer exists for `regen_exports.py` |
| 11 | Blank Is The Product (reframe hero metric) | Duplicates stronger 1 Waterfall + 4 Triage; merged into those |
| 12 | Receipt Chain Waggle+Honker | Duplicates stronger 1 Waterfall / CT Log; signage without UI |
| 13 | Pipeline That Writes Itself (OpenSpace) | Duplicates stronger 5 DSPy Workbench; needs SQLite infra |
| 14 | Start From Render (Frontman inverse) | Duplicates stronger 3 Upload Doctor + 6 Offline Explorer |
| 15 | Provenance Gold Flywheel (contribute verified record) | Too expensive relative to hackathon win — needs 10k runs to compound; better as roadmap |
| 16 | DSPy-Compiled Extractor Weaver (duplicate) | Duplicates stronger 5 DSPy Workbench |
| 17 | 252-Column Plugin SDK | Too expensive — requires community/external teams before win |
| 18 | Verification Ledger as Service | Duplicates stronger incremental gauntlet runner; already covered by 12 gates |
| 19 | GraphRAG Over Transcript (broad) | Duplicates stronger 7 Brand Graph (narrow, actionable) |
| 20 | Embeddable Trust Badge | Interesting but better as brainstorm variant for distribution, not accuracy win |
| 21 | Immune Self/Non-Self analogy | Too vague — analogy not actionable steal; brainstorm variant |
| 22 | Speedrun Anti-Cheat TAS | Too vague — theatre without ship artifact |
| 23 | Certificate Transparency Log | Duplicates 1 Waterfall; CT is implementation of same trace |
| 24 | Renaissance Cartography | Too vague — justifies blanks but doesn't ship feature |
| 25 | Double-Entry Bookkeeping | Too vague — audit metaphor without code |
| 26 | Forensic Chain-of-Custody | Duplicates 1 Waterfall |
| 27 | Shazam Fingerprinting | Duplicates 5 Zero-LLM deterministic flex |
| 28 | ELIO Zero $0 WASM inference | Too expensive — WASM compilation + model download heavy for hackathon |
| 29 | ELIO Swarm 100 Specialists | Too expensive — 100 agents infra + merge complexity vs single DAG |
| 30 | ELIO Ghost Zero Human | Duplicates 8 No-Cockpit; removes judge-visible surface |
| 31 | ELIO Instant 150ms distilled | Too expensive — distillation latency tradeoff not judged; not in rubric |
| 32 | ELIO 5 Ultra-Narrow Perfect 5 | Subject-replacement — abandons 252-col contract judges grade |
| 33 | ELIO Dream Synthetic Fill (hallucinate) | Not grounded — violates dual-pass invariant (blanks are 4 classes, never guesses) |
| 34 | ELIO Headless Pure MCP | Too expensive — kills frontend; judges grade cockpit quality |
| 35 | Incremental Gauntlet Runner (parallel gates) | Duplicates 5 DSPy lab's incremental runner; merged |
| 36 | Command Palette + Bulk Triage | Duplicates 4 Triage Queue; merged as palette detail |
| 37 | Blank-as-feature (already) | Duplicates 1 + 4 |
