"""Exhaustive finite-domain and mutation checks for the ZBA 1.1 reference profile."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
from pathlib import Path

from zba_reference import EVIDENCE, PHASES, POLARITIES, SPEC, State, seal, verify_chain

HERE = Path(__file__).resolve().parent


def make_chain():
    payload = hashlib.sha256(b"public-zba-test-payload").hexdigest()
    common = dict(spec=SPEC, asset_id="urn:zba:test:asset-001",
                  recursion_depth=0, policy_id="zba-reference",
                  policy_version="1.1.0", payload_commitment=payload,
                  commitment_algorithm="sha-256")
    rows = []
    definitions = [
        ("create.enter", "positive", "entering", "claimed"),
        ("create.seal", "neutral", "boundary", "checked"),
        ("create.emerge", "positive", "emerging", "sealed"),
        ("verify.enter", "positive", "entering", "sealed"),
        ("verify.seal", "neutral", "boundary", "sealed"),
        ("verify.emerge", "positive", "emerging", "sealed"),
    ]
    previous = None
    for sequence, (operation, polarity, phase, evidence_status) in enumerate(definitions):
        row = dict(common, sequence=sequence, operation=operation,
                   polarity=polarity, phase=phase,
                   evidence_status=evidence_status,
                   previous_commitment=previous)
        if sequence >= 3: row["recursion_depth"] = 1
        row = seal(row); rows.append(row); previous = row["commitment"]
    return rows


def main():
    states = [State(p, b, r, e) for p, b, r, e in
              itertools.product(POLARITIES, PHASES, range(4), EVIDENCE)]
    properties = {
        "state_count": len(states),
        "mirror_involution_pass": sum(s.mirror().mirror() == s for s in states),
        "reset_idempotence_pass": sum(s.reset().reset() == s.reset() for s in states),
        "mirror_reset_commutation_pass": sum(s.reset().mirror() == s.mirror().reset() for s in states),
    }
    chain = make_chain()
    positive = verify_chain(chain)
    mutations = {
        "phase": (2, "phase", "boundary"),
        "polarity": (2, "polarity", "negative"),
        "operation": (2, "operation", "tampered.operation"),
        "policy_version": (2, "policy_version", "9.9.9"),
        "previous_commitment": (2, "previous_commitment", "00" * 32),
        "payload_commitment": (2, "payload_commitment", "11" * 32),
        "recursion_depth": (2, "recursion_depth", 99),
        "evidence_status": (2, "evidence_status", "rejected"),
        "asset_id": (2, "asset_id", "urn:zba:test:other"),
        "sequence": (2, "sequence", 9),
        "commitment": (2, "commitment", "22" * 32),
    }
    mutation_results = {}
    for name, (index, field, value) in mutations.items():
        altered = copy.deepcopy(chain); altered[index][field] = value
        mutation_results[name] = verify_chain(altered)
    deleted = chain[:2] + chain[3:]
    reordered = chain[:1] + [chain[2], chain[1]] + chain[3:]
    mutation_results["deletion"] = verify_chain(deleted)
    mutation_results["reordering"] = verify_chain(reordered)
    mutation_results["duplication"] = verify_chain(chain[:3] + [chain[2]] + chain[3:])
    results = {
        "spec": SPEC,
        "properties": properties,
        "positive_chain": positive,
        "mutation_count": len(mutation_results),
        "mutations_detected": sum(not value["valid"] for value in mutation_results.values()),
        "mutation_results": mutation_results,
    }
    (HERE / "test-vectors.json").write_text(json.dumps({"valid_chain": chain}, indent=2) + "\n", encoding="utf-8")
    (HERE / "property-check-results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    assert positive["valid"]
    assert properties["mirror_involution_pass"] == len(states)
    assert properties["reset_idempotence_pass"] == len(states)
    assert properties["mirror_reset_commutation_pass"] == len(states)
    assert results["mutations_detected"] == results["mutation_count"]
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
