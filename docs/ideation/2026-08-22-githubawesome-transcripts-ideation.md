---
date: 2026-08-22
topic: githubawesome-transcripts
focus: https://www.youtube.com/@GithubAwesome/videos get all vids transcript
mode: elsewhere-software
---

# Ideation: GithubAwesome Channel — Bulk Transcript Pipeline

## Grounding Context

**Topic context:** Channel `@GithubAwesome` — 60.4K subs, 437 videos (live websearch 2026-08-22), daily/weekly format: GitHub Trending Today/Weekly/Monthly, Hacker News Show, 35 Self-Hosted Projects lists. Avg 12–15 min/video. User intent: get *all* transcripts in one pass, structured and re-fetchable. Manual path = 3 clicks/video in YouTube transcript panel (~1300 clicks, ~1h tedious, per Transcribr estimate). No existing local pipeline in this repo; `unihack_catalog/` is frozen, `elio-frontend/` is Next.js cockpit — no YouTube tooling present.

**External context (2026-08-22 live):**
- Stable local primitive: `yt-dlp --write-sub --write-auto-sub --skip-download` downloads VTT without video (konadu.dev 2026-06-30) — avoids brittle DOM scraping, survives YouTube markup reshuffles; auto captions repeat tail → dedupe consecutive lines.
- Bulk open-source: `yt-dlp-transcripts` PyPI 0.1.1 (2025-08-29, LinuxIsCool) — `yt-dlp + youtube-transcript-api`, auto-detect video/playlist/channel, resume capability, CSV with `video_id,title,url,transcript,upload_date,duration,view_count`, respects rate limits.
- Managed APIs: TranscriptAPI.com (1 credit/fetch, batch 50, `GET /channel/videos?channel=@TED` returns all uploads), Apify `influship/youtube-channel-transcripts` (handle, videoLimit, sortBy: newest/popular/oldest, language, includeSegments, 5-star), BulkTranscripts.co, Transcribr (Chrome ext + server-side: 5000 URLs, parallel 100 batches, 60–90s for 500 videos, 5 export formats TXT/SRT/VTT/CSV/JSON, flags 5–10% no-caption).
- Fallback path: AssemblyAI + yt-dlp guide — when `--list-subs` empty, download `m4a/bestaudio` then local Whisper transcription.
- Cost signals: free yt-dlp path = $0 but proxy maintenance risk; managed API Production ~$49/mo for 25k credits; free tiers 100 credits/mo; transcriptfetch.com batch 50 concurrent with proxy fallback.

**Past learnings:** None yet for YouTube transcript extraction in `docs/solutions/` — ELIO's provenance ledger pattern (`SourceEvidence` + `MethodLineage` in `models.py`) is analogous for per-transcript lineage and is reused as warrant.

## Ranked Ideas

### 1. Local-first one-command bulk extractor (hybrid yt-dlp + resume)
**Description:** Ship `scripts/githubawesome_transcripts.py` wrapping `yt-dlp-transcripts` with `data/tmp/yt-dlp` temp root (Hermes pattern `data/tmp/yt-dlp`), `--paths` isolation, resume file, and VTT→TXT dedupe. Input: `https://www.youtube.com/@GithubAwesome/videos`; output: `artifacts/githubawesome/transcripts.jsonl` + `transcripts.csv` (UTF-8-sig). Handles channel pagination beyond 100-item playlist limits, 437 videos in one run. Run: `python -B scripts/githubawesome_transcripts.py --channel @GithubAwesome --out artifacts/githubawesome/`.
**Warrant:** `direct:` channel has 437 videos (websearch `@GithubAwesome` header: 60.4K subs · 437 videos); `external:` yt-dlp stable over DOM scraping (konadu.dev 2026-06-30: "brittle DOM scraping breaks every YouTube reshuffle; yt-dlp one-liner beats it") + `yt-dlp-transcripts` auto-detect channel + resume (PyPI description: "Auto-Detection, Resume Capability, 5k batch").
**Rationale:** Directly kills the 1300-click manual cost with the tool the ecosystem already maintains; resume makes 437-video bulk interrupt-safe and pagination-safe — the lowest-risk path to "get all vids transcript" today.
**Downsides:** 5–10% videos lack captions (flagged not failed); YouTube may rate-limit at bulk — needs backoff (already in library).
**Confidence:** 90%
**Complexity:** Low
**Status:** Unexplored

