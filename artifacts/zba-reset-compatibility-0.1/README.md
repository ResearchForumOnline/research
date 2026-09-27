# ZBA reset compatibility — reproducibility package 0.1

[Paper and summary](../../papers/zba-reset-compatibility-0.1.md) · [Complete proofs in LaTeX](../../papers/zba-reset-compatibility-0.1.tex)

Run with Python 3, without third-party packages or API keys:

```sh
python verify_reset_algebra.py
```

Expected: `passed`, 496 exhaustive validator cases, 248 feasible synthesis cases. Assertion failures return a nonzero exit status. Running the program rewrites `results.json` with its reproducible results.

- `verify_reset_algebra.py`: explicit transformation closure and policy enumeration.
- `results.json`: recorded results; the 36-state full distribution is formula-derived.
- `source-manifest.json`: exact public baseline revisions, URLs, and SHA-256 hashes.
- `sources/`: pinned public specification and reference-code snapshots from GitHub and Hugging Face. Original attribution and license statements remain in those files.
- `SHA256SUMS.txt`: release-file integrity hashes.

The checks cover every validator for five specified small involutions, not every possible involution. Mathematical proofs are in the manuscript. AI assistance is disclosed there; external peer review has not occurred. No compiled PDF is included.
