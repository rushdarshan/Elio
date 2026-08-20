import json
import os
import pickle
import re
import sys
import time
from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\rushd\Downloads\Jesus WIn")
sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline

SAMPLE = ROOT / "Unihack_ Sample Dataset - Input.csv"
GOLD_CSV = ROOT / "Unihack_ Expected Output - Delivery Format.csv"
CACHE = ROOT / "scripts" / ".gauntlet_results.pkl"
INPUT_COLS = {"PART_NUMBER", "SKU - MY_PART_NUMBER", "Mfg_Part_Num", "Part_Desc",
              "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf"}
GOLD_MPNS = {"PDSH4816AF", "WDTS7024RZ"}
HOLDOUT_FRAC = 0.25

distributor_blacklist = {
    "appde", "jam industrial", "parksite", "palmer donavin", 
    "us lumber", "westwood", "tech gear", "g turner", "distributor", "co."
}

problematic_fines = {
    "Sanding Belts & Sheets", "Cutting & Grinding Discs", "Reciprocating & Band Saw Blades",
    "Drill Bits", "Electrical Wire", "Electrical Outlets & Receptacles", "Electrical Wall Plates",
    "Light Bulbs", "Railing & Balusters", "Impact Drivers", "Planers"
}


def score_difficulty(row, fine_class):
    score = 0
    desc = str(row.get("Part_Desc", "")).strip().lower()
    mpn = str(row.get("Mfg_Part_Num", "")).strip().lower()
    mfr = str(row.get("Part_Manuf", "")).strip().lower()
    
    # 1. Sparse description
    if len(desc) <= 15:
        score += 3
    elif len(desc) <= 25:
        score += 2
    elif len(desc) <= 45:
        score += 1
        
    # 2. MPN-only behavior (description is mostly the MPN or just contains it)
    if desc == mpn or desc.startswith(mpn) or desc.endswith(mpn):
        score += 2
        
    # 3. Unknown manufacturer or blacklisted distributor
    if mfr in ("", "-", "unknown", "none"):
        score += 3
    elif any(b in mfr for b in distributor_blacklist):
        score += 2
        
    # 4. Unit-heavy / conversion-heavy
    unit_patterns = [
        r'\d+.*["\']', 
        r'\d+\s*[xX]\s*\d+', 
        r'\d+\s*mm\b', 
        r'\d+\s*[vV]\b', 
        r'\d+\s*[aA]\b',
        r'\d+\s*(?:ft|foot|feet)\b',
        r'\b\d+/\d+\b'
    ]
    matches = sum(1 for p in unit_patterns if re.search(p, desc))
    if matches >= 3:
        score += 3
    elif matches >= 2:
        score += 2
    elif matches >= 1:
        score += 1

    # 5. Problematic categories
    if fine_class in problematic_fines:
        score += 3

    return score


def adversarial_holdout(df, results):
    strata = {}
    for _, row in df.iterrows():
        mpn = str(row["Mfg_Part_Num"]).strip().upper()
        if mpn in GOLD_MPNS:
            continue
        fine = results[mpn]["fine"]
        diff_score = score_difficulty(row, fine)
        strata.setdefault(fine, []).append((diff_score, mpn))
        
    holdout = []
    for fine, items in sorted(strata.items()):
        # Sort by difficulty score descending, then by MPN string to make it deterministic
        items.sort(key=lambda x: (-x[0], x[1]))
        n = max(1, int(len(items) * HOLDOUT_FRAC))
        holdout.extend([mpn for score, mpn in items[:n]])
    return holdout


def metrics(results, mpns):
    rows = [results[m] for m in mpns]
    n = len(rows)
    attrs = sum(r["n_attrs"] for r in rows) / n
    other = sum(1 for r in rows if r["fine"] == "Other") / n
    dpf = sum(1 for r in rows if r["dual_pass_fail"])
    return {"rows": n, "attrs_per_row": round(attrs, 3), "other_frac": round(other, 4),
            "other_pct": round(other * 100, 1), "dual_pass_fails": dpf}


def gold_check():
    gold_df = pd.read_csv(GOLD_CSV, encoding="utf-8-sig")
    total = correct = 0
    for _, g in gold_df.iterrows():
        raw = {
            "Mfg_Part_Num": g["Mfg_Part_Num"], "Part_Desc": g["Part_Desc"],
            "Part_Manuf": g["Part_Manuf"], "E1_Brand": g["E1_Brand"],
            "Unilog_Brand": g["Unilog_Brand"], "DIB_Brand": g["DIB_Brand"],
        }
        _, flat = run_pipeline(raw)
        for col in g.index:
            if col in INPUT_COLS:
                continue
            v = g[col]
            if pd.isna(v) or str(v).strip() in ("", "nan"):
                continue
            total += 1
            if str(flat.get(col, "")).strip() == str(v).strip():
                correct += 1
    return correct, total


def run_all(sample_df):
    results = {}
    t0 = time.time()
    for _, row in sample_df.iterrows():
        raw = {
            "Mfg_Part_Num": row["Mfg_Part_Num"], "Part_Desc": row["Part_Desc"],
            "Part_Manuf": row["Part_Manuf"], "E1_Brand": row["E1_Brand"],
            "Unilog_Brand": row["Unilog_Brand"], "DIB_Brand": row["DIB_Brand"],
        }
        rec, flat = run_pipeline(raw)
        mpn = str(rec.input.mpn).strip().upper()
        results[mpn] = {
            "mpn": mpn,
            "fine": rec.classpath.fine,
            "dept": rec.classpath.dept,
            "n_attrs": len([a for a in rec.attributes if a.value]),
            "dual_pass_fail": any("Dual-pass verification failed" in r for r in rec.quality.review_reasons),
            "flat": flat,
        }
    print(f"ran {len(results)} rows in {time.time()-t0:.1f}s", file=sys.stderr)
    return results


def main():
    sample_df = pd.read_csv(SAMPLE, encoding="utf-8-sig")
    cache_hit = False
    if CACHE.exists():
        with open(CACHE, "rb") as f:
            cached = pickle.load(f)
        if cached.get("rows") == len(sample_df):
            results = cached["results"]
            cache_hit = True
    if not cache_hit:
        results = run_all(sample_df)
        with open(CACHE, "wb") as f:
            pickle.dump({"rows": len(sample_df), "results": results}, f)

    # Determine adversarial holdout using difficulty scoring
    holdout = adversarial_holdout(sample_df, results)
    m = metrics(results, holdout)
    correct, total = gold_check()
    
    print(json.dumps({
        "holdout_size": m["rows"],
        "attrs_per_row": m["attrs_per_row"],
        "other_pct": m["other_pct"],
        "dual_pass_fails": m["dual_pass_fails"],
        "gold": f"{correct}/{total}",
    }, indent=2))

    # Save outputs
    import csv
    with open(ROOT / "scripts" / "adversarial_mpns.json", "w") as f:
        json.dump(holdout, f)
    with open(ROOT / "scripts" / "adversarial_holdout.csv", "w", newline="", encoding="utf-8-sig") as f:
        sample_row = next(iter(results.values()))["flat"]
        w = csv.DictWriter(f, fieldnames=list(sample_row.keys()))
        w.writeheader()
        for m2 in holdout:
            w.writerow(results[m2]["flat"])


if __name__ == "__main__":
    main()
