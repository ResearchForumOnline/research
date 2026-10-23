"""Independent synthetic checks for ORP-001; SPDX-License-Identifier: MIT.
Copyright (c) 2026 Shafaet Brady Hussain
"""
import copy
import math
import unittest
from unittest.mock import patch

from protocol import analyze_results, build_manifest, generate_results, validate_manifest
from reference import canonical_sha256, normalize_result, reconstructed_counts, simulate, total_variation, wilson_interval


class OfflineProtocolTests(unittest.TestCase):
    def setUp(self):
        self.manifest = build_manifest()
        self.results = generate_results(self.manifest)

    def test_all_ten_local_circuits_match_specification(self):
        report = analyze_results(self.manifest, self.results)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(report["circuits"]), 10)
        self.assertEqual(report["external_jobs"], 0)

    def test_qubit_order_uses_integer_bits(self):
        self.assertEqual(self.results["least_significant_bit"], {"1": 1.0})
        self.assertEqual(self.results["most_significant_bit"], {"8": 1.0})

    def test_bell_state_reference(self):
        result = simulate([{"gate": "h", "target": 0}, {"gate": "x", "control": 0, "target": 1}], 2)
        self.assertEqual(set(result), {0, 3})
        self.assertAlmostEqual(result[0], 0.5)
        self.assertAlmostEqual(result[3], 0.5)

    def test_analytical_uniform_and_reversed_order(self):
        expected = {str(state): 1 / 16 for state in range(16)}
        self.assertEqual(self.results["uniform_forward"], expected)
        self.assertEqual(self.results["uniform_reverse"], expected)

    def test_duplicate_circuit_hashes_agree(self):
        circuits = self.manifest["circuits"]
        self.assertEqual(circuits[4]["circuit_sha256"], circuits[8]["circuit_sha256"])
        self.assertEqual(circuits[7]["circuit_sha256"], circuits[9]["circuit_sha256"])

    def test_gate_tampering_is_rejected(self):
        self.manifest["circuits"][0]["circuit"][0]["target"] = 1
        with self.assertRaisesRegex(ValueError, "frozen"):
            validate_manifest(self.manifest)

    def test_manifest_hash_tampering_is_rejected(self):
        self.manifest["manifest_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            validate_manifest(self.manifest)

    def test_missing_or_extra_result_names_rejected(self):
        for operation in (lambda result: result.pop("interference_zero"), lambda result: result.update({"unknown": {"0": 1}})):
            result = copy.deepcopy(self.results)
            operation(result)
            with self.assertRaisesRegex(ValueError, "one-to-one"):
                analyze_results(self.manifest, result)

    def test_wrong_normalized_result_fails_scientific_check(self):
        self.results["least_significant_bit"] = {"0": 1.0}
        self.assertEqual(analyze_results(self.manifest, self.results)["status"], "FAIL")

    def test_out_of_width_and_noncanonical_state_rejected(self):
        for key in ("16", "01", "-1", "1.0", "\u0661"):
            self.results["least_significant_bit"] = {key: 1.0}
            with self.assertRaises(ValueError):
                analyze_results(self.manifest, self.results)

    def test_invalid_probability_values_rejected(self):
        for value in (math.nan, math.inf, -0.1, 1.1, True, "1"):
            self.results["least_significant_bit"] = {"1": value}
            with self.assertRaises(ValueError):
                analyze_results(self.manifest, self.results)

    def test_zero_or_incorrect_mass_rejected(self):
        for value in (0.0, 0.7):
            self.results["least_significant_bit"] = {"1": value}
            with self.assertRaises(ValueError):
                analyze_results(self.manifest, self.results)

    def test_local_resource_limits(self):
        for width in (-1, 0, 13, True, 2.5):
            with self.assertRaises(ValueError):
                simulate([], width)
        with self.assertRaises(ValueError):
            simulate([{"gate": "x", "target": 0}] * 4097, 1)

    def test_invalid_gate_target_control_and_rotation(self):
        operations = [{"gate": "unknown", "target": 0}, {"gate": "x", "target": 2},
                      {"gate": "x", "target": True}, {"gate": "x", "target": 0, "control": 0},
                      {"gate": "x", "target": 0, "control": True},
                      {"gate": "rz", "target": 0, "rotation": math.nan}]
        for operation in operations:
            with self.assertRaises(ValueError):
                simulate([operation], 2)

    def test_counts_and_binomial_interval_are_bounded(self):
        self.assertEqual(reconstructed_counts({0: 0.25, 1: 0.75}, 100, 1e-9), {0: 25, 1: 75})
        low, high = wilson_interval(50, 100)
        self.assertTrue(0 < low < 0.5 < high < 1)
        with self.assertRaises(ValueError):
            reconstructed_counts({0: 0.333, 1: 0.667}, 100, 1e-9)

    def test_small_serialization_error_normalizes_only_within_bound(self):
        self.assertEqual(normalize_result({"0": 0.4999999999999, "1": 0.4999999999999}, "synthetic", 1e-12), {0: 0.5, 1: 0.5})
        with self.assertRaises(ValueError):
            normalize_result({"0": 0.998}, "synthetic", 1e-12)

    def test_offline_protocol_runs_with_networking_disabled(self):
        with patch("socket.socket", side_effect=AssertionError("network prohibited")):
            report = analyze_results(self.manifest, generate_results(self.manifest))
        self.assertEqual(report["network_calls"], 0)
        self.assertEqual(report["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
