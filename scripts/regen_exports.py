import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unihack_catalog.stages import run_pipeline, stage_export

INPUT_COLS = ["Mfg_Part_Num", "Part_Desc", "Part_Manuf", "E1_Brand", "Unilog_Brand", "DIB_Brand"]


def process(df: pd.DataFrame) -> pd.DataFrame:
    flats = []
    for _, row in df.iterrows():
        raw = {c: ("" if pd.isna(row[c]) else str(row[c])) for c in INPUT_COLS}
        rec, _ = run_pipeline(raw)
        rec, flat = stage_export(rec)
        flats.append(flat)
    return pd.DataFrame(flats)


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    sample = pd.read_csv(root / "Unihack_ Sample Dataset - Input.csv", encoding="utf-8-sig")
    full = process(sample)
    full.to_csv(root / "Unihack_Full_Export_1000.csv", index=False, encoding="utf-8-sig")
    print(f"full: {full.shape}")

    demo = pd.read_csv(root / "demo_input_50.csv", encoding="utf-8-sig")
    demo_out = process(demo)
    demo_out.to_csv(root / "demo_export_50.csv", index=False, encoding="utf-8-sig")
    print(f"demo: {demo_out.shape}")


if __name__ == "__main__":
    main()