# PLAN: ELIO Frontend — Judge-Ready Quality Pass

Mission: bring the whole frontend to the quality bar of the approved landing +
dashboard; rebuild cockpit tabs with real data; unify typography; harmonize
colors with the landing's lime family; kill AI slop.

## Contracts (shared surfaces)
- Single cockpit file: `elio-frontend/src/app/app/dashboard/page.tsx`.
  Chunk A (types, helpers, state, handlers, metrics) is WRITTEN and ends with
  marker `// __CHUNK_A_END__`. Every chunk B-E REPLACES that marker with its
  content + the marker again (append-only).
- Components available from chunk A: MiniBarChart, StreamChart, SidebarIcon,
  DecisionPill, VerifyChip, MetricCard (props: label, value, badge1?, badge2?,
  chartColor, bars, gradStart, gradEnd, valueColor?).
- State available: activeTab, datasetSize, demoData/fullData/uploadedData,
  uploading, uploadError, uploadStatus, searchQuery, explorerPage, reviewPage,
  abstentionFilter, drawerIdx/drawerAttr/drawerOpen, decisions, data, metrics,
  getDecision, getAttrValue, handleApplyOverride, handleDecisionStatus,
  handleFileUpload, handleExportCSV, openDrawer, closeDrawer, filteredRecords,
  reviewRecords, abstentionTypes, abstainedRecords, drawerRow, drawerAttrObj,
  drawerDecision, statusBarBars/supportBars/missingBars/escBars.
- Tabs: upload | dashboard | explorer | review | abstention | export.
- Visual rules: dark shell #0a0a0d, cards #141418, border rgba(255,255,255,0.07),
  radius 14px; brand accent = lime #c8d84a (NOT blue); mono = data/numbers only;
  amber = refusal/attention only; teal = accepted, purple = escalated/review,
  red = reject/error; no em dashes, no invented stats.
- Data rules: numbers derive from `data` records (metrics, decisions histograms,
  verification counts); upload via handleFileUpload (FormData → /api/run);
  export via handleExportCSV.

## Leaves
- L1 (lead): Chunk B — render shell: outer bg + grid overlay, sidebar (logo, 6
  nav icons, bar-4-freeze label), main panel, header (TAB_TITLES/TAB_SUBTITLES,
  dataset switcher, Export CSV), body container, upload tab.
- L2 (lead): Chunk C — dashboard tab: 4 MetricCards, Evidence Summary 230px,
  Pipeline Analytics 1fr (StreamChart + real counts + llm/cost), Review Queue
  snapshot 260px, Recent Records table.
- L3 (lead): Chunk D — explorer tab (search, table, pagination, row click) +
  review tab (queue, accept/reject, pagination).
- L4 (lead): Chunk E — abstention tab (dynamic filters, table) + export tab
  (deliverable cards) + custody drawer (dual pane, overrides, dossier,
  description pack) + closing braces.
- L5 (lead): lime harmonization edits to chunk A (DECISION_STYLES review →
  purple, SidebarIcon active → lime), landing CTA href check.
- L6 (sub-agent): gpt-taste AI-slop audit of landing + cockpit → findings.
- L7 (sub-agent): browser screenshots / + /app/dashboard (1440 + 390) → report.

## Status log (append only)
- [done] GATES.md rewritten for judge-ready quality mission.
- [done] Palette audit: landing = cream #f0efe8 + ink #18180e + lime #c8d84a/#8cac28.
- [done] Typography audit: Geist Sans UI + Geist Mono data already the pattern.
- [done] Chunks B-E.
- [done] Lime harmonization + landing CTA check.
- [done] Build + routes (exit 0, 5 routes).
- [done] Slop audit (L6) + visual verification (L7) reports received.
- [done] Iter 2 fixes: drawer crash (.text on descriptions objects), AttributeRow defaultValue removed, landing scroll lock (html/body h-full removed from layout.tsx), mobile 390 (nav wrap, auto-fit grids, clamp padding), slop fixes (dead buttons/links gone, real stats 50/50 + 50.0 + 106/2500 + 2394, eyebrow stack fixed: ELIO Cockpit/Core Capabilities/Why ELIO/Plug & Play, capabilities dark band #18180e, monochrome chips, dashes, contrast #888870→#6a6a58, transitionDelay removed, comments trimmed, DAG labels 10px), cockpit polish (bar-4-freeze→elio, est $ chip, keyboard rows, role=dialog, neutral info dots, Accept/Reject 11px). Re-verified via playwright: scroll OK, mobile OK, drawer crash gone.
- [done] Upload flow E2E (G1d): set_input_files(demo_input_50.csv) → POST /api/run 200 → Uploaded chip active lime → auto-switch to dashboard.
- [pending] gpt-taste re-audit on final state (G4c) + visual eyeball when vision bridge has credits (G7a) + remaining G1 sub-gates (explorer/review/abstention/export click-throughs — code-reviewed, not yet playwright-clicked).

## Judge-Proof Uni-Hack Execution

This execution supersedes the stale frontend-only completion claims above. The
frozen `unihack_catalog/` contract at `38db2af` is read-only. Work is limited to
verification, artifacts, scripts, documentation, and frontend surfaces.

### Work units

- U1: official input/output contract and frozen-boundary audit.
- U2: receipt-chain and mutation rejection audit.
- U3: artifact and live cockpit judge-walk audit.
- U4: evaluator-upload and export-shape audit.
- U5: frontend interaction and visual judge-flow audit.
- U6: fresh-clone documentation and claim reconciliation.

### Integration contract

- `Unihack_ Expected Output - Delivery Format.csv` is the output-header source
  of truth; no script may silently replace it with a synthetic schema.
- `artifacts/metrics.json` is the source for headline numbers.
- `artifacts/evidence.json` and `artifacts/decision_log.jsonl` are the evidence
  and replay sources.
- Any unavailable publisher bytes must be reported as unavailable, never faked.
- `GATES.md` is the completion ledger; no completion claim is valid while a box
  is unchecked or evidence remains pending.

### Status log

- [in progress] Replaced stale acceptance ledger with executable judge-proof gates.
