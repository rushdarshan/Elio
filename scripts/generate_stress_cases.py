"""
ARC Task Gen-Style Adversarial & Distribution-Matched Stress Case Generator for ELIO.

Generates reproducible stress testing cases with parameterized random seeds:
- Abbreviated titles & distributor noise
- Multi-brand / Parent-brand disambiguation (Diablo vs Freud, DeWalt vs SBD)
- Unit variant & compound fraction conversions
- Near-neighbor taxonomy challenges
- Sparse & missing field scenarios
"""

import sys
import random
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUTPUT_CSV = ROOT / "artifacts" / "stress_test_suite.csv"


STRESS_TEMPLATES = [
    {
        "mfr_alias": "Freud Inc. (FREUD)",
        "brand_alias": "Diablo",
        "mpn": "D0724A_{i}",
        "desc_tmpl": "7-1/4 in. x 24-Teeth Tracking Point Framing Saw Blade {i} pk",
        "expected_class": "Saw Blades",
        "expected_brand": "Diablo",
        "expected_mfr": "Freud Inc.",
        "difficulty": "parent_brand_disambiguation"
    },
    {
        "mfr_alias": "Stanley Black & Decker / Dewalt (SBD)",
        "brand_alias": "-- Unbranded --",
        "mpn": "DCG413B_{i}",
        "desc_tmpl": "20V MAX 4-1/2 in Brushless Angle Grinder (Tool Only) 9000 RPM",
        "expected_class": "Angle Grinders",
        "expected_brand": "DEWALT",
        "expected_mfr": "Stanley Black & Decker",
        "difficulty": "brand_from_description"
    },
    {
        "mfr_alias": "Techtronic Industries (TTI)",
        "brand_alias": "-- No Unilog Brand --",
        "mpn": "48-22-8426_{i}",
        "desc_tmpl": "PACKOUT 22 in. Rolling Modular Tool Box XL Capacity",
        "expected_class": "Tool Organizers",
        "expected_brand": "Milwaukee",
        "expected_mfr": "Techtronic Industries",
        "difficulty": "brand_sub_brand_linkage"
    },
    {
        "mfr_alias": "Appliance Dealers Co-Op (APPDE)",
        "brand_alias": "None",
        "mpn": "LDFN4542S_{i}",
        "desc_tmpl": "LG QuadWash Front Control Dishwasher SS 48 dBA 15 Place Settings",
        "expected_class": "Dishwashers",
        "expected_brand": "LG",
        "expected_mfr": "LG Electronics",
        "difficulty": "distributor_masking"
    },
    {
        "mfr_alias": "Palmer Donavin (PALDO)",
        "brand_alias": "-- Unbranded --",
        "mpn": "1728BL_{i}",
        "desc_tmpl": "2x4 Black Acoustic Fissured Ceiling Tile 5/8 in thick",
        "expected_class": "Ceiling Tiles",
        "expected_brand": "Unbranded",
        "expected_mfr": "Manufacturer",
        "difficulty": "terse_unit_heavy"
    }
]


def generate_stress_cases(count: int = 20, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    print(f"=== GENERATING {count} STRESS CASES (SEED: {seed}) ===")

    rows = []
    for i in range(count):
        tmpl = random.choice(STRESS_TEMPLATES)
        mpn_val = tmpl["mpn"].format(i=i+1)
        desc_val = tmpl["desc_tmpl"].format(i=i+1)
        
        # Inject realistic noise variations
        if random.random() < 0.3:
            desc_val = desc_val.lower()
        if random.random() < 0.2:
            desc_val += " [LIMITED AVAILABILITY]"
            
        rows.append({
            "Mfg_Part_Num": mpn_val,
            "Part_Desc": desc_val,
            "Part_Manuf": tmpl["mfr_alias"],
            "E1_Brand": tmpl["brand_alias"],
            "Unilog_Brand": tmpl["brand_alias"],
            "DIB_Brand": tmpl["brand_alias"],
            "Target_Class": tmpl["expected_class"],
            "Target_Brand": tmpl["expected_brand"],
            "Difficulty": tmpl["difficulty"]
        })

    df = pd.DataFrame(rows)
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} stress cases to {OUTPUT_CSV}")
    print("[PASS] Generated stress test suite successfully.")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ELIO Stress Case Generator")
    parser.add_argument("--count", type=int, default=20, help="Number of stress cases")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()
    
    generate_stress_cases(count=args.count, seed=args.seed)
    sys.exit(0)
