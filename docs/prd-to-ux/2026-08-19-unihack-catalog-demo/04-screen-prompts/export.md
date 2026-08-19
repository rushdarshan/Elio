# Screen Prompts — Export (Report Delivery)

## Screen: Export Panel

### State: Empty

**What this screen is for:** The pre-run state — nothing to export.

**What's visible:** "Nothing to export yet — run the pipeline first." (Reachable only by direct navigation pre-run; the flow normally prevents it.)

**What the user can do:** Return to the flow.

**Feel:** Honest-report calm.

**State context:** Empty state — no run, no export.

**Critical affordances:** The path back must be one step.

---

### State: Loading

**What this screen is for:** Export generation on click.

**What's visible:** A brief "Assembling 252-column contract…" line (sanitization + projection run here) — seconds-class.

**What the user can do:** Wait; cancel.

**Feel:** Quiet precision — the contract language reinforces the standards being met.

**State context:** Loading state — export assembling.

**Critical affordances:** The "252-column contract" phrasing must survive — it names the standard.

---

### State: Populated

**What this screen is for:** Let the judge take the artifact home.

**What's visible:** Two download controls (CSV / JSON), a verification line — "252 columns, contract order ✓ — formula-injection sanitized" — per-row compliance flags (char-limit/LOV) attached to the file, and the dashboard's headline number repeated as the file's cover note.

**What the user can do:** Download CSV; download JSON; re-verify.

**Feel:** The report's back cover — clean, final, confident; the verification line is the last trust beat.

**State context:** Populated state — export ready.

**Critical affordances:** The contract-verification line must state "contract order" and "sanitized" — those two words are the quality claim; the headline number must ride along in the file's metadata.

---

### State: Error

**What this screen is for:** Fail honestly, never silently.

**What's visible:** "Could not assemble export — see the changelog" with a retry affordance; a contract-check failure blocks download with its reason.

**What the user can do:** Read the reason; retry.

**Feel:** Calm precision — a blocked download is better than a wrong file.

**State context:** Error state — export assembly failed.

**Critical affordances:** The contract check must gate the download (never a silently-wrong file); retry must be one step.

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

**What this screen is for:** The export under unusual runs.

**What's visible:** Held-but-unreviewed values export blank with a "held — unreviewed" flag column (never guessed values); full evidence JSON is large by design — noted in the download label.

**What the user can do:** Download either format knowing the tradeoff.

**Feel:** Same clean finality.

**State context:** Edge-case variations of the export panel.

**Critical affordances:** The "held — unreviewed" flag column must survive in the CSV; the JSON size note must be in the label.