# UX Philosophy — ELIO Frontend

## Chosen Philosophy: The Ops Console (hybrid of Production Line + Evidence Console + Record-First)

**Organizing metaphor / mental model:**
A working operations console: the catalog moves along a production-line journey (Upload to Export) dressed as a dark evidence console, where search is the front door and every number on screen drills down to its source trace.

**How the PRD features map into this structure:**
- **Upload & Run:** the intake hatch of the production line; console-style drop zone with strict CSV validation and a schema dry-run.
- **Acceptance Dashboard:** the console's headline readout / quality gate at the top of the line; every metric is a drillable instrument, never a bare badge.
- **Evidence Explorer:** record-first drill-down, the hero. Search a part, every value carries its custody chain (search result -> page -> content hash -> region/span -> snippet); abstentions show their reason.
- **Review Queue:** the sign-off station; approve/reject/edit, decisions flow to the export and write back to the decision log.
- **Abstention / Trust:** the refuse-with-reason panel; signed refusals in the audit trail, grouped by reason (missing evidence, conflicting evidence, unsupported category, validation failure).
- **Export & Delivery:** the shipping dock; 252-col schema check, accepted/reviewed/abstained counts, CSV/JSON download, "ready for import" status.
- **Developer / Architecture:** a hidden utility under a debug menu, out of the judge journey.

**Trade-offs:**
- Good at: the workflow story (production line) plus the trust texture (evidence console) plus the fastest path to the hero action (record-first search). Serves judges and later ops reviewers from one coherent system.
- Sacrifices: none of the three is taken to its extreme; the production-line framing can fight the record-first free navigation, so the shell must stay light and the sidebar must own navigation while the line framing only sets the visual story.

**Why the user chose this:**
User requested a hybrid of the three presented philosophies. This is the synthesized blend: Production Line as the structural backbone, Evidence Console as the aesthetic/trust layer, Record-First as the interaction model on Explorer + Review.

---

## Rejected Alternative 1: The Evidence Console (pure)

**Metaphor:** a forensic operator console where every surface is a layer over the evidence chain.
**Feature mapping summary:** dashboard = headline readout; explorer = case files; abstention = signed refusals; review = decision desk; export = official filing.
**Trade-offs:** Good at maximum demo trust and the dark engineering aesthetic; reads more like a verification tool than a catalog product.
**Why rejected:** Too forensic; risks feeling engineering-heavy to an ops buyer. Folded its trust/aesthetic layer into the hybrid instead.

## Rejected Alternative 2: Record-First Explorer (pure)

**Metaphor:** the part record is the atom; search is the front door and everything is a facet of the records.
**Feature mapping summary:** explorer = home; dashboard = aggregates; review = inline on the record; abstention = the record's unresolved panel.
**Trade-offs:** Good at shortest click-path to the hero interaction; can feel like a powerful lookup tool rather than a product.
**Why rejected:** Subordinates the linear product journey and the headline-numbers moment. Folded its search/drill-down interaction model into the hybrid instead.