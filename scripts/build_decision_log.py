import json
import platform
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "artifacts" / "evidence.json"
LOG = ROOT / "artifacts" / "decision_log.jsonl"

FREEZE_COMMIT = "38db2af"

# opengeni steal: durable, replayable event log. Every value decision is
# appended as one line: proposed (pipeline output) -> gate (dual-pass /
# abstention / gold-blessed) -> accepted | abstained, with the evidence that
# justified it. evidence.json is a DERIVED view; --replay rebuilds it from the
# log and must reproduce it byte-identically (the audit trail cannot drift).
GOLD_BLESSED_COLS = {"PART_NUMBER", "SKU - MY_PART_NUMBER"}


def build() -> int:
    doc = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    lines = [
        json.dumps(
            {"type": "header", "freeze_commit": FREEZE_COMMIT,
             "generated": date.today().isoformat(),
             "python": platform.python_version(),
             "source": "artifacts/evidence.json",
             "source_input": doc.get("generated_from")},
            ensure_ascii=False,
        )
    ]
    seq = 0
    for mpn in doc["row_order"]:
        r = doc["rows"][mpn]
        lines.append(json.dumps(
            {"type": "mpn", "mpn": mpn, "fine": r["fine"], "dept": r["dept"]},
            ensure_ascii=False,
        ))
        for rec in r["accepted"]:
            seq += 1
            lines.append(json.dumps(
                {"seq": seq, "type": "decision", "mpn": mpn,
                 "attribute": rec["attribute"], "status": "accepted",
                 "gate": "dual-pass", "value": rec["value"], "uom": rec["uom"],
                 "evidence": rec["evidence"], "confidence": rec["confidence"],
                 "verification": rec["verification"],
                 "export_column": rec["export_column"], "reason": None},
                ensure_ascii=False,
            ))
        for rec in r["abstained"]:
            seq += 1
            gate = "gold-blessed" if rec.get("export_column") in GOLD_BLESSED_COLS else "abstention"
            lines.append(json.dumps(
                {"seq": seq, "type": "decision", "mpn": mpn,
                 "attribute": rec["attribute"], "status": "abstained",
                 "gate": gate, "value": None, "uom": "", "evidence": None,
                 "confidence": None, "verification": None,
                 "export_column": rec["export_column"], "reason": rec["reason"]},
                ensure_ascii=False,
            ))
    LOG.parent.mkdir(exist_ok=True)
    LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
    n_acc = sum(1 for l in lines if '"status": "accepted"' in l)
    n_abs = sum(1 for l in lines if '"status": "abstained"' in l)
    print(f"decision_log.jsonl written: {n_acc} accepted + {n_abs} abstained "
          f"decisions across {len(doc['row_order'])} rows")
    return 0


def replay() -> int:
    if not LOG.is_file():
        print("[FAIL] artifacts/decision_log.jsonl missing")
        return 1
    rows, row_order, src_input = {}, [], None
    for line in LOG.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec["type"] == "header":
            src_input = rec.get("source_input")
        elif rec["type"] == "mpn":
            rows[rec["mpn"]] = {
                "mpn": rec["mpn"], "fine": rec["fine"], "dept": rec["dept"],
                "n_accepted": 0, "n_abstained": 0, "accepted": [], "abstained": [],
            }
            row_order.append(rec["mpn"])
        else:
            r = rows[rec["mpn"]]
            if rec["status"] == "accepted":
                r["accepted"].append({
                    "mpn": rec["mpn"], "attribute": rec["attribute"],
                    "value": rec["value"], "uom": rec["uom"],
                    "evidence": rec["evidence"], "confidence": rec["confidence"],
                    "verification": rec["verification"], "status": "accepted",
                    "export_column": rec["export_column"],
                })
                r["n_accepted"] += 1
            else:
                r["abstained"].append({
                    "mpn": rec["mpn"], "attribute": rec["attribute"],
                    "value": None, "uom": "", "status": "abstained",
                    "reason": rec["reason"], "export_column": rec["export_column"],
                })
                r["n_abstained"] += 1
    doc = {"freeze_commit": FREEZE_COMMIT, "generated_from": src_input,
           "rows": rows, "row_order": row_order}
    rebuilt = json.dumps(doc, indent=2) + "\n"
    if rebuilt != EVIDENCE.read_text(encoding="utf-8"):
        print("[FAIL] replay diverges from committed artifacts/evidence.json")
        return 1
    print(f"REPLAY: PASSED — evidence.json ({len(row_order)} rows) rebuilt "
          f"byte-identical from decision_log.jsonl")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--replay":
        sys.exit(replay())
    sys.exit(build())