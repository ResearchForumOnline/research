"""Local circuit primitives extracted from the author's offline research code.

SPDX-License-Identifier: MIT
Copyright (c) 2026 Shafaet Brady Hussain
No networking, account integration or external execution path is present.
"""
from __future__ import annotations
import cmath
from fractions import Fraction
import hashlib
import json
import math
from typing import Any

ALLOWED_GATES = {"h", "x", "rz"}

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def parse_rational(value: str | int | float) -> float:
    if isinstance(value, str) and "/" in value:
        return float(Fraction(value))
    return float(value)


def expected_distribution(entry: dict[str, Any]) -> dict[int, float]:
    expected = entry["expected"]
    if expected["type"] in {"point_mass", "explicit_distribution"}:
        return {int(key): parse_rational(value) for key, value in expected["probabilities"].items()}
    if expected["type"] == "uniform_integer_range":
        low = int(expected["minimum_state"])
        high = int(expected["maximum_state"])
        probability = parse_rational(expected["probability_each"])
        return {state: probability for state in range(low, high + 1)}
    raise ValueError(f"unsupported expected distribution type: {expected['type']}")


def _apply_single(state: list[complex], operation: dict[str, Any]) -> None:
    target = int(operation["target"])
    stride = 1 << target
    for base in range(0, len(state), stride * 2):
        for offset in range(stride):
            left = base + offset
            right = left + stride
            a, b = state[left], state[right]
            gate = operation["gate"]
            if gate == "h":
                state[left] = (a + b) / math.sqrt(2.0)
                state[right] = (a - b) / math.sqrt(2.0)
            elif gate == "x":
                state[left], state[right] = b, a
            elif gate == "rz":
                rotation = float(operation["rotation"])
                state[left] = a * cmath.exp(-0.5j * rotation)
                state[right] = b * cmath.exp(0.5j * rotation)
            else:
                raise ValueError(f"unsupported single-qubit gate: {gate}")


def _apply_controlled_x(state: list[complex], operation: dict[str, Any]) -> None:
    control = int(operation["control"])
    target = int(operation["target"])
    if control == target:
        raise ValueError("control and target must differ")
    for index in range(len(state)):
        if ((index >> control) & 1) and not ((index >> target) & 1):
            partner = index | (1 << target)
            state[index], state[partner] = state[partner], state[index]


def simulate(circuit: list[dict[str, Any]], qubits: int) -> dict[int, float]:
    if type(qubits) is not int or not 1 <= qubits <= 12:
        raise ValueError("local reference supports 1 to 12 integer qubits")
    if not isinstance(circuit, list) or len(circuit) > 4096:
        raise ValueError("circuit must be a list with at most 4096 operations")
    state = [0j] * (1 << qubits)
    state[0] = 1.0 + 0j
    for operation in circuit:
        if not isinstance(operation, dict) or type(operation.get("target")) is not int:
            raise ValueError("gate target must be an integer")
        if operation.get("gate") == "rz" and (isinstance(operation.get("rotation"), bool) or not isinstance(operation.get("rotation"), (int, float)) or not math.isfinite(operation["rotation"])):
            raise ValueError("rotation must be a finite number")
        if operation["gate"] not in ALLOWED_GATES:
            raise ValueError(f"unsupported gate: {operation['gate']}")
        target = int(operation["target"])
        if not 0 <= target < qubits:
            raise ValueError(f"target outside width: {operation}")
        if "control" in operation:
            if type(operation["control"]) is not int:
                raise ValueError("gate control must be an integer")
            if operation["gate"] != "x":
                raise ValueError("only controlled-x is supported")
            control = int(operation["control"])
            if not 0 <= control < qubits:
                raise ValueError(f"control outside width: {operation}")
            _apply_controlled_x(state, operation)
        else:
            _apply_single(state, operation)
    probabilities = {index: abs(amplitude) ** 2 for index, amplitude in enumerate(state) if abs(amplitude) ** 2 > 1e-14}
    total = math.fsum(probabilities.values())
    if abs(total - 1.0) > 1e-12:
        raise ValueError(f"local probability mass is {total:.15f}")
    return {state_id: probability / total for state_id, probability in probabilities.items()}


def total_variation(left: dict[int, float], right: dict[int, float]) -> float:
    return 0.5 * math.fsum(abs(left.get(key, 0.0) - right.get(key, 0.0)) for key in set(left) | set(right))


def normalize_result(raw: dict[str, Any], label: str, tolerance: float) -> dict[int, float]:
    if not math.isfinite(tolerance) or not 0 <= tolerance < 1:
        raise ValueError("mass tolerance must be finite and below one")
    if not isinstance(raw, dict) or not raw:
        raise ValueError(f"{label}: result must be a non-empty object")
    parsed: dict[int, float] = {}
    for key, value in raw.items():
        state = int(key)
        probability = float(value)
        if state < 0 or not math.isfinite(probability) or not 0 <= probability <= 1:
            raise ValueError(f"{label}: invalid probability {key}={value}")
        if state in parsed:
            raise ValueError(f"{label}: duplicate integer state {state}")
        parsed[state] = probability
    total = math.fsum(parsed.values())
    if total <= 0 or abs(total - 1.0) > tolerance:
        raise ValueError(f"{label}: probability mass {total:.15f} outside tolerance")
    return {state: probability / total for state, probability in parsed.items()}


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if not 0 <= successes <= trials or trials <= 0:
        raise ValueError("invalid binomial counts")
    p = successes / trials
    denominator = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denominator
    half = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denominator
    return max(0.0, centre - half), min(1.0, centre + half)


def reconstructed_counts(distribution: dict[int, float], shots: int, tolerance: float) -> dict[int, int]:
    counts: dict[int, int] = {}
    for state, probability in distribution.items():
        expected = probability * shots
        rounded = round(expected)
        if abs(expected - rounded) > tolerance:
            raise ValueError(f"state {state}: probability is not consistent with {shots} shots")
        counts[state] = int(rounded)
    if sum(counts.values()) != shots:
        raise ValueError("reconstructed counts do not sum to shots")
    return counts
