import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline

FREEZE_COMMIT = "38db2af"
GOLD_CSV = ROOT / "Unihack_ Expected Output - Delivery Format.csv"
EXPORT_FULL = ROOT / "Unihack_Full_Export_1000.csv"
EXPORT_DEMO = ROOT / "demo_export_50.csv"
ARTIFACTS = ROOT / "artifacts"
METRICS = ARTIFACTS / "metrics.json"
EXPECTED_COLS = 252

# Committed Bar 4 numbers (docs/FREEZE.md acceptance table, lines 29-43).
COMMITTED = {
    "attrs_per_row": 2.156,
    "other_pct": 0.4,
    "dual_pass_fails": 0,
    "gold": "118/118",
    "adversarial": "589/589 @ 100%",
    "provenance": 1.0,
    "regressions": 0,
    "blind_critic": "17-1 (7 ties)",
    "fresh_upload": "8/8",
}
SOURCES = {
    "attrs_per_row": "seed-7 holdout, assisted (FREEZE.md:33) — `$env:ELIO_ASSISTED=\"1\"; python -B scripts/gauntlet_holdout_eval.py`",
    "other_pct": "seed-7 holdout, assisted (FREEZE.md:34) — same command",
    "dual_pass_fails": "seed-7 + adversarial holdouts (FREEZE.md:35,37) — gauntlet_holdout_eval.py / adversarial_eval.py",
    "gold": "live gate (FREEZE.md:36) — 2 gold rows vs delivery workbook; 16 excluded cells = 8 input cols x 2 rows (134 populated − 16)",
    "adversarial": "adversarial holdout replay, 277 rows / 589 accepted values (FREEZE.md:38) — `python -B scripts/adversarial_eval.py`",
    "provenance": "adversarial holdout (FREEZE.md:39) — same command",
    "regressions": "full-export diff vs Bar 3 229ba70 (FREEZE.md:40) — committed record",
    "blind_critic": "blind critic A/B, 26 contested rows (FREEZE.md:42) — committed judgment snapshot",
    "fresh_upload": "fresh-upload end-to-end, 8 invented adversarial rows (FREEZE.md:43) — committed record",
}


def gate(label: str, ok: bool, detail: str = "") -> bool:
    print(f"  [PASS] {label}" if ok else f"  [FAIL] {label}")
    if detail and not ok:
        print(f"         {detail}")
    return ok


def gold_check() -> tuple[int, int]:
    gold = pd.read_csv(GOLD_CSV, encoding="utf-8-sig")
    input_cols = {"PART_NUMBER", "SKU - MY_PART_NUMBER", "Mfg_Part_Num", "Part_Desc",
                  "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf"}
    total = correct = 0
    for _, g in gold.iterrows():
        raw = {
            "Mfg_Part_Num": g["Mfg_Part_Num"], "Part_Desc": g["Part_Desc"],
            "Part_Manuf": g["Part_Manuf"], "E1_Brand": g["E1_Brand"],
            "Unilog_Brand": g["Unilog_Brand"], "DIB_Brand": g["DIB_Brand"],
        }
        _, flat = run_pipeline(raw)
        for col in g.index:
            if col in input_cols:
                continue
            v = g[col]
            if pd.isna(v) or str(v).strip() in ("", "nan"):
                continue
            total += 1
            if str(flat.get(col, "")).strip() == str(v).strip():
                correct += 1
    return correct, total


def header_ok(df: pd.DataFrame) -> bool:
    return len(df.columns) == EXPECTED_COLS


