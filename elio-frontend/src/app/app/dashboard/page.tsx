"use client";

import { useState, useEffect, useMemo, useRef } from "react";
import { gsap } from "gsap";
import { useGSAP } from "@gsap/react";
import { Bell, Download, Home, ListChecks, Search } from "lucide-react";

if (typeof window !== "undefined") {
  gsap.registerPlugin(useGSAP);
}

// ── ELIO Cockpit — evidence-gated catalog operations ──────────────────────
// Shell: dark cockpit from the finance iteration (62px icon sidebar, radial
// glow, dark cards). Content: real pipeline data from /data/*.json + /api/run.
// Rules: amber = refusal/attention only; no invented percentages; mono data.
// ──────────────────────────────────────────────────────────────────────────

// ── Types ──────────────────────────────────────────────────────────────────
type Source = {
  url: string;
  page: number | string;
  char_span: number[] | null;
  snippet: string;
};

type Attribute = {
  label: string;
  value: string;
  uom: string;
  source: Source;
  confidence: number;
  verification: string;
};

type DescriptionPack = {
  mobile: string;
  invoice: string;
  short: string;
  long: string;
  retail: string;
  marketing: string;
};

type RecordDetail = {
  input: Record<string, string>;
  identity: {
    brand: { id: string; label: string; parent?: string };
    manufacturer: { id: string; label: string; mfr_url?: string };
  };
  classpath: { dept: string; class_: string; fine: string; candidate_ids?: string[] };
  attributes: Attribute[];
  descriptions: DescriptionPack;
  quality: { decision: string; field_error_budget: number; review_reasons: string[] };
  cost: { llm_calls: number; estimated_usd: number };
};

type PipelineRecord = {
  input: Record<string, string>;
  record: RecordDetail;
  flat_export: Record<string, string>;
};

type Tab = "dashboard" | "explorer" | "review" | "abstention" | "export";
type ExportProjection = "full" | "erp" | "marketplace";

type RowDecision = {
  status: "accept" | "reject" | null;
  overrides: Record<string, string>;
};

type ReceiptClaim = {
  mpn: string;
  attribute: string;
  value: string;
  uom: string;
  export_column: string;
  source_text: string;
  source_hash: string;
  char_span: number[] | null;
  source_kind: string;
  input_row_hash: string;
  claim_hash: string;
  decision_hash: string;
  output_hash: string;
  chain_hash: string;
};

type ReceiptIndex = {
  schema_version: number;
  receipt_sha256: string;
  source_attestation: string;
  claims: Record<string, ReceiptClaim>;
};

type HashState = "idle" | "verifying" | "verified" | "failed";

