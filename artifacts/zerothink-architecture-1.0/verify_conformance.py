#!/usr/bin/env python3
"""Dependency-free verifier for the ZeroThink 1.0 release invariants."""
import json
import sys
from pathlib import Path

ORDER = {name: i for i, name in enumerate(["RECEIVED", "PREFLIGHT", "EVIDENCE", "CANDIDATES", "VERIFY", "ROUTE"])}
TERMINALS = {"RELEASED": "release", "ABSTAINED": "abstain", "DENIED": "deny"}

def check(trace):
    errors = []
    required = {"trace_id", "states", "permissions", "evidence_gate", "findings", "release"}
    missing = sorted(required - set(trace))
    if missing:
        return ["missing fields: " + ", ".join(missing)]
    states = trace["states"]
    if not states or states[0] != "RECEIVED" or states[-1] not in TERMINALS:
        errors.append("trace must start RECEIVED and end in a terminal state")
    ranked = [ORDER[s] for s in states if s in ORDER]
    if ranked != sorted(ranked) or len(states) != len(set(states)):
        errors.append("states must be unique and follow declared order")
    decision = trace["release"].get("decision")
    if states and states[-1] in TERMINALS and TERMINALS[states[-1]] != decision:
        errors.append("terminal state and decision disagree")
    if decision == "release":
        if trace["release"].get("authority") != "release_guard":
            errors.append("only release_guard may release")
        if not trace["evidence_gate"].get("completed") or "EVIDENCE" not in states:
            errors.append("release requires completed evidence gate")
        if not trace["permissions"].get("granted"):
            errors.append("release requires permission")
        if any(f.get("severity") == "hard_failure" for f in trace["findings"]):
            errors.append("hard failure blocks release")
    if trace["permissions"].get("source") == "untrusted_content" and trace["permissions"].get("granted"):
        errors.append("untrusted content cannot grant permission")
    return errors

def main(path):
    vectors = json.loads(Path(path).read_text(encoding="utf-8"))
    unexpected = 0
    for vector in vectors:
        errors = check(vector["trace"])
        observed = "PASS" if not errors else "FAIL"
        ok = observed == vector["expected"]
        unexpected += not ok
        detail = "ok" if not errors else "; ".join(errors)
        print(f"{vector['name']}: expected={vector['expected']} observed={observed} [{detail}]")
    print(f"summary: {len(vectors) - unexpected}/{len(vectors)} expectations matched")
    return unexpected != 0

if __name__ == "__main__":
    default = Path(__file__).with_name("test-vectors.json")
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else default))
