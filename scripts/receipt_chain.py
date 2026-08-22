"""Build and verify an honest, content-addressed ELIO evidence receipt.

The frozen pipeline emits an evidence excerpt and a locator, but it does not
ship the publisher document bytes. This module therefore binds the evidence
excerpt itself and labels that limitation explicitly instead of claiming an
external source hash that cannot be recomputed offline.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
INPUT_COLUMNS = (
    "Mfg_Part_Num",
    "Part_Desc",
    "Part_Manuf",
    "E1_Brand",
    "Unilog_Brand",
    "DIB_Brand",
)


class ReceiptError(ValueError):
    """Raised when a receipt-bound artifact is malformed or inconsistent."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_value(value: Any) -> str:
    return digest_bytes(canonical_bytes(value))


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def _relative_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def _required_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ReceiptError(f"{label} must be a full 64-character SHA-256 digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ReceiptError(f"{label} is not hexadecimal") from exc
    return value


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _input_row_hash(row: dict[str, str]) -> str:
    return digest_value({key: row.get(key, "") for key in INPUT_COLUMNS})


def _source_hash(evidence: dict[str, Any]) -> str:
    text = evidence.get("text")
    if not isinstance(text, str) or not text:
        raise ReceiptError("accepted evidence must contain non-empty source text")
    return digest_bytes(text.encode("utf-8"))


def _validate_span(span: Any) -> None:
    if span is None:
        return
    if (
        not isinstance(span, list)
        or len(span) != 2
        or any(isinstance(part, bool) or not isinstance(part, int) for part in span)
        or span[0] < 0
        or span[1] < span[0]
    ):
        raise ReceiptError(f"invalid character span: {span!r}")


def _decision_keys(path: Path) -> set[tuple[str, str, str, str]]:
    keys: set[tuple[str, str, str, str]] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ReceiptError(f"invalid decision log JSON at line {line_number}") from exc
            if event.get("type") == "decision" and event.get("status") == "accepted":
                keys.add(
                    (
                        str(event.get("mpn", "")),
                        str(event.get("attribute", "")),
                        str(event.get("value", "")),
                        str(event.get("uom", "")),
                    )
                )
    return keys


def build_receipt(
    *,
    evidence_path: Path = ROOT / "artifacts" / "evidence.json",
    input_path: Path = ROOT / "demo_input_50.csv",
    export_path: Path = ROOT / "demo_export_50.csv",
    decision_log_path: Path = ROOT / "artifacts" / "decision_log.jsonl",
    receipt_path: Path = ROOT / "artifacts" / "receipt.json",
) -> dict[str, Any]:
    evidence_doc = json.loads(evidence_path.read_text(encoding="utf-8"))
    rows = evidence_doc.get("rows")
    row_order = evidence_doc.get("row_order")
    if not isinstance(rows, dict) or not isinstance(row_order, list) or not row_order:
        raise ReceiptError("evidence.json requires non-empty rows and row_order")
    if len(set(row_order)) != len(row_order) or set(row_order) != set(rows):
        raise ReceiptError("evidence row_order is not a unique bijection")

    input_rows = _read_csv(input_path)
    input_by_mpn = {str(row.get("Mfg_Part_Num", "")).strip().upper(): row for row in input_rows}
    output_rows = _read_csv(export_path)
    output_by_mpn = {str(row.get("Mfg_Part_Num", "")).strip().upper(): row for row in output_rows}
    decisions = _decision_keys(decision_log_path)

    claims: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for mpn in row_order:
        row = rows[mpn]
        input_row = input_by_mpn.get(str(mpn).upper())
        output_row = output_by_mpn.get(str(mpn).upper())
        if input_row is None or output_row is None:
            raise ReceiptError(f"{mpn}: missing input or export row")
        for item in row.get("accepted", []):
            key = (str(mpn), str(item.get("attribute", "")))
            if key in seen:
                raise ReceiptError(f"duplicate accepted claim: {key}")
            seen.add(key)
            evidence = item.get("evidence")
            if not isinstance(evidence, dict):
                raise ReceiptError(f"{mpn}: accepted claim has no evidence object")
            _validate_span(evidence.get("char_span"))
            source_hash = _source_hash(evidence)
            attribute = str(item.get("attribute", ""))
            value = str(item.get("value", ""))
            uom = str(item.get("uom", ""))
            export_column = item.get("export_column")
            if not isinstance(export_column, str) or not export_column:
                raise ReceiptError(f"{mpn}/{attribute}: missing export column")
            decision_key = (str(mpn), attribute, value, uom)
            if decision_key not in decisions:
                raise ReceiptError(f"{mpn}/{attribute}: missing accepted decision event")
            if export_column not in output_row:
                raise ReceiptError(f"{mpn}/{attribute}: export column does not exist")
            claim_payload = {
                "mpn": str(mpn),
                "attribute": attribute,
                "value": value,
                "uom": uom,
                "export_column": export_column,
                "source_hash": source_hash,
                "char_span": evidence.get("char_span"),
                "source_kind": evidence.get("kind"),
            }
            claim_hash = digest_value(claim_payload)
            decision_payload = {
                "claim_hash": claim_hash,
                "status": "accepted",
                "verification": item.get("verification"),
                "gate": "dual-pass",
            }
            decision_hash = digest_value(decision_payload)
            output_payload = {
                "mpn": str(mpn),
                "column": export_column,
                "value": output_row[export_column],
            }
            output_hash = digest_value(output_payload)
            claims.append(
                {
                    **claim_payload,
                    "input_row_hash": _input_row_hash(input_row),
                    "decision_hash": decision_hash,
                    "output_hash": output_hash,
                    "claim_hash": claim_hash,
                    "chain_hash": digest_value(
                        {
                            "input_row_hash": _input_row_hash(input_row),
                            "source_hash": source_hash,
                            "claim_hash": claim_hash,
                            "decision_hash": decision_hash,
                            "output_hash": output_hash,
                        }
                    ),
                }
            )

    core = {
        "schema_version": 1,
        "freeze_commit": evidence_doc.get("freeze_commit"),
        "source_attestation": "artifact-excerpt-only; publisher bytes are not bundled",
        "artifacts": {
            "input": {"path": _relative_path(input_path), "sha256": digest_file(input_path)},
            "evidence": {"path": _relative_path(evidence_path), "sha256": digest_file(evidence_path)},
            "decision_log": {"path": _relative_path(decision_log_path), "sha256": digest_file(decision_log_path)},
            "export": {"path": _relative_path(export_path), "sha256": digest_file(export_path)},
        },
        "row_count": len(row_order),
        "claim_count": len(claims),
        "claims": claims,
    }
    receipt = {**core, "receipt_sha256": digest_value(core)}
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


def verify_receipt(
    receipt_path: Path = ROOT / "artifacts" / "receipt.json",
) -> dict[str, Any]:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    stored_receipt_hash = _required_digest(receipt.get("receipt_sha256"), "receipt_sha256")
    core = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    if digest_value(core) != stored_receipt_hash:
        raise ReceiptError("receipt root digest mismatch")
    if receipt.get("schema_version") != 1:
        raise ReceiptError("unsupported receipt schema")
    artifacts = receipt.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ReceiptError("receipt artifacts object is missing")
    paths: dict[str, Path] = {}
    for name, meta in artifacts.items():
        if not isinstance(meta, dict):
            raise ReceiptError(f"{name}: malformed artifact metadata")
        path = (ROOT / str(meta.get("path", ""))).resolve()
        if ROOT.resolve() not in path.parents:
            raise ReceiptError(f"{name}: artifact path escapes repository")
        if not path.is_file():
            raise ReceiptError(f"{name}: artifact is missing")
        expected = _required_digest(meta.get("sha256"), f"{name}.sha256")
        actual = digest_file(path)
        if actual != expected:
            raise ReceiptError(f"{name}: digest mismatch")
        paths[name] = path

    evidence_doc = json.loads(paths["evidence"].read_text(encoding="utf-8"))
    rows = evidence_doc.get("rows", {})
    input_rows = _read_csv(paths["input"])
    output_rows = _read_csv(paths["export"])
    input_by_mpn = {str(row.get("Mfg_Part_Num", "")).strip().upper(): row for row in input_rows}
    output_by_mpn = {str(row.get("Mfg_Part_Num", "")).strip().upper(): row for row in output_rows}
    decisions = _decision_keys(paths["decision_log"])
    seen: set[tuple[str, str]] = set()
    claims = receipt.get("claims")
    if not isinstance(claims, list) or receipt.get("claim_count") != len(claims):
        raise ReceiptError("claim_count does not match claims")
    if receipt.get("row_count") != len(evidence_doc.get("row_order", [])):
        raise ReceiptError("row_count does not match evidence row_order")

    for claim in claims:
        mpn = str(claim.get("mpn", ""))
        attribute = str(claim.get("attribute", ""))
        key = (mpn, attribute)
        if key in seen:
            raise ReceiptError(f"duplicate receipt claim: {key}")
        seen.add(key)
        row = rows.get(mpn)
        if not isinstance(row, dict):
            raise ReceiptError(f"{mpn}: claim row missing from evidence")
        matching = [item for item in row.get("accepted", []) if item.get("attribute") == attribute]
        if len(matching) != 1:
            raise ReceiptError(f"{mpn}/{attribute}: evidence claim is missing or duplicated")
        item = matching[0]
        evidence = item.get("evidence") or {}
        _validate_span(evidence.get("char_span"))
        for field in ("value", "uom", "export_column"):
            if str(item.get(field, "")) != str(claim.get(field, "")):
                raise ReceiptError(f"{mpn}/{attribute}: {field} does not match evidence")
        if evidence.get("char_span") != claim.get("char_span") or evidence.get("kind") != claim.get("source_kind"):
            raise ReceiptError(f"{mpn}/{attribute}: evidence locator does not match receipt")
        if _source_hash(evidence) != claim.get("source_hash"):
            raise ReceiptError(f"{mpn}/{attribute}: source excerpt digest mismatch")
        input_row = input_by_mpn.get(mpn.upper())
        output_row = output_by_mpn.get(mpn.upper())
        if input_row is None or output_row is None:
            raise ReceiptError(f"{mpn}: input/export row missing")
        if _input_row_hash(input_row) != claim.get("input_row_hash"):
            raise ReceiptError(f"{mpn}: input row digest mismatch")
        export_column = claim.get("export_column")
        if export_column not in output_row:
            raise ReceiptError(f"{mpn}/{attribute}: export column missing")
        output_hash = digest_value({"mpn": mpn, "column": export_column, "value": output_row[export_column]})
        if output_hash != claim.get("output_hash"):
            raise ReceiptError(f"{mpn}/{attribute}: output cell digest mismatch")
        decision_key = (mpn, attribute, str(claim.get("value", "")), str(claim.get("uom", "")))
        if decision_key not in decisions:
            raise ReceiptError(f"{mpn}/{attribute}: decision event missing")
        claim_payload = {
            "mpn": mpn,
            "attribute": attribute,
            "value": str(claim.get("value", "")),
            "uom": str(claim.get("uom", "")),
            "export_column": export_column,
            "source_hash": claim.get("source_hash"),
            "char_span": claim.get("char_span"),
            "source_kind": claim.get("source_kind"),
        }
        claim_hash = digest_value(claim_payload)
        if claim_hash != claim.get("claim_hash"):
            raise ReceiptError(f"{mpn}/{attribute}: claim digest mismatch")
        decision_hash = digest_value(
            {
                "claim_hash": claim_hash,
                "status": "accepted",
                "verification": item.get("verification"),
                "gate": "dual-pass",
            }
        )
        if decision_hash != claim.get("decision_hash"):
            raise ReceiptError(f"{mpn}/{attribute}: decision digest mismatch")
        chain_hash = digest_value(
            {
                "input_row_hash": claim.get("input_row_hash"),
                "source_hash": claim.get("source_hash"),
                "claim_hash": claim_hash,
                "decision_hash": decision_hash,
                "output_hash": output_hash,
            }
        )
        if chain_hash != claim.get("chain_hash"):
            raise ReceiptError(f"{mpn}/{attribute}: chain digest mismatch")

    expected_claims = {
        (str(mpn), str(item.get("attribute")))
        for mpn in evidence_doc.get("row_order", [])
        for item in rows[mpn].get("accepted", [])
    }
    if seen != expected_claims:
        raise ReceiptError("receipt does not cover every accepted evidence claim")
    return {
        "receipt_sha256": stored_receipt_hash,
        "rows": receipt["row_count"],
        "claims": receipt["claim_count"],
        "source_attestation": receipt.get("source_attestation"),
    }
