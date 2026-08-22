"""Generate the content-addressed receipt for the canonical demo artifacts."""

import json
import sys

from receipt_chain import ReceiptError, build_receipt


def main() -> int:
    try:
        receipt = build_receipt()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[FAIL] receipt build: {exc}")
        return 1
    print(
        f"[PASS] receipt built: {receipt['claim_count']} claims / "
        f"{receipt['row_count']} rows -> artifacts/receipt.json"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
