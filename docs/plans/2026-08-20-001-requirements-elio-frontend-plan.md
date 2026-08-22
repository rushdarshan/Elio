---
title: ELIO Frontend - Plan
type: feat
date: 2026-08-20
topic: elio-frontend
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: ce-brainstorm
execution: code
---

## Goal Capsule

* **Objective**: Define the product requirements and design system constraints for the ELIO Next.js visual data-ops frontend web application.
* **Product Authority**: rushdarshan/Elio
* **Open Blockers**: None.

---

## Product Contract

> [!NOTE]
> **Product Contract preservation**: Product Contract unchanged from brainstorm.

### Summary
A hosted Next.js web application that visualizes the frozen, evidence-gated ELIO catalog data, providing judges with a visual custody chain and operations reviewers with a split-pane review worklist to perform inline overrides.

### Problem Frame
The ELIO catalog pipeline is proven and delivers results, but its verification outputs only exist as static files. Without an interactive ops dashboard, judges cannot easily trace generated values, and reviewers cannot edit or export corrected files.

### Key Decisions
* **Two-Tone Theming**: Light mode cream/lime aesthetic for the judge landing and upload screen; Dark mode slate/indigo aesthetic for the interactive dashboard and review cockpit.
* **Slide-over Drawer for Verification**: Clicking any cell in the Evidence Explorer slides open a drawer on the right rather than opening a modal or expanding row inline.
* **Inline Edit Actions**: Integrating the "Edit Value" input fields and "Override" buttons directly inside the Custody Drawer to merge the explorer and review workflows.

---

### Requirements

#### Upload & Intake
- R1. Accept CSV uploads containing `Mfg_Part_Num`, `Part_Desc`, `Part_Manuf`, `E1_Brand`, `Unilog_Brand`, and `DIB_Brand`.
- R2. Enforce dry-run validation against the 252-column export schema on upload.
- R3. Display a progress bar during processing and output the file's SHA-256 hash and row count.

#### Dashboard & Performance
- R4. Render headline metrics: attributes per row, gold cells byte-exact matches, validation fails, and untraceable values.
- R5. Provide a toggle switch to filter data between the 50-row Demo and the 1000-row Full holdout.

#### Evidence Drawer & Custody Chain
- R6. Clicking an explorer cell slides out the Custody Drawer in a dual-pane layout.
- R7. Left pane shows metadata: Confidence, URL, Page, Character Span. Right pane shows the raw text block with the matching characters highlighted.
- R8. Format all MPNs, hashes, page spans, and raw snippets in `Geist Mono` font.
- R9. Cells where the pipeline abstained display the specific validation or missing evidence reason.

#### Review Operations & Export
- R10. Allow reviewers to edit attributes inside the Custody Drawer, highlighting changed cells with an amber indicator.
- R11. Save edited overrides to a local `decision_log.jsonl` file.
- R12. Export the reviewed catalog as a CSV/JSON file sanitized against formula-injection.

---

### Key Flows

- F1. Evidence Custody Check
  - **Trigger**: Operator clicks a cell in the explorer.
  - **Actors**: Ops Reviewer, Judge.
  - **Steps**: The slide-over drawer opens from the right; structured metadata loads in the left panel; raw text page with highlighted offsets loads in the right panel; the edit input highlights the current value.
  - **Covered by**: R6, R7, R8, R10.

---

### Acceptance Examples

- AE1. Validating Ceiling Tile Conversion
  - **Covers R7, R8.**
  - **Given**: An input row with MPN `1728ABL` and Part_Desc `2x2 Black Fine Fissured 1728BL`.
  - **When**: The explorer cell for Size `2 ft x 2 ft` is clicked.
  - **Then**: The drawer right panel displays the snippet `2x2 Black Fine Fissured` with the text `2x2` highlighted in yellow.

- AE2. Blacklisted Distributor Flag
  - **Covers R9.**
  - **Given**: An input row with Part_Manuf `Palmer Donavin Mfg Company (PALDO)`.
  - **When**: The brand field is displayed.
  - **Then**: The brand is marked `Unbranded` with a warning tooltip: `Distributor blacklist: Palmer Donavin`.

---

## Planning Contract

### Key Technical Decisions
* **Next.js & TypeScript Setup**: Scaffold a greenfield Next.js v15 App Router app in `elio-frontend/` directory with TypeScript enabled.
* **Tailwind CSS v4 Configuration**: Integrate Tailwind CSS v4 in the application to enforce utility-first styling matching the design references.
* **Server-Side Pipeline Invocation**: API route triggers the local python pipeline (`app.py`) via `child_process` execution of `python app.py --file <path>`.
* **State Management**: Use React context for active catalog data, metrics recalculations, and reviewer decisions stack before writing to `decision_log.jsonl`.
* **Static File Fallbacks**: Read `data/evidence.json` and `data/metrics.json` directly as pre-bundled assets for the static demo dashboard toggle.

### Assumptions
* **Browser Sandbox**: The app runs locally on `http://localhost:3000` with direct file system access permissions to write `decision_log.jsonl`.
* **Python Environment**: The active Python environment has all `unihack_catalog` dependencies pre-installed.

### Open Questions
* **[DEFERRED] Pipeline Execution Time**: How should the UI handle execution times exceeding 10 seconds for the full 1000-row dataset? (Out of scope for V1 demo, but deferred for later UX design).

---

## Implementation Units

