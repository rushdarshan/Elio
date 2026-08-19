# Screen Prompts — Pipeline Run

## Screen: Run

### State: Empty

**What this screen is for:** Not reachable as a standalone state — a run only starts from a fully mapped upload. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state — the run view has no entry without a mapped upload.

**Critical affordances:** None.

---

### State: Loading

**What this screen is for:** Let the judge watch the report being assembled — nine stages in visible order, never a hang.

**What's visible:** A nine-stage tracker (Intake → Resolve → Classify → Research → Fetch → Extract → Verify → Describe → Export) lighting up in order, the current stage's row count ticking, and a live-fetch indicator ("Fetching 3 sources…") with per-URL status. If degraded mode engages, a banner appears immediately: "Running in deterministic-only mode — no LLM. Scores will be labeled accordingly."

**What the user can do:** Watch; expand a stage for per-URL fetch detail.

**Feel:** Quietly confident — the tracker reads like instruments on a report being drafted; movement within the first seconds is essential; the degraded-mode banner is plain-spoken, not alarming.

**State context:** Loading state — a 30-second-class run in progress.

**Critical affordances:** The nine stages must be visible and ordered (the DAG is the story); the live-fetch indicator must be distinguishable from idle; the deterministic-only banner must appear the moment degradation engages — the honest label is part of the trust story.

---

### State: Populated

**What this screen is for:** The completed-run transition — tell the judge the report is ready and move them to it.

**What's visible:** A completion banner — "Run complete — 30 rows enriched in 24s. See the report." — with auto-advance to the dashboard.

**What the user can do:** Nothing required — the advance is automatic.

**Feel:** A quiet, confident close to the wait; the duration shown reads as proof of work.

**State context:** Populated state — the run finished; this is a transition moment, not a resting screen.

**Critical affordances:** The completion banner must include row count and elapsed time; auto-advance must not feel abrupt.

---

### State: Error

**What this screen is for:** Keep the run alive when individual rows fail, and degrade honestly when the whole run is impaired.

**What's visible:** Per-row failures never abort — a row counter shows "2 rows abstained (reasons logged)" while the tracker continues. Whole-run degradation (dead cache/LLM) shows the deterministic-only banner and completes with labeled scores. Mid-run restart shows a "run restarted cleanly" notice. Never a frozen spinner.

**What the user can do:** Watch the run complete with honest labels.

**Feel:** The calm of a well-built machine — failures are reported as data, not as drama.

**State context:** Error state — partial failures absorbed into the run, full degradation labeled.

**Critical affordances:** Abstained-row counts must link to the changelog reasons; the deterministic-only label must persist onto the dashboard, not vanish at completion.

---

### State: Permission-denied

**What this screen is for:** Not applicable — no auth. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state.

**Critical affordances:** None.

---

### State: Edge cases

**What this screen is for:** The run's behavior when the judge's file is unusual.

**What's visible:** A pre-run notice when rows will fetch live ("N rows will fetch live — expect a longer run") in the operator flow; a zero-enrichable-rows completion that states the fact explicitly ("no enrichable rows found") rather than showing a dashboard of zeros.

**What the user can do:** Proceed knowing the expectation is set.

**Feel:** The same honest-report calm — expectations set before the wait, facts stated after.

**State context:** Edge-case variations of the run.

**Critical affordances:** The live-fetch warning must precede the run, not appear mid-run; the zero-enrichable completion must be a distinct message, not a zeroed dashboard.