# ZMath ecosystem encryption-profile audit

Date: 18 August 2026
Scope: reviewed local source snapshots and targeted regression tests
Conclusion: nine identifiable protection profiles/integrations, including at least seven author-created constructions, formats, or application integrations around established primitives.

## Evidence classes

| Profile | Reviewed evidence | Test status |
| --- | --- | --- |
| ZME1 Portable / Exclusive | `zmath-core.js` derivation, metadata AAD, AES-GCM container paths | Local-processing and separate-factor contract passed |
| ZMath Shield `.zmath` | Zmail Shield implementation and tests | 6/6 targeted tests passed |
| CallChat ZShield/ZSHIELD1 | `zshield-core.js` and its vector suite | Round-trip, factor, tamper, and resource tests passed |
| Zmail protected mail | `zmath-mail-crypto.js` and Roundcube integration tests | 6/6 targeted tests passed |
| ZNotes encrypted store | Connector documentation and store integration | Classified as service-readable encrypted-at-rest storage |
| ZeroThink `.ztz` / Z-Pepper | Parser, KDF, HMAC stream, MAC, and digest verification paths in `zmath-core.js` | Decryption implementation reviewed; custom construction flagged for independent review |
| Matrix Olm/Megolm | Matrix client integration and Matrix specification | Third-party E2EE integration; not an author-created cipher |
| Local auto-shield | `zmath-auto.js` and test | Local-processing contract passed |
| QPU-factor extension | `qpu-factor-core.js` and tests | Derivation, evidence, tamper, and simulator-boundary tests passed |

## Targeted test summary

- Zmail protected mail: 6 passed, 0 failed.
- ZMath Shield: 6 passed, 0 failed.
- Zmail opaque/purpose-bound token crypto: 3 passed, 0 failed.
- CallChat ZShield suite: passed.
- QPU-factor suite: passed.
- ZMath Auto contract: passed.

These are regression results from author-controlled code, not an independent cryptographic audit or certification.

## Claim permitted by the evidence

> The ZMath ecosystem implements at least seven distinct author-created encryption or protected-data profiles, plus integrated Matrix end-to-end encryption, using established cryptographic primitives. These are original compositions, formats, and application protocols—not claims of seven newly invented base ciphers.

## Claims not permitted

- that AES-GCM, HKDF, HMAC, ECDH, ECDSA, or Matrix Olm/Megolm were invented by the author;
- that two AES-GCM layers are AES-512;
- that every profile has received independent cryptographic review;
- that an IonQ/QPU factor is QKD or quantum encryption;
- that classical P-256 ECDH is post-quantum secure.
