# ZME1 1.0 reproducibility companion

This package publishes structure, bounds, hashes, and negative vectors without publishing private ZMath key-management or policy-service code.

Run `python verify_structure.py`. Four of four expectations must match; the three negative vectors must be rejected. The verifier does not decrypt and is not an independent cryptographic implementation or certification.
