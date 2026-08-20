import json
import sys
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

# Sort by fine class to group similar products
holdout_df = holdout_df.copy()
# We need to temporarily run the pipeline to get the fine class for sorting
fine_classes = {}
for _, row in holdout_df.iterrows():
    raw = {
        "Mfg_Part_Num": row["Mfg_Part_Num"], "Part_Desc": row["Part_Desc"],
        "Part_Manuf": row["Part_Manuf"], "E1_Brand": row["E1_Brand"],
        "Unilog_Brand": row["Unilog_Brand"], "DIB_Brand": row["DIB_Brand"],
    }
    rec, _ = run_pipeline(raw)
    fine_classes[raw["Mfg_Part_Num"]] = rec.classpath.fine

holdout_df["fine"] = holdout_df["Mfg_Part_Num"].apply(lambda m: fine_classes.get(m, "Other"))
holdout_df = holdout_df.sort_values("fine")

output_lines = []
for _, row in holdout_df.iterrows():
    raw = {
        "Mfg_Part_Num": row["Mfg_Part_Num"], "Part_Desc": row["Part_Desc"],
        "Part_Manuf": row["Part_Manuf"], "E1_Brand": row["E1_Brand"],
        "Unilog_Brand": row["Unilog_Brand"], "DIB_Brand": row["DIB_Brand"],
    }
    rec, flat = run_pipeline(raw)
    
    attrs_str = ", ".join([f"{a.label}={a.value}{' ' + a.uom if a.uom else ''}" for a in rec.attributes if a.value])
    
    output_lines.append(f"MPN: {row['Mfg_Part_Num']}")
    output_lines.append(f"Desc: {row['Part_Desc']}")
    output_lines.append(f"Manuf: {row['Part_Manuf']} | Brand (Resolved): {rec.identity.brand.label}")
    output_lines.append(f"Class: {rec.classpath.dept} > {rec.classpath.class_} > {rec.classpath.fine}")
    output_lines.append(f"Attrs: {attrs_str}")
    output_lines.append("-" * 80)

with open(ROOT / "scripts" / "adversarial_inspected.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("Wrote adversarial_inspected.txt")
