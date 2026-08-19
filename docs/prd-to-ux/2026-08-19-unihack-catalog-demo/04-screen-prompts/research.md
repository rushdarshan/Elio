# Screen Prompts — Research (Source Index)

## Screen: Source Index

### State: Empty

**What this screen is for:** State honestly that no sources were consulted.

**What's visible:** "No sources were consulted — rows abstained earlier (see changelog)." With the changelog link.

**What the user can do:** Jump to the changelog.

**Feel:** Honest-report calm — a statement of fact.

**State context:** Empty state — nothing was fetched.

**Critical affordances:** The changelog link; the framing "abstained earlier" (never a broken pipeline impression).

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

**What this screen is for:** Let the judge audit every source consulted — including the rejections that prove the guardrails.

**What's visible:** Per-row source timelines, collapsed to a count by default ("4 sources"): each consulted URL tagged cache hit / live / fallback / rejected, with the allowlist decision shown for rejected hosts (e.g., "amazon.com — rejected: marketplace"). Rejected marketplaces appear as evidence of the guard — never hidden, never framed as failure. Clicking a source opens its fetched snippet and hash.

**What the user can do:** Expand a timeline; open a source's snippet; continue to the custody chain.

**Feel:** The appendix of the report — a precise ledger of citations; the rejected-marketplace entries read as proof of the guardrails, which is the demo's credibility moment.

**State context:** Populated state — the post-run source ledger.

**Critical affordances:** The cache-hit / live / fallback / rejected tags must be visually distinct; rejected marketplace entries must read as deliberate evidence (tag "rejected: marketplace"), not errors; each entry must be clickable to its content.

---

### State: Error

**What this screen is for:** Render fetch failures as ledger entries, not app errors.

**What's visible:** Timeline entries with the failure reason ("timeout — 3 retries") and the fallback that took over.

**What the user can do:** Open the entry; read the fallback path.

**Feel:** Calm and precise — failures are data.

**State context:** Error state — fetch failures absorbed into the ledger.

**Critical affordances:** The fallback entry must state what replaced the failed fetch; the reason must be specific (retries, timeout, rejection).

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

**What this screen is for:** The ledger under unusual sourcing.

**What's visible:** Allowlisted sites unreachable → fallback entries with reasons; a flight-critical field with no second source appears as a missing second source in the timeline (explaining why the value was held); first-50-row cap noted.

**What the user can do:** Read the timeline; follow to review for held values.

**Feel:** Same ledger precision.

**State context:** Edge-case variations of the source ledger.

**Critical affordances:** The "missing second source" entry must visually explain the held verdict downstream — the timeline is the why.