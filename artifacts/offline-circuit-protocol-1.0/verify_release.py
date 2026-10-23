"""Verify this package's explicit local file allowlist; SPDX-License-Identifier: MIT.
Copyright (c) 2026 Shafaet Brady Hussain
"""
import hashlib
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
FILES = {
    "AI_ASSISTANCE.md", "AUTHORS.md", "CHANGELOG.md", "CITATION.cff",
    "CONFLICTS_AND_FUNDING.md", "DEPENDENCIES_AND_LICENSES.md", "LICENSE", "NOTICE",
    "PROVENANCE.json", "README.md", "SECURITY.md", "environment-release.json",
    "local_analysis.json", "local_results.json", "manifest.json", "protocol.py",
    "reference.py", "test_protocol.py", "verify_release.py",
}


def main():
    try:
        entries = {}
        for line in (HERE / "SHA256SUMS.txt").read_text(encoding="ascii").splitlines():
            digest, name = line.split("  ", 1)
            if name in entries or name not in FILES or len(digest) != 64:
                raise ValueError("invalid or duplicate release hash entry")
            int(digest, 16)
            entries[name] = digest
        if set(entries) != FILES:
            raise ValueError("release hash list does not match the explicit public allowlist")
        for name, expected in entries.items():
            path = HERE / name
            if path.is_symlink() or not path.is_file() or path.resolve().parent != HERE:
                raise ValueError(f"missing or unsafe release path: {name}")
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError(f"release hash mismatch: {name}")
        print(f"PASS: {len(entries)} explicit public package files match SHA256SUMS.txt")
        return 0
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
