# Offline Circuit Research Protocol 1.0

By Shafaet Brady Hussain. MIT licensed. Protocol identifier: **ORP-001**.

This is a public, provider-neutral subset of the author's local validation and
analysis research. It verifies deterministic bit mapping, small exact statevector
simulation, an analytically specified probability distribution, duplicate
circuits and a frozen-manifest integrity boundary. All inputs and output
fixtures in this directory were newly created for this release and are local
and synthetic. No account, API key, paid service or research device is needed.

## Reproduce

With Python 3.10 or later, run from this directory:

```console
python verify_release.py
python protocol.py
python -m unittest -v test_protocol
```

Expected: integrity PASS, ten local exact circuits PASS, 17 tests PASS, zero
external jobs. These checks are software/fixture evidence, not device or
real-world performance measurements. To intentionally regenerate the same local
manifest and fixtures, run `python protocol.py --write`; review any differences.

## What is included

- `reference.py`: explicitly selected, author-owned offline helpers for H, X,
  controlled-X and RZ gates, distribution comparison, bounded normalization,
  integer-count reconstruction and Wilson intervals.
- `protocol.py` and `manifest.json`: a newly frozen four-qubit protocol with
  ten circuits, little-endian integer bit mapping, independently specified
  expected probabilities, two duplicate pairs and a canonical manifest hash.
- `local_results.json` and `local_analysis.json`: newly computed local exact
  fixtures, clearly labeled LOCAL_EXACT_ONLY.
- `test_protocol.py`: analytic checks, mutation and malformed-data checks,
  resource limits and a run with network sockets disabled.
- `PROVENANCE.json`, `SHA256SUMS.txt` and `verify_release.py`: source-extraction
  provenance and a release-only explicit integrity allowlist.

The reference simulator is bounded to 1-12 qubits and 4,096 operations. The
protocol validates the specific published four-qubit manifest, rather than
accepting arbitrary jobs. Exact local distributions are compared with tolerance
1e-12; normalization refuses larger mass deviations. Wilson and count utilities
have synthetic unit checks and do not imply any external sampling experiment.

## Interpretation and rights

The release establishes only that these local software checks reproduce for
the specified circuits and synthetic data. It does not establish hardware
behavior, quantum advantage, physical fidelity, biological mechanism, medical
utility, better model reasoning, stronger encryption, product readiness or
commercial value. Earlier private-study manuscripts, service outputs,
identifiers, original research PDFs, private source, user data, screenshots,
accounts and credentials are excluded.

Read LICENSE, NOTICE, AUTHORS.md, AI_ASSISTANCE.md, CONFLICTS_AND_FUNDING.md,
SECURITY.md and DEPENDENCIES_AND_LICENSES.md. The parent repository's separate
research licenses and third-party notices remain in effect. No unrelated data
or application is relicensed by this package.
