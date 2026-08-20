import sys
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import run_pipeline

# UAT Verification Cases: inputs and expected normalization outputs
VERIFICATION_CASES = [
    {
        "id": "Ceiling Tile Unit Correction (1728ABL)",
        "input": {
            "Mfg_Part_Num": "1728ABL",
            "Part_Desc": "2x2 Black Fine Fissured 1728BL",
            "Part_Manuf": "Palmer Donavin Mfg Company (PALDO)",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
        },
        "expected": {
            "class_fine": "Ceiling Tiles",
            "brand": "Unbranded",
            "attributes": {
                "Size": "2 ft x 2 ft",
                "Color": "Black",
                "Type": "Fissured"
            }
        }
    },
    {
        "id": "Jumpstarter Classification & Type Verbatim (SL1672)",
        "input": {
            "Mfg_Part_Num": "SL1672",
            "Part_Desc": "SL1672 Jumpstart & Pwr Supply",
            "Part_Manuf": "-",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "Schumacher",
        },
        "expected": {
            "class_fine": "Power Supplies",
            "brand": "Schumacher",
            "attributes": {
                "Type": "Jumpstart"
            }
        }
    },
    {
        "id": "Phone Holster Classification & LG Brand Guard (5328)",
        "input": {
            "Mfg_Part_Num": "5328",
            "Part_Desc": "5328 Lg. Leather Phone Holster - Clip-on",
            "Part_Manuf": "-",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
        },
        "expected": {
            "class_fine": "Tool Organizers",
            "brand": "Unbranded",
            "attributes": {
                "Type": "Holster"
            }
        }
    },
    {
        "id": "Glove Sizing LG Brand Guard (MWUG36010425)",
        "input": {
            "Mfg_Part_Num": "MWUG36010425",
            "Part_Desc": "MWUG36010425 BLK LG Aerial Snow Heated Glove",
            "Part_Manuf": "Tech Gear 5.7 Inc (TECGE)",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
        },
        "expected": {
            "class_fine": "Heated Apparel",
            "brand": "Unbranded",
            "attributes": {
                "Type": "Glove"
            }
        }
    },
    {
        "id": "Angle Grinder Norm (DCG402B)",
        "input": {
            "Mfg_Part_Num": "DCG402B",
            "Part_Desc": "DCG402B Dewalt 20V 4.5\" Angle Grinder (Bare)",
            "Part_Manuf": "Black & Decker/dewlt (2585)",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
        },
        "expected": {
            "class_fine": "Angle Grinders",
            "brand": "DEWALT",
            "attributes": {
                "Voltage Rating": "20 V",
                "Size": "4.5 in",
                "Type": "Angle Grinder"
            }
        }
    },
    {
        "id": "LG Microwave OEM Validation (MSER2090S)",
        "input": {
            "Mfg_Part_Num": "MSER2090S",
            "Part_Desc": "MSER2090S LG Microwave SS",
            "Part_Manuf": "Appliance Dealers Cooperative (APPDE)",
            "E1_Brand": "-- Unbranded --",
            "Unilog_Brand": "-- No Unilog Brand --",
            "DIB_Brand": "-- No DIB Brand --",
        },
        "expected": {
            "class_fine": "Microwaves",
            "brand": "LG",
            "attributes": {
                "Material": "Stainless Steel"
            }
        }
    }
]


def run_ledger_tests() -> bool:
    print("=== STARTING HARDENED VERIFICATION LEDGER ===")
    failed = 0
    passed = 0

    for case in VERIFICATION_CASES:
        case_id = case["id"]
        inp = case["input"]
        exp = case["expected"]

        print(f"\nRunning UAT Case: {case_id}")
        try:
            rec, flat = run_pipeline(inp)
            
            # Check fine class
            actual_fine = rec.classpath.fine
            if actual_fine != exp["class_fine"]:
                print(f"  [FAIL] Fine Class mismatch. Expected: '{exp['class_fine']}', Got: '{actual_fine}'")
                failed += 1
                continue
            else:
                print(f"  [PASS] Fine Class matches: '{actual_fine}'")

            # Check Brand
            actual_brand = rec.identity.brand.label
            if actual_brand != exp["brand"]:
                print(f"  [FAIL] Brand mismatch. Expected: '{exp['brand']}', Got: '{actual_brand}'")
                failed += 1
                continue
            else:
                print(f"  [PASS] Brand matches: '{actual_brand}'")

            # Check Attributes from rec.attributes
            actual_attrs = {}
            for attr in rec.attributes:
                if attr.value:
                    val_str = str(attr.value).strip()
                    if attr.uom:
                        val_str += f" {attr.uom}"
                    actual_attrs[attr.label] = val_str

            attr_errors = 0
            for attr_lbl, exp_val in exp["attributes"].items():
                actual_val = actual_attrs.get(attr_lbl, "")
                if str(actual_val).strip() != str(exp_val).strip():
                    print(f"  [FAIL] Attribute '{attr_lbl}' mismatch. Expected: '{exp_val}', Got: '{actual_val}'")
                    attr_errors += 1
                else:
                    print(f"  [PASS] Attribute '{attr_lbl}' matches: '{actual_val}'")

            if attr_errors > 0:
                failed += 1
            else:
                passed += 1

        except Exception as e:
            print(f"  [ERROR] Pipeline crashed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "="*40)
    print(f"VERIFICATION RESULTS: {passed} PASSED, {failed} FAILED")
    print("="*40)
    return failed == 0


if __name__ == "__main__":
    success = run_ledger_tests()
    sys.exit(0 if success else 1)
