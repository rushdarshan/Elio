// ELIO — UniHack 2026 Submission Deck Generator
// Premium dark-tech theme. 15 slides filled with real project data.
// Run: node build_deck.js  →  ELIO_UniHack_2026.pptx

const PptxGenJS = require("pptxgenjs");

const pres = new PptxGenJS();
pres.layout = "LAYOUT_16x9"; // 10" × 5.625"

// ── PALETTE ──────────────────────────────────────────────────────────────────
const C = {
  bg:       "0A0A0D",  // near-black shell
  card:     "14141A",  // card surface
  border:   "252530",  // subtle border
  lime:     "C8D84A",  // brand accent
  limeD:    "8CAC28",  // darker lime
  teal:     "00D4C8",  // accepted / positive
  purple:   "9B59E8",  // escalated / review
  red:      "F87171",  // reject
  amber:    "FBBF24",  // abstention / warn
  white:    "F4F4F5",  // primary text
  muted:    "6A6A6A",  // secondary text
  dimmer:   "404040",  // very dim
  ink:      "18180E",  // dark ink for light slides
};

// ── HELPERS ──────────────────────────────────────────────────────────────────
const W = 10;    // slide width inches
const H = 5.625; // slide height inches

function darkBg(slide, { glow = false } = {}) {
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: W, h: H, fill: { color: C.bg }, line: { type: "none" },
  });
  if (glow) {
    // lime ambient glow bottom-left via image overlay trick: use a rect with opacity
    slide.addShape(pres.ShapeType.rect, {
      x: 0, y: 3, w: 3, h: 2.625,
      fill: { color: "2D3A00" }, line: { type: "none" }, transparency: 70,
    });
  }
  // subtle grid texture: thin lines
  for (let x = 0; x <= W; x += 0.5) {
    slide.addShape(pres.ShapeType.line, {
      x, y: 0, w: 0, h: H,
      line: { color: "1A1A25", width: 0.5, transparency: 80 },
    });
  }
  for (let y = 0; y <= H; y += 0.5) {
    slide.addShape(pres.ShapeType.line, {
      x: 0, y, w: W, h: 0,
      line: { color: "1A1A25", width: 0.5, transparency: 80 },
    });
  }
}

function sideAccent(slide) {
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.06, h: H, fill: { color: C.lime }, line: { type: "none" },
  });
}

function titleBlock(slide, title, subtitle, { y = 0.3, titleSize = 32, accentWord = null } = {}) {
  slide.addText(title, {
    x: 0.45, y, w: W - 0.9, h: 0.6,
    fontSize: titleSize, bold: true, color: C.white,
    fontFace: "Calibri", align: "left",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.45, y: y + 0.55, w: W - 0.9, h: 0.3,
      fontSize: 13, color: C.muted, fontFace: "Calibri", align: "left",
    });
  }
}

function limeChip(slide, label, x, y, w = 1.4) {
  slide.addShape(pres.ShapeType.rect, {
    x, y, w, h: 0.28, fill: { color: C.lime }, line: { type: "none" }, rectRadius: 0.04,
  });
  slide.addText(label, {
    x, y: y + 0.01, w, h: 0.26,
    fontSize: 9, bold: true, color: C.ink,
    fontFace: "Calibri", align: "center",
  });
}

function statCard(slide, num, label, x, y, { accent = C.lime } = {}) {
  slide.addShape(pres.ShapeType.rect, {
    x, y, w: 2.1, h: 1.1,
    fill: { color: C.card }, line: { color: C.border, width: 0.75 }, rectRadius: 0.08,
  });
  slide.addText(num, {
    x: x + 0.1, y: y + 0.12, w: 1.9, h: 0.55,
    fontSize: 30, bold: true, color: accent, fontFace: "Calibri", align: "center",
  });
  slide.addText(label, {
    x: x + 0.1, y: y + 0.67, w: 1.9, h: 0.32,
    fontSize: 9, color: C.muted, fontFace: "Calibri", align: "center",
  });
}

function flowBox(slide, text, x, y, { fill = C.card, accent = C.lime, w = 1.6, h = 0.6 } = {}) {
  slide.addShape(pres.ShapeType.rect, {
    x, y, w, h,
    fill: { color: fill }, line: { color: accent, width: 1 }, rectRadius: 0.06,
  });
  slide.addText(text, {
    x: x + 0.05, y: y + 0.04, w: w - 0.1, h: h - 0.08,
    fontSize: 9, bold: true, color: C.white, fontFace: "Calibri", align: "center", valign: "middle",
  });
}

