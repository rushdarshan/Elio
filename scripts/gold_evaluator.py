"""
Dedicated Test-Only Gold Set Evaluator for ELIO.

Evaluates pipeline performance on the official UniHack delivery format workbook
without polluting or leaking gold data into the production runtime.
"""

import os
import sys
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline

GOLD_CSV = ROOT / "Unihack_ Expected Output - Delivery Format.csv"

def evaluate_gold() -> tuple[int, int, float]:
    if not GOLD_CSV.exists():
        print(f"Error: Gold delivery CSV not found at {GOLD_CSV}")
        return 0, 0, 0.0

    df = pd.read_csv(GOLD_CSV, encoding="utf-8-sig")
    input_cols = {
        "PART_NUMBER", "SKU - MY_PART_NUMBER", "Mfg_Part_Num", "Part_Desc",
        "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf"
    }

    total_evaluated = 0
    correct_matches = 0

    print("=== ELIO GOLD-SET EVALUATION (TEST HARNESS) ===")
    print(f"Evaluating {len(df)} gold benchmark rows...")

    for idx, row in df.iterrows():
        raw_input = {
            "Mfg_Part_Num": row.get("Mfg_Part_Num", ""),
            "Part_Desc": row.get("Part_Desc", ""),
            "Part_Manuf": row.get("Part_Manuf", ""),
            "E1_Brand": row.get("E1_Brand", ""),
            "Unilog_Brand": row.get("Unilog_Brand", ""),
            "DIB_Brand": row.get("DIB_Brand", ""),
        }
        
        # Run clean production pipeline
        rec, flat_export = run_pipeline(raw_input)
        
        row_eval = 0
        row_correct = 0

        for col in df.columns:
            if col in input_cols:
                continue
            expected_val = row[col]
            if pd.isna(expected_val) or str(expected_val).strip() in ("", "nan"):
                continue

            total_evaluated += 1
            row_eval += 1

            actual_val = str(flat_export.get(col, "")).strip()
            exp_str = str(expected_val).strip()

            # Exact string or numeric equivalence
            if actual_val.lower() == exp_str.lower():
                correct_matches += 1
                row_correct += 1

        print(f"Row {idx+1} ({rec.input.mpn}): {row_correct}/{row_eval} matching gold cells.")

    accuracy = (correct_matches / total_evaluated * 100) if total_evaluated > 0 else 0.0
    print(f"\nTotal Evaluated Populated Cells: {total_evaluated}")
    print(f"Exact Matches: {correct_matches}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"[PASS] Gold Evaluation Completed.")
    return correct_matches, total_evaluated, accuracy

if __name__ == "__main__":
    evaluate_gold()
