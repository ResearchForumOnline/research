# Zero Boundary Algebra 1.1 reference profile

The reference profile turns the paper's structural claims into executable checks.

Run with Python 3.11 or later:

```bash
python property_check.py
```

Expected public results:

- 144 finite-domain states checked;
- 144/144 mirror-involution checks pass;
- 144/144 reset-idempotence checks pass;
- 144/144 structural mirror/reset commutation checks pass;
- one six-record valid chain accepted;
- 14/14 seeded mutations, deletions, reorderings, and duplications rejected.

This is a research verifier, not production cryptographic software. It deliberately excludes signatures, key custody, AEAD, trusted timestamps, external witness validation, and endpoint security.
