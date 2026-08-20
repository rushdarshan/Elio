import json
import sys
import re
from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\rushd\Downloads\Jesus WIn")
sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline

SAMPLE = ROOT / "Unihack_ Sample Dataset - Input.csv"
with open(ROOT / "scripts" / "adversarial_mpns.json") as f:
    holdout_mpns = set(json.load(f))

df = pd.read_csv(SAMPLE, encoding="utf-8-sig").fillna("")
holdout_df = df[df["Mfg_Part_Num"].apply(lambda m: m.strip().upper() in holdout_mpns)]

print(f"Analyzing {len(holdout_df)} holdout rows...")

anomalies = []
coverage_gaps = []

# Whitelists for known units
uoms = {"in", "mm", "v", "w", "lm", "k", "awg", "ft", "dba", "ga", "a"}

for _, row in holdout_df.iterrows():
    raw = {
        "Mfg_Part_Num": row["Mfg_Part_Num"], "Part_Desc": row["Part_Desc"],
        "Part_Manuf": row["Part_Manuf"], "E1_Brand": row["E1_Brand"],
        "Unilog_Brand": row["Unilog_Brand"], "DIB_Brand": row["DIB_Brand"],
    }
    rec, flat = run_pipeline(raw)
    desc = raw["Part_Desc"]
    mpn = raw["Mfg_Part_Num"]
    
    # 1. Check for Amperage anomalies
    amp_attr = next((a for a in rec.attributes if a.label == "Amperage Rating"), None)
    if amp_attr and amp_attr.value:
        val = amp_attr.value
        # Check if the amperage is extremely high (e.g. > 1000) or looks like an MPN/part of desc
        try:
            num = float(re.sub(r'[^\d\.]', '', val))
            if num >= 60 and num not in (100, 200): # Allow standard load centers
                anomalies.append({
                    "mpn": mpn, "desc": desc, "type": "Amperage Rating", "value": val,
                    "reason": f"High amperage value {val} - possible false positive from MPN or model code"
                })
        except ValueError:
            pass

    # 2. Check for Size anomalies
    size_attr = next((a for a in rec.attributes if a.label == "Size"), None)
    if size_attr and size_attr.value:
        val = size_attr.value
        # If size contains "'" but does not contain "ft", or contains "in" but refers to feet in desc
        if "'" in desc and "ft" not in val and "in" in val and not any(k in val for k in ("1 in x 8 in", "1 in x 12 in")):
            anomalies.append({
                "mpn": mpn, "desc": desc, "type": "Size", "value": val,
                "reason": f"Desc contains foot mark (') but Size value '{val}' is in inches - possible unit error"
            })
            
    # 3. Check for general dual-pass verification (all attributes)
    for a in rec.attributes:
        if a.value:
            # Check if UOM is standard
            if a.uom and a.uom.lower() not in uoms:
                anomalies.append({
                    "mpn": mpn, "desc": desc, "type": a.label, "value": f"{a.value} {a.uom}",
                    "reason": f"Non-standard UOM '{a.uom}'"
                })
            
            # Check if value is in raw text
            val_l = a.value.lower()
            desc_l = desc.lower()
            base = re.sub(r'\s*(in|mm|v|w|lm|k|awg|ft|dba|ga)\s*$', '', val_l)
            if val_l not in desc_l and base not in desc_l and not (re.search(r'\b\d+\b', a.value) and val_l.split()[0] in desc_l):
                # Check for standard expansions
                if a.label == "Material" and val_l in ("stainless steel", "stainless") and any(ab in desc_l for ab in ("ss", "sst", "s/s")):
                    continue
                anomalies.append({
                    "mpn": mpn, "desc": desc, "type": a.label, "value": a.value,
                    "reason": "Value not found in source description (dual-pass failure)"
                })

    # 4. Check for Classpath Other
    if rec.classpath.fine == "Other":
        coverage_gaps.append({
            "mpn": mpn, "desc": desc, "reason": "Fine class is 'Other' - missing classification coverage"
        })

print(f"\n--- ANOMALIES FOUND: {len(anomalies)} ---")
for idx, a in enumerate(anomalies[:15]):
    print(f"{idx+1}. MPN: {a['mpn']} | Value: {a['value']} ({a['type']})")
    print(f"   Desc: {a['desc']}")
    print(f"   Reason: {a['reason']}")

print(f"\n--- COVERAGE GAPS (Other fine class): {len(coverage_gaps)} ---")
for idx, g in enumerate(coverage_gaps[:10]):
    print(f"{idx+1}. MPN: {g['mpn']} | Desc: {g['desc']}")
