# Screen Prompts — Custody Drill-Down (Audit Trail)

## Screen: Custody Modal

### State: Empty

**What this screen is for:** Make the "no evidence" case meaningful — abstention explained at the point of click.

**What's visible:** "No evidence — this value abstained by design. See the changelog for the attempt history." With the changelog link. Reachable only from abstained cells; never a dead click.

**What the user can do:** Open the changelog; close.

**Feel:** Honest-report calm — the modal honors the click even when there is nothing to show.

**State context:** Empty state — an abstained value's custody chain.

**Critical affordances:** The "by design" framing must survive; the changelog link must be present.

---

### State: Loading

**What this screen is for:** Hash-verification wait when a snippet is re-fetched from cache.

**What's visible:** A brief verification line — "Verifying content hash…" — seconds-class.

**What the user can do:** Wait; close.

**Feel:** Quiet and legible; the verification line reinforces the custody promise.

**State context:** Loading state — cache re-fetch with hash check.

**Critical affordances:** The verification language must survive ("Verifying content hash") — it is the audit promise in micro.

---

### State: Populated

**What this screen is for:** The full chain — search result → page → datasheet → hash → region → snippet, plus the field's change history.

**What's visible:** An ordered hop list, each hop collapsed to one line by default: search result → product page → (linked) datasheet → content hash → page region/span → snippet. Each hop expandable to its evidence fields (URL, fetched time, hash). The field changelog renders below the chain: what changed, why, and by which stage — git-style, replayable.

**What the user can do:** Expand hops; scroll the changelog; close.

**Feel:** The report's footnote mechanism made whole — precise, ledger-like, quietly impressive; the modal reads like a notary page.

**State context:** Populated state — a value's complete audit trail.

**Critical affordances:** The hop order must survive (search → page → datasheet → hash → region → snippet); hash and region must be pinned visible per hop; the changelog must read as replayable history (stage + reason per change).

---

### State: Error

**What this screen is for:** Render a re-fetch failure without breaking the chain.

**What's visible:** The chain renders from stored evidence with a "cached copy (hash verified at capture)" note when re-fetch fails.

**What the user can do:** Read the stored chain; close.

**Feel:** Calm — the chain is never broken; the note states the assurance level honestly.

**State context:** Error state — live re-fetch failed, stored evidence shown.

**Critical affordances:** The "hash verified at capture" note must be explicit; the chain must still render fully.

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

**What this screen is for:** The modal under unusual evidence.

**What's visible:** Image-only PDF datasheets (no text layer) render the hop as "no text layer — abstained (OCR out of scope)" — honest, not a broken link; long snippets scroll within the modal with hash and region pinned at top.

**What the user can do:** Scroll; read; close.

**Feel:** Same notary precision.

**State context:** Edge-case variations of the custody modal.

**Critical affordances:** The "no text layer" hop must be explicit about abstention; pinned hash/region must not scroll away.