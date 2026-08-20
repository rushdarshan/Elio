import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from unihack_catalog.stages import _DISTRIBUTOR_BLACKLIST
from unihack_catalog.category_extractors import CATEGORY_TRIGGERS
from unihack_catalog.reference_loader import BRAND_VOCAB


def sanity_check_rules() -> None:
    print("\n>>> RUNNING PIPELINE RULES SANITY LINTER <<<")

    trigger_to_cats = {}
    for cat, triggers in CATEGORY_TRIGGERS.items():
        for t in triggers:
            trigger_to_cats.setdefault(t.lower(), []).append(cat)

    dupes = {t: cats for t, cats in trigger_to_cats.items() if len(cats) > 1}
    for t, cats in sorted(dupes.items()):
        print(f"  [LINTER INFO] Trigger keyword '{t}' is shared across categories: {cats}")

    for brand, info in BRAND_VOCAB.items():
        mfr = info.get("manufacturer")
        if brand in _DISTRIBUTOR_BLACKLIST:
            print(f"  [LINTER WARNING] Brand '{brand}' is in the distributor blacklist!")
        if mfr and mfr in _DISTRIBUTOR_BLACKLIST:
            print(f"  [LINTER WARNING] Manufacturer parent '{mfr}' of brand '{brand}' is in the distributor blacklist!")

    for cat, triggers in CATEGORY_TRIGGERS.items():
        for t in triggers:
            if len(t) <= 2:
                print(f"  [LINTER WARNING] Trigger '{t}' in category '{cat}' is very short (<= 2 chars) and may cause false positives.")
            if any(char in t for char in [".", "*", "+", "?", "^", "$", "(", ")", "[", "]", "{", "}"]):
                print(f"  [LINTER WARNING] Trigger '{t}' in category '{cat}' contains regex special characters without being escaped.")
    print(">>> PIPELINE RULES SANITY LINTER COMPLETED <<<\n")


if __name__ == "__main__":
    sanity_check_rules()