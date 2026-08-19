import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ROOT = Path(__file__).resolve().parent.parent


def load(p):
    return pd.read_csv(p, encoding="utf-8-sig", dtype=str).fillna("")


def main() -> None:
    old = load(r"C:\Users\rushd\AppData\Local\Temp\opencode\old_full.csv")
    new = load(ROOT / "Unihack_Full_Export_1000.csv")

    assert list(old.columns) == list(new.columns), "SCHEMA MISMATCH"
    print(f"schema: 252 headers, identical order ({len(old.columns)} cols)")

    mpn = "Mfg_Part_Num" if "Mfg_Part_Num" in old.columns else "PART_NUMBER"

    def pop_count(df):
        return (df != "").sum(axis=1)

    o, n = pop_count(old), pop_count(new)
    print(f"populated cells/row: old {o.mean():.1f} (min {o.min()}) -> new {n.mean():.1f} (min {n.min()})")
    print(f"rows with MORE cells: {(n > o).sum()}, FEWER: {(n < o).sum()}, same: {(n == o).sum()}")

    fine_col = next((c for c in old.columns if c.strip().lower() == "fine"), None)
    if fine_col:
        for label, df in [("old", old), ("new", new)]:
            other = (df[fine_col] == "Other").sum()
            print(f"{label}: Fine=Other {other}/1000")

    cols = [c for c in new.columns if c not in (mpn, "Part_Desc")]
    v2b = b2v = v2v = 0
    col_changes = []
    for c in cols:
        a, b = old[c], new[c]
        n_v2b = ((a != "") & (b == "")).sum()
        n_b2v = ((a == "") & (b != "")).sum()
        n_v2v = ((a != "") & (b != "") & (a != b)).sum()
        if n_v2b or n_b2v or n_v2v:
            col_changes.append((c, int(n_v2b), int(n_b2v), int(n_v2v)))
        v2b += n_v2b
        b2v += n_b2v
        v2v += n_v2v
    print(f"cell changes: value->blank {v2b}, blank->value {b2v}, value->different {v2v}")

    col_changes.sort(key=lambda t: -(t[1] + t[2] + t[3]))
    print("\ntop changed columns (col, v2b, b2v, v2v):")
    for t in col_changes[:20]:
        print("  ", t)

    old_d = load(r"C:\Users\rushd\AppData\Local\Temp\opencode\old_demo.csv")
    new_d = load(ROOT / "demo_export_50.csv")
    assert list(old_d.columns) == list(new_d.columns)
    print(f"\ndemo: populated cells/row old {pop_count(old_d).mean():.1f} -> new {pop_count(new_d).mean():.1f}")


if __name__ == "__main__":
    main()