"""Executable reference profile for Zero Boundary Algebra 1.1.

This is a research verifier, not production cryptographic software. It uses the
restricted JSON profile defined by the paper and SHA-256 commitments. Signature,
AEAD, trust-store, and external-witness verification are intentionally separate.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from typing import Any, Iterable

SPEC = "zba-evidence/1.1"
DOMAIN = b"ZBA-EVENT-COMMITMENT-V1.1\x00"
PHASES = ("entering", "boundary", "emerging")
POLARITIES = ("positive", "neutral", "negative")
EVIDENCE = ("claimed", "checked", "sealed", "rejected")
CRITICAL = (
    "spec", "asset_id", "sequence", "operation", "polarity", "phase",
    "recursion_depth", "policy_id", "policy_version",
    "previous_commitment", "payload_commitment", "evidence_status",
    "commitment_algorithm",
)


def canonical_bytes(value: Any) -> bytes:
    """Canonical bytes for the restricted JSON data model used in the vectors."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def committed_projection(record: dict[str, Any]) -> dict[str, Any]:
    return {key: record[key] for key in CRITICAL}


def compute_commitment(record: dict[str, Any]) -> str:
    previous = record.get("previous_commitment")
    previous_bytes = bytes(32) if previous is None else bytes.fromhex(previous)
    return hashlib.sha256(DOMAIN + previous_bytes +
                          canonical_bytes(committed_projection(record))).hexdigest()


@dataclass(frozen=True)
class State:
    polarity: str
    phase: str
    recursion_depth: int
    evidence_status: str

    def mirror(self) -> "State":
        opposite = {"positive": "negative", "negative": "positive", "neutral": "neutral"}
        return replace(self, polarity=opposite[self.polarity])

    def reset(self) -> "State":
        status = "rejected" if self.evidence_status == "rejected" else "checked"
        return replace(self, polarity="neutral", phase="boundary", evidence_status=status)


def validate_shape(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = [key for key in (*CRITICAL, "commitment") if key not in record]
    if missing:
        return ["missing:" + ",".join(missing)]
    if record["spec"] != SPEC: errors.append("unsupported_spec")
    if record["phase"] not in PHASES: errors.append("invalid_phase")
    if record["polarity"] not in POLARITIES: errors.append("invalid_polarity")
    if record["evidence_status"] not in EVIDENCE: errors.append("invalid_evidence_status")
    if record["commitment_algorithm"] != "sha-256": errors.append("unsupported_commitment_algorithm")
    if not isinstance(record["sequence"], int) or isinstance(record["sequence"], bool) or record["sequence"] < 0:
        errors.append("invalid_sequence")
    depth = record["recursion_depth"]
    if not isinstance(depth, int) or isinstance(depth, bool) or not 0 <= depth <= 4294967295:
        errors.append("invalid_recursion_depth")
    for field in ("payload_commitment", "commitment"):
        try:
            if len(bytes.fromhex(record[field])) != 32: errors.append("invalid_" + field)
        except (TypeError, ValueError): errors.append("invalid_" + field)
    previous = record["previous_commitment"]
    if previous is not None:
        try:
            if len(bytes.fromhex(previous)) != 32: errors.append("invalid_previous_commitment")
        except (TypeError, ValueError): errors.append("invalid_previous_commitment")
    return errors


def transition_errors(previous: dict[str, Any] | None, current: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if previous is None:
        if current["sequence"] != 0: errors.append("genesis_sequence_not_zero")
        if current["previous_commitment"] is not None: errors.append("genesis_has_predecessor")
        return errors
    if current["asset_id"] != previous["asset_id"]: errors.append("asset_changed")
    if current["sequence"] != previous["sequence"] + 1: errors.append("sequence_discontinuity")
    if current["previous_commitment"] != previous["commitment"]: errors.append("predecessor_mismatch")
    allowed = {"emerging": "entering", "entering": "boundary", "boundary": "emerging"}
    if current["phase"] != allowed[previous["phase"]]: errors.append("phase_order_violation")
    if previous["evidence_status"] == "rejected" and current["operation"] != "recover":
        errors.append("rejected_without_recovery")
    return errors


def verify_chain(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    checked = 0
    previous = None
    for record in records:
        errors = validate_shape(record)
        if not errors and record["commitment"] != compute_commitment(record):
            errors.append("commitment_mismatch")
        if not errors: errors.extend(transition_errors(previous, record))
        if errors:
            return {"valid": False, "records_checked": checked,
                    "failed_sequence": record.get("sequence"), "errors": errors}
        previous = record
        checked += 1
    return {"valid": True, "records_checked": checked,
            "failed_sequence": None, "errors": []}


def seal(record: dict[str, Any]) -> dict[str, Any]:
    result = dict(record)
    result["commitment"] = compute_commitment(result)
    return result
