# Screen Prompts — Resolve (Identity Annex)

## Screen: Identity Annex

### State: Empty

**What this screen is for:** State honestly that no identity claims could be resolved.

**What's visible:** "No identity claims were resolvable for these rows — see the changelog for why." Placeholder values render as placeholders; nothing is inferred.

**What the user can do:** Jump to the changelog for reasons.

**Feel:** Honest-report calm — the empty state is a statement of fact, not a failure wall.

**State context:** Empty state — a run produced no resolvable identities.

**Critical affordances:** The changelog link must be present; placeholder semantics must never be rendered as real brands.

---

### State: Loading

**What this screen is for:** Not a standalone state — the annex renders with the post-run report. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state.

**Critical affordances:** None.

---

### State: Populated

**What this screen is for:** Let the judge audit identity claims — brand, manufacturer, and distributor as separate typed edges.

**What's visible:** Per-row identity cards, collapsed to a summary line by default: resolved brand, manufacturer, and distributor as distinct edges with match scores and the evidence that produced them. Conflicts (one alias mapping to two brands) render flagged, never silently picked. Each edge is clickable into its custody chain.

**What the user can do:** Expand a card; click an edge for its custody chain.

**Feel:** Report annex quality — quiet tables and small cards, generous whitespace; the identity claims read like footnoted facts, not dashboard chrome.

**State context:** Populated state — the post-run identity annex.

**Critical affordances:** Brand and manufacturer must stay visually distinct (separate typed edges — never collapsed into one string); conflict flags must be explicit; edges must link to the shared custody drill-down.

---

### State: Error

**What this screen is for:** Show resolution failures as abstained edges with reasons.

**What's visible:** Edges marked abstained with the reason (e.g., "no vocab match — not guessed"), inline per row.

**What the user can do:** Expand the edge for the changelog reason.

**Feel:** Same calm — failures are data points.

**State context:** Error state — resolution failures absorbed into the annex.

**Critical affordances:** The abstained edge must state "not guessed" explicitly — honesty over completion.

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

**What this screen is for:** The annex under unusual runs.

**What's visible:** Unknown manufacturers show abstained edges with "no vocab match"; capped uploads note the 50-row limit on the annex itself.

**What the user can do:** Read reasons; proceed.

**Feel:** Consistent report calm.

**State context:** Edge-case variations of the annex.

**Critical affordances:** The cap note must appear on the annex (not only at upload).