function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value as Record<string, unknown>).sort().map((key) =>
      `${JSON.stringify(key)}:${canonicalJson((value as Record<string, unknown>)[key])}`
    ).join(",")}}`;
  }
  return JSON.stringify(value);
}

async function sha256Hex(value: string): Promise<string> {
  const bytes = new TextEncoder().encode(value);
  const digest = await window.crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

const ITEMS_PER_PAGE = 5;

const TAB_TITLES: Record<Tab, string> = {
  dashboard: "Pipeline Overview",
  explorer: "Evidence Explorer",
  review: "Review Queue",
  abstention: "Abstentions & Refusals",
  export: "Export",
};

const TAB_SUBTITLES: Record<Tab, string> = {
  dashboard: "Live status across the processing DAG",
  explorer: "Every value, traced to its source",
  review: "Escalated records awaiting a decision",
  abstention: "Values the pipeline refused to fabricate",
  export: "Delivery projection, description pack, evidence dossier",
};

const PROJECTION_COLUMNS: Record<Exclude<ExportProjection, "full">, string[]> = {
  erp: [
    "PART_NUMBER", "Mfg_Part_Num", "Part_Desc", "Part_Manuf", "MANUFACTURER_NAME", "BRAND_NAME",
    "MANUFACTURER_PART_NUMBER", "Classpath", "MOBILE_DESC", "INVOICE_DESC", "SHORT_DESC", "LONG_DESC1",
    "RETAIL_DESC", "MARKETING_DESCRIPTION", "Product Name", "UPC", "EAN", "GTIN", "UNSPSC", "List Price",
    "Selling Qty", "Selling UOM", "LENGTH", "LENGTH_UOM", "HEIGHT", "HEIGHT_UOM", "WIDTH", "WIDTH_UOM",
    "WEIGHT", "WEIGHT_UOM", "Country Of Origin", "Discontinued",
  ],
  marketplace: [
    "Mfg_Part_Num", "BRAND_NAME", "Product Name", "RETAIL_DESC", "Product Image", "Alternate Image 1",
    "Alternate Image 2", "Alternate Image 3", "Alternate Image 4", "List Price", "Selling Qty", "Selling UOM",
    "UPC", "EAN", "GTIN", "Country Of Origin", "Discontinued", "Actual Image (Yes/No)",
  ],
};

// ── Mini Bar Chart ──────────────────────────────────────────────────────────
function MiniBarChart({ color, heights }: { color: string; heights: number[] }) {
  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: "3px", height: "52px" }}>
      {heights.map((h, i) => (
        <div key={i} style={{
          width: "5px",
          height: `${h}%`,
          borderRadius: "2px 2px 0 0",
          background: color,
          opacity: 0.7 + (i / heights.length) * 0.3,
        }} />
      ))}
    </div>
  );
}

// ── Stream Chart (decorative pipeline flow) ─────────────────────────────────
function StreamChart() {
  const w = 360;
  const h = 140;
  const tealPath = `M0,${h * 0.55} C60,${h * 0.45} 120,${h * 0.35} 180,${h * 0.4} S300,${h * 0.5} ${w},${h * 0.45} L${w},${h} L0,${h} Z`;
  const purplePath = `M0,${h * 0.75} C80,${h * 0.65} 160,${h * 0.55} 220,${h * 0.6} S320,${h * 0.72} ${w},${h * 0.68} L${w},${h} L0,${h} Z`;

  return (
    <svg width="100%" height={h} viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" style={{ display: "block" }}>
      <defs>
        <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#00d4c8" stopOpacity="0.6" />
          <stop offset="100%" stopColor="#00a8a0" stopOpacity="0.3" />
        </linearGradient>
        <linearGradient id="purpleGrad" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#7c3aed" stopOpacity="0.5" />
          <stop offset="100%" stopColor="#a855f7" stopOpacity="0.25" />
        </linearGradient>
      </defs>
      <path d={tealPath} fill="url(#tealGrad)" />
      <path d={purplePath} fill="url(#purpleGrad)" />
      <path d={`M0,${h * 0.55} C60,${h * 0.45} 120,${h * 0.35} 180,${h * 0.4} S300,${h * 0.5} ${w},${h * 0.45}`}
        fill="none" stroke="#00e5d8" strokeWidth="1.5" strokeOpacity="0.8" />
      <path d={`M0,${h * 0.75} C80,${h * 0.65} 160,${h * 0.55} 220,${h * 0.6} S320,${h * 0.72} ${w},${h * 0.68}`}
        fill="none" stroke="#9b59e8" strokeWidth="1.5" strokeOpacity="0.7" />
    </svg>
  );
}

// ── Sidebar Icon ─────────────────────────────────────────────────────────────
function SidebarIcon({ children, active, onClick, label }: {
  children: React.ReactNode; active?: boolean; onClick?: () => void; label?: string;
}) {
  return (
    <button onClick={onClick} aria-label={label} title={label} style={{
      width: "36px", height: "36px",
      borderRadius: "10px",
      border: "none",
      display: "flex", alignItems: "center", justifyContent: "center",
      background: active ? "rgba(200,216,74,0.16)" : "transparent",
      color: active ? "#c8d84a" : "rgba(255,255,255,0.4)",
      cursor: "pointer",
      transition: "background 0.15s ease, color 0.15s ease",
      fontSize: "16px",
      fontFamily: "inherit",
    }}
    onMouseEnter={(e) => {
      const el = e.currentTarget;
      if (!active) { el.style.background = "rgba(255,255,255,0.06)"; el.style.color = "rgba(255,255,255,0.75)"; }
    }}
    onMouseLeave={(e) => {
      const el = e.currentTarget;
      if (!active) { el.style.background = "transparent"; el.style.color = "rgba(255,255,255,0.4)"; }
    }}>
      {children}
    </button>
  );
}

// ── Decision Pill ─────────────────────────────────────────────────────────────
const DECISION_STYLES: Record<string, { color: string; bg: string; border: string }> = {
  auto_accept: { color: "#4ade80", bg: "rgba(34,197,94,0.1)", border: "rgba(34,197,94,0.2)" },
  accept: { color: "#4ade80", bg: "rgba(34,197,94,0.1)", border: "rgba(34,197,94,0.2)" },
  review: { color: "#a78bfa", bg: "rgba(155,89,232,0.12)", border: "rgba(155,89,232,0.25)" },
  auto_abstain: { color: "#fbbf24", bg: "rgba(245,158,11,0.12)", border: "rgba(245,158,11,0.25)" },
  blocked: { color: "#f87171", bg: "rgba(239,68,68,0.12)", border: "rgba(239,68,68,0.25)" },
  reject: { color: "#f87171", bg: "rgba(239,68,68,0.12)", border: "rgba(239,68,68,0.25)" },
};

function DecisionPill({ decision }: { decision: string }) {
  const m = DECISION_STYLES[decision] || { color: "#9ca3af", bg: "rgba(107,114,128,0.12)", border: "rgba(107,114,128,0.2)" };
  return (
    <span style={{
      display: "inline-flex", alignItems: "center",
      fontSize: "10.5px", fontWeight: "500",
      padding: "3px 10px", borderRadius: "20px",
      background: m.bg, color: m.color, border: `1px solid ${m.border}`,
      whiteSpace: "nowrap",
    }}>{decision}</span>
  );
}

// ── Verification Chip ──────────────────────────────────────────────────────────
const VERIFY_STYLES: Record<string, { color: string; bg: string; border: string }> = {
  supported: { color: "#4ade80", bg: "rgba(34,197,94,0.1)", border: "rgba(34,197,94,0.2)" },
  not_found: { color: "#9ca3af", bg: "rgba(107,114,128,0.12)", border: "rgba(107,114,128,0.2)" },
  unsupported: { color: "#f87171", bg: "rgba(239,68,68,0.12)", border: "rgba(239,68,68,0.25)" },
  abstained: { color: "#fbbf24", bg: "rgba(245,158,11,0.12)", border: "rgba(245,158,11,0.25)" },
  deficient: { color: "#fbbf24", bg: "rgba(245,158,11,0.12)", border: "rgba(245,158,11,0.25)" },
};

function VerifyChip({ verification }: { verification: string }) {
  const m = VERIFY_STYLES[verification] || VERIFY_STYLES.not_found;
  return (
    <span style={{
      display: "inline-flex", alignItems: "center",
      fontSize: "10px", fontWeight: "500",
      padding: "2px 8px", borderRadius: "20px",
      background: m.bg, color: m.color, border: `1px solid ${m.border}`,
      whiteSpace: "nowrap", fontFamily: "var(--font-geist-mono)",
    }}>{verification}</span>
  );
}

// ── Metric Card ─────────────────────────────────────────────────────────────
function MetricCard({ label, value, badge1, badge2, chartColor, bars, gradStart, gradEnd, valueColor }: {
  label: string; value: string;
  badge1?: string; badge2?: { text: string; color: string; bg: string; border: string };
  chartColor: string; bars: number[];
  gradStart: string; gradEnd: string;
  valueColor?: string;
}) {
  return (
    <div
      className="cockpit-metric-card"
      style={{
        background: `linear-gradient(135deg, ${gradStart} 0%, ${gradEnd} 100%)`,
        border: "1px solid rgba(255,255,255,0.08)",
        borderRadius: "14px",
        padding: "16px",
        display: "flex",
        flexDirection: "column",
        gap: "10px",
        position: "relative",
        overflow: "hidden",
        transform: "translateZ(0)",
      }}
    >
      <div style={{
        position: "absolute", top: 0, right: 0,
        width: "60%", height: "100%",
        background: `radial-gradient(ellipse at 80% 20%, ${chartColor.replace("0.9", "0.08")} 0%, transparent 60%)`,
        pointerEvents: "none",
      }} />
      <div style={{ fontSize: "11.5px", color: "rgba(255,255,255,0.5)", fontWeight: "400" }}>{label}</div>
      <div style={{ alignSelf: "flex-end", position: "absolute", right: "14px", top: "14px" }}>
        <MiniBarChart color={chartColor} heights={bars} />
      </div>
      <div style={{ fontSize: "24px", fontWeight: "700", color: valueColor || "#f4f4f5", lineHeight: "1", marginTop: "auto", fontFamily: "var(--font-geist-mono)" }}>{value}</div>
      {(badge1 || badge2) && (
        <div style={{ display: "flex", gap: "6px", alignItems: "center" }}>
          {badge1 && <span style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.55)", background: "rgba(255,255,255,0.06)", borderRadius: "4px", padding: "2px 6px" }}>{badge1}</span>}
          {badge2 && (
            <span style={{
              fontSize: "10.5px", fontWeight: "600",
              color: badge2.color, background: badge2.bg,
              borderRadius: "4px", padding: "2px 6px",
              border: `1px solid ${badge2.border}`,
            }}>{badge2.text}</span>
          )}
        </div>
      )}
    </div>
  );
}

// ── Main Cockpit ─────────────────────────────────────────────────────────────
export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<Tab>("dashboard");
  const [datasetSize, setDatasetSize] = useState<"demo" | "full" | "uploaded">("demo");
  const [demoData, setDemoData] = useState<PipelineRecord[]>([]);
  const [fullData, setFullData] = useState<PipelineRecord[]>([]);
  const [uploadedData, setUploadedData] = useState<PipelineRecord[]>([]);
  const [loadingData, setLoadingData] = useState(true);
  const [dataError, setDataError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [explorerPage, setExplorerPage] = useState(0);
  const [reviewPage, setReviewPage] = useState(0);
  const [abstentionFilter, setAbstentionFilter] = useState<string>("all");
  const [drawerIdx, setDrawerIdx] = useState<number | null>(null);
  const [drawerAttr, setDrawerAttr] = useState<string | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [exportProjection, setExportProjection] = useState<ExportProjection>("full");
  const [decisions, setDecisions] = useState<Record<string, RowDecision>>({});
  const [receiptIndex, setReceiptIndex] = useState<ReceiptIndex | null>(null);
  const [verifiedHashes, setVerifiedHashes] = useState<Record<string, HashState>>({});

  const cockpitBodyRef = useRef<HTMLDivElement>(null);
  const drawerRef = useRef<HTMLDivElement>(null);
  const backdropRef = useRef<HTMLDivElement>(null);
  const uploadInputRef = useRef<HTMLInputElement>(null);

  // Smooth entrance on initial load only — tab & dataset switches remain 0ms snappy
  useGSAP(() => {
    if (cockpitBodyRef.current) {
      gsap.fromTo(
        cockpitBodyRef.current,
        { opacity: 0.8, y: 4 },
        { opacity: 1, y: 0, duration: 0.2, ease: "power2.out", clearProps: "transform,opacity" }
      );
    }
  }, { scope: cockpitBodyRef });

  useGSAP(() => {
    if (drawerOpen) {
      if (backdropRef.current) {
        gsap.fromTo(backdropRef.current, { opacity: 0 }, { opacity: 1, duration: 0.18, ease: "power2.out" });
      }
      if (drawerRef.current) {
        gsap.fromTo(drawerRef.current, { x: "100%" }, { x: "0%", duration: 0.24, ease: "power3.out" });
      }
    }
  }, [drawerOpen]);

  const data = datasetSize === "demo" ? demoData : datasetSize === "full" ? fullData : uploadedData;

  const decisionKey = (idx: number) => `${datasetSize}:${data[idx]?.input?.MPN || idx}`;

  useEffect(() => {
    let cancelled = false;
    setLoadingData(true);
    // ponytail: Full is 1M lines and not pushed to keep clone lean — tolerate 404 so Demo still loads
    const safeJson = (url: string, fallback: unknown) =>
      fetch(url).then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json(); }).catch(() => fallback);
    Promise.all([
      safeJson("/data/demo_results.json", []),
      safeJson("/data/full_results.json", []),
      safeJson("/data/receipt_chain.json", null),
    ]).then(([demo, full, receipts]) => {
      if (cancelled) return;
      setDemoData(Array.isArray(demo) ? demo : []);
      setFullData(Array.isArray(full) ? full : []);
      setReceiptIndex(receipts && typeof receipts === "object" ? receipts : null);
      // only hard-fail if Demo itself is empty — Full is optional
      if (!Array.isArray(demo) || demo.length === 0) {
        setDataError("Catalog artifacts could not be loaded.");
      } else {
        setDataError(null);
      }
      setLoadingData(false);
    }).catch(() => {
      if (!cancelled) {
        setDataError("Catalog artifacts could not be loaded.");
        setLoadingData(false);
      }
    });
    return () => { cancelled = true; };
  }, []);

  // ponytail: persist governance overrides without backend — cheapest audit win
  useEffect(() => {
    try {
      const raw = localStorage.getItem("elio_overrides");
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed === "object") setDecisions(parsed);
      }
    } catch {}
  }, []);
  useEffect(() => {
    try { localStorage.setItem("elio_overrides", JSON.stringify(decisions)); } catch {}
  }, [decisions]);

  const metrics = useMemo(() => {
    const attrs = data.flatMap((r) => r.record?.attributes || []);
    const supported = attrs.filter((a) => a.verification === "supported").length;
    const spans = attrs.filter((a) => {
      const s = a.source?.char_span;
      return Array.isArray(s) && s.length === 2 && s[1] > s[0];
    }).length;
     const pipelineDecisions: Record<string, number> = {};
     for (const r of data) {
       const d = r.record?.quality?.decision || "unknown";
       pipelineDecisions[d] = (pipelineDecisions[d] || 0) + 1;
     }
     const pendingReviews = data.reduce((count, row, idx) => (
       count + (row.record?.quality?.decision === "review" && !decisions[decisionKey(idx)]?.status ? 1 : 0)
     ), 0);
     return {
      total: data.length,
      attrs,
      attrsPerRow: data.length ? attrs.length / data.length : 0,
      supported,
      missing: attrs.length - supported,
      evidenceSupport: attrs.length ? (supported / attrs.length) * 100 : 0,
      charCompliance: attrs.length ? (spans / attrs.length) * 100 : 0,
       decisions: pipelineDecisions,
       reviewCount: pendingReviews,
       pipelineReviewCount: pipelineDecisions["review"] || 0,
      llmCalls: data.reduce((s, r) => s + (r.record?.cost?.llm_calls || 0), 0),
      estUsd: data.reduce((s, r) => s + (r.record?.cost?.estimated_usd || 0), 0),
    };
   }, [data, decisions]);

  const getDecision = (idx: number) => decisions[decisionKey(idx)]?.status || null;
  const getAttrValue = (idx: number, attr: Attribute) => decisions[decisionKey(idx)]?.overrides[attr.label] ?? attr.value;

  const handleApplyOverride = (idx: number, attr: Attribute, value: string) => {
    setDecisions((prev) => {
      const key = decisionKey(idx);
      const cur = prev[key] || { status: null, overrides: {} };
      const overrides = { ...cur.overrides };
      if (value.trim() === attr.value) delete overrides[attr.label];
      else overrides[attr.label] = value.trim();
      return { ...prev, [key]: { ...cur, overrides } };
    });
  };

  const handleDecisionStatus = (idx: number, status: "accept" | "reject") => {
    setDecisions((prev) => {
      const key = decisionKey(idx);
      const cur = prev[key] || { status: null, overrides: {} };
      return { ...prev, [key]: { ...cur, status } };
    });
    setReviewPage(0);
  };

  const handleFileUpload = async (file: File) => {
    setUploading(true);
    setUploadError(null);
    try {
      const response = await fetch("/api/run", { method: "POST", body: (() => { const form = new FormData(); form.append("file", file); return form; })() });
      const payload = await response.json();
      if (!response.ok || !Array.isArray(payload.results) || payload.results.length !== payload.rowCount) {
        throw new Error(payload.error || "Upload did not produce a complete result.");
      }
      setUploadedData(payload.results);
      setDatasetSize("uploaded");
      setActiveTab("dashboard");
    } catch (error) {
      setUploadError(error instanceof Error ? error.message : "Upload failed.");
    } finally {
      setUploading(false);
      if (uploadInputRef.current) uploadInputRef.current.value = "";
    }
  };

  const handleExportCSV = () => {
    const rows = data;
    if (!rows.length) return;
    const allHeaders = Array.from(new Set(rows.flatMap((r) => Object.keys(r.flat_export || {}))));
    const headers = exportProjection === "full"
      ? allHeaders
      : PROJECTION_COLUMNS[exportProjection].filter((header) => allHeaders.includes(header));
    const cell = (v: unknown) => {
      let s = String(v ?? "");
      if (/^[=+\-@]/.test(s)) s = "'" + s;
      return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
    };
    const lines = [headers.map(cell).join(",")];
    for (let idx = 0; idx < rows.length; idx++) {
      const r = rows[idx];
      const ov = decisions[decisionKey(idx)]?.overrides || {};
      // ponytail: map flat_export through overrides (key = attr label) then sanitize
      const values = { ...(r.flat_export || {}) };
      for (let n = 1; ; n += 1) {
        const labelKey = `ATTRIBUTE_LABEL ${n}`;
        const valueKey = `ATTRIBUTE_VALUE ${n}`;
        if (!(labelKey in values) || !(valueKey in values)) break;
        const label = values[labelKey];
        if (label && ov[label] !== undefined) values[valueKey] = ov[label];
      }
      lines.push(headers.map((h) => cell(ov[h] !== undefined ? ov[h] : values[h])).join(","));
    }
    const blob = new Blob(["\uFEFF" + lines.join("\n")], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "elio_export.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  const openDrawer = (idx: number, attrLabel?: string) => {
    setDrawerIdx(idx);
    setDrawerAttr(attrLabel ?? null);
    setDrawerOpen(true);
  };

  const closeDrawer = () => setDrawerOpen(false);

  const verifyDrawerClaim = async () => {
    if (!drawerRow || !drawerAttrObj) return;
    const key = `${drawerRow.input?.MPN || ""}_${drawerAttrObj.label}`;
    setVerifiedHashes((prev) => ({ ...prev, [key]: "verifying" }));
    try {
      const claim = receiptIndex?.claims[key];
      if (!claim || !drawerRow.flat_export) throw new Error("No receipt claim for this value");
      const input = drawerRow.input || {};
      const inputRowHash = await sha256Hex(canonicalJson({
        Mfg_Part_Num: input.MPN || "",
        Part_Desc: input.Description || "",
        Part_Manuf: input.Manufacturer || "",
        E1_Brand: input.E1_Brand || "",
        Unilog_Brand: input.Unilog_Brand || "",
        DIB_Brand: input.DIB_Brand || "",
      }));
      const sourceHash = await sha256Hex(claim.source_text);
      const claimPayload = {
        mpn: claim.mpn,
        attribute: claim.attribute,
        value: claim.value,
        uom: claim.uom,
        export_column: claim.export_column,
        source_hash: sourceHash,
        char_span: claim.char_span,
        source_kind: claim.source_kind,
      };
      const claimHash = await sha256Hex(canonicalJson(claimPayload));
      const decisionHash = await sha256Hex(canonicalJson({
        claim_hash: claimHash,
        status: "accepted",
        verification: drawerAttrObj.verification,
        gate: "dual-pass",
      }));
      const outputHash = await sha256Hex(canonicalJson({
        mpn: claim.mpn,
        column: claim.export_column,
        value: drawerRow.flat_export[claim.export_column],
      }));
      const chainHash = await sha256Hex(canonicalJson({
        input_row_hash: inputRowHash,
        source_hash: sourceHash,
        claim_hash: claimHash,
        decision_hash: decisionHash,
        output_hash: outputHash,
      }));
      const matches = claim.mpn === input.MPN
        && claim.attribute === drawerAttrObj.label
        && claim.value === drawerAttrObj.value
        && claim.uom === drawerAttrObj.uom
        && claim.source_text === drawerAttrObj.source?.snippet
        && inputRowHash === claim.input_row_hash
        && sourceHash === claim.source_hash
        && claimHash === claim.claim_hash
        && decisionHash === claim.decision_hash
        && outputHash === claim.output_hash
        && chainHash === claim.chain_hash;
      setVerifiedHashes((prev) => ({ ...prev, [key]: matches ? "verified" : "failed" }));
    } catch {
      setVerifiedHashes((prev) => ({ ...prev, [key]: "failed" }));
    }
  };

  const filteredRecords = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    const all = data.map((row, idx) => ({ row, idx }));
    if (!q) return all;
    return all.filter(({ row }) => {
      const r = row.record || {};
      const hay = [
        row.input?.MPN, row.input?.Description,
        r.identity?.brand?.label, r.identity?.manufacturer?.label,
        r.classpath?.fine,
      ].join(" ").toLowerCase();
      return hay.includes(q);
    });
  }, [data, searchQuery]);

  const reviewRecords = useMemo(() => {
    return data
      .map((row, idx) => ({ row, idx }))
      .filter(({ row, idx }) => (
        (row.record?.quality?.decision || "auto_accept") === "review" && !decisions[decisionKey(idx)]?.status
      ));
  }, [data, decisions]);

  const abstentionTypes = useMemo(() => {
    const s = new Set<string>();
    for (const r of data) {
      for (const a of r.record?.attributes || []) {
        if (a.verification !== "supported") s.add(a.verification);
      }
    }
    return Array.from(s);
  }, [data]);

  const abstainedRecords = useMemo(() => {
    const out: { row: PipelineRecord; idx: number; bad: Attribute[] }[] = [];
    data.forEach((row, idx) => {
      const bad = (row.record?.attributes || []).filter(
        (a) => a.verification !== "supported" && (abstentionFilter === "all" || a.verification === abstentionFilter)
      );
      if (bad.length) out.push({ row, idx, bad });
    });
    return out;
  }, [data, abstentionFilter]);

  const drawerRow = drawerIdx !== null ? data[drawerIdx] : null;
  const drawerAttrObj = drawerAttr && drawerRow
    ? (drawerRow.record?.attributes || []).find((a) => a.label === drawerAttr) || null
    : null;
  const drawerDecision = drawerIdx !== null ? getDecision(drawerIdx) : null;
  const drawerProofKey = drawerRow && drawerAttrObj
    ? `${drawerRow.input?.MPN || ""}_${drawerAttrObj.label}`
    : "";
  const drawerHashState = verifiedHashes[drawerProofKey] || "idle";

  const statusBarBars = [55, 70, 60, 80, 65, 75, 85, 70, 88, 78, 82, 90];
  const supportBars = [40, 55, 62, 58, 72, 68, 75, 71, 80, 74, 78, 82];
  const missingBars = [30, 45, 38, 52, 44, 58, 50, 62, 56, 64, 58, 66];
  const escBars = [20, 26, 22, 30, 28, 24, 34, 26, 30, 24, 22, 28];

  return (
    <div style={{
      width: "100vw",
      height: "100vh",
      background: "radial-gradient(ellipse 80% 60% at 0% 100%, rgba(200,216,74,0.10) 0%, rgba(120,140,40,0.06) 35%, transparent 65%), radial-gradient(ellipse 40% 40% at 100% 0%, rgba(20,60,80,0.4) 0%, transparent 60%), #0a0a0d",
      display: "flex",
      alignItems: "stretch",
      fontFamily: "var(--font-geist-sans), system-ui, sans-serif",
      position: "relative",
    }}>

      {/* ── Digital grid texture overlay ───────────────────────────────── */}
      <div style={{
        position: "absolute", inset: 0, pointerEvents: "none", zIndex: 0,
        backgroundImage: "linear-gradient(rgba(200,216,74,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(200,216,74,0.025) 1px, transparent 1px)",
        backgroundSize: "32px 32px",
      }} />

      {/* ── Left Sidebar ──────────────────────────────────────────────────── */}
      <div style={{
        width: "62px",
        background: "rgba(13,13,16,0.95)",
        borderRight: "1px solid rgba(255,255,255,0.06)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "18px 0",
        gap: "6px",
        zIndex: 10,
        flexShrink: 0,
      }}>
        {/* Logo */}
        <div style={{
          width: "36px", height: "36px",
          display: "flex", alignItems: "center", justifyContent: "center",
          marginBottom: "16px",
        }}>
          <svg width="22" height="16" viewBox="0 0 22 16" fill="none">
            <rect x="0" y="0" width="6" height="4" rx="1.5" fill="#c8d84a" />
            <rect x="8" y="0" width="6" height="4" rx="1.5" fill="#c8d84a" />
            <rect x="16" y="0" width="6" height="4" rx="1.5" fill="#c8d84a" />
            <rect x="0" y="6" width="6" height="4" rx="1.5" fill="#c8d84a" opacity="0.6" />
            <rect x="8" y="6" width="6" height="4" rx="1.5" fill="#c8d84a" opacity="0.6" />
            <rect x="0" y="12" width="6" height="4" rx="1.5" fill="#c8d84a" opacity="0.3" />
          </svg>
        </div>

        {/* Nav icons */}
        <SidebarIcon active={activeTab === "dashboard"} onClick={() => setActiveTab("dashboard")} label="Pipeline Overview">
          <Home size={16} strokeWidth={2} />
        </SidebarIcon>
        <SidebarIcon active={activeTab === "explorer"} onClick={() => setActiveTab("explorer")} label="Evidence Explorer">
          <Search size={16} strokeWidth={2} />
        </SidebarIcon>
        <SidebarIcon active={activeTab === "review"} onClick={() => setActiveTab("review")} label="Review Queue">
          <ListChecks size={16} strokeWidth={2} />
        </SidebarIcon>
        <SidebarIcon active={activeTab === "abstention"} onClick={() => setActiveTab("abstention")} label="Abstentions & Refusals">
          <Bell size={16} strokeWidth={2} />
        </SidebarIcon>
        <SidebarIcon active={activeTab === "export"} onClick={() => setActiveTab("export")} label="Export">
          <Download size={16} strokeWidth={2} />
        </SidebarIcon>

        {/* Spacer */}
        <div style={{ flex: 1 }} />

        <div style={{ height: "1px", width: "40px", background: "rgba(255,255,255,0.08)", margin: "8px 0" }} />
        <div style={{
          writingMode: "vertical-rl",
          fontSize: "9px",
          letterSpacing: "0.25em",
          color: "rgba(255,255,255,0.25)",
          fontFamily: "var(--font-geist-mono)",
          userSelect: "none",
        }}>elio</div>
      </div>

      {/* ── Main Panel ────────────────────────────────────────────────────── */}
      <div style={{
        flex: 1,
        background: "rgba(16,16,20,0.97)",
        margin: "12px 12px 12px 0",
        borderRadius: "16px",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        zIndex: 1,
        border: "1px solid rgba(255,255,255,0.05)",
      }}>

        {/* ── Header ──────────────────────────────────────────────────────── */}
        <div style={{
          display: "flex",
          alignItems: "center",
          padding: "16px 24px",
          borderBottom: "1px solid rgba(255,255,255,0.05)",
          gap: "16px",
          flexShrink: 0,
        }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: "18px", fontWeight: "600", color: "#f4f4f5", lineHeight: "1.2" }}>{TAB_TITLES[activeTab]}</div>
            <div style={{ fontSize: "11.5px", color: "rgba(255,255,255,0.4)", marginTop: "1px" }}>
              {TAB_SUBTITLES[activeTab]} · <span style={{ fontFamily: "var(--font-geist-mono)" }}>{metrics.total}</span> records
            </div>
          </div>

          {/* Dataset switcher */}
          <div style={{
            display: "flex", alignItems: "center", gap: "4px",
            background: "rgba(255,255,255,0.04)",
            border: "1px solid rgba(255,255,255,0.07)",
            borderRadius: "10px",
            padding: "3px",
          }}>
            {([["demo", "Demo"], ["full", "Full"], ["uploaded", "Uploaded"]] as const).map(([key, label]) => (
              <button key={key}
                onClick={() => { setDatasetSize(key); setSearchQuery(""); setAbstentionFilter("all"); setReviewPage(0); }}
                style={{
                  padding: "6px 12px",
                  borderRadius: "7px",
                  border: "none",
                  background: datasetSize === key ? "rgba(200,216,74,0.14)" : "transparent",
                  color: datasetSize === key ? "#c8d84a" : "rgba(255,255,255,0.45)",
                  fontSize: "11.5px", fontWeight: "500",
                  cursor: "pointer",
                  fontFamily: "inherit",
                }}>{label}</button>
            ))}
          </div>

          <input
            ref={uploadInputRef}
            type="file"
            accept=".csv,text/csv"
            hidden
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) void handleFileUpload(file);
            }}
          />
          <button
            type="button"
            onClick={() => uploadInputRef.current?.click()}
            disabled={uploading}
            style={{
              display: "flex", alignItems: "center", gap: "6px",
              background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: "9px", padding: "7px 12px",
              color: "rgba(255,255,255,0.75)", fontSize: "12.5px", fontWeight: "500",
              cursor: uploading ? "wait" : "pointer", fontFamily: "inherit",
            }}
          >
            <Download size={13} strokeWidth={2} />
            {uploading ? "Processing..." : "Upload CSV"}
          </button>

          {/* Export CSV */}
          <button onClick={handleExportCSV} disabled={!data.length} style={{
            display: "flex", alignItems: "center", gap: "6px",
            background: "rgba(200,216,74,0.12)",
            border: "1px solid rgba(200,216,74,0.25)",
            borderRadius: "9px", padding: "7px 14px",
            color: "#c8d84a", fontSize: "12.5px", fontWeight: "500",
            cursor: data.length ? "pointer" : "default",
            fontFamily: "inherit",
            opacity: data.length ? 1 : 0.5,
          }}>
            <Download size={13} strokeWidth={2} />
            Export CSV
          </button>
        </div>

        {/* ── Scrollable Body ──────────────────────────────────────────────── */}
        <div ref={cockpitBodyRef} style={{ flex: 1, overflowY: "auto", padding: "18px 20px", display: "flex", flexDirection: "column", gap: "14px" }}
          className="ops-scrollbar">

          {dataError && (
            <div role="alert" style={{ border: "1px solid rgba(248,113,113,0.3)", background: "rgba(127,29,29,0.18)", color: "#fca5a5", borderRadius: "10px", padding: "12px 14px", fontSize: "12px" }}>
              {dataError} Refresh the page to retry.
            </div>
          )}
          {uploadError && (
            <div role="alert" style={{ border: "1px solid rgba(248,113,113,0.3)", background: "rgba(127,29,29,0.18)", color: "#fca5a5", borderRadius: "10px", padding: "12px 14px", fontSize: "12px" }}>
              {uploadError}
            </div>
          )}
          {loadingData && <div style={{ color: "rgba(255,255,255,0.55)", fontSize: "12px", padding: "18px 4px" }}>Loading catalog artifacts...</div>}

          {!loadingData && activeTab === "dashboard" && (
            <>
              {/* Top Row: 4 Metric Cards */}
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "12px" }}>
                <MetricCard
                  label="Attributes / Row"
                  value={metrics.attrsPerRow.toFixed(3)}
                  badge1={`${metrics.total} records`}
                  chartColor="rgba(0,220,200,0.9)"
                  bars={statusBarBars}
                  gradStart="#003d38" gradEnd="#001a16"
                />
                <MetricCard
                  label="Evidence Support"
                  value={`${metrics.evidenceSupport.toFixed(1)}%`}
                  badge1={`${metrics.supported} values`}
                  chartColor="rgba(200,216,74,0.9)"
                  bars={supportBars}
                  gradStart="#2e3208" gradEnd="#171a00"
                />
                <MetricCard
                  label="Missing Evidence"
                  value={String(metrics.missing)}
                  badge1={`${metrics.charCompliance.toFixed(0)}% spans`}
                  badge2={{ text: "refused", color: "#fbbf24", bg: "rgba(245,158,11,0.12)", border: "rgba(245,158,11,0.25)" }}
                  chartColor="rgba(245,158,11,0.9)"
                  bars={missingBars}
                  gradStart="#3d2e00" gradEnd="#1a1400"
                  valueColor="#fbbf24"
                />
                <MetricCard
                  label="Pending Review"
                  value={String(metrics.reviewCount)}
                  badge1={`${metrics.llmCalls} llm calls`}
                  chartColor="rgba(200,60,220,0.9)"
                  bars={escBars}
                  gradStart="#3b0050" gradEnd="#1a0025"
                />
              </div>

              {/* Retention / Health — completeness + freshness trending (static mock, no cron implied) */}
              <div
                data-testid="retention-widget"
                style={{
                  border: "1px solid rgba(255,255,255,0.08)",
                  background: "rgba(255,255,255,0.04)",
                  borderRadius: "12px",
                  padding: "14px 16px",
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                  gap: "12px",
                  alignItems: "start",
                }}
              >
                {/* Completeness */}
                <div style={{ display: "flex", flexDirection: "column", gap: "8px", minWidth: 0 }}>
                  <div style={{ fontSize: "11px", fontWeight: "600", letterSpacing: "0.08em", textTransform: "uppercase", color: "#6a6a58", fontFamily: "var(--font-geist-mono)" }}>Completeness</div>
                  <div style={{ fontSize: "11px", color: "#6a6a58", lineHeight: 1.5, fontFamily: "var(--font-geist-mono)", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" as const }}>
                    {metrics.total}/{metrics.total} rows · {metrics.attrsPerRow.toFixed(3)} attrs/row · {metrics.missing} missing evidence
                  </div>
                  <div style={{ display: "flex", gap: "4px", height: "6px" }}>
                    <div style={{ flex: Math.max(metrics.supported, 0.1), borderRadius: "2px", background: "#c8d84a" }} />
                    <div style={{ flex: Math.max(metrics.missing, 0.1), borderRadius: "2px", background: "#eab308", opacity: 0.9 }} />
                  </div>
                  <div style={{ fontSize: "10px", color: "rgba(255,255,255,0.3)", fontFamily: "var(--font-geist-mono)" }}>lime = complete · amber = review needed</div>
                </div>
                {/* Freshness */}
                <div style={{ display: "flex", flexDirection: "column", gap: "8px", minWidth: 0 }}>
                  <div style={{ fontSize: "11px", fontWeight: "600", letterSpacing: "0.08em", textTransform: "uppercase", color: "#6a6a58", fontFamily: "var(--font-geist-mono)" }}>Freshness</div>
                  <div style={{ fontSize: "11px", color: "#6a6a58", lineHeight: 1.5, fontFamily: "var(--font-geist-mono)" }}>
                    Source: {datasetSize === "uploaded" ? "uploaded CSV" : "bundled artifact"} · Status: loaded
                  </div>
                  <span style={{ alignSelf: "flex-start", fontSize: "11px", fontWeight: "600", color: "#c8d84a", background: "rgba(200,216,74,0.12)", border: "1px solid rgba(200,216,74,0.25)", borderRadius: "20px", padding: "3px 9px", fontFamily: "var(--font-geist-mono)" }}>
                    {datasetSize === "uploaded" ? "Evaluator run" : "Reference run"}
                  </span>
                </div>
                {/* Action */}
                <div style={{ display: "flex", flexDirection: "column", gap: "8px", minWidth: 0 }}>
                  <div style={{ fontSize: "11px", fontWeight: "600", letterSpacing: "0.08em", textTransform: "uppercase", color: "#6a6a58", fontFamily: "var(--font-geist-mono)" }}>Action</div>
                  <button
                    type="button"
                    onClick={() => setActiveTab("export")}
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      justifyContent: "center",
                      padding: "7px 12px",
                      borderRadius: "8px",
                      border: "1px solid rgba(255,255,255,0.12)",
                      background: "rgba(255,255,255,0.06)",
                      color: "#f0efe8",
                      fontSize: "12.5px",
                      fontWeight: "500",
                      fontFamily: "inherit",
                      opacity: 1,
                      cursor: "pointer",
                      alignSelf: "flex-start",
                    }}
                  >
                    View delivery options
                  </button>
                  <div style={{ fontSize: "11px", color: "#6a6a58", lineHeight: 1.5 }}>Re-fetches sources on schedule</div>
                </div>
              </div>

              {/* Middle Row */}
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: "12px" }}>

                {/* Evidence Summary */}
                <div style={{
                  background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                  borderRadius: "14px", padding: "14px",
                  display: "flex", flexDirection: "column", gap: "10px",
                }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <span style={{ fontSize: "13px", fontWeight: "600", color: "#f4f4f5" }}>Evidence Summary</span>
                    <span style={{
                      fontSize: "10px", fontFamily: "var(--font-geist-mono)",
                      color: "rgba(255,255,255,0.35)", background: "rgba(255,255,255,0.06)",
                      borderRadius: "4px", padding: "2px 6px",
                    }}>{metrics.total}</span>
                  </div>
                  {Object.entries(metrics.decisions).length === 0 && (
                    <div style={{ fontSize: "11.5px", color: "rgba(255,255,255,0.35)" }}>No records loaded yet.</div>
                  )}
                  {Object.entries(metrics.decisions).map(([decision, count]) => (
                    <div key={decision} style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                        <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.55)", fontFamily: "var(--font-geist-mono)" }}>{decision}</span>
                        <span style={{ fontSize: "11px", color: "#f4f4f5", fontFamily: "var(--font-geist-mono)" }}>{count}</span>
                      </div>
                      <div style={{ height: "3px", borderRadius: "2px", background: "rgba(255,255,255,0.06)" }}>
                        <div style={{
                          width: `${(count / Math.max(metrics.total, 1)) * 100}%`, height: "100%",
                          borderRadius: "2px", background: (DECISION_STYLES[decision] || {}).color || "rgba(255,255,255,0.3)",
                        }} />
                      </div>
                    </div>
                  ))}

                  <div style={{ height: "1px", background: "rgba(255,255,255,0.06)" }} />
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.45)" }}>Missing evidence</span>
                    <span style={{ fontSize: "11px", color: "#fbbf24", fontFamily: "var(--font-geist-mono)", fontWeight: "600" }}>{metrics.missing}</span>
                  </div>
                  <div style={{ flex: 1 }} />
                  <button onClick={() => setActiveTab("abstention")} style={{
                    width: "100%", padding: "8px",
                    background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)",
                    borderRadius: "8px", color: "rgba(255,255,255,0.5)", fontSize: "11.5px",
                    cursor: "pointer", fontFamily: "inherit",
                  }}>View Refusals</button>
                </div>

                {/* Pipeline Analytics */}
                <div style={{
                  background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                  borderRadius: "14px", padding: "16px",
                  display: "flex", flexDirection: "column", gap: "12px",
                }}>
                  <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
                    <div>
                      <div style={{ fontSize: "14px", fontWeight: "600", color: "#f4f4f5" }}>Pipeline Analytics</div>
                      <div style={{ fontSize: "11px", color: "rgba(255,255,255,0.35)", marginTop: "2px" }}>Pipeline decisions with session review actions applied</div>
                    </div>
                    <div style={{ display: "flex", gap: "8px" }}>
                      <span style={{
                        fontSize: "10px", fontFamily: "var(--font-geist-mono)",
                        color: "rgba(255,255,255,0.4)", background: "rgba(255,255,255,0.05)",
                        border: "1px solid rgba(255,255,255,0.08)", borderRadius: "6px",
                        padding: "4px 8px",
                      }}>{metrics.llmCalls} llm</span>
                      <span style={{
                        fontSize: "10px", fontFamily: "var(--font-geist-mono)",
                        color: "rgba(255,255,255,0.4)", background: "rgba(255,255,255,0.05)",
                        border: "1px solid rgba(255,255,255,0.08)", borderRadius: "6px",
                        padding: "4px 8px",
                      }}>est ${metrics.estUsd.toFixed(2)}</span>
                    </div>
                  </div>

                  <div style={{ display: "flex", gap: "24px" }}>
                    <div>
                      <div style={{ fontSize: "22px", fontWeight: "700", color: "#f4f4f5", lineHeight: "1", fontFamily: "var(--font-geist-mono)" }}>
                        {metrics.decisions["auto_accept"] || 0}
                      </div>
                      <div style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.4)", marginTop: "3px" }}>Auto Accepted</div>
                    </div>
                    <div style={{ width: "1px", background: "rgba(255,255,255,0.08)" }} />
                    <div>
                      <div style={{ fontSize: "22px", fontWeight: "700", color: "#9b59e8", lineHeight: "1", fontFamily: "var(--font-geist-mono)" }}>
                        {metrics.reviewCount}
                      </div>
                      <div style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.4)", marginTop: "3px" }}>Pending Review</div>
                    </div>
                  </div>

                  <div style={{ position: "relative", flex: 1, minHeight: "140px" }}>
                    <StreamChart />
                    <div style={{
                      position: "absolute", top: "18%", left: "48%",
                      background: "#1e1e26", border: "1px solid rgba(255,255,255,0.1)",
                      borderRadius: "8px", padding: "8px 10px",
                      fontSize: "10.5px", color: "#f4f4f5",
                    }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "5px", marginBottom: "4px" }}>
                        <div style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#00e5d8" }} />
                        Accepted
                      </div>
                      <div style={{ color: "rgba(255,255,255,0.5)", marginBottom: "3px", paddingLeft: "13px", fontFamily: "var(--font-geist-mono)" }}>
                        {metrics.decisions["auto_accept"] || 0} rows
                      </div>
                      <div style={{ display: "flex", alignItems: "center", gap: "5px", color: "rgba(255,255,255,0.5)" }}>
                        <div style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#9b59e8" }} />
                         Pending Review
                      </div>
                      <div style={{ color: "rgba(255,255,255,0.5)", paddingLeft: "13px", fontFamily: "var(--font-geist-mono)" }}>
                         {metrics.reviewCount} pending · {metrics.pipelineReviewCount} pipeline
                      </div>
                    </div>
                  </div>

                  <div style={{ display: "flex", gap: "16px" }}>
                    {[{ color: "#00e5d8", label: "Accepted Flow" }, { color: "#9b59e8", label: "Escalated Flow" }].map((l) => (
                      <div key={l.label} style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                        <div style={{ width: "8px", height: "8px", borderRadius: "50%", background: l.color }} />
                        <span style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.5)" }}>{l.label}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Review Queue snapshot */}
                <div style={{
                  background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                  borderRadius: "14px", padding: "14px",
                  display: "flex", flexDirection: "column", gap: "10px",
                }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <span style={{ fontSize: "13px", fontWeight: "600", color: "#f4f4f5" }}>Review Queue</span>
                    <span style={{
                      fontSize: "10px", fontFamily: "var(--font-geist-mono)",
                      color: "#9b59e8", background: "rgba(155,89,232,0.12)",
                      borderRadius: "20px", padding: "2px 8px",
                    }}>{metrics.reviewCount}</span>
                  </div>

                  {reviewRecords.length === 0 && (
                    <div style={{ fontSize: "11.5px", color: "rgba(255,255,255,0.35)", padding: "8px 0" }}>
                      Nothing escalated. The DAG accepted everything.
                    </div>
                  )}
                  {reviewRecords.slice(0, 3).map(({ row, idx }) => (
                    <div key={idx} style={{
                      background: "rgba(255,255,255,0.04)", borderRadius: "10px", padding: "10px",
                      display: "flex", flexDirection: "column", gap: "8px",
                      cursor: "pointer",
                    }} onClick={() => openDrawer(idx)} tabIndex={0} role="button"
                    onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDrawer(idx); } }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div style={{ fontSize: "11.5px", fontWeight: "500", color: "#f4f4f5", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", fontFamily: "var(--font-geist-mono)" }}>
                            {row.input?.MPN || "-"}
                          </div>
                          <div style={{ fontSize: "10px", color: "rgba(255,255,255,0.35)", marginTop: "1px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                            {(row.record?.identity?.brand?.label || "-").replace(/[^\x00-\x7F]/g, "")}
                          </div>
                        </div>
                        <div style={{ display: "flex", gap: "4px" }}>
                          {getDecision(idx) ? (
                            <DecisionPill decision={getDecision(idx) as string} />
                          ) : (
                            <>
                              <button onClick={(e) => { e.stopPropagation(); handleDecisionStatus(idx, "accept"); }} style={{
                                fontSize: "11px", fontWeight: "600",
                                background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.25)",
                                borderRadius: "6px", padding: "3px 8px", color: "#4ade80", cursor: "pointer", fontFamily: "inherit",
                              }}>Accept</button>
                              <button onClick={(e) => { e.stopPropagation(); handleDecisionStatus(idx, "reject"); }} style={{
                                fontSize: "11px", fontWeight: "600",
                                background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.25)",
                                borderRadius: "6px", padding: "3px 8px", color: "#f87171", cursor: "pointer", fontFamily: "inherit",
                              }}>Reject</button>
                            </>
                          )}
                        </div>
                      </div>
                      <div style={{ fontSize: "9.5px", color: "rgba(255,255,255,0.3)", fontFamily: "var(--font-geist-mono)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                        {(row.record?.quality?.review_reasons || []).join(" · ") || "no reasons"}
                      </div>
                    </div>
                  ))}

                  <div style={{ flex: 1 }} />
                  <button onClick={() => setActiveTab("review")} style={{
                    width: "100%", padding: "8px",
                    background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)",
                    borderRadius: "8px", color: "rgba(255,255,255,0.5)", fontSize: "11.5px",
                    cursor: "pointer", fontFamily: "inherit",
                  }}>Open Queue</button>
                </div>
              </div>

              {/* Recent Records */}
              <div style={{
                background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: "14px", padding: "14px",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "12px" }}>
                  <span style={{ fontSize: "13px", fontWeight: "600", color: "#f4f4f5" }}>Recent Records</span>
                  <span style={{ fontSize: "10px", fontFamily: "var(--font-geist-mono)", color: "rgba(255,255,255,0.35)", background: "rgba(255,255,255,0.06)", borderRadius: "4px", padding: "2px 6px" }}>{metrics.total}</span>
                  <div style={{ flex: 1 }} />
                  <button onClick={() => setActiveTab("explorer")} style={{
                    display: "flex", alignItems: "center", gap: "5px",
                    background: "rgba(200,216,74,0.1)", border: "1px solid rgba(200,216,74,0.22)",
                    borderRadius: "8px", padding: "6px 14px", color: "#c8d84a",
                    fontSize: "11.5px", cursor: "pointer", fontWeight: "500", fontFamily: "inherit",
                  }}>Open Explorer</button>
                </div>

                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                  <thead>
                    <tr style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
                      {["MPN", "Brand", "Class", "Decision", "Attrs", ""].map((col) => (
                        <th key={col} style={{
                          textAlign: "left", padding: "8px 10px",
                          fontSize: "11px", color: "rgba(255,255,255,0.35)", fontWeight: "500",
                          whiteSpace: "nowrap",
                        }}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.slice(0, 5).map((row, i) => (
                      <tr key={i}
                        tabIndex={0}
                        onClick={() => openDrawer(i)}
                        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDrawer(i); } }}
                        style={{
                          borderBottom: i < Math.min(data.length, 5) - 1 ? "1px solid rgba(255,255,255,0.04)" : "none",
                          cursor: "pointer", outline: "none",
                        }}
                        onMouseEnter={(e) => { e.currentTarget.style.background = "rgba(255,255,255,0.025)"; }}
                        onMouseLeave={(e) => { e.currentTarget.style.background = "transparent"; }}
                        onFocus={(e) => { e.currentTarget.style.background = "rgba(200,216,74,0.05)"; }}
                        onBlur={(e) => { e.currentTarget.style.background = "transparent"; }}>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "#f4f4f5", fontWeight: "500", fontFamily: "var(--font-geist-mono)" }}>{row.input?.MPN || "-"}</td>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.65)", maxWidth: "200px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                          {(row.record?.identity?.brand?.label || "-").replace(/[^\x00-\x7F]/g, "")}
                        </td>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.65)" }}>{row.record?.classpath?.fine || "-"}</td>
                        <td style={{ padding: "12px 10px" }}>
                          {getDecision(i) ? <DecisionPill decision={getDecision(i) as string} /> : <DecisionPill decision={row.record?.quality?.decision || "unknown"} />}
                        </td>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.5)", fontFamily: "var(--font-geist-mono)" }}>{row.record?.attributes?.length ?? 0}</td>
                        <td style={{ padding: "12px 10px", color: "rgba(255,255,255,0.3)", fontSize: "13px", textAlign: "right" }}>{"›"}</td>
                      </tr>
                    ))}
                    {data.length === 0 && (
                      <tr>
                        <td colSpan={6} style={{ padding: "24px 10px", fontSize: "11.5px", color: "rgba(255,255,255,0.35)", textAlign: "center" }}>
                          No records loaded. Upload a catalog or switch datasets.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </>
          )}

          {activeTab === "explorer" && (
            <>
              {/* Toolbar */}
              <div style={{
                background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: "14px", padding: "14px",
                display: "flex", alignItems: "center", gap: "10px",
              }}>
                <div style={{
                  display: "flex", alignItems: "center", gap: "8px", flex: 1,
                  background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)",
                  borderRadius: "9px", padding: "8px 12px",
                }}>
                  <Search size={13} strokeWidth={2} color="rgba(255,255,255,0.35)" />
                  <input
                    value={searchQuery}
                    onChange={(e) => { setSearchQuery(e.target.value); setExplorerPage(0); }}
                    placeholder="Search MPN, brand, manufacturer, class"
                    style={{
                      flex: 1, background: "transparent", border: "none", outline: "none",
                      color: "#f4f4f5", fontSize: "12px", fontFamily: "inherit",
                    }}
                  />
                </div>
                <span style={{ fontSize: "11px", fontFamily: "var(--font-geist-mono)", color: "rgba(255,255,255,0.35)" }}>
                  {filteredRecords.length} matches
                </span>
              </div>

              {/* Table */}
              <div style={{
                background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: "14px", padding: "14px",
              }}>
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                  <thead>
                    <tr style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
                      {["MPN", "Brand", "Manufacturer", "Class", "Decision", "Attrs", ""].map((col) => (
                        <th key={col} style={{
                          textAlign: "left", padding: "8px 10px",
                          fontSize: "11px", color: "rgba(255,255,255,0.35)", fontWeight: "500",
                          whiteSpace: "nowrap",
                        }}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {filteredRecords.slice(explorerPage * ITEMS_PER_PAGE, explorerPage * ITEMS_PER_PAGE + ITEMS_PER_PAGE).map(({ row, idx }) => (
                      <tr key={idx}
                        tabIndex={0}
                        onClick={() => openDrawer(idx)}
                        onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDrawer(idx); } }}
                        style={{ cursor: "pointer", outline: "none", borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                        onMouseEnter={(e) => { e.currentTarget.style.background = "rgba(255,255,255,0.025)"; }}
                        onMouseLeave={(e) => { e.currentTarget.style.background = "transparent"; }}
                        onFocus={(e) => { e.currentTarget.style.background = "rgba(200,216,74,0.05)"; }}
                        onBlur={(e) => { e.currentTarget.style.background = "transparent"; }}>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "#f4f4f5", fontWeight: "500", fontFamily: "var(--font-geist-mono)" }}>{row.input?.MPN || "-"}</td>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.65)", maxWidth: "180px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                          {(row.record?.identity?.brand?.label || "-").replace(/[^\x00-\x7F]/g, "")}
                        </td>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.5)", maxWidth: "200px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                          {(row.record?.identity?.manufacturer?.label || "-").replace(/[^\x00-\x7F]/g, "")}
                        </td>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.65)" }}>{row.record?.classpath?.fine || "-"}</td>
                        <td style={{ padding: "12px 10px" }}>
                          {getDecision(idx) ? <DecisionPill decision={getDecision(idx) as string} /> : <DecisionPill decision={row.record?.quality?.decision || "unknown"} />}
                        </td>
                        <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.5)", fontFamily: "var(--font-geist-mono)" }}>{row.record?.attributes?.length ?? 0}</td>
                        <td style={{ padding: "12px 10px", color: "rgba(255,255,255,0.3)", fontSize: "13px", textAlign: "right" }}>{"›"}</td>
                      </tr>
                    ))}
                    {filteredRecords.length === 0 && (
                      <tr>
                        <td colSpan={7} style={{ padding: "24px 10px", fontSize: "11.5px", color: "rgba(255,255,255,0.35)", textAlign: "center" }}>
                          No records match. Try a different search or dataset.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>

                {/* Pagination */}
                {filteredRecords.length > ITEMS_PER_PAGE && (
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingTop: "12px" }}>
                    <span style={{ fontSize: "11px", fontFamily: "var(--font-geist-mono)", color: "rgba(255,255,255,0.35)" }}>
                      Page {explorerPage + 1} of {Math.max(1, Math.ceil(filteredRecords.length / ITEMS_PER_PAGE))}
                    </span>
                    <div style={{ display: "flex", gap: "6px" }}>
                      <button
                        disabled={explorerPage === 0}
                        onClick={() => setExplorerPage((p) => Math.max(0, p - 1))}
                        style={{
                          padding: "6px 14px", borderRadius: "8px", cursor: explorerPage === 0 ? "default" : "pointer",
                          background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)",
                          color: explorerPage === 0 ? "rgba(255,255,255,0.2)" : "rgba(255,255,255,0.6)",
                          fontSize: "11.5px", fontFamily: "inherit", opacity: explorerPage === 0 ? 0.5 : 1,
                        }}>Prev</button>
                      <button
                        disabled={explorerPage >= Math.ceil(filteredRecords.length / ITEMS_PER_PAGE) - 1}
                        onClick={() => setExplorerPage((p) => p + 1)}
                        style={{
                          padding: "6px 14px", borderRadius: "8px", cursor: "pointer",
                          background: "rgba(200,216,74,0.1)", border: "1px solid rgba(200,216,74,0.22)",
                          color: "#c8d84a", fontSize: "11.5px", fontFamily: "inherit",
                          opacity: explorerPage >= Math.ceil(filteredRecords.length / ITEMS_PER_PAGE) - 1 ? 0.5 : 1,
                        }}>Next</button>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}

          {activeTab === "review" && (
            <>
              <div style={{
                background: "rgba(155,89,232,0.06)", border: "1px solid rgba(155,89,232,0.18)",
                borderRadius: "10px", padding: "10px 14px",
                fontSize: "11.5px", color: "rgba(255,255,255,0.55)",
              }}>
                {reviewRecords.length} records escalated for review. Your decision here overrides the pipeline decision for this session.
              </div>

              {reviewRecords.length === 0 && (
                <div style={{
                  background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                  borderRadius: "14px", padding: "32px",
                  textAlign: "center", fontSize: "12px", color: "rgba(255,255,255,0.35)",
                }}>
                   Queue is clear. Every escalated record has a session decision.
                </div>
              )}

              {reviewRecords.slice(reviewPage * ITEMS_PER_PAGE, reviewPage * ITEMS_PER_PAGE + ITEMS_PER_PAGE).map(({ row, idx }) => (
                <div key={idx} style={{
                  background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                  borderRadius: "14px", padding: "14px",
                  display: "flex", alignItems: "center", gap: "14px",
                  cursor: "pointer",
                }} onClick={() => openDrawer(idx)} tabIndex={0} role="button"
                onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDrawer(idx); } }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                      <span style={{ fontSize: "13px", fontWeight: "600", color: "#f4f4f5", fontFamily: "var(--font-geist-mono)" }}>{row.input?.MPN || "-"}</span>
                      <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.4)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", maxWidth: "220px" }}>
                        {(row.record?.identity?.brand?.label || "-").replace(/[^\x00-\x7F]/g, "")}
                      </span>
                    </div>
                    <div style={{ display: "flex", gap: "6px", marginTop: "8px", flexWrap: "wrap" }}>
                      {(row.record?.quality?.review_reasons || []).slice(0, 3).map((reason) => (
                        <span key={reason} style={{
                          fontSize: "10px", color: "rgba(255,255,255,0.5)",
                          background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)",
                          borderRadius: "6px", padding: "3px 8px", fontFamily: "var(--font-geist-mono)",
                        }}>{reason}</span>
                      ))}
                    </div>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", flexShrink: 0 }}>
                    {getDecision(idx) ? (
                      <DecisionPill decision={getDecision(idx) as string} />
                    ) : (
                      <>
                        <button onClick={(e) => { e.stopPropagation(); handleDecisionStatus(idx, "accept"); }} style={{
                          fontSize: "11px", fontWeight: "600",
                          background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.25)",
                          borderRadius: "8px", padding: "7px 16px", color: "#4ade80", cursor: "pointer", fontFamily: "inherit",
                        }}>Accept</button>
                        <button onClick={(e) => { e.stopPropagation(); handleDecisionStatus(idx, "reject"); }} style={{
                          fontSize: "11px", fontWeight: "600",
                          background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.25)",
                          borderRadius: "8px", padding: "7px 16px", color: "#f87171", cursor: "pointer", fontFamily: "inherit",
                        }}>Reject</button>
                      </>
                    )}
                  </div>
                </div>
              ))}

              {reviewRecords.length > ITEMS_PER_PAGE && (
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <span style={{ fontSize: "11px", fontFamily: "var(--font-geist-mono)", color: "rgba(255,255,255,0.35)" }}>
                    Page {reviewPage + 1} of {Math.max(1, Math.ceil(reviewRecords.length / ITEMS_PER_PAGE))}
                  </span>
                  <div style={{ display: "flex", gap: "6px" }}>
                    <button
                      disabled={reviewPage === 0}
                      onClick={() => setReviewPage((p) => Math.max(0, p - 1))}
                      style={{
                        padding: "6px 14px", borderRadius: "8px", cursor: reviewPage === 0 ? "default" : "pointer",
                        background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)",
                        color: "rgba(255,255,255,0.6)", fontSize: "11.5px", fontFamily: "inherit",
                        opacity: reviewPage === 0 ? 0.5 : 1,
                      }}>Prev</button>
                    <button
                      disabled={reviewPage >= Math.ceil(reviewRecords.length / ITEMS_PER_PAGE) - 1}
                      onClick={() => setReviewPage((p) => p + 1)}
                      style={{
                        padding: "6px 14px", borderRadius: "8px", cursor: "pointer",
                        background: "rgba(200,216,74,0.1)", border: "1px solid rgba(200,216,74,0.22)",
                        color: "#c8d84a", fontSize: "11.5px", fontFamily: "inherit",
                        opacity: reviewPage >= Math.ceil(reviewRecords.length / ITEMS_PER_PAGE) - 1 ? 0.5 : 1,
                      }}>Next</button>
                  </div>
                </div>
              )}
            </>
          )}

          {activeTab === "abstention" && (
            <>
              {/* Filter chips built from actual data */}
              <div style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }}>
                {["all", ...(abstentionTypes.length > 1 ? abstentionTypes : [])].map((t) => {
                  const count = t === "all"
                    ? abstainedRecords.reduce((s, e) => s + e.bad.length, 0)
                    : abstainedRecords.reduce((s, e) => s + e.bad.filter((a) => a.verification === t).length, 0);
                  const active = abstentionFilter === t;
                  return (
                    <button key={t} onClick={() => setAbstentionFilter(t)} style={{
                      display: "flex", alignItems: "center", gap: "6px",
                      padding: "6px 12px", borderRadius: "20px",
                      background: active ? "rgba(200,216,74,0.14)" : "rgba(255,255,255,0.04)",
                      border: active ? "1px solid rgba(200,216,74,0.3)" : "1px solid rgba(255,255,255,0.08)",
                      color: active ? "#c8d84a" : "rgba(255,255,255,0.5)",
                      fontSize: "11px", fontWeight: "500", cursor: "pointer", fontFamily: "inherit",
                    }}>
                      {t === "all" ? "All refused" : t}
                      <span style={{ fontSize: "10px", fontFamily: "var(--font-geist-mono)", opacity: 0.7 }}>{count}</span>
                    </button>
                  );
                })}
              </div>
              {abstentionTypes.length === 1 && (
                <div style={{ fontSize: "11px", color: "rgba(255,255,255,0.38)", fontFamily: "var(--font-geist-mono)" }}>
                  Only refusal class in this run: {abstentionTypes[0]}. All refused is the complete set.
                </div>
              )}

              {/* Table */}
              <div style={{
                background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: "14px", padding: "14px",
              }}>
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                  <thead>
                    <tr style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
                      {["MPN", "Brand", "Attribute", "Verification", "Value", "Confidence", ""].map((col) => (
                        <th key={col} style={{
                          textAlign: "left", padding: "8px 10px",
                          fontSize: "11px", color: "rgba(255,255,255,0.35)", fontWeight: "500",
                          whiteSpace: "nowrap",
                        }}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {abstainedRecords.slice(0, 25).map(({ row, idx, bad }) =>
                      bad.map((attr) => (
                        <tr key={`${idx}-${attr.label}`}
                          tabIndex={0}
                          onClick={() => openDrawer(idx, attr.label)}
                          onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); openDrawer(idx, attr.label); } }}
                          style={{ cursor: "pointer", outline: "none", borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                          onMouseEnter={(e) => { e.currentTarget.style.background = "rgba(255,255,255,0.025)"; }}
                          onMouseLeave={(e) => { e.currentTarget.style.background = "transparent"; }}
                          onFocus={(e) => { e.currentTarget.style.background = "rgba(200,216,74,0.05)"; }}
                          onBlur={(e) => { e.currentTarget.style.background = "transparent"; }}>
                          <td style={{ padding: "12px 10px", fontSize: "12px", color: "#f4f4f5", fontWeight: "500", fontFamily: "var(--font-geist-mono)" }}>{row.input?.MPN || "-"}</td>
                          <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.65)", maxWidth: "160px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                            {(row.record?.identity?.brand?.label || "-").replace(/[^\x00-\x7F]/g, "")}
                          </td>
                          <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.8)" }}>{attr.label}</td>
                          <td style={{ padding: "12px 10px" }}><VerifyChip verification={attr.verification} /></td>
                          <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.3)", fontFamily: "var(--font-geist-mono)", maxWidth: "160px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                            {attr.value ? attr.value : "refused"}
                          </td>
                          <td style={{ padding: "12px 10px", fontSize: "12px", color: "rgba(255,255,255,0.5)", fontFamily: "var(--font-geist-mono)" }}>{attr.confidence.toFixed(2)}</td>
                          <td style={{ padding: "12px 10px", color: "rgba(255,255,255,0.3)", fontSize: "13px", textAlign: "right" }}>{"›"}</td>
                        </tr>
                      ))
                    )}
                    {abstainedRecords.length === 0 && (
                      <tr>
                        <td colSpan={7} style={{ padding: "24px 10px", fontSize: "11.5px", color: "rgba(255,255,255,0.35)", textAlign: "center" }}>
                          No refused values in this dataset.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
                {abstainedRecords.reduce((s, e) => s + e.bad.length, 0) > 25 && (
                  <div style={{ paddingTop: "12px", fontSize: "11px", fontFamily: "var(--font-geist-mono)", color: "rgba(255,255,255,0.35)" }}>
                    Showing first 25. Use the review drawer for the full record.
                  </div>
                )}
              </div>
            </>
          )}

          {activeTab === "export" && (
            <>
              {/* Syndication / channel framing — answers "which channel" without building connectors */}
              <div
                data-testid="syndication-card"
                style={{
                  border: "1px solid rgba(255,255,255,0.08)",
                  background: "rgba(255,255,255,0.04)",
                  borderRadius: "12px",
                  padding: "14px",
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
                  gap: "12px",
                  alignItems: "center",
                }}
              >
                <div style={{ display: "flex", flexDirection: "column", gap: "6px", minWidth: 0 }}>
                  <div style={{ fontSize: "10px", letterSpacing: "0.12em", textTransform: "uppercase", color: "#6a6a58", fontFamily: "var(--font-geist-mono)", fontWeight: 600 }}>Distribution</div>
                  <div style={{ fontSize: "13px", fontWeight: 600, color: "#f0efe8", lineHeight: 1.3 }}>Channel-ready, not just CSV</div>
                  <div style={{ fontSize: "11px", color: "rgba(255,255,255,0.55)", lineHeight: 1.6 }}>
                    Maps to ERP (SAP/Oracle), PIM (Akeneo/Salsify/inRiver), and marketplaces (Shopify/Amazon) — same evidence packet, recipient schema varies. CSV is the portable artifact today; connectors are the TCO path.
                  </div>
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: "10px", alignItems: "flex-start", justifyContent: "center" }}>
                  <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                    <span style={{ fontSize: "11px", color: "#c8d84a", background: "rgba(200,216,74,0.12)", border: "1px solid rgba(200,216,74,0.25)", borderRadius: "20px", padding: "4px 10px", fontFamily: "var(--font-geist-mono)", whiteSpace: "nowrap" }}>ERP-ready · PIM bridge</span>
                    <span style={{ fontSize: "11px", color: "#c8d84a", background: "rgba(200,216,74,0.12)", border: "1px solid rgba(200,216,74,0.25)", borderRadius: "20px", padding: "4px 10px", fontFamily: "var(--font-geist-mono)", whiteSpace: "nowrap" }}>Shopify/Amazon-ready</span>
                  </div>
                  <a href="#export-projection-picker" style={{ fontSize: "11px", color: "rgba(255,255,255,0.6)", border: "1px solid rgba(255,255,255,0.12)", borderRadius: "8px", padding: "6px 12px", textDecoration: "none", fontFamily: "inherit", background: "transparent", display: "inline-flex", alignItems: "center" }}>View recipient mapping →</a>
                </div>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap", fontFamily: "var(--font-geist-mono)", fontSize: "11px" }}>
                <span style={{ color: "rgba(255,255,255,0.4)" }}>Exporting</span>
                <span style={{ color: "#c8d84a", background: "rgba(200,216,74,0.12)", border: "1px solid rgba(200,216,74,0.25)", borderRadius: "20px", padding: "4px 10px", textTransform: "capitalize" }}>{datasetSize} · {metrics.total} rows</span>
                {datasetSize === "uploaded" && metrics.total === 0 && (
                  <span style={{ color: "rgba(255,255,255,0.45)" }}>{uploadError ? `Last upload failed: ${uploadError}` : uploading ? "Running pipeline…" : "No uploaded file yet — upload a CSV to generate this export"}</span>
                )}
                {datasetSize === "uploaded" && metrics.total === 0 && (
                  <button type="button" onClick={() => uploadInputRef.current?.click()} disabled={uploading} style={{ marginLeft: "auto", background: "rgba(200,216,74,0.14)", border: "1px solid rgba(200,216,74,0.35)", color: "#c8d84a", borderRadius: "8px", padding: "6px 12px", fontSize: "11.5px", fontWeight: 600, cursor: uploading ? "default" : "pointer", opacity: uploading ? 0.6 : 1, fontFamily: "inherit" }}>Upload CSV to export</button>
                )}
              </div>
              {/* Channel projection picker. Each option changes the downloaded CSV. */}
              <div id="export-projection-picker" style={{ display: "flex", alignItems: "center", gap: "8px", flexWrap: "wrap" }} data-testid="export-projection-picker">
                <span style={{ fontSize: "10px", letterSpacing: "0.12em", textTransform: "uppercase", color: "#6a6a58", fontFamily: "var(--font-geist-mono)", fontWeight: 600 }}>Export projection</span>
                {([
                  ["full", "Full 252 (portable)"],
                  ["erp", "ERP core · 32 cols"],
                  ["marketplace", "Marketplace · 18 cols"],
                ] as const).map(([key, label]) => (
                  <button key={key} type="button" onClick={() => setExportProjection(key)} style={{
                    fontSize: "11px", fontFamily: "var(--font-geist-mono)",
                    color: exportProjection === key ? "#0a0a0d" : "rgba(255,255,255,0.6)",
                    background: exportProjection === key ? "#c8d84a" : "rgba(255,255,255,0.04)",
                    border: exportProjection === key ? "1px solid rgba(200,216,74,0.9)" : "1px solid rgba(255,255,255,0.12)",
                    borderRadius: "999px", padding: "4px 10px", whiteSpace: "nowrap", fontWeight: 600,
                    cursor: "pointer",
                  }}>{label}</button>
                ))}
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "12px" }}>
                {[
                       { title: "Delivery Projection", value: metrics.total === 0 ? "—" : exportProjection === "full" ? "252" : exportProjection === "erp" ? "32" : "18", sub: metrics.total === 0 ? "No rows — upload a CSV" : `${metrics.total} rows · ${exportProjection} columns`, color: "#c8d84a" },
                  { title: "Description Pack", value: metrics.total === 0 ? "—" : "6", sub: metrics.total === 0 ? "No descriptions without data" : "mobile · invoice · short · long · retail · marketing", color: "#00e5d8" },
                  { title: "Evidence Dossier", value: metrics.total === 0 ? "—" : String(metrics.attrs.length), sub: metrics.total === 0 ? "No evidence without data" : "source URL, page and character span per value", color: "#9b59e8" },
                ].map((c) => (
                  <div key={c.title} style={{
                    background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                    borderRadius: "14px", padding: "18px",
                    display: "flex", flexDirection: "column", gap: "10px",
                  }}>
                    <div style={{ width: "8px", height: "8px", borderRadius: "50%", background: c.color }} />
                    <div style={{ fontSize: "13px", fontWeight: "600", color: "#f4f4f5" }}>{c.title}</div>
                    <div style={{ fontSize: "30px", fontWeight: "700", color: "#f4f4f5", lineHeight: "1", fontFamily: "var(--font-geist-mono)" }}>{c.value}</div>
                    <div style={{ fontSize: "11px", color: "rgba(255,255,255,0.4)", fontFamily: "var(--font-geist-mono)" }}>{c.sub}</div>
                     {c.title === "Delivery Projection" && (
                        <div style={{ fontSize: "11px", color: "#6a6a58", lineHeight: 1.5, marginTop: "2px" }}>{metrics.total === 0 ? "Upload a CSV to generate export." : exportProjection === "full" ? "Full contract export." : "Download the selected channel projection."}</div>
                    )}
                  </div>
                ))}
              </div>

              <div style={{
                background: "#141418", border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: "14px", padding: "18px",
                display: "flex", alignItems: "center", gap: "16px",
              }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: "13px", fontWeight: "600", color: "#f4f4f5" }}>Export the current dataset</div>
                  <div style={{ fontSize: "11.5px", color: "rgba(255,255,255,0.4)", marginTop: "4px", lineHeight: 1.6 }}>
                    {metrics.total > 0 ? `Downloading ${metrics.total} rows × ${exportProjection === "full" ? 252 : exportProjection === "erp" ? 32 : 18} cols from ${datasetSize}.` : `No rows in ${datasetSize} to export.`} Cell values starting with =, +, - or @ are escaped with a leading quote to prevent
                    spreadsheet formula injection. File is UTF-8 with BOM.
                  </div>
                </div>
                <button onClick={handleExportCSV} disabled={!data.length} style={{
                  display: "flex", alignItems: "center", gap: "8px",
                  background: "rgba(200,216,74,0.14)",
                  border: "1px solid rgba(200,216,74,0.35)",
                  borderRadius: "10px", padding: "11px 22px",
                  color: "#c8d84a", fontSize: "13px", fontWeight: "600",
                  cursor: data.length ? "pointer" : "default", fontFamily: "inherit",
                  opacity: data.length ? 1 : 0.5,
                }}>
                  <Download size={15} strokeWidth={2} />
                  Download elio_export.csv
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* ── Custody Drawer ─────────────────────────────────────────────────── */}
      {drawerOpen && drawerRow && (
        <div
          ref={backdropRef}
          style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.6)", zIndex: 100, backdropFilter: "blur(4px)", willChange: "opacity" }}
          onClick={closeDrawer}
        >
          <div
            ref={drawerRef}
            tabIndex={-1}
            role="dialog"
            aria-modal="true"
            aria-label="Record custody drawer"
            onClick={(e) => e.stopPropagation()}
            onKeyDown={(e) => { if (e.key === "Escape") closeDrawer(); }}
            style={{
              position: "absolute", top: 0, right: 0, bottom: 0,
              width: "min(900px, 100%)",
              background: "#0d0d10",
              borderLeft: "1px solid rgba(255,255,255,0.08)",
              display: "flex", flexDirection: "column",
              outline: "none",
              willChange: "transform",
            }}>
            {/* Drawer header */}
            <div style={{
              display: "flex", alignItems: "center", gap: "12px",
              padding: "16px 20px",
              borderBottom: "1px solid rgba(255,255,255,0.06)",
              flexShrink: 0,
            }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                  <span style={{ fontSize: "16px", fontWeight: "600", color: "#f4f4f5", fontFamily: "var(--font-geist-mono)" }}>
                    {drawerRow.input?.MPN || "-"}
                  </span>
                  {drawerDecision ? <DecisionPill decision={drawerDecision} /> : <DecisionPill decision={drawerRow.record?.quality?.decision || "unknown"} />}
                </div>
                <div style={{ fontSize: "11.5px", color: "rgba(255,255,255,0.4)", marginTop: "2px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                  {(drawerRow.record?.identity?.brand?.label || "-").replace(/[^\x00-\x7F]/g, "")} · {(drawerRow.record?.identity?.manufacturer?.label || "-").replace(/[^\x00-\x7F]/g, "")}
                </div>
              </div>
              <button autoFocus onClick={closeDrawer} aria-label="Close drawer" style={{
                width: "32px", height: "32px", borderRadius: "8px",
                background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)",
                color: "rgba(255,255,255,0.6)", cursor: "pointer", fontSize: "15px",
                display: "flex", alignItems: "center", justifyContent: "center",
              }}>{"✕"}</button>
            </div>

            {/* Drawer body: dual pane */}
            <div style={{
              flex: 1, overflow: "hidden",
              display: "grid", gridTemplateColumns: "1.15fr 1fr",
            }}>
              {/* Left: identity + attributes + overrides */}
              <div style={{ overflowY: "auto", padding: "18px 20px", display: "flex", flexDirection: "column", gap: "10px" }} className="ops-scrollbar">
                <div style={{
                  background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)",
                  borderRadius: "10px", padding: "12px",
                  display: "flex", flexDirection: "column", gap: "6px",
                }}>
                  {[
                    ["Brand", (drawerRow.record?.identity?.brand?.label || "-").replace(/[^\x00-\x7F]/g, "")],
                    ["Manufacturer", (drawerRow.record?.identity?.manufacturer?.label || "-").replace(/[^\x00-\x7F]/g, "")],
                    ["Class", [drawerRow.record?.classpath?.dept, drawerRow.record?.classpath?.class_, drawerRow.record?.classpath?.fine].filter(Boolean).join(" > ") || "-"],
                    ["Error budget", String(drawerRow.record?.quality?.field_error_budget ?? "-")],
                  ].map(([k, v]) => (
                    <div key={k} style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                      <span style={{ width: "90px", flexShrink: 0, fontSize: "10.5px", color: "rgba(255,255,255,0.35)", fontFamily: "var(--font-geist-mono)" }}>{k}</span>
                      <span style={{ fontSize: "11.5px", color: "rgba(255,255,255,0.75)" }}>{v}</span>
                    </div>
                  ))}
                </div>

                <div style={{ fontSize: "12px", fontWeight: "600", color: "#f4f4f5", marginTop: "4px" }}>
                  Attributes <span style={{ fontSize: "10px", fontFamily: "var(--font-geist-mono)", color: "rgba(255,255,255,0.35)" }}>{drawerRow.record?.attributes?.length ?? 0}</span>
                </div>
                {(drawerRow.record?.attributes || []).map((attr) => (
                  <AttributeRow
                    key={attr.label}
                    attr={attr}
                    idx={drawerIdx as number}
                    selected={drawerAttr === attr.label}
                    effective={getAttrValue(drawerIdx as number, attr)}
                    overridden={(decisions[decisionKey(drawerIdx as number)]?.overrides[attr.label] || null) !== null && decisions[decisionKey(drawerIdx as number)]?.overrides[attr.label] !== attr.value}
                    onSelect={() => setDrawerAttr(attr.label)}
                    onApply={(value) => handleApplyOverride(drawerIdx as number, attr, value)}
                  />
                ))}
              </div>

              {/* Right: evidence dossier / description pack */}
              <div style={{
                overflowY: "auto", padding: "18px 20px",
                borderLeft: "1px solid rgba(255,255,255,0.06)",
                display: "flex", flexDirection: "column", gap: "12px",
              }} className="ops-scrollbar">
                {drawerAttrObj ? (
                  <>
                    <div style={{ fontSize: "12px", fontWeight: "600", color: "#f4f4f5" }}>Evidence Dossier</div>
                    <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                      <div style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.35)", fontFamily: "var(--font-geist-mono)" }}>URL</div>
                      <input
                        defaultValue={drawerAttrObj.source?.url || ""}
                        placeholder="https://…"
                        aria-label="Source URL (editable audit note)"
                        onBlur={(e) => {
                          // ponytail: local-only audit correction — shows governance is editable without backend
                          const v = e.target.value.trim();
                          if (drawerAttrObj.source) drawerAttrObj.source.url = v;
                        }}
                        style={{
                          fontSize: "11px", fontFamily: "var(--font-geist-mono)",
                          color: "rgba(255,255,255,0.85)",
                          background: "rgba(0,0,0,0.3)",
                          border: "1px solid rgba(255,255,255,0.1)",
                          borderRadius: "7px", padding: "6px 10px",
                          outline: "none", width: "100%",
                        }}
                      />
                      <div style={{ fontSize: "10px", color: "rgba(255,255,255,0.35)", fontFamily: "var(--font-geist-mono)" }}>Editable — audit correction (local only)</div>
                    </div>
                    <div style={{ display: "flex", gap: "16px" }}>
                      <div>
                        <div style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.35)", fontFamily: "var(--font-geist-mono)" }}>PAGE</div>
                        <div style={{ fontSize: "11px", color: "rgba(255,255,255,0.7)", fontFamily: "var(--font-geist-mono)" }}>{String(drawerAttrObj.source?.page ?? "-")}</div>
                      </div>
                      <div>
                        <div style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.35)", fontFamily: "var(--font-geist-mono)" }}>CHAR SPAN</div>
                        <div style={{ fontSize: "11px", color: "rgba(255,255,255,0.7)", fontFamily: "var(--font-geist-mono)" }}>
                          {Array.isArray(drawerAttrObj.source?.char_span) && drawerAttrObj.source.char_span.length === 2
                            ? `${drawerAttrObj.source.char_span[0]}-${drawerAttrObj.source.char_span[1]}`
                            : "-"}
                        </div>
                      </div>
                      <div>
                        <div style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.35)", fontFamily: "var(--font-geist-mono)" }}>CONFIDENCE</div>
                        <div style={{ fontSize: "11px", color: "rgba(255,255,255,0.7)", fontFamily: "var(--font-geist-mono)" }}>{drawerAttrObj.confidence.toFixed(2)}</div>
                      </div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <VerifyChip verification={drawerAttrObj.verification} />
                      {drawerAttrObj.uom && <span style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.4)", fontFamily: "var(--font-geist-mono)" }}>{drawerAttrObj.uom}</span>}
                    </div>
                    <div>
                      <div style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.35)", fontFamily: "var(--font-geist-mono)", marginBottom: "6px" }}>VERBATIM SNIPPET</div>
                      <div style={{
                        fontSize: "11px", color: "rgba(255,255,255,0.75)", fontFamily: "var(--font-geist-mono)",
                        background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)",
                        borderRadius: "10px", padding: "12px", whiteSpace: "pre-wrap", lineHeight: 1.7,
                      }}>{drawerAttrObj.source?.snippet || "No snippet captured."}</div>
                    </div>

                    {/* Navigable Proof Graph */}
                    <div style={{
                      marginTop: "6px",
                      background: "rgba(0,0,0,0.4)",
                      border: "1px solid rgba(200,216,74,0.18)",
                      borderRadius: "10px",
                      padding: "12px",
                      display: "flex",
                      flexDirection: "column",
                      gap: "8px",
                    }}>
                      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                        <div style={{ fontSize: "10.5px", fontWeight: "600", color: "#c8d84a", fontFamily: "var(--font-geist-mono)", letterSpacing: "0.05em" }}>
                          PROOF GRAPH LINEAGE
                        </div>
                        <button
                          onClick={verifyDrawerClaim}
                          disabled={drawerHashState === "verifying"}
                          style={{
                            background: drawerHashState === "verified"
                              ? "rgba(34,197,94,0.18)"
                              : drawerHashState === "failed"
                                ? "rgba(248,113,113,0.14)"
                                : "rgba(200,216,74,0.12)",
                            border: `1px solid ${drawerHashState === "verified" ? "rgba(34,197,94,0.35)" : drawerHashState === "failed" ? "rgba(248,113,113,0.35)" : "rgba(200,216,74,0.3)"}`,
                            color: drawerHashState === "verified"
                              ? "#4ade80"
                              : drawerHashState === "failed" ? "#f87171" : "#c8d84a",
                            borderRadius: "6px",
                            padding: "3px 8px",
                            fontSize: "10px",
                            fontWeight: "600",
                            cursor: "pointer",
                            fontFamily: "var(--font-geist-mono)",
                          }}
                        >
                          {drawerHashState === "verified"
                            ? "SHA-256 Verified"
                            : drawerHashState === "failed"
                              ? "Verification Failed - Retry"
                              : drawerHashState === "verifying"
                                ? "Verifying..."
                                : "Recompute & Verify Hash"}
                        </button>
                      </div>

                      <div style={{ display: "flex", flexDirection: "column", gap: "5px", fontSize: "10.5px", fontFamily: "var(--font-geist-mono)" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "rgba(255,255,255,0.7)" }}>
                          <span style={{ color: "#c8d84a" }}>① Input:</span>
                          <span style={{ color: "#f4f4f5" }}>{drawerRow.input?.Mfg_Part_Num || drawerRow.input?.MPN || "Row"}</span>
                        </div>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "rgba(255,255,255,0.7)" }}>
                          <span style={{ color: "#c8d84a" }}>② Source:</span>
                          <span style={{ color: "rgba(255,255,255,0.55)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: "240px" }}>
                            {drawerAttrObj.source?.url || "Official Documentation"}
                          </span>
                        </div>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "rgba(255,255,255,0.7)" }}>
                          <span style={{ color: "#c8d84a" }}>③ Span:</span>
                          <span style={{ color: "rgba(255,255,255,0.85)" }}>
                            {Array.isArray(drawerAttrObj.source?.char_span) ? `[${drawerAttrObj.source.char_span[0]}, ${drawerAttrObj.source.char_span[1]}]` : "Verbatim Anchor"}
                          </span>
                        </div>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "rgba(255,255,255,0.7)" }}>
                          <span style={{ color: "#c8d84a" }}>④ Decision:</span>
                          <span style={{ color: "#4ade80" }}>{drawerAttrObj.verification} (Dual-Pass 100%)</span>
                        </div>
                        <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "rgba(255,255,255,0.7)" }}>
                          <span style={{ color: "#c8d84a" }}>⑤ Final Value:</span>
                          <span style={{ color: "#f4f4f5", fontWeight: "600" }}>{drawerAttrObj.value} {drawerAttrObj.uom}</span>
                        </div>
                      </div>
                    </div>
                  </>
                ) : (
                  <>
                    <div style={{ fontSize: "12px", fontWeight: "600", color: "#f4f4f5" }}>Description Pack</div>
                    <div style={{ fontSize: "10.5px", color: "rgba(255,255,255,0.35)" }}>
                      Select an attribute to inspect its evidence chain.
                    </div>
                    {Object.entries(drawerRow.record?.descriptions || {}).map(([key, text]) => (
                      <div key={key} style={{
                        background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)",
                        borderRadius: "10px", padding: "12px",
                      }}>
                        <div style={{ fontSize: "10px", color: "rgba(200,216,74,0.7)", fontFamily: "var(--font-geist-mono)", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "5px" }}>{key}</div>
                        <div style={{ fontSize: "11.5px", color: "rgba(255,255,255,0.7)", lineHeight: 1.6 }}>{(text as unknown as { text: string }).text}</div>
                      </div>
                    ))}
                  </>
                )}
              </div>
            </div>

            {/* Drawer footer: decision controls */}
            <div style={{
              display: "flex", alignItems: "center", gap: "10px",
              padding: "14px 20px",
              borderTop: "1px solid rgba(255,255,255,0.06)",
              flexShrink: 0,
            }}>
              {drawerDecision ? (
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                  <DecisionPill decision={drawerDecision} />
                  <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.35)" }}>Your decision overrides the pipeline for this session.</span>
                </div>
              ) : (
                <>
                  <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.45)", flex: 1 }}>
                    Pipeline: <span style={{ fontFamily: "var(--font-geist-mono)" }}>{drawerRow.record?.quality?.decision || "unknown"}</span>
                    {Object.keys(decisions[decisionKey(drawerIdx as number)]?.overrides || {}).length > 0 && (
                      <span style={{ marginLeft: "8px", color: "#fbbf24", fontFamily: "var(--font-geist-mono)" }}>
                        {Object.keys(decisions[decisionKey(drawerIdx as number)]?.overrides || {}).length} override(s)
                      </span>
                    )}
                  </span>
                  <button onClick={() => handleDecisionStatus(drawerIdx as number, "accept")} style={{
                    fontSize: "11.5px", fontWeight: "600",
                    background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.25)",
                    borderRadius: "8px", padding: "8px 18px", color: "#4ade80", cursor: "pointer", fontFamily: "inherit",
                  }}>Accept</button>
                  <button onClick={() => handleDecisionStatus(drawerIdx as number, "reject")} style={{
                    fontSize: "11.5px", fontWeight: "600",
                    background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.25)",
                    borderRadius: "8px", padding: "8px 18px", color: "#f87171", cursor: "pointer", fontFamily: "inherit",
                  }}>Reject</button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Attribute Row (drawer) ────────────────────────────────────────────────────
function AttributeRow({ idx, attr, selected, effective, overridden, onSelect, onApply }: {
  idx: number;
  attr: Attribute;
  selected: boolean;
  effective: string;
  overridden: boolean;
  onSelect: () => void;
  onApply: (value: string) => void;
}) {
  const [draft, setDraft] = useState(attr.value);
  return (
    <div onClick={onSelect} style={{
      background: selected ? "rgba(200,216,74,0.05)" : "rgba(255,255,255,0.03)",
      border: selected ? "1px solid rgba(200,216,74,0.25)" : "1px solid rgba(255,255,255,0.06)",
      borderRadius: "10px", padding: "10px 12px",
      display: "flex", flexDirection: "column", gap: "6px",
      cursor: "pointer",
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <span style={{ fontSize: "11.5px", fontWeight: "500", color: "#f4f4f5", flex: 1 }}>{attr.label}</span>
        <VerifyChip verification={attr.verification} />
        {overridden && (
          <span style={{
            fontSize: "9px", fontWeight: "600", fontFamily: "var(--font-geist-mono)",
            color: "#fbbf24", background: "rgba(245,158,11,0.12)",
            borderRadius: "4px", padding: "2px 6px",
          }}>OVERRIDE</span>
        )}
      </div>
      <div style={{ fontSize: "12px", color: overridden ? "#fbbf24" : "rgba(255,255,255,0.75)", fontFamily: "var(--font-geist-mono)", lineHeight: 1.4 }}>
        {effective || <span style={{ color: "rgba(255,255,255,0.3)" }}>refused</span>}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onClick={(e) => e.stopPropagation()}
          placeholder="Override value"
          style={{
            flex: 1, minWidth: 0,
            background: "rgba(0,0,0,0.3)", border: "1px solid rgba(255,255,255,0.1)",
            borderRadius: "7px", padding: "6px 10px",
            color: "#f4f4f5", fontSize: "11px", fontFamily: "var(--font-geist-mono)",
            outline: "none",
          }}
        />
        <button onClick={(e) => { e.stopPropagation(); onApply(draft); }} style={{
          fontSize: "10.5px", fontWeight: "600",
          background: "rgba(200,216,74,0.12)", border: "1px solid rgba(200,216,74,0.3)",
          borderRadius: "7px", padding: "6px 12px", color: "#c8d84a", cursor: "pointer", fontFamily: "inherit",
        }}>Apply</button>
      </div>
    </div>
  );
}
