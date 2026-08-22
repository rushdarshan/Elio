# Q&A log — elio-frontend

**Raw ask:** "we are going create frontend for this project & 'c:\Users\rushd\Downloads\Jesus WIn\docs' & 'c:\Users\rushd\Downloads\Jesus WIn\graphify-out'"

**Mode:** default

## Round 1 — Problem & audience + Core behavior

### Q: Who is the frontend primarily built for? (judges vs ops)
- **Chosen:** Judges (demo wow)
- **Notes:** Evidence traceability and headline numbers front-and-center.

### Q: What is the single most important action a user performs?
- **Chosen:** Explore evidence per value
- **Notes:** Search a part → see each extracted value with source trace, abstention reason, verification state.

### Q: How should the frontend be built?
- **Chosen:** React/Next.js app
- **Notes:** Real framework, componentized; build pipeline + dev server acceptable.

### Q: Which surfaces belong in THIS frontend? (multi-select)
- **Chosen:** Evidence explorer, Acceptance dashboard, Upload & run, Decision review queue
- **Notes:** User's "Other" answer (verbatim):
  - Keep: evidence explorer (hero), acceptance dashboard, decision review queue, upload & run.
  - Move out of main flow: codebase graph view → developer/debug page ("Developer → Architecture").
  - Add #6: Export & delivery — 252-col schema validation, rows processed, accepted/reviewed/abstained counts, CSV/JSON download, "ready for import" status.
  - Add #7: Abstention / Trust view — why Elio refused a value (missing evidence, conflicting evidence, unsupported category, validation failure).
  - Final flow: UPLOAD & RUN → ACCEPTANCE DASHBOARD → EVIDENCE EXPLORER → REVIEW QUEUE → ABSTENTION/TRUST → EXPORT & DELIVERY.
  - No generic Home/About/How-it-works/Settings screens — "should feel like a working catalog operations product, not a showcase."

## Round 2 — UX / states + Platforms & constraints

### Q: How should users move between the 6 surfaces?
- **Chosen:** Sidebar nav + free navigation
- **Notes:** Persistent sidebar, any surface reachable anytime — better for a daily ops tool.

### Q: Where does the frontend read its data?
- **Chosen:** Hybrid: static for demo + API for upload
- **Notes:** Prebuilt artifacts for the demo run; API backend only for the Upload & Run surface.

### Q: How important is offline/airgapped operation?
- **Chosen:** Deploy online (judges will use it live)
- **Notes:** Fine if there's internet at the demo; don't over-engineer for offline.

### Q: Data volume — 50-row demo or 1000-row full export?
- **Chosen:** Both, with a size toggle
- **Notes:** Demo mode default, full mode opt-in.

## Round 3 — Scope boundaries + Edge cases & failure

### Q: What input does Upload & Run accept, and how strictly should it validate?
- **Chosen:** CSV only, strict
- **Notes:** CSV with the 6 required columns (Mfg_Part_Num, Part_Desc, Part_Manuf, E1/Unilog/DIB_Brand); refuse upload with clear errors if columns missing.

### Q: How does the pipeline run — synchronous or async?
- **Chosen:** Synchronous for demo rows
- **Notes:** Run inline with a progress bar; cap rows so the judge sees results fast.

### Q: What happens when a user approves/rejects/edits a value in the Review Queue?
- **Chosen:** Yes + written back to a log
- **Notes:** Decisions persist to a decision log file (extends the existing decision_log.jsonl pattern); export reflects the change.

### Q: Does the frontend need users/roles/permissions?
- **Chosen:** No auth — single operator
- **Notes:** Demo runs are operator-driven; no login, no roles. Simplest possible.

## Round 4 — Visual design + Edge-state handling + Performance/a11y + Deployment

### Q: What visual direction?
- **Chosen:** Mixed: dark app + light landing
- **Notes:** Dark app surfaces, light marketing/pitch landing — two-tone.

### Q: How important are in-between states (empty, loading, error, permission-denied)?
- **Chosen:** Handle all states everywhere
- **Notes:** Empty/loading/error states on every surface; upload errors are first-class UI with recovery paths.

### Q: What accessibility/performance bar?
- **Chosen:** Baseline a11y + fast render
- **Notes:** Keyboard nav, focus states, sufficient contrast, semantic HTML; 1000-row table virtualized or paginated.

### Q: Where is this deployed?
- **Chosen:** Render or Railway
- **Notes:** Hosted Node/Next.js on Render or Railway; not Vercel, not static export.