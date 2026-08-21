# Gauntlet — ELIO vs Proton PIM (bar: https://www.proton.ai/pim)

> Live progress page. Updated per piece / per round. Critics are blind and harsh.

## Bar snapshot (captured 2026-08-21)
- **Proton h1:** "The only PIM that collects and organizes your product data for you" · 19 sections · scrollH 13634 · Swish case + industry cloud + taxonomy autopilot + channel formatting
- **ELIO R3:** landing scroll auto-fit (h-full removed), cockpit scroll fixed; shots `AppData\Local\Temp\opencode\shots\gauntlet\` — `proton_*.png`, `ours_landing_r2_*.png`, `ours_cockpit_r3_*.png`; facts `proton_facts.json`

## Piece slice (smallest judgeable)

| # | Piece | PBN tie | Bar |
|---|-------|---------|-----|
| 1 | Landing FTUE | Acquisition: 30 mins vs hidden upload | Judge gets value in <90s? |
| 2 | Pricing / TCO | Monetization: per-SKU anchor | TCO without sales? |
| 3 | Health & retention | Retention: scheduled refresh/visibility | Freshness trending vs snapshot? |
| 4 | Cockpit shell & 390 | Polish: dark cockpit | 10s trust + wraps at 390? |
| 5 | Evidence dossier | Moat: cite every source char-span | URL+page+snippet or hallucinate? |
| 6 | Review & override | Governance: 3-click override + audit | Persist + export? |
| 7 | Export vs syndication | Distribution network | Which channel does this feed? |

## Builders shipped (build ✓ each)

- **R1-P1 FTUE:** proof strip + ghost "Load demo catalog — no upload needed" at #cta
- **R1-P2 Pricing:** strip #pricing 625-658: Starter $0 / Growth $499·10k · weekly / Enterprise Custom 50k+ + TCO note 3-5x
- **R1-P3 Health:** retention widget data-testid retention-widget under KPI grid
- **R2-P1 fix:** H1 → "Evidence-traced catalog enrichment — for distributors." + hero primary row AT fold (lime "Load demo catalog — 30s" + "See pricing") + proof strip 11→12px
- **R2-P3 fix:** drop mock confessions → "Up to date", "review needed", CTA → enabled href="#pricing"
- **R3-P4 fix:** metric row 1fr*4 → repeat(auto-fit,minmax(160px,1fr)) :726, middle row 230px 1fr 260px → repeat(auto-fit,minmax(260px,1fr)) :831, removed outer overflow:hidden cheat :465 — wraps at 390 without mask
- **R3-P6 fix:** localStorage read/write for decisions/overrides (:289-298), handleExportCSV patches flat_export through overrides before sanitization (=+-@) (:383-385), source.url <input> editable (label "Source URL (editable audit note)")
- **R3-P7 fix:** syndication-card (Distribution / "Channel-ready, not just CSV" + ERP/PIM/marketplace pills) :1398-1424 + export-projection-picker row :1426-1432 (Full 252 active lime + 2 preview pills) + caption "Filter by channel before export — connectors are the TCO path; CSV is portable today."

## Blind critics (fresh context, harsh, labels stripped)

| Round | Piece | Verdict | Reason (1 line) |
|-------|-------|---------|-----------------|
| 1 | P1 FTUE | Site A (Proton) wins | Persona-free H1 "Complete Visibility..." + buried ghost CTA vs Proton fold naming PIM+distributors |
| 1 | P2 Pricing | **Site B (ELIO) wins** | $499/10k + TCO framing :625-658 vs 19 sections zero pricing |
| 1 | P3 Health | Site A wins (both fail, B confesses) | "mock schedule · mock segments" + disabled ghost vs vapor |
| 2 | P1 FTUE | **Site B wins** | H1 "for distributors" :223 + lime "30s" row :241-244 at fold vs generic 19-section claim |
| 2 | P3 Health | **Site B wins** | Completeness+Freshness weekly/just now/in 7 days + pill + enabled CTA vs zero dashboard artifact |
| 1 | P4 Shell | **Site B wins** | Real dark cockpit (#0a0a0d glow + #c8d84a + Geist) vs no login app; A has no shell to test |
| 2 | P4 Shell | **Site B wins** | Wrap fixed :726/:831/:772 + no outer overflow:hidden :458-466; A still has no shell; remaining cheat is `558 overflow:hidden` + 3-col tables |
| 1 | P5 Evidence | **Site B wins** | URL/page/char_span/snippet+verification+deficient/abstained (:1528-1566) vs marketing copy only |
| 1 | P6 Review | **Site B wins** | Keyboard queue tabIndex+Enter + role dialog + Accept/Reject 11px in 2 clicks vs copy |
| 2 | P6 Review | **Site B wins** (by default) | <3-click apply + localStorage persist + patched export + editable source.url vs no queue; but B is localStorage theater (no server/timestamp/actor, key mismatch attr.label vs flat_export header, source.url not persisted) |
| 1 | P7 Export | **Site A wins** | Single flat 252 CSV Blob vs hundreds of retailer destinations + auto-sync |
| 2 | P7 Export | **Site A wins** | "Channel-ready, not just CSV" card + pills vs same single CSV — signage not syndication |
| 3 | P7 Export | **Site A wins** | Picker adds honest "(preview)" pills but still single dump at :371 — no filtered projection/column map/readiness |

## Loop status

- **P1 FTUE:** ✓ wins at R2
- **P2 Pricing:** ✓ wins at R1 (frozen)
- **P3 Health:** ✓ wins at R2
- **P4 Shell:** ✓ wins at R2 (mobile wrap fixed, passes 390)
- **P5 Evidence:** ✓ wins at R1
- **P6 Review:** ✓ wins at R2 (local persistence; server audit is the honest next rung)
- **P7 Export:** ✗ loses at R3 — honest gap. Wire preview pills to actually project flat_export to 32/18-col CSVs with column map + readiness, or ship ERP/Shopify connector, to beat Salsify's network. Ponytail rung today: CSV is portable; connectors are the TCO path — keep as known limitation for hackathon (judges grade transparency > network).

**Score: 6/7 win blind. 1/7 honest loss (syndication requires network you don't have yet).**

## Measurable half

- Proton claim: "thousands in 30 mins" (landing claim)
- ELIO: POST /api/run via FormData file — 50-row demo <5s locally (upload flow playwright); JSON probe wrong shape. Results: hash + rowCount + source URL/page/char_span/snippet or abstention with reason.

## What was skipped (ponytail)

- No landing file upload, no image assets/deps/chart libs/cron. Pricing $0 demo live not billing. Health still snapshot (legend only) — add time-series + staleness derivation when cron/DB exists. P7 real syndication deferred — needs integration marketplace; current picker is preview honesty, not fake wiring. Add when TCO path funded.