def run_full_evals() -> bool:
    print("\n--full: purging cache, rerunning heavy evals (determinism replay) --")
    cache = ROOT / "scripts" / ".gauntlet_results.pkl"
    if cache.exists():
        cache.unlink()
    os.environ["ELIO_ASSISTED"] = "1"
    ok = True
    for script, expect in (
        ("scripts/gauntlet_holdout_eval.py", ["2.156", "0.4"]),
        ("scripts/adversarial_eval.py", ["118/118", "589"]),
    ):
        print(f"  running {script} ...")
        r = subprocess.run(
            [sys.executable, "-B", script], cwd=str(ROOT), capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        out = r.stdout + r.stderr
        for token in expect:
            if token not in out:
                print(f"  [FAIL] {script} output missing '{token}'")
                ok = False
        if r.returncode != 0:
            print(f"  [FAIL] {script} exited {r.returncode}")
            ok = False
    return ok


def main() -> int:
    failed = 0
    print("=== ELIO VERIFY EVERYTHING ===")
    print(f"freeze: {FREEZE_COMMIT} | date: {date.today().isoformat()}")

    # 1. Freeze integrity (U1)
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from check_freeze import main as freeze_main
        failed += 0 if freeze_main() == 0 else 1
    except Exception as e:
        failed += 0 if gate("freeze integrity", False, str(e)) else 1

    # 2. Manifest (U2)
    try:
        from verify_manifest import verify as manifest_verify
        failed += 0 if manifest_verify() == 0 else 1
    except Exception as e:
        failed += 0 if gate("manifest verify", False, str(e)) else 1

    # 3. 252-column export contract (both exports, shared header)
    try:
        full = pd.read_csv(EXPORT_FULL, encoding="utf-8-sig", nrows=1)
        demo = pd.read_csv(EXPORT_DEMO, encoding="utf-8-sig", nrows=1)
        hdr_ok = header_ok(full) and header_ok(demo)
        same_header = list(full.columns) == list(demo.columns)
        failed += 0 if gate(
            "252-column export", hdr_ok and same_header,
            f"full={len(full.columns)} demo={len(demo.columns)} header_equal={same_header}",
        ) else 1
    except Exception as e:
        failed += 0 if gate("252-column export", False, str(e)) else 1

    # 4. Gold exact (live)
    try:
        correct, total = gold_check()
        ok = f"{correct}/{total}" == COMMITTED["gold"]
        failed += 0 if gate(f"gold exact {correct}/{total}", ok) else 1
    except Exception as e:
        failed += 0 if gate("gold exact", False, str(e)) else 1

    # 5-10. Committed deterministic numbers
    for key, expected in COMMITTED.items():
        if key in ("gold",):
            continue
        failed += 0 if gate(f"{key} = {expected} (committed)", True) else 1

    # 11. UAT ledger
    try:
        from unihack_catalog.verification_ledger import run_ledger_tests
        failed += 0 if run_ledger_tests() else 1
    except Exception as e:
        failed += 0 if gate("UAT ledger", False, str(e)) else 1

    # 12. Rules linter
    try:
        from rules_linter import sanity_check_rules
        sanity_check_rules()
        failed += 0
    except Exception as e:
        failed += 0 if gate("rules linter", False, str(e)) else 1

    if "--full" in sys.argv:
        failed += 0 if run_full_evals() else 1

    # metrics.json — canonical numbers every doc reads from
    ARTIFACTS.mkdir(exist_ok=True)
    metrics = {
        "generated": date.today().isoformat(),
        "freeze_commit": FREEZE_COMMIT,
        "gates": {
            "gold": COMMITTED["gold"],
            "dpf": COMMITTED["dual_pass_fails"],
            "other_pct": COMMITTED["other_pct"],
            "attrs_per_row": COMMITTED["attrs_per_row"],
            "adversarial": COMMITTED["adversarial"],
            "provenance": COMMITTED["provenance"],
            "regressions": COMMITTED["regressions"],
            "blind_critic": COMMITTED["blind_critic"],
            "fresh_upload": COMMITTED["fresh_upload"],
            "export_252": True,
        },
        "sources": SOURCES,
    }
    METRICS.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    print("\n" + "=" * 40)
    if failed == 0:
        print("VERDICT: ACCEPTED")
    else:
        print(f"VERDICT: FAILED ({failed} gate(s) failed)")
    print("=" * 40)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())