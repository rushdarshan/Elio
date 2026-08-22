"""Small mutation checks for the receipt verifier; no test framework required."""

import json
import shutil
import tempfile
from pathlib import Path

from receipt_chain import ROOT, ReceiptError, build_receipt, verify_receipt


def main() -> int:
    (ROOT / "tmp").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
        work = Path(directory)
        evidence = work / "evidence.json"
        input_file = work / "input.csv"
        export = work / "export.csv"
        decision_log = work / "decision_log.jsonl"
        receipt = work / "receipt.json"
        for source, target in (
            (ROOT / "artifacts" / "evidence.json", evidence),
            (ROOT / "demo_input_50.csv", input_file),
            (ROOT / "demo_export_50.csv", export),
            (ROOT / "artifacts" / "decision_log.jsonl", decision_log),
        ):
            shutil.copyfile(source, target)

        build_receipt(
            evidence_path=evidence,
            input_path=input_file,
            export_path=export,
            decision_log_path=decision_log,
            receipt_path=receipt,
        )
        verify_receipt(receipt)

        def must_reject(path: Path, mutation) -> None:
            before = path.read_bytes()
            mutation(path)
            try:
                verify_receipt(receipt)
            except ReceiptError:
                path.write_bytes(before)
                return
            path.write_bytes(before)
            raise AssertionError(f"mutated {path.name} unexpectedly verified")

        def mutate_evidence(path: Path) -> None:
            value = json.loads(path.read_text(encoding="utf-8"))
            value["rows"]["PDSH4816AF"]["accepted"][0]["evidence"]["text"] += " tampered"
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

        must_reject(evidence, mutate_evidence)
        must_reject(input_file, lambda path: path.write_bytes(path.read_bytes() + b"\n"))
        must_reject(export, lambda path: path.write_bytes(path.read_bytes() + b"\n"))
        must_reject(decision_log, lambda path: path.write_bytes(path.read_bytes() + b"{}\n"))

        def mutate_receipt(path: Path) -> None:
            value = json.loads(path.read_text(encoding="utf-8"))
            value["claims"][0]["value"] = "tampered"
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

        must_reject(receipt, mutate_receipt)

    print("[PASS] receipt mutation checks: input/source/decision/output tamper rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
