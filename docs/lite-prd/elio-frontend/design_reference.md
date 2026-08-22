# ELIO Frontend — Design Reference Specification

This document details the visual guidelines, typography system, color tokens, and layout components for the ELIO Frontend application, built in accordance with the `design-taste-frontend` and `gpt-taste` design engineering directives.

---

## 1. The Design Read & Dial Configuration

* **Design Read**: A hybrid two-tone system comprising a light-themed, high-editorial landing page for judges, and a dark-themed, high-density data-ops cockpit for operations reviewers, leaning toward custom Bento grid components, glassmorphism panels, and GSAP sticky scroll transitions.
* **Layout Dials**:
  * `DESIGN_VARIANCE: 7` (Asymmetric widgets, off-center grids)
  * `MOTION_INTENSITY: 6` (GSAP scroll-reveals, skeletal transitions, card hovers)
  * `VISUAL_DENSITY: 8` (High-density tabular data, side-by-side custody grids, and status charts)

---

## 2. Design System Map (Tailwind v4 & Radix Tokens)

### 2.A Color Palette
We utilize a strict two-tone theme. Sections do not toggle randomly; rather, the app features a clear boundary between the public landing section (Light Mode) and the operational dashboards (Dark Mode).

#### Dark Mode (Operations Surfaces)
* **Background Canvas**: Slate-950 (`#020617` / `#09090b` base)
* **Card & Panel Surface**: Slate-900/800 (`#0f172a` / `#1e293b`) with a 1px border (`border-white/10`) and subtle top-highlight inset shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.05)]`).
* **Primary Accents**:
  * Electric Green (`#22c55e` / Emerald-500): Indicates fully supported/verified evidence.
  * Electric Violet/Indigo (`#6366f1` / `#a855f7`): Primary brand highlight, charts, and buttons.
  * Soft Amber (`#f59e0b`): Indicates manual review flags and queue escalations.
  * Crimson (`#ef4444`): Indicates contradicted evidence or validation fails.

#### Light Mode (Landing & Pitch Page)
* **Background Canvas**: Muted Cream / Off-White (`#fcfbf7` / `#f7f5f0`)
* **Supporting Accents**: Sage Green (`#16a34a` / `#15803d`) and Soft Charcoal (`#1e293b`).

### 2.B Typography System
* **Primary Sans Font**: `Geist Sans` & `Plus Jakarta Sans`
* **Technical Monospace Font**: `Geist Mono` (Mandatory for all MPNs, Content Hashes, Page Spans, Snippet Traces, and raw logs).
* **Editorial Serif (Landing Page Headlines only)**: `Domaine Display` or `Playfair Display` (Italic variant only, used for emphasis, e.g., "*Visibility and Control*").

---

## 3. View Architectures & Layouts

### View 1: Landing & Upload Page (Light Mode)
*Inspired by the premium spacing and visual modules of Image 5.*
* **Hero layout**: Wide container (`max-w-5xl`), asymmetric split layout. Left side hosts a 2-line headline (`text-5xl font-semibold tracking-tight`), right side features a floating product widget.
* **Upload Card**: Bounded drag-and-drop area with a thin dashed border. Once a file is dropped:
  * Emits input filename, row count, and a SHA-256 hash.
  * Triggers a synchronous horizontal progress bar (`bg-indigo-600` on neutral slate).
  * Executes a dry-run check against the 252-column contract.

### View 2: Acceptance Dashboard (Dark Mode Cockpit)
*Inspired by the metrics grid of Image 1 and ribbon analytics of Image 2.*
* **Headline Metrics Bento Grid**:
  * Card 1: `Attributes/Row` (Display number: `2.16` in large Geist Sans font).
  * Card 2: `Gold Cells` (Display status: `118/118` byte-exact badge).
  * Card 3: `Dual-Pass Failures` (`0` in bright green).
  * Card 4: `Adversarial Accepted` (`589/589 @ 100%`).
* **Visual Progress Flow**: Stream ribbon charts displaying the flow of rows from Intake → Classification → Verification → Export.
* **Size Toggle**: A persistent capsule switch allowing users to filter between the `Demo Dataset (50 rows)` and the `Full Holdout (1000 rows)`.

### View 3: Evidence Explorer & Custody Chain (Dark Mode)
*Inspired by the stock tables of Image 2 and list layouts of Image 6.*
* **Paginated Grid**: Monospace-formatted table representing rows. Clicking a row expands an inline drawer.
* **Custody Card Drawer**: Open layout (flat, no cards-inside-cards) showing the 5-point custody chain:
  1. `Source Document`: Clickable `file:///` link.
  2. `Page Number`: `Page 1`.
  3. `Content Hash`: Monospace `sha256:7f9a2b...` snippet.
  4. `Character Span`: Highlighted span range `[104, 118]`.
  5. `Verbatim Snippet`: Boxed text block with yellow highlighting matching the exact extracted UOM or value.
* **Abstention Indicators**: Cells where the pipeline refused to guess are styled in muted orange text with tooltip reasons (e.g. `[Abstained: Missing Evidence]`).

### View 4: Operations Review Queue & Editor (Dark Mode)
*Inspired by the sidebar controls of Image 6.*
* **Queue List**: Left-aligned split screen. Left side lists parts requiring manual intervention, right side displays the full edit card.
* **Edit Card Action**:
  * Form inputs have labels aligned strictly above inputs.
  * Inputs are styled with slate-800 fields and active blue focus rings.
  * Changing a value and clicking "Approve" adds the change to the `decision_log.jsonl` log list and marks the cell with a subtle amber dot marker.

---

## 4. Interaction & Motion Directives

### 4.A GSAP Sticky-Stack Walkthrough
As the user scrolls down the landing page, 3 feature summary cards stack on top of each other dynamically to explain the trust-verbatim system:
* ScrollTrigger pins the stack wrapper at `start: "top top"`.
* Cards slide up sequentially from the bottom, fading previous cards out to `opacity: 0.5` and scaling them down to `scale: 0.95`.

### 4.B Tabular Hover States
* Hovering any row in the Evidence Explorer triggers a subtle background highlight (`bg-slate-800/50`) and scale transition on the search icon.
* Clickable badges scale down dynamically (`scale-98`) on click to simulate button tactile push.

### 4.C Skeletal Loaders
During CSV processing, metric cards and tables display animated pulsing outlines matching the structural borders rather than generic spinning loaders.
