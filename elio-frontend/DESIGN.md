---
name: ELIO
description: Evidence-gated catalog intelligence console
colors:
  primary: "#2563eb"
  primary-soft: "#1d4ed8"
  neutral-bg-dark: "#09090b"
  neutral-surface-dark: "#18181b"
  neutral-hover-dark: "#27272a"
  neutral-text-dark: "#f4f4f5"
  neutral-text-secondary-dark: "#a1a1aa"
  neutral-bg-light: "#fcfbf7"
  neutral-surface-light: "#f7f5f0"
  neutral-text-light: "#18181b"
  neutral-text-secondary-light: "#52525b"
  semantic-verified: "#22c55e"
  semantic-review: "#f59e0b"
  highlight-snippet: "#f59e0b"
typography:
  display:
    fontFamily: "var(--font-geist-sans), ui-sans-serif, system-ui, sans-serif"
    fontWeight: 900
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  title:
    fontFamily: "var(--font-geist-sans), ui-sans-serif, system-ui, sans-serif"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "var(--font-geist-sans), ui-sans-serif, system-ui, sans-serif"
    fontWeight: 400
    lineHeight: 1.6
  mono:
    fontFamily: "var(--font-geist-mono), ui-monospace, monospace"
    fontWeight: 400
rounded:
  sm: "6px"
  md: "10px"
  lg: "16px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral-bg-dark}"
    rounded: "{rounded.sm}"
    padding: "12px 20px"
    typography: "{typography.mono}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.neutral-text-dark}"
    rounded: "{rounded.sm}"
    padding: "8px 12px"
    typography: "{typography.body}"
  chip:
    backgroundColor: "transparent"
    textColor: "{colors.neutral-text-secondary-dark}"
    rounded: "{rounded.sm}"
    padding: "6px 10px"
    typography: "{typography.mono}"
  card:
    backgroundColor: "{colors.neutral-surface-dark}"
    textColor: "{colors.neutral-text-dark}"
    rounded: "{rounded.md}"
    padding: "{spacing.lg}"
---

# Design System: ELIO

## 1. Overview

**Creative North Star: "The Ledger"**

Every surface in ELIO is a page from a provenance ledger. The dark cockpit is the working book: rows, hairline rules, mono numerals, and verdicts recorded in ink. The light landing is the front cover: crisp, calm, one blue mark of ownership. Nothing on any page is decorative; each element is either an entry, a rule, or a recorded verdict.

The system is deliberately unfashionable. It rejects the AI-slop dashboard reflex: no bento-card grids, no invented metrics, no gradient accents, no glowing badges, no infinite pulse animations. It equally rejects neon crypto/cyberpunk styling: no glow, no garish gradients, no tech-larp. ELIO's confidence comes from what the pipeline actually proves, and the visual system exists to make that proof legible.

Color is a semantic vocabulary, not decoration. Blue is the interactive hand of the console. Green marks values verified against source evidence. Amber marks refusals, escalations, and review states. Neutrals are the bench itself. Any color that does not carry one of those meanings is a mistake.

**Key Characteristics:**
- Dark working surface, light front cover; two tones, one identity.
- Mono numerals and identifiers for every data point; sans for prose.
- Hairline rules separate; hover-lift and the drawer separate deeper.
- Motion is a one-beat acknowledgment (drawer in, hover lift), never a loop.
- The honesty contract is visual: abstentions are amber and explained, never blank.

## 2. Colors

A semantic vocabulary on a neutral bench: dark zinc for the working surface, warm near-white for the cover, and three verdict colors that each own one meaning and never leak across roles.

