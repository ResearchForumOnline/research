"""Independent finite checks for the proposed ZBA validator-reset extension.

Python 3.10+, standard library only. This is a finite verification companion,
not a proof for arbitrary finite sets and not a replacement for ZBA 1.1.
Run: python verify_reset_algebra.py [--output results.json]
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


def compose(f, g):
    """f after g, represented as full lookup tables."""
    return tuple(f[g[x]] for x in range(len(f)))


def closure(*generators):
    known = set(generators)
    pending = list(known)
    while pending:
        f = pending.pop()
        for g in tuple(known):
            for h in (compose(f, g), compose(g, f)):
                if h not in known:
                    known.add(h)
                    pending.append(h)
    return known


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def predicted_size(v, mirror, anchors=(0, 1)):
    a0, a1 = anchors
    invariant = all(v[mirror[x]] == v[x] for x in range(len(v)))
    g = (v[a0], v[a1])
    if g == (0, 1):
        return 3 if invariant else 4
    if g == (1, 0):
        return 4 if invariant else 6
    b = g[0]
    return 3 if all(y == b for y in v) else 4 if invariant else 5


def inspect(v, mirror, anchors=(0, 1)):
    identity = tuple(range(len(v)))
    reset = tuple(anchors[y] for y in v)
    actual = closure(identity, mirror, reset)
    expected = predicted_size(v, mirror, anchors)
    require(len(actual) == expected, ("monoid size", v, len(actual), expected))
    idempotent = compose(reset, reset) == reset
    stable = all(v[reset[x]] == v[x] for x in range(len(v)))
    require(idempotent == stable, ("idempotence", v))
    commuting = compose(reset, mirror) == compose(mirror, reset)
    invariant = all(v[mirror[x]] == v[x] for x in range(len(v)))
    require(commuting == invariant, ("commutation", v))
    return len(actual), idempotent, commuting


def counts(n, orbit_count):
    h, j = 2 ** (n - 2), 2 ** (orbit_count - 2)
    return {3: j + 2, 4: h + 2 * j - 2, 5: 2 * (h - j), 6: h - j}


def finite_case(n):
    mirror = list(range(n))
    pairs = [(2, 3)] + ([(4, 5)] if n >= 6 else [])
    for x, y in pairs:
        mirror[x], mirror[y] = y, x
    mirror = tuple(mirror)
    orbit_count = n - len(pairs)
    observed = {3: 0, 4: 0, 5: 0, 6: 0}
    vectors = list(itertools.product((0, 1), repeat=n))
    # Independently enumerate admissible validators; do not generate them
    # from the proposed synthesis formula.
    admissible = [w for w in vectors if w[0] == 0 and w[1] == 1
                  and all(w[x] == w[mirror[x]] for x in range(n))]
    synthesis_cases = 0
    for v in vectors:
        size, _, _ = inspect(v, mirror)
        observed[size] += 1
        if v[1] == 1:
            synthesized = tuple(0 if x == 0 else v[x] & v[mirror[x]]
                                for x in range(n))
            feasible = [w for w in admissible
                        if all(w[x] <= v[x] for x in range(n))]
            require(synthesized in feasible, ("synthesis feasible", v))
            require(all(all(w[x] <= synthesized[x] for x in range(n))
                        for w in feasible), ("synthesis greatest", v))
            synthesis_cases += 1
    expected = counts(n, orbit_count)
    require(observed == expected, ("distribution", n, observed, expected))
    require(sum(expected.values()) == 2 ** n, "partition count")
    return {"states": n, "mirror": mirror, "mirror_orbits": orbit_count,
            "validators_exhaustively_checked": len(vectors),
            "monoid_sizes_observed": observed, "monoid_sizes_predicted": expected,
            "synthesis_inputs_exhaustively_checked": synthesis_cases,
            "candidate_synthesis_validators_enumerated": len(admissible)}


def fiber_case():
    states = list(itertools.product((-1, 0, 1), (-1, 0, 1), range(4)))
    index = {s: i for i, s in enumerate(states)}
    mirror = tuple(index[(-p, b, e)] for p, b, e in states)
    anchors = (index[(0, 0, 0)], index[(0, 0, 1)])
    validators = {
        "size_3_idempotent_commuting": tuple(int(e == 1) for p, b, e in states),
        "size_4_idempotent_noncommuting": tuple(int(e == 1 or p == 1) for p, b, e in states),
        "size_5_constant_anchor_noncommuting": tuple(int(p == 1) for p, b, e in states),
        "size_6_anchor_swap_noncommuting": tuple(int(e == 0 or p == 1) for p, b, e in states),
    }
    examples = {}
    for name, v in validators.items():
        size, idem, commutes = inspect(v, mirror, anchors)
        examples[name] = {"validator": v, "monoid_size": size,
                          "idempotent": idem, "commuting": commutes}
    require({e["monoid_size"] for e in examples.values()} == {3, 4, 5, 6}, "all sizes")
    v = tuple(int(p != -1 and e != 0) for p, b, e in states)
    size, idem, commutes = inspect(v, mirror, anchors)
    require(idem and not commutes, "counterexample")
    reset = tuple(anchors[y] for y in v)
    witness = next(x for x in range(36) if compose(reset, mirror)[x] != compose(mirror, reset)[x])
    predicted = counts(36, 24)
    require(sum(predicted.values()) == 2 ** 36, "36-state count partition")
    return {"states": 36, "coordinates": {"polarity": [-1, 0, 1],
            "boundary": [-1, 0, 1], "evidence": [0, 1, 2, 3]},
            "anchors": [states[a] for a in anchors], "mirror_orbits": 24,
            "distribution_method": "symbolic count formula only; NOT exhaustive over 2^36 validators",
            "predicted_distribution": predicted, "total_validators": 2 ** 36,
            "deterministic_fixtures": examples,
            "counterexample": {"validator_rule": "polarity != -1 and evidence != 0",
              "idempotent": idem, "commuting": commutes, "monoid_size": size,
              "input": states[witness],
              "reset_after_mirror": states[compose(reset, mirror)[witness]],
              "mirror_after_reset": states[compose(mirror, reset)[witness]]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = parser.parse_args()
    results = {"status": "passed", "scope": "finite evidence, not a general proof",
               "exhaustive_small_cases": [finite_case(n) for n in range(4, 9)],
               "zba_fiber": fiber_case()}
    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "exhaustive_validator_cases": sum(
        c["validators_exhaustively_checked"] for c in results["exhaustive_small_cases"]),
        "synthesis_cases": sum(c["synthesis_inputs_exhaustively_checked"]
                               for c in results["exhaustive_small_cases"]),
        "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
