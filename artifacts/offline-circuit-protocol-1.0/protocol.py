"""ORP-001: a new, entirely local synthetic circuit verification protocol.

SPDX-License-Identifier: MIT
Copyright (c) 2026 Shafaet Brady Hussain
"""
import argparse
import json
from pathlib import Path

from reference import canonical_sha256, expected_distribution, normalize_result, simulate, total_variation

HERE = Path(__file__).resolve().parent
PROTOCOL_ID = "ORP-001"


def build_manifest():
    h = lambda target: {"gate": "h", "target": target}
    x = lambda target: {"gate": "x", "target": target}
    cx = lambda control, target: {"gate": "x", "control": control, "target": target}
    definitions = [
        ("zero_uncompute", [h(2), h(2)], {"0": "1"}),
        ("least_significant_bit", [x(0)], {"1": "1"}),
        ("most_significant_bit", [x(3)], {"8": "1"}),
        ("pair_uncompute", [h(0), cx(0, 1), cx(0, 1), h(0)], {"0": "1"}),
        ("uniform_forward", [h(i) for i in range(4)], {str(i): "1/16" for i in range(16)}),
        ("uniform_reverse", [h(i) for i in reversed(range(4))], {str(i): "1/16" for i in range(16)}),
        ("interference_zero", [h(0), {"gate": "rz", "target": 0, "rotation": 0.0}, h(0)], {"0": "1"}),
        ("interference_one", [h(0), {"gate": "rz", "target": 0, "rotation": 3.141592653589793}, h(0)], {"1": "1"}),
        ("duplicate_uniform", [h(i) for i in range(4)], {str(i): "1/16" for i in range(16)}),
        ("duplicate_interference", [h(0), {"gate": "rz", "target": 0, "rotation": 3.141592653589793}, h(0)], {"1": "1"}),
    ]
    circuits = []
    for order, (name, gates, probabilities) in enumerate(definitions, 1):
        circuits.append({"order": order, "name": name, "qubits": 4, "circuit": gates,
                         "circuit_sha256": canonical_sha256(gates),
                         "expected": {"type": "explicit_distribution", "probabilities": probabilities}})
    manifest = {"schema": "offline-research-protocol.v1", "protocol_id": PROTOCOL_ID,
                "version": "1.0.0", "execution": "LOCAL_EXACT_ONLY",
                "synthetic_inputs_only": True, "external_execution_available": False,
                "state_convention": "logical qubit i is integer bit 2**i",
                "circuits": circuits}
    manifest["manifest_sha256"] = canonical_sha256(manifest)
    return manifest


def validate_manifest(manifest):
    # This is a frozen reference protocol, rather than a generic job runner.
    if canonical_sha256(manifest) != canonical_sha256(build_manifest()):
        raise ValueError("manifest differs from the frozen ORP-001 reference protocol")
    for entry in manifest["circuits"]:
        actual = simulate(entry["circuit"], entry["qubits"])
        if total_variation(actual, expected_distribution(entry)) > 1e-12:
            raise ValueError("reference distribution does not match its independent specification")
    return manifest


def generate_results(manifest):
    validate_manifest(manifest)
    return {entry["name"]: {str(state): probability for state, probability in
            simulate(entry["circuit"], entry["qubits"]).items()} for entry in manifest["circuits"]}


def analyze_results(manifest, results):
    validate_manifest(manifest)
    if not isinstance(results, dict) or set(results) != {entry["name"] for entry in manifest["circuits"]}:
        raise ValueError("result names must map one-to-one to all reference circuits")
    rows = []
    for entry in manifest["circuits"]:
        raw = results[entry["name"]]
        if not isinstance(raw, dict) or any(not isinstance(key, str) or not key.isascii() or not key.isdecimal() or str(int(key)) != key for key in raw):
            raise ValueError("state keys must be canonical nonnegative decimal integer strings")
        if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in raw.values()):
            raise ValueError("probabilities must be numeric, excluding booleans")
        distribution = normalize_result(raw, entry["name"], 1e-12)
        if any(state >= 2 ** entry["qubits"] for state in distribution):
            raise ValueError("result state lies outside the declared circuit width")
        tv = total_variation(distribution, expected_distribution(entry))
        rows.append({"name": entry["name"], "total_variation": tv, "passed": tv <= 1e-12})
    return {"schema": "offline-research-analysis.v1", "protocol_id": PROTOCOL_ID,
            "manifest_sha256": manifest["manifest_sha256"], "execution": "LOCAL_EXACT_ONLY",
            "external_jobs": 0, "network_calls": 0,
            "status": "PASS" if all(row["passed"] for row in rows) else "FAIL", "circuits": rows,
            "boundary": "Local synthetic software checks only; no device, biological, clinical, security-strength or product-quality finding."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write regenerated local synthetic fixtures")
    args = parser.parse_args()
    manifest = build_manifest()
    results = generate_results(manifest)
    report = analyze_results(manifest, results)
    if args.write:
        for name, value in (("manifest.json", manifest), ("local_results.json", results), ("local_analysis.json", report)):
            (HERE / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    else:
        for name, value in (("manifest.json", manifest), ("local_results.json", results), ("local_analysis.json", report)):
            if json.loads((HERE / name).read_text(encoding="utf-8")) != value:
                raise ValueError(f"published local fixture differs: {name}")
    print(json.dumps({"status": report["status"], "circuits": len(report["circuits"]),
                      "execution": report["execution"], "external_jobs": 0}, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
