import json
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DEMO_IN = ROOT / "demo_input_50.csv"
DEMO_OUT = ROOT / "demo_export_50.csv"
EVIDENCE = ROOT / "artifacts" / "evidence.json"
OUT = ROOT / "demo.html"

CORE_COLS = ["MFR URL", "Dept", "Class", "Fine", "Classpath", "MANUFACTURER_NAME",
             "BRAND_NAME", "MANUFACTURER_PART_NUMBER", "MOBILE_DESC", "INVOICE_DESC",
             "SHORT_DESC", "LONG_DESC1", "RETAIL_DESC", "MARKETING_DESCRIPTION",
             "Product Name", "Part_Desc"]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ELIO — Evidence Explorer (offline)</title>
<style>
  :root { --ink:#1a1d21; --mut:#5c6470; --acc:#0b6e4f; --warn:#9a6700; --bg:#f7f8fa; --line:#dfe3e8; }
  * { box-sizing: border-box; }
  body { font: 15px/1.5 -apple-system, "Segoe UI", Roboto, sans-serif; color: var(--ink);
         background: var(--bg); margin: 0; padding: 24px; }
  h1 { font-size: 20px; margin: 0 0 4px; } h1 code { color: var(--acc); }
  .sub { color: var(--mut); margin-bottom: 20px; font-size: 13px; }
  #search { width: min(560px, 100%); padding: 10px 14px; font-size: 15px; border: 1px solid var(--line);
            border-radius: 8px; outline: none; }
  #search:focus { border-color: var(--acc); }
  #results { margin-top: 14px; }
  .card { background: #fff; border: 1px solid var(--line); border-radius: 10px;
          padding: 16px 20px; margin-bottom: 14px; }
  .card h2 { font-size: 16px; margin: 0 0 2px; }
  .card .meta { color: var(--mut); font-size: 12.5px; margin-bottom: 12px; }
  .panel-title { font-weight: 600; font-size: 12.5px; letter-spacing: .04em; text-transform: uppercase;
                 color: var(--mut); margin: 12px 0 6px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 8px; }
  .cell { border: 1px solid var(--line); border-radius: 6px; padding: 6px 10px; background: #fbfcfd; }
  .cell .k { font-size: 11.5px; color: var(--mut); text-transform: uppercase; letter-spacing: .03em; }
  .cell .v { font-size: 14px; word-break: break-word; }
  .cell.accepted { border-left: 3px solid var(--acc); }
  .cell.abstained { border-left: 3px solid var(--warn); background: #fffdf5; }
  .why { display: none; margin-top: 6px; font-size: 12.5px; color: #444;
         background: #eef6f2; border-radius: 6px; padding: 6px 10px; }
  .why b { color: var(--ink); }
  .why .span { font-family: Consolas, monospace; font-size: 12px; color: #333; background: #e4ece8;
               padding: 1px 5px; border-radius: 4px; }
  .why-btn { background: none; border: none; color: var(--acc); font-size: 12px; cursor: pointer;
             padding: 0; font-weight: 600; }
  .why-btn:hover { text-decoration: underline; }
  .abst-reason { font-size: 12.5px; color: #7a5b00; }
  .reveal { margin-top: 12px; font-size: 13px; }
  .reveal-btn { background: none; border: 1px solid var(--line); border-radius: 6px; padding: 6px 12px;
                cursor: pointer; color: var(--ink); font-size: 13px; }
  .reveal-btn:hover { border-color: var(--acc); color: var(--acc); }
  #rest { display: none; margin-top: 10px; }
  .rest-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 6px;
               max-height: 420px; overflow: auto; }
  .rest-cell { border: 1px solid var(--line); border-radius: 5px; padding: 4px 8px; font-size: 12px; }
  .rest-cell .k { color: var(--mut); font-size: 10.5px; }
  footer { margin-top: 28px; color: var(--mut); font-size: 12.5px; border-top: 1px solid var(--line);
           padding-top: 12px; }
  .empty { color: var(--mut); padding: 20px; text-align: center; }
</style>
</head>
<body>
  <h1>ELIO <code>demo.html</code> — evidence explorer</h1>
  <div class="sub">Search an MPN or keyword. Every emitted value carries a WHY (dual-pass evidence trace);
  every abstained cell carries its reason. Fully offline — no network.</div>
  <input id="search" placeholder="Search MPN or description, e.g. PDSH4816AF or dishwasher" autocomplete="off">
  <div id="results"></div>

<script id="app-data" type="application/json">%DATA%</script>
<script>
const data = JSON.parse(document.getElementById("app-data").textContent);
const out = document.getElementById("results");
const search = document.getElementById("search");
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function whyHtml(rec) {
  if (rec.status !== "accepted") return "";
  const ev = rec.evidence || {};
  const t = ev.text || "";
  const span = ev.char_span ? ` @chars ${ev.char_span[0]}-${ev.char_span[1]}` : "";
  return `<div class="why" data-why="1">Evidence (<b>${esc(ev.kind || "raw")}</b>)<span class="span">${esc(t)}</span>${span}
          — confidence ${rec.confidence} · verification: ${esc(rec.verification || "supported")}</div>`;
}

function cellHtml(rec) {
  const k = esc(rec.attribute), v = esc(rec.value ?? "");
  if (rec.status === "accepted") {
    return `<div class="cell accepted"><div class="k">${k}</div><div class="v">${v} ${esc(rec.uom || "")}
            <button class="why-btn" onclick="toggleWhy(this)">WHY?</button></div>${whyHtml(rec)}</div>`;
  }
  return `<div class="cell abstained"><div class="k">${k}</div><div class="v">[ABSTAINED]</div>
          <div class="abst-reason">${esc(rec.reason)}</div></div>`;
}

function rowCard(mpn) {
  const row = data.rows[mpn];
  if (!row) return "";
  const raw = data.raw[mpn] || {};
  const exp = data.export_rows[mpn] || {};
  const restCells = Object.entries(exp).filter(([k]) => !["Part_Desc"].includes(k)
    && !row.accepted.some(r => r.export_column === k)
    && !row.abstained.some(r => r.export_column === k));
  const core = [["Fine class", `${row.dept} &gt; ${row.fine}`],
                ["Brand", exp["BRAND_NAME"] || ""],
                ["Manufacturer", exp["MANUFACTURER_NAME"] || ""],
                ["MFR URL", exp["MFR URL"] || ""],
                ["Long description", exp["LONG_DESC1"] || ""]];
  const attrCells = [...row.accepted, ...row.abstained].map(cellHtml).join("");
  const restHtml = `<div id="rest" class="rest-grid">` + restCells.map(([k, v]) =>
    `<div class="rest-cell"><div class="k">${esc(k)}</div>${esc(v)}</div>`).join("") + `</div>`;
  return `<div class="card"><h2>${esc(mpn)}</h2>
    <div class="meta">${row.n_accepted} accepted with evidence · ${row.n_abstained} abstained with reasons · ${esc(row.fine)}</div>
    <div class="panel-title">Raw input</div>
    <div class="grid">${Object.entries(raw).map(([k, v]) =>
      `<div class="cell"><div class="k">${esc(k)}</div><div class="v">${esc(v)}</div></div>`).join("")}</div>
    <div class="panel-title">ELIO output — evidence-bearing cells first</div>
    <div class="grid">${core.map(([k, v]) =>
      `<div class="cell"><div class="k">${esc(k)}</div><div class="v">${esc(v)}</div></div>`).join("")}</div>
    <div class="grid">${attrCells}</div>
    <div class="reveal"><button class="reveal-btn" onclick="toggleRest(this)">Show remaining ${restCells.length} export columns</button></div>
    ${restHtml}
  </div>`;
}

function toggleWhy(btn) { const w = btn.parentElement.parentElement.querySelector("[data-why]");
  w.style.display = w.style.display === "none" ? "block" : "none"; }
function toggleRest(btn) { const rest = btn.closest(".card").querySelector("#rest");
  rest.style.display = rest.style.display === "none" ? "grid" : "none";
  btn.textContent = rest.style.display === "grid" ? "Hide remaining columns" : "Show remaining export columns"; }

function render() {
  const q = search.value.trim().toLowerCase();
  const hits = data.row_order.filter(mpn => {
    const r = data.rows[mpn], raw = data.raw[mpn] || {};
    return mpn.toLowerCase().includes(q) ||
      Object.values(raw).some(v => String(v).toLowerCase().includes(q));
  });
  if (!q) { out.innerHTML = `<div class="empty">Type an MPN or keyword — try PDSH4816AF (gold row).</div>`; return; }
  if (!hits.length) { out.innerHTML = `<div class="empty">No rows match "${esc(q)}".</div>`; return; }
  out.innerHTML = hits.slice(0, 8).map(rowCard).join("");
}
search.addEventListener("input", render);
render();
</script>

<footer>
  <p><b>How this works:</b> every emitted value is dual-pass verified — it must appear in the source
  text (or be a documented unit conversion), or the cell is abstained with a reason, never invented.</p>
  <p>Numbers: <a href="docs/FREEZE.md">docs/FREEZE.md</a> (acceptance table) · verify everything with
  <code>python -B scripts\verify_everything.py</code>.</p>
</footer>
</body>
</html>
"""


def main() -> int:
    if not EVIDENCE.is_file():
        raise SystemExit("[FAIL] artifacts/evidence.json missing — run scripts/build_evidence.py first")
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    demo_in = pd.read_csv(DEMO_IN, encoding="utf-8-sig")
    demo_out = pd.read_csv(DEMO_OUT, encoding="utf-8-sig")

    raw = {}
    for _, r in demo_in.iterrows():
        raw[str(r["Mfg_Part_Num"]).strip().upper()] = {
            "Mfg_Part_Num": r["Mfg_Part_Num"], "Part_Desc": r["Part_Desc"],
            "Part_Manuf": r["Part_Manuf"], "E1_Brand": r["E1_Brand"],
            "Unilog_Brand": r["Unilog_Brand"], "DIB_Brand": r["DIB_Brand"]}
    export_rows = {}
    for _, r in demo_out.iterrows():
        mpn = str(r["Mfg_Part_Num"]).strip().upper()
        export_rows[mpn] = {c: ("" if pd.isna(r[c]) else str(r[c])) for c in r.index}

    payload = {"rows": evidence["rows"], "row_order": evidence["row_order"],
               "raw": raw, "export_rows": export_rows}
    html = TEMPLATE.replace("%DATA%", json.dumps(payload))
    OUT.write_text(html, encoding="utf-8")

    # Self-checks
    ok = True
    if "PDSH4816AF" not in evidence["rows"]:
        print("[FAIL] PDSH4816AF missing"); ok = False
    for pat in ("src=\"http", "href=\"http", "@import", "url(http"):
        if pat in html:
            print(f"[FAIL] offline invariant broken: {pat}"); ok = False
    for mpn, row in evidence["rows"].items():
        for r in row["abstained"]:
            if not r.get("reason"):
                print(f"[FAIL] {mpn} abstained without reason"); ok = False
        for r in row["accepted"]:
            if not r.get("evidence"):
                print(f"[FAIL] {mpn} accepted without evidence"); ok = False
    print(f"demo.html written: {len(evidence['rows'])} rows, {len(html)} bytes")
    print("SELF-CHECK: PASSED" if ok else "SELF-CHECK: FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())