### Primary
- **Brand Blue** (#2563eb): interaction only. Links, active states, the upload action, the interactive hand of the console. Never used to decorate a static element. In depth, **Deep Blue** (#1d4ed8) for hover states of blue surfaces.

### Secondary
- **Verified Green** (#22c55e): evidence-verified status only. Values that carry a source span, schema-verified states. Never used for generic success confetti.

### Tertiary
- **Review Amber** (#f59e0b): refusal, escalation, and review states. Abstained values, escalated rows, refusals with reasons. Amber always comes with a stated reason, never a bare badge.

### Neutral
- **Ledger Black** (#09090b): the working surface. Never pure black; tinted toward blue.
- **Entry Surface** (#18181b): cards, panels, rows on the bench.
- **Hover Surface** (#27272a): hover/toggle-background step above Entry Surface.
- **Ink Light** (#f4f4f5): primary text on dark.
- **Ink Muted** (#a1a1aa): secondary text, labels, footnotes on dark.
- **Paper** (#fcfbf7): the light landing surface; warm near-white, never pure white.
- **Paper Accent** (#f7f5f0): secondary light surfaces, icon wells.
- **Ink Dark** (#18181b): primary text on light.
- **Ink Dark Muted** (#52525b): secondary text on light.

### Named Rules
**The One Meaning Rule.** Each verdict color owns exactly one meaning and never leaks. Green never decorates a header; amber never marks a generic warning; blue never marks a status.

**The No-Pure-White Rule.** The landing surface is warm paper, never #ffffff. Pure white reads as unowned SaaS chrome.

## 3. Typography

**Display Font:** Geist Sans (with system-ui fallback)
**Body Font:** Geist Sans (with system-ui fallback)
**Label/Mono Font:** Geist Mono (with ui-monospace fallback)

**Character:** A precise sans for prose, a utilitarian mono for data. The pairing says "instrument" not "magazine": the sans is confident but quiet, the mono is where the numbers live.

### Hierarchy
- **Display** (900, clamp up to ~3.75rem, 1.1, -0.03em): the landing headline and the largest dashboard numerals. Appears rarely; its rarity is its power.
- **Title** (700, ~1.125rem, 1.2): section headers, card titles, panel headings.
- **Body** (400, ~0.875-1rem, 1.6): prose on both surfaces. Light body capped at ~65ch.
- **Label** (400, 0.75rem, mono, uppercase with letterspacing for section labels): the uppercase kicker style used across dashboard and drawer labels.
- **Mono Data** (400, 0.75-0.875rem, mono): every number, identifier, metric, MPN, tag, and footnote.

### Named Rules
**The Mono Data Rule.** All data is mono. Any number that is not in mono type is a heading, not a datum.

## 4. Elevation

Hybrid: flat at rest, shadow only where the ledger physically lifts. The bench is flat; entries sit on it with hairline rules, not shadows. Depth appears in two moments: the evidence drawer slides in from the right on a raised plane with a soft ambient shadow, and the light landing's upload card lifts slightly from the paper.

### Shadow Vocabulary
- **Drawer Shadow** (`0 25px 50px -12px rgba(0,0,0,0.35)`): the evidence drawer only.
- **Lift Shadow** (`0 4px 12px rgba(0,0,0,0.12)`): the landing upload card at rest; small hover-lift on interactive cards.

### Named Rules
**The Flat-By-Default Rule.** Surfaces are flat at rest. Shadows exist only where the ledger physically lifts (drawer, upload card, hover). Never a glow, never a neon edge.

## 5. Components

### Buttons
- **Shape:** Gently squared corners (6px radius).
- **Primary:** Brand Blue fill, dark ink text, mono label, 12px 20px padding. Hover shifts to Deep Blue. Used for the single forward action per screen (Upload, Download).
- **Ghost / Secondary:** Transparent, Ink Light text, 8px 12px padding. Hover tints the surface. Used for in-console navigation and secondary actions.

### Chips / Tags
- **Style:** Transparent background, hairline border, mono uppercase label. One verdict color per chip, always matching its meaning (verified green, review amber, brand blue for interactive).
- **State:** Segmented filters use a filled Hover Surface for the active segment and Ink Muted for inactive.

### Cards / Containers
- **Corner Style:** Gently squared (10px radius); the landing surface cards sit at 16px for a softer cover feel.
- **Background:** Entry Surface on the bench; white on the paper landing.
- **Shadow Strategy:** Flat by default; the drawer and upload card carry the only shadows (see Elevation).
- **Border:** Hairline (1px at low opacity) on the bench; subtle zinc hairline on paper.
- **Internal Padding:** 24px on the bench cards; 24px on landing cards.

### Inputs / Fields
- **Style:** Hairline border on the bench surface, mono hint text.
- **Focus:** Border shifts to Brand Blue; no glow, no ring-thickening theatrics.
- **Error:** Muted red border with the specific reason in plain text; never a bare "error" banner.

### Navigation
- **Sidebar (bench):** Column of mono labels, Brand Blue on active, Ink Muted at rest, Hover Surface on hover. Version/pipeline tag at the foot in mono.
- **Landing header:** Minimal wordmark + one quiet note; no nav sprawl.

### The Custody Drawer (Signature)
The record's evidence pane, slid in from the right on the Drawer Shadow. Left pane: attribute entries, each with its extracted value and verification state, selectable. Right pane: the raw evidence for the selected attribute: source link, page reference, and verbatim snippet with the matching value highlighted in Review Amber. When nothing is selected, the right pane holds a quiet instruction. This is the product's thesis in one component: value, source, and the highlighted span that proves the connection.

## 6. Do's and Don'ts

### Do:
- **Do** derive every number on screen from the loaded data. A metric that cannot be computed must not exist.
- **Do** show abstentions as amber refusals with a stated reason; the reason is the product's personality.
- **Do** use mono for every datum, identifier, and footnote.
- **Do** use Brand Blue for interaction and only interaction.
- **Do** let flat surfaces carry hairline rules; reserve shadows for the drawer and the upload card.
- **Do** cap light-surface prose at ~65ch.
- **Do** keep the two surfaces consistent: the same verdict colors, the same mono voice, on both sides of the light/dark door.

### Don't:
- **Don't** build bento-card grids, invent metrics, use gradient accents, glowing badges, or infinite pulse animations (AI-slop dashboard anti-reference).
- **Don't** use glow, garish gradients, or tech-larp styling (neon crypto/cyberpunk anti-reference).
- **Don't** use an em dash anywhere. Comma, colon, semicolon, period, or parentheses instead. Also not `--`.
- **Don't** leave a border-left or border-right greater than 1px as a colored accent stripe. Use full borders, background tints, or nothing.
- **Don't** use gradient text (`background-clip: text`). Emphasis is weight and size, never a gradient.
- **Don't** hardcode a metric that pretends a run happened. Zero-filled dashboards are lies.
- **Don't** show a refusal as a blank cell. Every abstention is amber and explained.
- **Don't** use pure black or pure white anywhere; tint neutrals toward the brand.
- **Don't** name-drop product aesthetics ("like Linear, like Stripe"); describe the quality instead.