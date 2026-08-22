# Upload & Run — Screen Prompts

_Each block below is self-contained. Copy one block, paste into Stitch / Figma AI / Pencil / Claude Design._

---

## Upload Landing — Empty State

````
**What this screen is for:**
The intake hatch of the product: a light, pitch-quality landing page where the user hands over a product catalog CSV to be enriched and evidence-traced.

**What's visible:**
A calm light surface. At the top, a small wordmark and a subtle "Target: Unihack Gold Standard" note. Centered hero: one bold, confident headline ("Every catalog value, traced to its source.") with a short supporting sentence explaining the product enriches catalogs from manufacturer evidence and abstains with a reason when it cannot trace a value. Below the hero, a large dashed drop zone — roomy, generous padding, an upload icon, "Upload your product catalog CSV" with a small mono-style hint about dragging or browsing. Next to it, a Browse Files button. Under the drop zone, two quiet informational cards side by side: one about structured verification (every property maps to a re-fetchable document snippet and offset span), one about gold-standard alignment (continuous dry-run checks against the 252-column export standard).

**What the user can do:**
- Primary: drag a CSV onto the drop zone, or click Browse Files and pick a file.
- Secondary: read the two info cards; view the dataset-size toggle only after a run exists.

**Feel:**
Crisp light theme, near-white warm surface, one blue accent used sparingly for interactive elements, black headline type, generous whitespace, industrial-precise but calm — an engineering product that respects the reader. Mono type only for technical hints and numbers.

**State context:**
This is the empty state — no file has been uploaded and nothing has been processed yet.

**Critical affordances:**
The drop zone must feel like a real target: obvious affordance to drop or browse, clear visual feedback on drag-over (the zone visibly activates). The headline must be the strongest element on the page. Keep the whole page scrollable and self-contained — no chrome, no sidebar.
````

---

## Upload Landing — Drag-Over

````
**What this screen is for:**
Same intake hatch, but the user is actively dragging a file — the screen must confirm that dropping here works.

**What's visible:**
The drop zone is now in an activated state: the dashed border strengthens to the blue accent, the background tints, the icon circle inverts to the accent color, and the whole zone lifts slightly. Everything else stays the same.

**What the user can do:**
- Primary: release the file to drop it.
- Secondary: drag away to cancel (zone returns to idle).

**Feel:**
The activation should feel physical and immediate — one beat of motion, no elaborate animation. Crisp light theme, single blue accent.

**State context:**
Transient state — the user is mid-drag.

**Critical affordances:**
The drop target is the whole dashed zone; the entire zone must accept the drop, not just a small sub-area.
````

---

## Upload — Loading (Pipeline Running)

````
**What this screen is for:**
The user has dropped a valid file and the enrichment pipeline is running — the screen shows progress honestly.

**What's visible:**
Inside the upload card, a progress row appears below the drop zone: a mono label ("Running Python ingestion pipeline...") with a percentage, and a thin progress bar filling beneath it. The drop zone remains visible but disabled.

**What the user can do:**
- Nothing but wait; the run is synchronous and cannot be cancelled.

**Feel:**
Deterministic, not flashy: a plain thin bar at a believable step, no spinner theatrics, no fake stage names. Calm engineering tone.

**State context:**
Loading state — file accepted, execution in progress.

**Critical affordances:**
The progress must reflect a real synchronous run; do not imply cancellable jobs, streaming, or parallel stages that do not exist. The bar should feel like a measured single pass.
````

---

## Upload — Error (Validation / Execution Failed)

````
**What this screen is for:**
The user handed over a file the pipeline cannot process — the screen states exactly why, without jargon theater.

**What's visible:**
A compact error panel inside the upload card: a warning icon, a clear title ("Pipeline Execution Failed"), and the specific failure reason in plain text. The drop zone is re-enabled so the user can try another file.

**What the user can do:**
- Primary: drop or browse a different file and retry.
- Secondary: read the failure reason.

**Feel:**
Calm red, not alarm: a muted error surface, honest copy, no skull-and-bones styling. Light theme, one semantic red used only for failure.

**State context:**
Error state — upload or execution failed (bad schema, missing required columns, or a pipeline crash).

**Critical affordances:**
The failure reason must be specific enough to act on (e.g., missing required columns named out loud). The retry path must be immediate — the drop zone is live again with no refresh needed.
````

---

## Upload — Success (Run Completed)

````
**What this screen is for:**
The pipeline finished cleanly — this is the handoff beat from intake to the rest of the console.

**What's visible:**
A brief completion signal: the upload card resolves into a short success confirmation (rows processed, run accepted), and the console chrome — sidebar with the feature navigation (Dashboard, Explorer, Review, Abstention, Export) and a dataset-size toggle (Demo / Full / Uploaded) — becomes available so the user can step into the results.

**What the user can do:**
- Primary: move into the Dashboard to see the headline readout.
- Secondary: switch dataset size (Demo / Full / Uploaded) from the chrome.

**Feel:**
The moment the light landing hands off to the dark console. Completion reads as one confident confirmation, then the interface shifts tone: dark surfaces, mono numerals, single blue accent.

**State context:**
Success state — the run completed; the console shell is now live.

**Critical affordances:**
The transition from light landing to dark console must feel like a deliberate door opening, not a theme toggle. The uploaded dataset becomes selectable alongside the built-in Demo and Full sets.
````