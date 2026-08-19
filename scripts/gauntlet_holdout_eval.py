import json, os, pickle, random, sys, time
from pathlib import Path

import pandas as pd

ROOT = Path(r"C:\Users\rushd\Downloads\Jesus WIn")
sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline
from unihack_catalog.reference_loader import ReferenceLoader

SAMPLE = ROOT / "Unihack_ Sample Dataset - Input.csv"
GOLD_CSV = ROOT / "Unihack_ Expected Output - Delivery Format.csv"
CACHE = ROOT / "scripts" / ".gauntlet_results.pkl"
INPUT_COLS = {"PART_NUMBER", "SKU - MY_PART_NUMBER", "Mfg_Part_Num", "Part_Desc",
              "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf"}
GOLD_MPNS = {"PDSH4816AF", "WDTS7024RZ"}
SEED = 7
HOLDOUT_FRAC = 0.25


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


def stratified_holdout(results):
    rng = random.Random(SEED)
    strata = {}
    for mpn, r in results.items():
        if mpn in GOLD_MPNS:
            continue
        strata.setdefault(r["fine"], []).append(mpn)
    holdout = []
    for fine, mpns in sorted(strata.items()):
        rng.shuffle(mpns)
        n = max(1, int(len(mpns) * HOLDOUT_FRAC))
        holdout.extend(mpns[:n])
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

    holdout = stratified_holdout(results)
    m = metrics(results, holdout)
    correct, total = gold_check()
    print(json.dumps({
        "holdout_size": m["rows"],
        "attrs_per_row": m["attrs_per_row"],
        "other_pct": m["other_pct"],
        "dual_pass_fails": m["dual_pass_fails"],
        "gold": f"{correct}/{total}",
    }, indent=2))

    # Dump holdout flat exports for critic A/B + baseline export CSV
    import csv
    with open(ROOT / "scripts" / "holdout_mpns.json", "w") as f:
        json.dump(holdout, f)
    with open(ROOT / "scripts" / "baseline_holdout.csv", "w", newline="", encoding="utf-8-sig") as f:
        sample_row = next(iter(results.values()))["flat"]
        w = csv.DictWriter(f, fieldnames=list(sample_row.keys()))
        w.writeheader()
        for m2 in holdout:
            w.writerow(results[m2]["flat"])


if __name__ == "__main__":
    main()