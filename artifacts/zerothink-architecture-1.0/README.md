# ZeroThink 1.0 executable conformance companion

This package encodes a deliberately narrow subset of the architecture's release invariants. It is a reproducibility aid, not a security certification or correctness proof.

Run with Python 3 and no external dependencies:

```console
python verify_conformance.py
```

Expected result: all six test-vector expectations match. The negative vectors must be rejected. `trace.schema.json` documents the record shape; the verifier supplies the cross-field and transition rules that JSON Schema alone does not express.