### 2. Provenance-anchored transcript store (ELIO-style ledger)
**Description:** Each transcript is a claim with `url, video_id, title, language, source_type (manual/auto/whisper), retrieved_at, sha256, word_count, char_span`, hop_chain `channel → video_id → subtitle_track`. Persist as JSONL with per-video hash for re-fetch verification; rejected/missing captions get abstention reason ("no captions: manual+auto empty"). Mirrors `models.py:ClaimRecord/SourceEvidence` so `artifacts/metrics.json` can report provenance coverage.
**Warrant:** `direct:` `unihack_catalog/models.py:88` defines `SourceEvidence(url, quote, retrieved_at, sha256)` + `MethodLineage` + `ReviewAudit` for abstention-with-reason; `external:` Apify actor returns `source: auto-generated/manual, language, word_count, error` — the same fields.
**Rationale:** Makes "got transcript" verifiable, not asserted — dual-pass style: value must be re-fetchable from YouTube captions track, abstentions are explicit. Prevents drift when channel adds videos.
**Downsides:** Adds schema weight vs plain TXT dump; requires dedup hash logic.
**Confidence:** 85%
**Complexity:** Low-Medium
**Status:** Unexplored

### 3. Timestamped repo-aware chunking → searchable catalog + RAG index
**Description:** Parse each transcript with timestamped segments, extract mentioned repos (`github.com/org/repo`, bare `org/repo` mentions), and chunk at natural talk boundaries (30s or per-repo segment). Emit two artifacts: (a) `repos.csv` (video, timestamp, repo_url, repo_name, stars_mentioned, category inferred from series), (b) SQLite + vector index (e.g., sqlite-vec) for semantic search: "show me self-hosted Rust projects from last 60 days." Powers `docs/ideation` search without rewatching.
**Warrant:** `reasoned:` 437 videos × ~15 min × ~130 wpm ≈ 850k words — unsearchable as flat TXT; repo mentions are the structured value inside unstructured talk, so chunking by repo turn converts linear video watch-time into queryable rows at near-zero marginal cost once transcript exists.
**Rationale:** Second-order compounding: first transcript fetch is cost, every future query is free. Turns channel from watch-list into queryable GitHub trend database — distinct from ELIO but same leverage pattern (build once, query many).
**Downsides:** NER for repo mentions is noisy; needs light heuristic + manual review for edge cases.
**Confidence:** 75%
**Complexity:** Medium
**Status:** Unexplored

