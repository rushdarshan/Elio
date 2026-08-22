"""Run an evidence-backed judge walk, with an optional live cockpit smoke test.

The default mode validates the five surfaces against canonical artifacts and
the shipped source contract. ``--live`` additionally requires a running
Next.js cockpit and exercises its HTML, receipt index, and upload API.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

from receipt_chain import ROOT, ReceiptError, verify_receipt


ALLOWED_REFUSAL_MARKERS = (
    "gold-blessed",
    "no traceable source evidence",
    "pendant",
    "dual-platform",
    "mixed-unit",
    "flight-critical attributes missing",
)
def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def surface_pipeline() -> None:
    metrics = load_json(ROOT / "artifacts" / "metrics.json")
    gates = metrics.get("gates", {})
    expected = {
        "gold": "118/118",
        "dpf": 0,
        "other_pct": 0.4,
        "attrs_per_row": 2.156,
        "adversarial": "589/589 @ 100%",
        "provenance": 1.0,
        "regressions": 0,
        "export_252": True,
    }
    for key, value in expected.items():
        if gates.get(key) != value:
            raise ValueError(f"metrics.gates.{key} is {gates.get(key)!r}, expected {value!r}")
    if metrics.get("freeze_commit") != "23b9115":
        raise ValueError("metrics is not bound to frozen commit 23b9115")


def surface_evidence() -> dict:
    report = verify_receipt()
    evidence = load_json(ROOT / "artifacts" / "evidence.json")
    rows = evidence.get("rows", {})
    if not rows:
        raise ValueError("evidence.json contains no rows")
    accepted = 0
    for mpn, row in rows.items():
        for item in row.get("accepted", []):
            accepted += 1
            ev = item.get("evidence") or {}
            if not ev.get("text"):
                raise ValueError(f"{mpn}: accepted claim has no excerpt")
            span = ev.get("char_span")
            if span is not None and (not isinstance(span, list) or len(span) != 2 or span[0] < 0 or span[1] < span[0]):
                raise ValueError(f"{mpn}: malformed evidence span")
    if accepted != report["claims"]:
        raise ValueError(f"receipt covers {report['claims']} claims, evidence has {accepted}")
    return report


def surface_review() -> int:
    events = []
    with (ROOT / "artifacts" / "decision_log.jsonl").open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("type") == "decision":
                required = {"seq", "mpn", "attribute", "status", "gate", "export_column"}
                if not required.issubset(event):
                    raise ValueError(f"decision event line {line_number} is missing required fields")
                if event["status"] not in {"accepted", "abstained"}:
                    raise ValueError(f"unsupported decision status on line {line_number}")
                events.append(event)
    if not events or not any(event["status"] == "accepted" for event in events) or not any(event["status"] == "abstained" for event in events):
        raise ValueError("decision log does not contain both accepted and abstained decisions")
    page = (ROOT / "elio-frontend" / "src" / "app" / "app" / "dashboard" / "page.tsx").read_text(encoding="utf-8")
    for required in ("localStorage", "handleDecisionStatus", "handleApplyOverride"):
        if required not in page:
            raise ValueError(f"cockpit review contract is missing {required}")
    return len(events)


def surface_abstentions() -> int:
    evidence = load_json(ROOT / "artifacts" / "evidence.json")
    total = 0
    for mpn, row in evidence.get("rows", {}).items():
        for item in row.get("abstained", []):
            reason = str(item.get("reason", "")).strip().lower()
            if not reason or not any(marker in reason for marker in ALLOWED_REFUSAL_MARKERS):
                raise ValueError(f"{mpn}/{item.get('attribute')}: unsupported or missing abstention reason")
            if item.get("value") not in (None, ""):
                raise ValueError(f"{mpn}/{item.get('attribute')}: abstention contains a value")
            total += 1
    if not total:
        raise ValueError("no abstentions recorded")
    return total


def surface_export() -> None:
    import csv

    with (ROOT / "demo_export_50.csv").open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    if len(header) != 252 or len(set(header)) != 252:
        raise ValueError("demo export does not have 252 unique columns")
    if "Mfg_Part_Num" not in header:
        raise ValueError("demo export has no row identity column")
    page = (ROOT / "elio-frontend" / "src" / "app" / "app" / "dashboard" / "page.tsx").read_text(encoding="utf-8")
    for required in (r"\uFEFF", "createObjectURL", "elio_export.csv"):
        if required not in page:
            raise ValueError(f"cockpit export contract is missing {required}")


def get(url: str) -> tuple[int, bytes]:
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status, response.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(f"live cockpit unavailable at {url}: {exc}") from exc


def live_walk(base_url: str, input_path: Path) -> int:
    status, page = get(f"{base_url}/app/dashboard")
    if status != 200:
        raise RuntimeError(f"cockpit returned HTTP {status}")
    status, receipt_index = get(f"{base_url}/data/receipt_chain.json")
    if status != 200 or b"receipt_sha256" not in receipt_index:
        raise RuntimeError("live cockpit did not serve the receipt index")
    boundary = "----elio-judge-walk"
    file_bytes = input_path.read_bytes()
    expected_rows = sum(1 for line in file_bytes.splitlines() if line.strip()) - 1
    if expected_rows < 1:
        raise RuntimeError(f"upload fixture has no data rows: {input_path}")
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{input_path.name}"\r\n'
        "Content-Type: text/csv\r\n\r\n"
    ).encode() + file_bytes + f"\r\n--{boundary}--\r\n".encode()
    request = urllib.request.Request(
        f"{base_url}/api/run",
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            if response.status != 200:
                raise RuntimeError(f"upload API returned HTTP {response.status}")
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"upload API returned HTTP {exc.code}") from exc
    if not isinstance(result.get("hash"), str) or result.get("rowCount") != expected_rows or not isinstance(result.get("results"), list) or len(result["results"]) != expected_rows:
        raise RuntimeError(f"upload API response is missing hash, rowCount={expected_rows}, or results")
    return expected_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="also check a running cockpit")
    parser.add_argument("--base-url", default="http://localhost:3000")
    parser.add_argument("--input", type=Path, default=ROOT / "demo_input_50.csv", help="CSV fixture for the live upload check")
    args = parser.parse_args()
    print("=== ELIO EVIDENCE-BACKED JUDGE WALK ===")
    try:
        surface_pipeline()
        receipt = surface_evidence()
        events = surface_review()
        abstentions = surface_abstentions()
        surface_export()
        uploaded_rows = live_walk(args.base_url.rstrip("/"), args.input) if args.live else None
    except (OSError, ValueError, ReceiptError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"[FAIL] {exc}")
        return 1
    mode = " + live cockpit" if args.live else " + artifact/source contract"
    print(f"[PASS] pipeline metrics verified")
    print(f"[PASS] evidence receipt verified: {receipt['claims']} claims")
    print(f"[PASS] review decisions verified: {events} events")
    print(f"[PASS] abstentions verified: {abstentions} refused values")
    print("[PASS] export contract verified: 252 columns")
    if uploaded_rows is not None:
        print(f"[PASS] live upload verified: {uploaded_rows} rows")
    print(f"JUDGE_WALK_STATUS: VERIFIED{mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