### U1. Scaffolding & Project Setup
* **Goal**: Initialize the Next.js TypeScript application structure in the `elio-frontend` directory with Tailwind CSS v4.
* **Requirements**: R1, R8.
* **Dependencies**: None.
* **Files**:
  - `elio-frontend/package.json`
  - `elio-frontend/tsconfig.json`
  - `elio-frontend/src/app/layout.tsx`
  - `elio-frontend/src/app/page.tsx`
* **Approach**: Bootstraps the project using `npx create-next-app` under the custom subdirectory, specifying TypeScript, Tailwind CSS, ESLint, and Next.js App Router. Registers the baseline fonts (`Plus Jakarta Sans` and `Geist Mono`).
* **Test scenarios**:
  - Happy Path: App starts successfully on `localhost:3000` and displays page with Tailwind styles.
* **Verification**: Run `npm run dev` in `elio-frontend` and view root page.

### U2. API Route & Backend Integration
* **Goal**: Implement the API route that runs the Python parsing pipeline on upload.
* **Requirements**: R1, R2, R3.
* **Dependencies**: U1.
* **Files**:
  - `elio-frontend/src/app/api/run/route.ts`
* **Approach**: Writes a Next.js App Router POST handler that saves the uploaded CSV file temporarily, checks for required columns, dry-runs schema compatibility, spawns `python app.py` on it, and streams console log updates back.
* **Test scenarios**:
  - Happy Path: Valid CSV upload processes successfully and returns JSON logs.
  - Edge Case: Missing required columns (e.g. `Mfg_Part_Num`) returns a 400 Bad Request with a clear list of missing headers.
  - Error Path: Python script exits with non-zero code; API catches output stderr and returns 500 error body.
* **Verification**: Mock a POST request using `curl` and inspect response payload.

### U3. UI Layout & Upload Surface
* **Goal**: Build the light-mode landing page with drag-and-drop file upload using Tailwind v4.
* **Requirements**: R1, R2, R3.
* **Dependencies**: U1, U2.
* **Files**:
  - `elio-frontend/src/app/globals.css`
  - `elio-frontend/src/components/UploadArea.tsx`
* **Approach**: Follows the cream/lime editorial typography layout using Tailwind v4 utilities. Provides a drag-and-drop box that parses files client-side first for header checks, then sends them to the API route, displaying a progress bar.
* **Test scenarios**:
  - Happy Path: Dropping a valid CSV transitions UI to "Processing..." progress state.
  - Edge Case: Dropping an invalid file format (e.g., `.png`) triggers a validation error toast.
* **Verification**: Drag `demo_input_50.csv` to the upload zone and verify transition to processing state.

### U4. Acceptance Dashboard Cockpit
* **Goal**: Implement the dark-mode cockpit dashboard and metrics display.
* **Requirements**: R4, R5.
* **Dependencies**: U3.
* **Files**:
  - `elio-frontend/src/components/MetricsDashboard.tsx`
* **Approach**: Swaps styles to dark theme. Renders the Bento grid metrics cards for precision and coverage, with the capsule switch to filter data between the Demo and Full holdouts.
* **Test scenarios**:
  - Happy Path: Clicking "Full" toggle updates the total cards to reflect full dataset metrics.
* **Verification**: Toggle the dataset sizes and inspect metrics updates.

### U5. Evidence Explorer & Custody Drawer
* **Goal**: Implement the paginated search table and slide-over custody drawer.
* **Requirements**: R6, R7, R8, R9.
* **Dependencies**: U4.
* **Files**:
  - `elio-frontend/src/components/EvidenceExplorer.tsx`
  - `elio-frontend/src/components/CustodyDrawer.tsx`
* **Approach**: Renders the main results table. Clicking any cell slides out a right-anchored pane. Displays structured metadata on the left of the pane, and the raw text offsets highlighted in yellow on the right.
* **Test scenarios**:
  - Covers AE1.
  - Happy Path: Clicking a size cell opens the drawer and highlights the verbatim source matching characters.
  - Covers AE2.
  - Edge Case: Clicking an abstained cell displays the custom warning badge with the specific reason (e.g., blacklisted distributor).
* **Verification**: Click cell for size `2 ft x 2 ft` and verify drawer highlights `2x2` in yellow.

### U6. Review Overrides & Export
* **Goal**: Implement the inline override form and sanitizing CSV exporter.
* **Requirements**: R10, R11, R12.
* **Dependencies**: U5.
* **Files**:
  - `elio-frontend/src/components/ReviewControls.tsx`
* **Approach**: Mounts the override text inputs inside the drawer. On submit, recalculates front-end metrics, highlights the cell with an amber border, logs to `decision_log.jsonl`, and exports a sanitized CSV download.
* **Test scenarios**:
  - Happy Path: Overriding a brand value writes the decision, flags the cell, and updates the dashboard metrics.
  - Edge Case: Export sanitizes all fields prefixed with `=`/`+`/`-` to prevent formula injection.
* **Verification**: Perform an override, export the CSV, and verify the override cell is marked correctly.

---

## Verification Contract

Run the following test suites to verify implementation unit correctness:
* Jest Component Suite:
  ```bash
  npm run test
  ```
* Next.js build validation:
  ```bash
  npm run build
  ```

---

## Definition of Done

* App builds and runs locally with zero compiler or linting errors.
* Uploading any CSV triggers the python backend and loads the dashboard.
* Overrides recalculate local metrics and save logs to `decision_log.jsonl`.
* No experimental or dead-end code branches left in the repository.