### 4. Channel taxonomy preservation (series-aware grouping)
**Description:** Preserve series as first-class grouping: Trending Today (#41, #36…), Weekly (#41, #40…), Monthly (#7), Hacker News Show (#10…#1), Self-Hosted Projects. Group `transcripts.csv` by `playlist/series` derived from title regex (`/^GitHub Trending (Today|Weekly|Monthly)|^Hacker News Show #|^\\d+ Self Hosted/`), emit `series_index.json`. Enables "get all Weekly #40–41 transcripts" slicing and series-level analytics.
**Warrant:** `direct:` websearch titles show explicit series prefixes (`Hacker News Show #10`, `GitHub Trending Weekly #41`, `35 Self Hosted Projects…`) with consistent naming; `reasoned:` treating 437 videos as flat list loses the editorial taxonomy the channel already provides — grouping preserves context for downstream catalog use.
**Rationale:** Without taxonomy, timeline queries require full scan; with it, product slices map to how viewers actually navigate the channel. Low code, high usefulness.
**Downsides:** Title regex brittle if channel renames series; needs fallback to "Uncategorized".
**Confidence:** 80%
**Complexity:** Low
**Status:** Unexplored

### 5. Hybrid cost ladder: local → API fallback → Whisper (with metrics)
**Description:** Implement cost-aware fallback chain: (1) local yt-dlp captions (free, `source=manual/auto`), (2) on 429/empty, retry via managed API batch 50 (TranscriptAPI/TranscriptFetch, paid credits), (3) on still-empty, download `m4a/bestaudio` then local Whisper (AssemblyAI pattern). Log per-video `source_type` + latency + credit cost to `transcript_metrics.json` (p50/median response 49ms for API hits vs local). Default is $0 local; paid path is opt-in via `TRANSCRIPT_API_KEY`.
**Warrant:** `external:` transcriptfetch.com comparison 2026-06-10: "library is free, but proxy bill + maintenance are not; managed API absorbs blocking at $0.01/credit — batch 50 concurrent"; `direct:` konadu.dev FAQ: "if --list-subs shows nothing, download audio + run Whisper yourself."
**Rationale:** Puts cost on a knob, not a surprise. 90% of 437 videos succeed locally; 5–10% hit the fallback, so measured spend is fractional. Matches ELIO's deterministic-first, assisted-second economics (FrugalGPT cascade).
**Downsides:** Whisper local needs model download (~150MB) and is slower; paid API adds env key management.
**Confidence:** 85%
**Complexity:** Medium
**Status:** Unexplored

### 6. Daily channel watch + diff + git-history dataset
**Description:** Add `scripts/check_githubawesome_daily.py` run via cron/GitHub Action: fetch `@GithubAwesome/videos` listing, compare to `artifacts/githubawesome/manifest.json` (video_id set), fetch new transcripts only (resume), append to JSONL, commit diff with message `data: GithubAwesome +N videos 2026-08-22`. Notifies via diff stat. Uses TranscriptAPI `/channel/subscribe` webhook (free, polled 15m) as optional trigger instead of cron.
**Warrant:** `external:` TranscriptAPI `/channel/subscribe` (free, 15m polling) and Apify sortBy newest (daily uploads) are designed for this; `reasoned:` channel publishes daily/weekly, so one-shot fetch decays within 24h — diff-over-time compounds the dataset without re-paying for 437 old videos.
**Rationale:** Converts one-time scrape into durable dataset; each day's fetch is incremental and auditable via git history — same pattern as ELIO's `decision_log.jsonl` append-only ledger.
**Downsides:** Requires scheduler (Action or cron) and idempotency; webhook adds infra.
**Confidence:** 75%
**Complexity:** Medium
**Status:** Unexplored

### 7. Offline transcript explorer (static HTML, no backend)
**Description:** Generate `artifacts/githubawesome/explorer.html` (self-contained, like `demo.html` / `rules_map.html` pattern already in repo) — search box over transcripts (client-side Fuse.js), series filter, click row → side-by-side transcript with repo links highlighted and timestamp jump to YouTube `?t=` anchor. Opens offline, zero install, shareable in `artifacts/`.
**Warrant:** `direct:` repo already ships `demo.html` (1MB static explorer) and `rules_map.html` as zero-backend surfaces per `README.md:43`; `external:` Transcribr feedback: "combined JSON perfect for AI tools/pipelines" — explorer is the human browsing layer on that JSON.
**Rationale:** Gives the non-technical consumer of the transcript bulk a 5-second search ("show HN #10 mindwalk segment") instead of grepping 437 TXT files. Fits repo's existing static-artifact distribution constraint.
**Downsides:** Client-side search over 850k words needs indexing; large HTML payload (~2–3MB) — needs pagination.
**Confidence:** 80%
**Complexity:** Medium
**Status:** Unexplored

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Pure browser DOM scrape via headless extension | Too vague/brittle — konadu.dev documents YouTube reshuffle breakage; yt-dlp subtitle endpoint is the maintained API |
| 2 | Single-video `youtubetotranscript.com` paste loop (437×) | Not actionable at scale — 3 clicks/video × 437 = not viable; exceeds free-site rate limits |
| 3 | Always-paid API (Apify 437 credits, no local fallback) | Too expensive relative to likely value — 90% achievable at $0 via yt-dlp; econ violation vs hybrid ladder |
| 4 | Download full video MP4s then transcribe everything via Whisper | Duplicates stronger idea #5; wastes bandwidth (yt-dlp --skip-download avoids); only valid when captions absent |
| 5 | Flat giant TXT dump (one combined file, no metadata) | Not grounded — loses video_id/title/upload_date/word_count needed for catalog queries; duplicates #1 but worse |
| 6 | Real-time live caption streaming during watch | Interesting but better as brainstorm variant for live HN Show coverage, not bulk historic fetch; above ambition floor for bulk |
| 7 | Manual repo extraction (watch + note repos by hand) | Unjustified — no warrant vs automated NER in #3; fails meeting-test for 437 videos |
| 8 | Ignore series taxonomy, store flat | Duplicates stronger idea #4; loses actionable slice that already exists in titles |
| 9 | Deleted: duplicates ELIO pipeline refactor | Not grounded in stated context — transcript bulk is not catalog normalization |
| 10 | Build custom proxy pool for transcript scraping | Too expensive relative to value — transcriptfetch.com already absorbs proxy maintenance; reinvention |
| 11 | Translate all transcripts to 10 languages via GPT-4.1 Nano | Unjustified — no articulated warrant; translation is downstream optional, not core to "get all transcripts" |
| 12 | Per-video embeddings via paid API only | Duplicates #3 but with cost lock-in; rejected in favor of local SQLite + on-demand embedding |

