# ZBA 1.0 reference artifacts

This directory accompanies the public preprint *Zero Boundary Algebra 1.0*.

- `zba.schema.json` defines the minimum evidence-record shape.
- Phase tags are strings. They are never serialized as JSON `-0`, `0`, or `+0` numbers.
- The schema validates structure only. Cryptographic verification, policy evaluation, canonicalization, and trust-anchor handling require a conforming verifier.

The artifacts are released under the MIT License. They contain no private ZMath code, secrets, customer data, or live-system details.
