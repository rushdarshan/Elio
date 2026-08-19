# Screen Prompts — Enrich (Evidence-Led Results)

## Screen: Results Table

### State: Empty

**What this screen is for:** State full abstention as engineered honesty.

**What's visible:** "No values could be enriched with evidence — full abstention. See the changelog for per-field reasons." With the changelog link.

**What the user can do:** Open the changelog.

**Feel:** Honest-report calm — the empty state is part of the honesty narrative, never a failure wall.

**State context:** Empty state — all rows abstained.

**Critical affordances:** The changelog link; the phrase "full abstention" (the abstention-is-honesty story must survive).

---

### State: Loading

**What this screen is for:** Not a standalone state — renders with the post-run report. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state.

**Critical affordances:** None.

---

### State: Populated

**What this screen is for:** Let the judge verify any value in one glance — every claim carries its citation.

**What's visible:** Per-row attribute lines: label, value, unit of measure, and a citation chip (source host + span). Unsupported fields render as "— not tested —" rows with a reason link. Placeholder semantics preserved. Status chips distinguish verified / held / abstained values at a glance. Score cells and values are clickable into the custody chain. Disputed values carry a "disputed" chip and route to review.

**What the user can do:** Expand a citation chip (snippet); click a value for its custody chain; click a disputed value into review; jump to the changelog.

**Feel:** The body of the report — a clean, dense-but-breathable results table where every cell is a footnoted fact. The "not tested" rows read as deliberate, not missing.

**State context:** Populated state — the evidence-led results table.

**Critical affordances:** The verified / held / abstained status chips must be visually distinct at a glance; every value must have a clickable citation; unsupported fields must render as "not tested" with a reason link — never as blank cells.

---

### State: Error

**What this screen is for:** Show extraction failures as abstained values with reasons — never invented values.

**What's visible:** Abstained values inline with their reasons.

**What the user can do:** Read the reason; jump to the changelog.

**Feel:** Calm precision — failures are data points.

**State context:** Error state — extraction failures absorbed into the table.

**Critical affordances:** The abstained value must state the reason inline; the "no fabrication" rule must be visible in the language ("abstained — no reliable source").

---

### State: Permission-denied

**What this screen is for:** Not applicable. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state.

**Critical affordances:** None.

---

### State: Edge cases

**What this screen is for:** The table under unusual data.

**What's visible:** Contradicted values show both citations with a "disputed" chip routed to review; long descriptions truncate with expand (never clipped silently); output-column parity is honored — unmapped values are dropped with an explicit reason, never silently.

**What the user can do:** Expand long values; follow disputed values to review.

**Feel:** Same report-grade precision.

**State context:** Edge-case variations of the results table.

**Critical affordances:** Disputed values must show both citations, never one; truncation must offer expand; every drop must be explained.