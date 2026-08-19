# Screen Prompts — Review (Disputed Findings)

## Screen: Review Panel

### State: Empty

**What this screen is for:** Confirm that nothing needed escalation — and make it a good moment.

**What's visible:** "No values held for review — every flight-critical value had two independent sources." Framed as positive confirmation, not an empty void.

**What the user can do:** Return to results.

**Feel:** Quiet confidence — the rare good-looking empty state; it reads as a machine doing its job.

**State context:** Empty state — nothing held. (In practice the demo escalates deliberately; this state is the exception, shown when runs clear.)

**Critical affordances:** The "two independent sources" phrasing must survive — it names the standard being met.

---

### State: Loading

**What this screen is for:** Not a standalone state — the panel appears post-run. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state.

**Critical affordances:** None.

---

### State: Populated

**What this screen is for:** Let the judge adjudicate held and disputed values with both sources visible, and see the report recompute from their verdict.

**What's visible:** Held values grouped by field type, each entry showing both sources side-by-side with their evidence hops (or an explicit "single source" note) and the candidate value(s); per-value Accept / Reject controls; immediate verdict feedback — the value's status chip updates, scoring recomputes visibly ("Score updated: 1 accepted, 1 rejected"), and the changelog records the verdict.

**What the user can do:** Accept or reject per value; open a source's custody chain; return to results.

**Feel:** An editorial review desk — two sources laid out like manuscript proofs, verdicts landing quietly; the recompute notice is the satisfying beat.

**State context:** Populated state — post-run review queue.

**Critical affordances:** Both sources must be visible side-by-side before a verdict — never a single-blind decision; per-value controls (no bulk accept — the audit trail stays per-verdict); the recompute notice must appear after each verdict.

---

### State: Error

**What this screen is for:** No error path of its own — the panel derives from the run. Recorded as inapplicable.

**What's visible:** (none)

**What the user can do:** (none)

**Feel:** (none)

**State context:** Inapplicable state.

**Critical affordances:** None.

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

**What this screen is for:** The review desk under pressure.

**What's visible:** Disagreement entries show both values and reasons with reject as the expected verdict; a time-pressed judge can export with unreviewed values flagged "held — unreviewed" (never guessed); review floods group by field with pagination — bulk accept is deliberately absent.

**What the user can do:** Verdict per value; export with flags; page through.

**Feel:** Same editorial calm — even a flood stays organized.

**State context:** Edge-case variations of the review panel.

**Critical affordances:** The "held — unreviewed" export flag must survive; the absence of bulk accept must hold — per-value verdicts are the audit guarantee.