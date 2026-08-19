import sys
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

EXPECTED = [
    "Unilog-Sample_200_Items-Input-vs-Output.xlsx",
    "Unicat_Lov_v1_0_Updated_With_Remarks.xlsx",
    "FAUCETS_LOV.xlsx",
    "Fittings_LOV.xlsx",
    "UniCat_Manufacturer_and_Brand_List.xlsx",
    "Unilog_Master_UOM_Standards_Abbreviations_and_Terms.xlsx",
    "Decimal_Fraction.xlsx",
    "UNILOG_INTERNAL_CONTENT_GUIDELINES.docx",
]

missing = []
for name in EXPECTED:
    path = RAW / name
    if path.is_file() and path.stat().st_size > 0:
        print(f"OK   {name} ({path.stat().st_size:,} bytes)")
    else:
        print(f"MISS {name}")
        missing.append(name)

if missing:
    print(f"\n{len(missing)} of {len(EXPECTED)} files missing. Drop them in {RAW} "
          f"(Resources tab on the UniHack dashboard), then re-run.")
    sys.exit(1)
print("\nAll reference files present. Day 1 can start.")