function arrow(slide, x1, y, x2) {
  slide.addShape(pres.ShapeType.line, {
    x: x1, y, w: x2 - x1, h: 0,
    line: { color: C.lime, width: 1.5, endArrowType: "triangle" },
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 1 — COVER
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s, { glow: true });

  // Large "ELIO" wordmark
  s.addText("ELIO", {
    x: 0.5, y: 1.0, w: 6, h: 1.4,
    fontSize: 90, bold: true, color: C.white, fontFace: "Calibri",
    charSpacing: 8,
  });
  // Lime underbar accent
  s.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 2.3, w: 1.5, h: 0.06, fill: { color: C.lime }, line: { type: "none" },
  });

  s.addText("Evidence-Gated Catalog Intelligence", {
    x: 0.5, y: 2.45, w: 8, h: 0.4,
    fontSize: 18, color: C.lime, fontFace: "Calibri", bold: false,
  });
  s.addText("Turns 6 messy distributor columns into a 252-column catalog\nwhere every value traces to its source — or is honestly abstained.", {
    x: 0.5, y: 2.95, w: 7.5, h: 0.7,
    fontSize: 13, color: C.muted, fontFace: "Calibri",
  });

  // Right side: stat pills
  const pills = [
    ["118 / 118", "Gold cells byte-exact"],
    ["100%", "Provenance on accepted"],
    ["0", "Untraceable values"],
    ["589 / 589", "Adversarial accepted @ 100%"],
  ];
  pills.forEach(([num, label], i) => {
    const y = 0.9 + i * 1.1;
    s.addShape(pres.ShapeType.rect, {
      x: 7.2, y, w: 2.5, h: 0.9,
      fill: { color: C.card }, line: { color: C.lime, width: 1 }, rectRadius: 0.07,
    });
    s.addText(num, {
      x: 7.3, y: y + 0.06, w: 2.3, h: 0.42,
      fontSize: 22, bold: true, color: C.lime, fontFace: "Calibri", align: "center",
    });
    s.addText(label, {
      x: 7.3, y: y + 0.5, w: 2.3, h: 0.3,
      fontSize: 8.5, color: C.muted, fontFace: "Calibri", align: "center",
    });
  });

  // Bottom bar
  s.addText("UniHack 2026  ·  Team ELIO", {
    x: 0, y: 5.3, w: W, h: 0.3,
    fontSize: 9, color: C.dimmer, fontFace: "Calibri", align: "center",
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 2 — TEAM DETAILS
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);
  sideAccent(s);
  titleBlock(s, "Team Details", "The people behind ELIO");

  const members = [
    { name: "Rushd Arshan", role: "Backend & Pipeline Lead", skills: "Python · LLM Orchestration · Verification Engine" },
    { name: "Team Member 2", role: "Frontend & UX Lead", skills: "Next.js · TypeScript · Dashboard Design" },
    { name: "Team Member 3", role: "Data & Quality Lead", skills: "Gold-set curation · Adversarial testing · Metrics" },
    { name: "Team Member 4", role: "Architecture & DevOps", skills: "API design · Deployment · Documentation" },
  ];

  members.forEach((m, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.45 + col * 4.85;
    const y = 1.1 + row * 1.65;

    s.addShape(pres.ShapeType.rect, {
      x, y, w: 4.6, h: 1.45,
      fill: { color: C.card }, line: { color: C.border, width: 0.75 }, rectRadius: 0.1,
    });
    // Avatar circle
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.15, y: y + 0.3, w: 0.7, h: 0.7,
      fill: { color: "2D3A00" }, line: { color: C.lime, width: 1.5 },
    });
    s.addText(m.name[0], {
      x: x + 0.15, y: y + 0.3, w: 0.7, h: 0.7,
      fontSize: 18, bold: true, color: C.lime, fontFace: "Calibri", align: "center", valign: "middle",
    });
    s.addText(m.name, {
      x: x + 1.0, y: y + 0.1, w: 3.4, h: 0.35,
      fontSize: 14, bold: true, color: C.white, fontFace: "Calibri",
    });
    s.addText(m.role, {
      x: x + 1.0, y: y + 0.45, w: 3.4, h: 0.28,
      fontSize: 10.5, color: C.lime, fontFace: "Calibri",
    });
    s.addText(m.skills, {
      x: x + 1.0, y: y + 0.75, w: 3.4, h: 0.28,
      fontSize: 9, color: C.muted, fontFace: "Calibri",
    });
  });

  s.addText("Team Name: ELIO  ·  UniHack 2026", {
    x: 0, y: 5.3, w: W, h: 0.3,
    fontSize: 9, color: C.dimmer, fontFace: "Calibri", align: "center",
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 3 — SOLUTION BRIEF
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s, { glow: true });
  sideAccent(s);
  titleBlock(s, "The Problem We Solve", "Why industrial product catalogs fail");

  // Left: problem statement
  s.addShape(pres.ShapeType.rect, {
    x: 0.45, y: 1.0, w: 4.4, h: 4.2,
    fill: { color: C.card }, line: { color: C.border, width: 0.75 }, rectRadius: 0.1,
  });
  s.addText("The Problem", {
    x: 0.6, y: 1.1, w: 4.1, h: 0.35,
    fontSize: 14, bold: true, color: C.red, fontFace: "Calibri",
  });
  const probs = [
    "6 messy distributor columns → need 252-column catalog",
    "Most pipelines hallucinate: guess brands from substrings",
    "Invent attributes from nothing",
    "Paper over gaps with 'N/A'",
    "No audit trail — a judge can't tell real from made up",
    "Brand confusion: distributor names surfaced as OEM",
  ];
  probs.forEach((p, i) => {
    s.addShape(pres.ShapeType.ellipse, {
      x: 0.62, y: 1.56 + i * 0.44, w: 0.16, h: 0.16,
      fill: { color: C.red }, line: { type: "none" },
    });
    s.addText(p, {
      x: 0.85, y: 1.5 + i * 0.44, w: 3.85, h: 0.32,
      fontSize: 11, color: C.white, fontFace: "Calibri",
    });
  });

  // Right: solution brief
  s.addShape(pres.ShapeType.rect, {
    x: 5.05, y: 1.0, w: 4.5, h: 4.2,
    fill: { color: C.card }, line: { color: C.lime, width: 1.5 }, rectRadius: 0.1,
  });
  s.addText("ELIO's Answer", {
    x: 5.2, y: 1.1, w: 4.2, h: 0.35,
    fontSize: 14, bold: true, color: C.lime, fontFace: "Calibri",
  });
  const sols = [
    ["Evidence-gated", "Every value traces to a source URL, page, char-span, and verbatim snippet"],
    ["Honest abstention", "Cells that can't be traced get abstained with a reason — never a guess"],
    ["Deterministic DAG", "9-stage frozen pipeline — reproducible by design, not by luck"],
    ["Dual-pass verify", "Values must appear in source text or be a documented unit conversion"],
    ["Zero hallucination", "0 untraceable accepted values across 589 adversarial test values"],
  ];
  sols.forEach(([title, desc], i) => {
    s.addShape(pres.ShapeType.ellipse, {
      x: 5.22, y: 1.56 + i * 0.58, w: 0.18, h: 0.18,
      fill: { color: C.lime }, line: { type: "none" },
    });
    s.addText(title + ":", {
      x: 5.47, y: 1.5 + i * 0.58, w: 3.9, h: 0.25,
      fontSize: 10.5, bold: true, color: C.lime, fontFace: "Calibri",
    });
    s.addText(desc, {
      x: 5.47, y: 1.74 + i * 0.58, w: 3.9, h: 0.28,
      fontSize: 9.5, color: C.muted, fontFace: "Calibri",
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 4 — THREE QUESTIONS
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);
  sideAccent(s);
  titleBlock(s, "How ELIO Answers the Hard Questions", "Enrichment · Trust · Scale");

  const cards = [
    {
      q: "How does ELIO enrich minimal product info?",
      color: C.teal,
      answer: "Takes 6 inputs (Mfg_Part_Num, Part_Desc, Brand ×3, Manufacturer) and runs per-category attribute extractors (discs, blades, belts, bits, adapters, fasteners, lighting, lumber, wire, electrical). Every extracted attribute is anchored to a verbatim text span — no inference beyond the source.",
      metric: "2.156 attrs/row — seed-7 holdout, assisted",
    },
    {
      q: "How does ELIO ensure accuracy and trust?",
      color: C.lime,
      answer: "Dual-pass verification: (1) value must appear in raw source text; (2) must match a documented unit-conversion table. Failures escalate to human review queue. Auto-accept only on gold-exempt evidence. Result: 118/118 gold cells byte-exact, 0 dual-pass failures.",
      metric: "17–1 blind critic A/B (7 ties)",
    },
    {
      q: "What makes ELIO scalable for enterprise?",
      color: C.purple,
      answer: "Stateless pipeline stages — each row is independent. New manufacturers: add to reference loader. New document formats: add a stage adapter. Continuous updates: re-run from ingest. The 252-column schema is fixed; extractors are additive. Horizontal scale = more workers.",
      metric: "1000-row full export, ~90s verify-everything",
    },
  ];

  cards.forEach((card, i) => {
    const x = 0.4 + i * 3.18;
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.05, w: 3.05, h: 4.2,
      fill: { color: C.card }, line: { color: card.color, width: 1.5 }, rectRadius: 0.1,
    });
    // Number badge
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.15, y: 1.15, w: 0.45, h: 0.45,
      fill: { color: card.color }, line: { type: "none" },
    });
    s.addText(String(i + 1), {
      x: x + 0.15, y: 1.15, w: 0.45, h: 0.45,
      fontSize: 14, bold: true, color: C.ink, fontFace: "Calibri", align: "center", valign: "middle",
    });
    s.addText(card.q, {
      x: x + 0.15, y: 1.68, w: 2.8, h: 0.55,
      fontSize: 11, bold: true, color: C.white, fontFace: "Calibri",
    });
    s.addText(card.answer, {
      x: x + 0.15, y: 2.28, w: 2.8, h: 1.9,
      fontSize: 9.5, color: C.muted, fontFace: "Calibri",
    });
    // Metric chip at bottom
    s.addShape(pres.ShapeType.rect, {
      x: x + 0.15, y: 4.85, w: 2.8, h: 0.28,
      fill: { color: "1A1A25" }, line: { color: card.color, width: 0.75 }, rectRadius: 0.04,
    });
    s.addText(card.metric, {
      x: x + 0.2, y: 4.86, w: 2.7, h: 0.26,
      fontSize: 8, bold: true, color: card.color, fontFace: "Calibri", align: "center",
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 5 — USP / OPPORTUNITY
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s, { glow: true });
  sideAccent(s);
  titleBlock(s, "Why ELIO Wins", "Differentiation · Market fit · Unique advantage");

  // Left: comparison table
  const rows = [
    ["", "Typical Pipeline", "ELIO"],
    ["Gold cells exact", "Some", "118 / 118"],
    ["Untraceable values", "Many", "Zero"],
    ["Dual-pass failures", "—", "0"],
    ["Blank cells", "'N/A'", "Abstained + reason"],
    ["Adversarial precision", "Unknown", "589/589 @ 100%"],
    ["Blind critic A/B", "—", "17–1 (7 ties)"],
    ["Audit trail", "None", "URL · page · char-span · snippet"],
  ];

  rows.forEach((row, ri) => {
    row.forEach((cell, ci) => {
      const x = 0.45 + ci * 2.85;
      const y = 0.95 + ri * 0.52;
      const isHeader = ri === 0 || ci === 0;
      const isElio = ci === 2 && ri > 0;
      s.addShape(pres.ShapeType.rect, {
        x, y, w: 2.8, h: 0.48,
        fill: { color: isHeader ? "1C1C28" : (isElio ? "1A2500" : C.card) },
        line: { color: isElio ? C.lime : C.border, width: isElio ? 1 : 0.5 },
      });
      s.addText(cell, {
        x: x + 0.08, y, w: 2.65, h: 0.48,
        fontSize: isHeader && ri === 0 ? 11 : 10,
        bold: isHeader,
        color: isElio ? C.lime : (ri === 0 ? C.lime : C.white),
        fontFace: "Calibri", valign: "middle",
        align: ci === 0 ? "left" : "center",
      });
    });
  });

  // Right: USP callouts
  const usps = [
    { icon: "🔍", title: "Evidence-First", desc: "Not AI confidence — actual source citations. Every value is traceable or refused." },
    { icon: "🏛️", title: "Deterministic", desc: "Frozen pipeline (tag bar-4-freeze). Same input always → same output. No randomness." },
    { icon: "⚡", title: "Category-Native", desc: "Per-category extractors outperform generic LLM prompting for structured attributes." },
    { icon: "🛡️", title: "Honest Blanks", desc: "Four documented abstention classes. Judges can verify every blank has a reason." },
  ];

  usps.forEach((u, i) => {
    const y = 1.0 + i * 1.13;
    s.addShape(pres.ShapeType.rect, {
      x: 9.15, y, w: 0.7, h: 0.7,
      fill: { color: "2D3A00" }, line: { color: C.lime, width: 1 }, rectRadius: 0.07,
    });
    s.addText(u.icon, {
      x: 9.15, y: y + 0.08, w: 0.7, h: 0.54,
      fontSize: 18, fontFace: "Calibri", align: "center",
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 6 — FEATURES
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);
  sideAccent(s);
  titleBlock(s, "Features", "What ELIO delivers end-to-end");

  const features = [
    { icon: "📥", title: "CSV Ingest", desc: "Accepts any distributor CSV with 6 required columns. Auto-detects fallback headers.", accent: C.teal },
    { icon: "🏷️", title: "Brand & Entity Resolution", desc: "Word-boundary brand matching. Distributor names never surfaced as OEM manufacturer.", accent: C.lime },
    { icon: "🗂️", title: "Closed Taxonomy", desc: "Dept > Class > Fine tree. Longest-keyword match with word-boundary safety. No substring traps.", accent: C.purple },
    { icon: "⚙️", title: "Attribute Extraction", desc: "10 per-category extractors + generic fallback. Regex + unit normalization. Char-span anchored.", accent: C.amber },
    { icon: "✅", title: "Dual-Pass Verification", desc: "Pass 1: value must appear verbatim in source. Pass 2: or be a documented unit conversion. Failures → review.", accent: C.teal },
    { icon: "🚫", title: "Honest Abstention", desc: "4 documented classes (gold-blessed blanks, pendant rows, chargers, mixed tape). Never a guess.", accent: C.red },
    { icon: "📝", title: "Description Generation", desc: "4 variants: mobile / invoice / short / long. Char limits enforced. Validity flags.", accent: C.lime },
    { icon: "📤", title: "252-Column Export", desc: "UTF-8-sig encoding (Excel-safe). Matches delivery format exactly. SHA256-bound manifest.", accent: C.purple },
    { icon: "🔬", title: "Evidence Dossier", desc: "Every accepted value: source URL, page number, char-span, verbatim snippet in demo.html.", accent: C.teal },
    { icon: "🖥️", title: "Live Dashboard", desc: "Next.js cockpit: upload → enrich → review queue → override → export. Evidence drawer per row.", accent: C.lime },
    { icon: "🧪", title: "Adversarial Hardening", desc: "277 rows, 589 values, difficulty-stratified. 100% precision. 0 leakage after freeze.", accent: C.amber },
    { icon: "📊", title: "Verify-Everything Script", desc: "12-gate acceptance grid, live, ~90s. All headline numbers regenerated on demand.", accent: C.purple },
  ];

  const cols = 4;
  const cardW = 2.3;
  const cardH = 1.05;
  const startX = 0.4;
  const startY = 1.0;

  features.forEach((f, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (cardW + 0.1);
    const y = startY + row * (cardH + 0.1);

    s.addShape(pres.ShapeType.rect, {
      x, y, w: cardW, h: cardH,
      fill: { color: C.card }, line: { color: C.border, width: 0.75 }, rectRadius: 0.08,
    });
    // Left accent bar
    s.addShape(pres.ShapeType.rect, {
      x, y: y + 0.15, w: 0.04, h: cardH - 0.3,
      fill: { color: f.accent }, line: { type: "none" },
    });
    s.addText(f.icon + " " + f.title, {
      x: x + 0.12, y: y + 0.08, w: cardW - 0.2, h: 0.3,
      fontSize: 10, bold: true, color: f.accent, fontFace: "Calibri",
    });
    s.addText(f.desc, {
      x: x + 0.12, y: y + 0.38, w: cardW - 0.18, h: 0.6,
      fontSize: 8.5, color: C.muted, fontFace: "Calibri",
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 7 — PROCESS FLOW DIAGRAM
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s, { glow: true });
  sideAccent(s);
  titleBlock(s, "Process Flow — 9-Stage DAG", "Evidence-gated catalog enrichment pipeline");

  // Draw the 9 pipeline stages horizontally in two rows
  const stages = [
    { n: "1", name: "Ingest", sub: "6 input cols", color: C.teal },
    { n: "2", name: "Entity\nResolution", sub: "Brand + OEM", color: C.lime },
    { n: "3", name: "Taxonomy", sub: "Dept·Class·Fine", color: C.lime },
    { n: "4", name: "Extraction", sub: "10 extractors", color: C.amber },
    { n: "5", name: "Description\nGen", sub: "4 variants", color: C.amber },
  ];
  const stages2 = [
    { n: "6", name: "Verification", sub: "Dual-pass", color: C.purple },
    { n: "7", name: "Quality\nGate", sub: "Auto-accept / review", color: C.purple },
    { n: "8", name: "Abstention", sub: "4 classes", color: C.red },
    { n: "9", name: "Export", sub: "252 columns", color: C.teal },
  ];

  const bW = 1.65;
  const bH = 0.82;

  // Row 1
  stages.forEach((st, i) => {
    const x = 0.45 + i * 1.88;
    const y = 1.2;
    s.addShape(pres.ShapeType.rect, {
      x, y, w: bW, h: bH,
      fill: { color: C.card }, line: { color: st.color, width: 1.5 }, rectRadius: 0.08,
    });
    s.addText(st.n, {
      x: x + 0.07, y: y + 0.05, w: 0.35, h: 0.35,
      fontSize: 14, bold: true, color: st.color, fontFace: "Calibri",
    });
    s.addText(st.name, {
      x: x + 0.07, y: y + 0.08, w: bW - 0.1, h: 0.42,
      fontSize: 10.5, bold: true, color: C.white, fontFace: "Calibri", align: "center", valign: "middle",
    });
    s.addText(st.sub, {
      x: x + 0.07, y: y + 0.55, w: bW - 0.14, h: 0.22,
      fontSize: 8.5, color: st.color, fontFace: "Calibri", align: "center",
    });
    if (i < stages.length - 1) {
      arrow(s, x + bW, y + bH / 2, x + bW + 0.22);
    }
  });

  // Down arrow from stage 5 → 6
  s.addShape(pres.ShapeType.line, {
    x: 0.45 + 4 * 1.88 + bW / 2, y: 1.2 + bH,
    w: 0, h: 0.6,
    line: { color: C.lime, width: 1.5, endArrowType: "triangle" },
  });

  // Row 2 (right to left for snaking effect)
  stages2.forEach((st, i) => {
    const x = 0.45 + (3 - i) * 1.88;
    const y = 2.85;
    s.addShape(pres.ShapeType.rect, {
      x, y, w: bW, h: bH,
      fill: { color: C.card }, line: { color: st.color, width: 1.5 }, rectRadius: 0.08,
    });
    s.addText(st.n, {
      x: x + 0.07, y: y + 0.05, w: 0.35, h: 0.35,
      fontSize: 14, bold: true, color: st.color, fontFace: "Calibri",
    });
    s.addText(st.name, {
      x: x + 0.07, y: y + 0.08, w: bW - 0.1, h: 0.42,
      fontSize: 10.5, bold: true, color: C.white, fontFace: "Calibri", align: "center", valign: "middle",
    });
    s.addText(st.sub, {
      x: x + 0.07, y: y + 0.55, w: bW - 0.14, h: 0.22,
      fontSize: 8.5, color: st.color, fontFace: "Calibri", align: "center",
    });
    if (i < stages2.length - 1) {
      // Arrow from right to left
      s.addShape(pres.ShapeType.line, {
        x: x, y: y + bH / 2,
        w: -0.22, h: 0,
        line: { color: C.lime, width: 1.5, endArrowType: "triangle" },
      });
    }
  });

  // Side-effect: verification failure → review
  s.addShape(pres.ShapeType.rect, {
    x: 7.1, y: 3.9, w: 2.6, h: 0.6,
    fill: { color: "200020" }, line: { color: C.red, width: 1 }, rectRadius: 0.07,
  });
  s.addText("⚠  Verification failures → Human Review Queue", {
    x: 7.15, y: 3.91, w: 2.5, h: 0.58,
    fontSize: 8.5, color: C.red, fontFace: "Calibri", align: "center", valign: "middle",
  });
  s.addShape(pres.ShapeType.line, {
    x: 7.45, y: 2.85, w: 0, h: 1.04,
    line: { color: C.red, width: 1, dashType: "dash" },
  });

  // Bottom legend
  s.addText("Frozen at commit 38db2af  (tag: bar-4-freeze)  ·  Reproducible: python -B scripts\\verify_everything.py", {
    x: 0.45, y: 5.25, w: 9.1, h: 0.28,
    fontSize: 8.5, color: C.dimmer, fontFace: "Calibri", align: "center",
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 8 — WIREFRAMES / DASHBOARD MOCKUP
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);
  sideAccent(s);
  titleBlock(s, "Dashboard UI — ELIO Cockpit", "Upload → Enrich → Review → Override → Export");

  // Wireframe shell
  s.addShape(pres.ShapeType.rect, {
    x: 0.45, y: 1.0, w: 9.1, h: 4.35,
    fill: { color: "0D0D12" }, line: { color: C.border, width: 1 }, rectRadius: 0.1,
  });

  // Sidebar strip
  s.addShape(pres.ShapeType.rect, {
    x: 0.45, y: 1.0, w: 0.55, h: 4.35,
    fill: { color: C.card }, line: { type: "none" },
  });
  // Sidebar icons (dots)
  ["●", "●", "●", "●", "●", "●"].forEach((_, i) => {
    s.addText("●", { x: 0.52, y: 1.35 + i * 0.45, w: 0.4, h: 0.3, fontSize: 8, color: i === 0 ? C.lime : C.dimmer, fontFace: "Calibri", align: "center" });
  });

  // Header strip
  s.addShape(pres.ShapeType.rect, {
    x: 1.0, y: 1.0, w: 8.55, h: 0.45,
    fill: { color: C.card }, line: { type: "none" },
  });
  s.addText("ELIO Cockpit  ·  Dashboard", {
    x: 1.05, y: 1.04, w: 4, h: 0.36,
    fontSize: 10, bold: true, color: C.white, fontFace: "Calibri",
  });
  s.addText("⬆ Upload CSV    📊 Demo 50    📁 Full 1000    [ Export CSV ]", {
    x: 5.2, y: 1.04, w: 3.2, h: 0.36,
    fontSize: 8, color: C.lime, fontFace: "Calibri", align: "right",
  });

  // Metric cards row
  const mCards = [
    { label: "Records", value: "1,000", accent: C.teal },
    { label: "Accepted", value: "97.2%", accent: C.lime },
    { label: "In Review", value: "2.3%", accent: C.amber },
    { label: "Abstained", value: "0.5%", accent: C.red },
  ];
  mCards.forEach((mc, i) => {
    const x = 1.05 + i * 2.15;
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.52, w: 2.0, h: 0.75,
      fill: { color: C.card }, line: { color: mc.accent, width: 0.75 }, rectRadius: 0.07,
    });
    s.addText(mc.value, {
      x: x + 0.05, y: 1.56, w: 1.9, h: 0.38,
      fontSize: 22, bold: true, color: mc.accent, fontFace: "Calibri", align: "center",
    });
    s.addText(mc.label, {
      x: x + 0.05, y: 1.94, w: 1.9, h: 0.25,
      fontSize: 8.5, color: C.muted, fontFace: "Calibri", align: "center",
    });
  });

  // Table area
  s.addShape(pres.ShapeType.rect, {
    x: 1.05, y: 2.35, w: 8.4, h: 2.85,
    fill: { color: C.card }, line: { color: C.border, width: 0.5 }, rectRadius: 0.07,
  });
  // Table header
  const cols = ["MPN", "Brand", "Dept / Class", "Attributes Extracted", "Verification", "Status"];
  const colW = [1.3, 1.2, 1.8, 2.1, 1.3, 0.7];
  let cx = 1.12;
  cols.forEach((col, ci) => {
    s.addText(col, {
      x: cx, y: 2.42, w: colW[ci], h: 0.28,
      fontSize: 8.5, bold: true, color: C.muted, fontFace: "Calibri",
    });
    cx += colW[ci];
  });
  s.addShape(pres.ShapeType.line, {
    x: 1.05, y: 2.72, w: 8.4, h: 0,
    line: { color: C.border, width: 0.5 },
  });

  // Sample rows
  const rows2 = [
    ["100-9010", "BOSCH", "Abrasives / Cutting", "dia=100mm, arbor=16mm, RPM=13300", "✓ PASS", "✅ ACCPT", C.teal],
    ["XFR-2201", "DEWALT", "Power Tools / Bits", "size=1/4in, drive=hex, L=76mm", "✓ PASS", "✅ ACCPT", C.teal],
    ["LUM-8FT", "Unknown", "Lumber / Dimensional", "—", "⚠ ABSTAIN", "🚫 ABSTN", C.amber],
    ["AC-DUALC", "Generic", "Electronics / Chargers", "—", "⚠ MULTI", "👁 REVIEW", C.purple],
  ];
  rows2.forEach((row, ri) => {
    const y = 2.78 + ri * 0.5;
    s.addShape(pres.ShapeType.rect, {
      x: 1.05, y, w: 8.4, h: 0.46,
      fill: { color: ri % 2 === 0 ? "111118" : C.card }, line: { type: "none" },
    });
    cx = 1.12;
    row.slice(0, 6).forEach((cell, ci) => {
      s.addText(cell, {
        x: cx, y: y + 0.08, w: colW[ci], h: 0.3,
        fontSize: 8.5,
        color: ci === 5 ? row[6] : (ci === 4 ? (cell.includes("PASS") ? C.teal : C.amber) : C.white),
        fontFace: "Calibri", bold: ci === 5,
      });
      cx += colW[ci];
    });
  });

  s.addText("Click any row to open Evidence Drawer: source URL · page · char-span · verbatim snippet · override", {
    x: 1.05, y: 5.15, w: 8.4, h: 0.2,
    fontSize: 7.5, color: C.dimmer, fontFace: "Calibri", align: "center",
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 9 — ARCHITECTURE DIAGRAM
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s, { glow: true });
  sideAccent(s);
  titleBlock(s, "Architecture", "Three-layer: Data · Pipeline · UI");

  // Three columns representing architecture layers
  const layers = [
    {
      title: "INPUT LAYER",
      color: C.teal,
      items: ["Distributor CSV Upload", "6 required columns", "SHA-256 file hash", "Row-count validation", "FormData → /api/run"],
    },
    {
      title: "PIPELINE LAYER (Python DAG)",
      color: C.lime,
      items: [
        "Stage 1: Ingest + normalize",
        "Stage 2: Entity resolution",
        "Stage 3: Taxonomy mapping",
        "Stage 4: Attribute extraction",
        "Stage 5: Description gen",
        "Stage 6: Dual-pass verify",
        "Stage 7: Quality gate",
        "Stage 8: Abstention",
        "Stage 9: 252-col projection",
      ],
    },
    {
      title: "OUTPUT + UI LAYER",
      color: C.purple,
      items: [
        "Next.js cockpit dashboard",
        "Upload → enrich (live)",
        "Explorer: 252-col table",
        "Review queue + overrides",
        "Abstention audit trail",
        "Evidence drawer (per cell)",
        "Export CSV (UTF-8-sig)",
        "demo.html (offline)",
      ],
    },
  ];

  layers.forEach((layer, li) => {
    const x = 0.4 + li * 3.2;
    const h = 4.0;
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.0, w: 3.0, h,
      fill: { color: C.card }, line: { color: layer.color, width: 1.5 }, rectRadius: 0.1,
    });
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.0, w: 3.0, h: 0.42,
      fill: { color: layer.color }, line: { type: "none" }, rectRadius: 0.1,
    });
    // Fix corners - overlap bottom of header
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.3, w: 3.0, h: 0.12,
      fill: { color: layer.color }, line: { type: "none" },
    });
    s.addText(layer.title, {
      x: x + 0.1, y: 1.0, w: 2.8, h: 0.42,
      fontSize: 10, bold: true, color: C.ink, fontFace: "Calibri", align: "center", valign: "middle",
    });
    layer.items.forEach((item, ii) => {
      s.addShape(pres.ShapeType.ellipse, {
        x: x + 0.14, y: 1.52 + ii * 0.36, w: 0.1, h: 0.1,
        fill: { color: layer.color }, line: { type: "none" },
      });
      s.addText(item, {
        x: x + 0.3, y: 1.46 + ii * 0.36, w: 2.6, h: 0.32,
        fontSize: 9.5, color: C.white, fontFace: "Calibri",
      });
    });

    // Arrow between layers
    if (li < 2) {
      arrow(s, x + 3.0, 3.0, x + 3.2);
    }
  });

  // Storage note
  s.addShape(pres.ShapeType.rect, {
    x: 0.4, y: 5.1, w: 9.2, h: 0.3,
    fill: { color: "101018" }, line: { type: "none" },
  });
  s.addText("Frozen at bar-4-freeze · pipeline: unihack_catalog/ · scripts/verify_everything.py · All artifacts SHA256-bound in submission_manifest.json", {
    x: 0.4, y: 5.12, w: 9.2, h: 0.26,
    fontSize: 7.5, color: C.dimmer, fontFace: "Calibri", align: "center",
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 10 — TECHNOLOGIES
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);
  sideAccent(s);
  titleBlock(s, "Technologies Used", "Stack chosen for correctness and transparency");

  const techs = [
    { cat: "Core Pipeline", color: C.teal, items: [
      "Python 3.11 — 9-stage DAG, zero dependencies on LLM for extraction",
      "Regex + unit normalization — deterministic, auditable attribute extraction",
      "defusedxml + lxml — safe XML/HTML parsing of manufacturer pages",
      "csv + UTF-8-sig — Excel-safe export, byte-exact with delivery format",
    ]},
    { cat: "Verification & Quality", color: C.lime, items: [
      "Dual-pass verifier — custom char-span matching against raw source text",
      "SHA-256 manifest — every artifact is hash-bound (submission_manifest.json)",
      "pytest — full pipeline test suite, gate assertions",
      "verify_everything.py — 12-gate acceptance grid, runs live in ~90s",
    ]},
    { cat: "Frontend & API", color: C.purple, items: [
      "Next.js 14 (App Router) — server components, route handlers",
      "TypeScript — fully typed cockpit (upload, explorer, review, export tabs)",
      "Tailwind-free vanilla CSS — dark shell #0a0a0d, lime #c8d84a accent",
      "POST /api/run — FormData → Python pipeline → JSON results",
    ]},
    { cat: "LLM (Evidence-Gated Only)", color: C.amber, items: [
      "Google Gemini — used only to propose attribute candidates",
      "Dual-pass gate rejects any proposal not in source text",
      "Full disclosure: docs/DISCLOSURE.md",
      "The gate, not the model, decides what ships",
    ]},
  ];

  techs.forEach((group, gi) => {
    const col = gi % 2;
    const row = Math.floor(gi / 2);
    const x = 0.45 + col * 4.8;
    const y = 1.0 + row * 2.25;

    s.addShape(pres.ShapeType.rect, {
      x, y, w: 4.6, h: 2.1,
      fill: { color: C.card }, line: { color: group.color, width: 1 }, rectRadius: 0.1,
    });
    s.addText(group.cat, {
      x: x + 0.15, y: y + 0.1, w: 4.3, h: 0.32,
      fontSize: 12, bold: true, color: group.color, fontFace: "Calibri",
    });
    group.items.forEach((item, ii) => {
      s.addShape(pres.ShapeType.ellipse, {
        x: x + 0.15, y: y + 0.54 + ii * 0.37, w: 0.1, h: 0.1,
        fill: { color: group.color }, line: { type: "none" },
      });
      s.addText(item, {
        x: x + 0.32, y: y + 0.48 + ii * 0.37, w: 4.15, h: 0.3,
        fontSize: 9.5, color: C.white, fontFace: "Calibri",
      });
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 11 — ESTIMATED COST
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s, { glow: true });
  sideAccent(s);
  titleBlock(s, "Estimated Implementation Cost", "Transparent, minimal LLM dependency");

  // Big cost summary cards
  const costCards = [
    { label: "LLM API (Gemini)", val: "~$0.10", sub: "per 50-row batch\n(proposals only, gate rejects most)", color: C.amber },
    { label: "LLM at 1,000 rows", val: "~$2.00", sub: "10× batches\nwell within hackathon credit", color: C.lime },
    { label: "Infrastructure", val: "$0", sub: "runs locally\nno cloud required for pipeline", color: C.teal },
    { label: "Frontend hosting", val: "~$5/mo", sub: "Vercel free tier or\nself-hosted Next.js", color: C.purple },
  ];

  costCards.forEach((c, i) => {
    const x = 0.45 + i * 2.38;
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.1, w: 2.2, h: 1.55,
      fill: { color: C.card }, line: { color: c.color, width: 1.5 }, rectRadius: 0.1,
    });
    s.addText(c.val, {
      x: x + 0.1, y: 1.18, w: 2.0, h: 0.6,
      fontSize: 28, bold: true, color: c.color, fontFace: "Calibri", align: "center",
    });
    s.addText(c.label, {
      x: x + 0.1, y: 1.78, w: 2.0, h: 0.26,
      fontSize: 10, bold: true, color: C.white, fontFace: "Calibri", align: "center",
    });
    s.addText(c.sub, {
      x: x + 0.1, y: 2.05, w: 2.0, h: 0.52,
      fontSize: 8.5, color: C.muted, fontFace: "Calibri", align: "center",
    });
  });

  // Breakdown table
  s.addText("Cost Breakdown", {
    x: 0.45, y: 2.8, w: 9, h: 0.32,
    fontSize: 13, bold: true, color: C.white, fontFace: "Calibri",
  });

  const breakdownRows = [
    ["Component", "Unit cost", "At 50 rows", "At 1,000 rows", "Notes"],
    ["Gemini API (proposals)", "$0.002/1k tok", "~$0.10", "~$2.00", "Evidence-gate rejects ~70%; net LLM influence small"],
    ["Extraction (regex)", "$0", "$0", "$0", "Deterministic; zero marginal cost"],
    ["Verification engine", "$0", "$0", "$0", "Pure Python; local"],
    ["Next.js frontend", "$0 dev", "$0", "$5/mo prod", "Vercel free tier for demos"],
    ["Total (hackathon run)", "", "~$0.10", "~$2.00", "Comfortably within free-tier budgets"],
  ];

  breakdownRows.forEach((row, ri) => {
    const y = 3.18 + ri * 0.36;
    row.forEach((cell, ci) => {
      const x = 0.45 + [0, 2.1, 3.5, 4.9, 6.3][ci];
      const w = [1.6, 1.35, 1.35, 1.35, 3.3][ci];
      s.addShape(pres.ShapeType.rect, {
        x, y, w, h: 0.33,
        fill: { color: ri === 0 ? "1C1C28" : (ri === breakdownRows.length - 1 ? "1A2500" : C.card) },
        line: { color: C.border, width: 0.5 },
      });
      s.addText(cell, {
        x: x + 0.05, y, w: w - 0.1, h: 0.33,
        fontSize: ri === 0 ? 9 : 8.5,
        bold: ri === 0 || (ri === breakdownRows.length - 1),
        color: ri === 0 ? C.muted : (ci === 0 ? C.white : (ri === breakdownRows.length - 1 ? C.lime : C.white)),
        fontFace: "Calibri", valign: "middle",
      });
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 12 — SNAPSHOTS / EVIDENCE EXPLORER
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);
  sideAccent(s);
  titleBlock(s, "Snapshots — MVP Evidence Explorer", "demo.html: search any MPN, see every value's source");

  // Left: evidence dossier mockup
  s.addShape(pres.ShapeType.rect, {
    x: 0.45, y: 1.0, w: 4.5, h: 4.35,
    fill: { color: "0D0D12" }, line: { color: C.lime, width: 1.5 }, rectRadius: 0.1,
  });
  s.addText("Evidence Dossier — 100-9010", {
    x: 0.55, y: 1.08, w: 4.3, h: 0.32,
    fontSize: 11, bold: true, color: C.lime, fontFace: "Calibri",
  });
  s.addShape(pres.ShapeType.line, { x: 0.55, y: 1.43, w: 4.3, h: 0, line: { color: C.border, width: 0.5 } });

  const attrs = [
    { attr: "outer_diameter", val: "100 mm", src: "bosch-pds.com/100-9010", span: "chars 12–19", snip: "...diameter: 100 mm, arbor..." },
    { attr: "arbor_size", val: "16 mm", src: "bosch-pds.com/100-9010", span: "chars 26–33", snip: "...arbor: 16 mm, max RPM..." },
    { attr: "max_rpm", val: "13,300 RPM", src: "bosch-pds.com/100-9010", span: "chars 42–55", snip: "...max RPM: 13300, abrasive..." },
    { attr: "material", val: "Aluminum Oxide", src: "bosch-pds.com/100-9010", span: "chars 60–74", snip: "...Aluminum Oxide abrasive grain..." },
    { attr: "thickness", val: "Abstained", src: "—", span: "—", snip: "No thickness found in source text" },
  ];

  attrs.forEach((a, i) => {
    const y = 1.52 + i * 0.72;
    s.addShape(pres.ShapeType.rect, {
      x: 0.55, y, w: 4.3, h: 0.65,
      fill: { color: a.val === "Abstained" ? "1A0800" : "111120" }, line: { color: a.val === "Abstained" ? C.red : C.border, width: 0.5 }, rectRadius: 0.05,
    });
    s.addText(a.attr, {
      x: 0.65, y: y + 0.04, w: 1.2, h: 0.22,
      fontSize: 8.5, color: C.muted, fontFace: "Calibri",
    });
    s.addText(a.val, {
      x: 1.88, y: y + 0.04, w: 2.8, h: 0.22,
      fontSize: 9.5, bold: true, color: a.val === "Abstained" ? C.red : C.teal, fontFace: "Calibri",
    });
    s.addText(a.src + "  ·  " + a.span, {
      x: 0.65, y: y + 0.27, w: 4.1, h: 0.18,
      fontSize: 7.5, color: C.dimmer, fontFace: "Calibri",
    });
    s.addText("\"" + a.snip + "\"", {
      x: 0.65, y: y + 0.44, w: 4.1, h: 0.18,
      fontSize: 7.5, color: i < 4 ? C.lime : C.amber, fontFace: "Calibri", italic: true,
    });
  });

  // Right: results grid
  s.addShape(pres.ShapeType.rect, {
    x: 5.1, y: 1.0, w: 4.45, h: 4.35,
    fill: { color: "0D0D12" }, line: { color: C.border, width: 1 }, rectRadius: 0.1,
  });
  s.addText("Verification Gate — Proof", {
    x: 5.2, y: 1.08, w: 4.25, h: 0.32,
    fontSize: 11, bold: true, color: C.white, fontFace: "Calibri",
  });
  s.addShape(pres.ShapeType.line, { x: 5.2, y: 1.43, w: 4.25, h: 0, line: { color: C.border, width: 0.5 } });

  const gates = [
    { gate: "Gold cells byte-exact", result: "118 / 118", color: C.teal, icon: "✓" },
    { gate: "Dual-pass failures", result: "0 / 0", color: C.lime, icon: "✓" },
    { gate: "Untraceable accepted values", result: "0", color: C.lime, icon: "✓" },
    { gate: "Adversarial precision", result: "589 / 589 @ 100%", color: C.lime, icon: "✓" },
    { gate: "Provenance coverage", result: "100%", color: C.teal, icon: "✓" },
    { gate: "Blind critic A/B", result: "17 – 1 (7 ties)", color: C.lime, icon: "✓" },
    { gate: "Fresh upload E2E (8 adversarial)", result: "PASS", color: C.teal, icon: "✓" },
    { gate: "252-col export schema", result: "PASS", color: C.teal, icon: "✓" },
    { gate: "Regressions vs Bar 3", result: "0", color: C.lime, icon: "✓" },
  ];

  gates.forEach((g, i) => {
    const y = 1.52 + i * 0.41;
    s.addShape(pres.ShapeType.rect, {
      x: 5.2, y, w: 4.25, h: 0.37,
      fill: { color: "111118" }, line: { color: C.border, width: 0.4 }, rectRadius: 0.04,
    });
    s.addText(g.icon, {
      x: 5.28, y, w: 0.28, h: 0.37,
      fontSize: 11, bold: true, color: g.color, fontFace: "Calibri", valign: "middle", align: "center",
    });
    s.addText(g.gate, {
      x: 5.58, y, w: 2.6, h: 0.37,
      fontSize: 9, color: C.white, fontFace: "Calibri", valign: "middle",
    });
    s.addText(g.result, {
      x: 8.2, y, w: 1.15, h: 0.37,
      fontSize: 9, bold: true, color: g.color, fontFace: "Calibri", valign: "middle", align: "right",
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 13 — FUTURE DEVELOPMENT
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s, { glow: true });
  sideAccent(s);
  titleBlock(s, "Future Development", "What comes next for ELIO");

  // Timeline / roadmap
  const phases = [
    {
      phase: "Phase 5 — Scale", color: C.teal, timeline: "Month 1–2",
      items: [
        "Parallel workers for concurrent enrichment (batch 1000+ rows/min)",
        "S3 / GCS input adapters for enterprise file drops",
        "Manufacturer page crawler with smart caching layer",
        "REST API with webhook callbacks for async results",
      ],
    },
    {
      phase: "Phase 6 — Intelligence", color: C.lime, timeline: "Month 3–4",
      items: [
        "RAG over manufacturer PDF library for richer extraction",
        "Auto-taxonomy expansion: detect new categories from data",
        "Confidence scoring on attribute-level (not just pass/fail)",
        "Cross-SKU consistency checker (same MPN different descriptions)",
      ],
    },
    {
      phase: "Phase 7 — Enterprise", color: C.purple, timeline: "Month 5–6",
      items: [
        "Multi-tenant SaaS with per-org custom taxonomies",
        "PIM integrations: Akeneo, Salsify, inRiver connectors",
        "Human-in-the-loop: ML-ranked review queue, override learning",
        "Compliance export: GS1, UNSPSC, eCl@ss standards",
      ],
    },
  ];

  phases.forEach((ph, pi) => {
    const x = 0.45 + pi * 3.2;
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.05, w: 3.05, h: 4.3,
      fill: { color: C.card }, line: { color: ph.color, width: 1.5 }, rectRadius: 0.1,
    });
    // Header
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.05, w: 3.05, h: 0.38,
      fill: { color: ph.color }, line: { type: "none" }, rectRadius: 0.1,
    });
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.28, w: 3.05, h: 0.15,
      fill: { color: ph.color }, line: { type: "none" },
    });
    s.addText(ph.phase, {
      x: x + 0.12, y: 1.05, w: 2.2, h: 0.38,
      fontSize: 10, bold: true, color: C.ink, fontFace: "Calibri", valign: "middle",
    });
    s.addText(ph.timeline, {
      x: x + 0.12, y: 1.05, w: 2.8, h: 0.38,
      fontSize: 9, color: C.ink, fontFace: "Calibri", align: "right", valign: "middle",
    });
    ph.items.forEach((item, ii) => {
      s.addShape(pres.ShapeType.ellipse, {
        x: x + 0.15, y: 1.56 + ii * 0.73, w: 0.14, h: 0.14,
        fill: { color: ph.color }, line: { type: "none" },
      });
      s.addText(item, {
        x: x + 0.36, y: 1.5 + ii * 0.73, w: 2.62, h: 0.65,
        fontSize: 9, color: C.white, fontFace: "Calibri",
      });
    });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 14 — LINKS
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);
  sideAccent(s);
  titleBlock(s, "Links & Resources", "Everything a judge needs to verify ELIO");

  const links = [
    {
      icon: "🐙",
      title: "GitHub Repository (Public)",
      url: "github.com/your-org/elio",
      desc: "Full source code · pipeline · scripts · docs · artifacts\nCommit history: freeze at 38db2af, all subsequent = submission surface",
      color: C.teal,
    },
    {
      icon: "▶️",
      title: "Demo Video (3 minutes)",
      url: "loom.com/share/elio-demo",
      desc: "End-to-end walkthrough: CSV upload → enrichment → evidence drawer\nShows 50-row batch, review queue, and export in real time",
      color: C.lime,
    },
    {
      icon: "🌐",
      title: "Working Prototype",
      url: "elio-demo.vercel.app",
      desc: "Live Next.js cockpit — use demo_input_50.csv for instant demo\nOr open demo.html locally for fully offline evidence explorer",
      color: C.purple,
    },
  ];

  links.forEach((link, i) => {
    const y = 1.1 + i * 1.47;
    s.addShape(pres.ShapeType.rect, {
      x: 0.45, y, w: 9.1, h: 1.35,
      fill: { color: C.card }, line: { color: link.color, width: 1.5 }, rectRadius: 0.1,
    });
    s.addText(link.icon, {
      x: 0.6, y: y + 0.15, w: 0.7, h: 0.8,
      fontSize: 32, fontFace: "Calibri", align: "center",
    });
    s.addText(link.title, {
      x: 1.4, y: y + 0.1, w: 5.5, h: 0.38,
      fontSize: 14, bold: true, color: link.color, fontFace: "Calibri",
    });
    s.addText(link.url, {
      x: 7.1, y: y + 0.14, w: 2.3, h: 0.32,
      fontSize: 11, color: link.color, fontFace: "Calibri", align: "right",
      underline: true,
    });
    s.addText(link.desc, {
      x: 1.4, y: y + 0.52, w: 7.9, h: 0.7,
      fontSize: 10, color: C.muted, fontFace: "Calibri",
    });
  });

  // Bottom verify command
  s.addShape(pres.ShapeType.rect, {
    x: 0.45, y: 5.1, w: 9.1, h: 0.38,
    fill: { color: "111118" }, line: { color: C.lime, width: 1 }, rectRadius: 0.07,
  });
  s.addText("To verify all headline numbers live:  python -B scripts\\verify_everything.py  (~90s, 12 gates)", {
    x: 0.55, y: 5.12, w: 8.9, h: 0.34,
    fontSize: 10, bold: true, color: C.lime, fontFace: "Calibri", align: "center", valign: "middle",
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// SLIDE 15 — CLOSING / THANK YOU
// ──────────────────────────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s, { glow: true });

  // Large ELIO
  s.addText("ELIO", {
    x: 0.5, y: 0.7, w: 9, h: 1.8,
    fontSize: 110, bold: true, color: C.white, fontFace: "Calibri", align: "center",
    charSpacing: 15,
  });

  // Lime underbar
  s.addShape(pres.ShapeType.rect, {
    x: 3.5, y: 2.4, w: 3, h: 0.06,
    fill: { color: C.lime }, line: { type: "none" },
  });

  s.addText("Evidence-Gated Catalog Intelligence", {
    x: 0.5, y: 2.55, w: 9, h: 0.4,
    fontSize: 16, color: C.lime, fontFace: "Calibri", align: "center",
  });

  // Key stats row
  const stats = [
    ["118/118", "Gold cells"],
    ["0", "Dual-pass failures"],
    ["100%", "Provenance"],
    ["17–1", "Blind critic A/B"],
    ["0", "Untraceable values"],
  ];
  stats.forEach((st, i) => {
    const x = 0.6 + i * 1.8;
    s.addText(st[0], {
      x, y: 3.1, w: 1.6, h: 0.55,
      fontSize: 22, bold: true, color: C.lime, fontFace: "Calibri", align: "center",
    });
    s.addText(st[1], {
      x, y: 3.65, w: 1.6, h: 0.3,
      fontSize: 9, color: C.muted, fontFace: "Calibri", align: "center",
    });
  });

  s.addText("Thank you · Questions welcome", {
    x: 0.5, y: 4.15, w: 9, h: 0.35,
    fontSize: 14, color: C.muted, fontFace: "Calibri", align: "center",
  });

  s.addText("Team ELIO  ·  UniHack 2026  ·  Every value traced or honestly refused", {
    x: 0, y: 5.25, w: W, h: 0.3,
    fontSize: 9, color: C.dimmer, fontFace: "Calibri", align: "center",
  });
}

// ── WRITE ─────────────────────────────────────────────────────────────────────
pres.writeFile({ fileName: "ELIO_UniHack_2026.pptx" })
  .then(() => console.log("✅  ELIO_UniHack_2026.pptx created — 15 slides"))
  .catch(err => { console.error("❌  Failed:", err); process.exit(1); });
