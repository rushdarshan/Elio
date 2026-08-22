# Evidence Explorer — Screen Prompts

_Each block below is self-contained. Copy one block, paste into Stitch / Figma AI / Pencil / Claude Design._

---

## Explorer — Empty (No Search Yet)

````
**What this screen is for:**
The front door of the evidence console: search is the hero action. The user lands here to find a specific catalog row and trace where its values came from.

**What's visible:**
A dark console surface with the sidebar chrome. The main area is dominated by a single prominent search field — wide, mono-styled hint text ("Search by MPN, brand, or description...") — with a hint below explaining that every result carries its custody chain. Nothing else competes; the search is the whole point of the screen.

**What the user can do:**
- Primary: type a query and search.
- Secondary: browse the review queue or dashboard from the sidebar.

**Feel:**
Dark ops-console tone, near-black surfaces, one blue accent on the interactive search element. The search field should feel like the cockpit's main instrument — large, obvious, quiet.

**State context:**
Empty state — no query entered yet.

**Critical affordances:**
Search must be the visual center of gravity. The field should signal it accepts MPN codes, brand names, and free text without a dropdown or filter ceremony.
````

---

## Explorer — Search Results (Populated)

````
**What this screen is for:**
The user searched and sees matching catalog rows — the first step of record-first drill-down.

**What's visible:**
A results list of matching rows, each rendered as a compact record card: the MPN in mono, the brand label, the taxonomy path (dept > fine), and the decision status (accepted or escalated) as a subtle tag. Results are tidy and scannable, one row after another, with a count of matches somewhere small.

**What the user can do:**
- Primary: click a record to open its custody trace.
- Secondary: refine the query; switch datasets from the chrome.

**Feel:**
Dark console, hairline separators between results, mono for identifiers, blue accent for the interactive status tags only where meaningful. Dense but breathable — a working list, not a gallery.

**State context:**
Populated state — query returned matches.

**Critical affordances:**
Each result must expose MPN, brand, taxonomy, and status at a glance. The decision status must be visible without opening the record (accepted vs escalated read differently).
````

---

## Explorer — Record Open (Custody Drawer)

````
**What this screen is for:**
The core trust moment: the user opened one record and can verify that every attribute value is traceable to a real source span — or see exactly why a value was abstained.

**What's visible:**
The results list remains on the left; a wide evidence drawer slides in from the right. The drawer has two panes. Left pane: the record's attributes — each attribute name with its extracted value, its verification state (supported / abstained), and a control to select it. Right pane: the raw evidence for the selected attribute — the source link, the page reference, and the verbatim raw snippet pulled from the manufacturer document, with the matching value visibly highlighted inside the snippet. When no attribute is selected, the right pane shows a quiet prompt to select one. Abstained attributes show their refusal reason in place of a source.

**What the user can do:**
- Primary: click attribute after attribute to walk its custody chain (value -> snippet highlight -> source link).
- Secondary: open the source link in a new tab; jump to the review action for escalated records.

**Feel:**
The drawer is the forensic layer of the console: darker than the main surface, hairline borders, mono type for snippets and identifiers, the value highlight in a warm amber so the traced text pops against the raw document text. Everything reads as evidence, not decoration.

**State context:**
Populated state — a record is selected and its custody chain is open.

**Critical affordances:**
The verbatim snippet is the star: the selected attribute's value must be visibly highlighted inside the raw text. The chain result -> page -> snippet -> highlighted span must read as one continuous trail. Abstained attributes must show a reason, not an empty gap.
````

---

## Explorer — No Match / Untraceable (Edge)

````
**What this screen is for:**
The user searched and got nothing, or opened an attribute that has no traceable source — the console must handle both with honesty.

**What's visible:**
For a no-match search: a short, plain "no results" message with the query echoed in mono — no empty-state illustration, no celebration animation. For an untraceable attribute in an open record: the evidence pane shows the refusal reason in amber (e.g., unsupported category, missing evidence) instead of a snippet, and the attribute is clearly marked as abstained rather than empty.

**What the user can do:**
- Primary: retry with a different query, or accept the abstention and move on.
- Secondary: filter results by decision status.

**Feel:**
Same dark console tone; the honesty of "we could not trace this" is the product's personality — plain words, amber for refusal, no apology styling.

**State context:**
Edge state — no results, or a value the pipeline refused to guess.

**Critical affordances:**
Abstention must read as a deliberate, explainable refusal (with reason), never as a bug or blank cell. No-match states must not imply the data is broken.
````