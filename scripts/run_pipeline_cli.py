import sys
import os
import argparse
import pandas as pd
import json
import traceback

# Ensure we can import unihack_catalog
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unihack_catalog.stages import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="ELIO Pipeline CLI Runner")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    args = parser.parse_args()

    print(f"Reading input file: {args.input}", flush=True)
    try:
        if args.input.endswith('.csv'):
            df = pd.read_csv(args.input, encoding="utf-8-sig")
        else:
            df = pd.read_excel(args.input)
        
        # Clean column names
        df.columns = [str(c).lstrip("\ufeff").strip() for c in df.columns]
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

    # Required columns map
    mapped_rows = []
    for _, row in df.iterrows():
        def text(value):
            return "" if pd.isna(value) else str(value).strip()

        def first(*names):
            for name in names:
                value = row.get(name)
                if value is not None and not pd.isna(value):
                    return text(value)
            return ""

        mpn = first("Mfg_Part_Num", "MPN")
        desc = first("Part_Desc", "Description")
        mfr = first("Part_Manuf", "Manufacturer")
        e1_brand = first("E1_Brand")
        unilog_brand = first("Unilog_Brand")
        dib_brand = first("DIB_Brand")

        mapped_rows.append({
            "Mfg_Part_Num": mpn,
            "Part_Desc": desc,
            "Part_Manuf": mfr,
            "E1_Brand": e1_brand,
            "Unilog_Brand": unilog_brand,
            "DIB_Brand": dib_brand
        })

    total_rows = len(mapped_rows)
    print(f"Starting pipeline run for {total_rows} rows...", flush=True)

    results = []
    failures = []
    for idx, row in enumerate(mapped_rows):
        mpn = row["Mfg_Part_Num"]
        print(f"PROGRESS:{idx+1}/{total_rows}:{mpn}", flush=True)
        try:
            rec, flat = run_pipeline(row)
            results.append({
                "input": {
                    "MPN": rec.input.mpn,
                    "Manufacturer": rec.input.part_manuf or "",
                    "Description": rec.input.raw_text,
                    "E1_Brand": rec.input.e1_brand,
                    "Unilog_Brand": rec.input.unilog_brand,
                    "DIB_Brand": rec.input.dib_brand
                },
                "record": rec.model_dump(),
                "flat_export": flat
            })
        except Exception as ex:
            print(f"Error processing row {idx+1} ({mpn}): {ex}", file=sys.stderr, flush=True)
            traceback.print_exc()
            failures.append((idx + 1, mpn, str(ex)))

    if failures:
        print(f"Pipeline failed for {len(failures)} of {total_rows} rows", file=sys.stderr, flush=True)
        sys.exit(1)

    # Save to output file
    try:
        out_dir = os.path.dirname(args.output)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Successfully wrote output JSON: {args.output}", flush=True)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
