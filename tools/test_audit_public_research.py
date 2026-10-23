"""Synthetic checks for the public catalog's privacy and integrity boundaries.

SPDX-License-Identifier: MIT
Copyright (c) 2026 Shafaet Brady Hussain
"""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import audit_public_research as audit


class PublicCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="public-research-catalog-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.tracked = []
        self.catalog = self.root / "docs" / "PUBLIC_RESEARCH_CATALOG.json"
        self.catalog.parent.mkdir()
        for target, replacement in (("ROOT", self.root), ("CATALOG", self.catalog)):
            patcher = patch.object(audit, target, replacement)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch.object(audit, "tracked_research_paths", lambda: sorted(self.tracked))
        patcher.start()
        self.addCleanup(patcher.stop)

    def put(self, relative, content, tracked=True):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        if tracked:
            self.tracked.append(relative)
        return path

    def test_untracked_private_file_never_enters_inventory(self):
        self.put("papers/example.md", b"---\ntitle: Example\nlicense: CC BY 4.0\n---\nPublic")
        self.put("papers/private-untracked.txt", b"SYNTHETIC_PRIVATE_MARKER", tracked=False)
        self.put("private-outside-scope.txt", b"SYNTHETIC_PRIVATE_MARKER", tracked=False)
        result = audit.build_catalog()
        self.assertEqual(result["file_count"], 1)
        self.assertNotIn("SYNTHETIC_PRIVATE_MARKER", json.dumps(result))
        self.assertEqual(result["files"][0]["license"], "CC BY 4.0")

    def test_missing_tracked_file_fails(self):
        self.tracked.append("papers/missing.md")
        with self.assertRaisesRegex(ValueError, "absent or unsafe"):
            audit.build_catalog()

    def test_formatted_original_tampering_fails(self):
        original = b"SYNTHETIC_FORMATTED_ORIGINAL"
        path = self.put("papers/formatted/example.pdf", original)
        ledger = {"files": [{"path": "example.pdf", "sha256": hashlib.sha256(original).hexdigest(), "bytes": len(original), "document_rights": "CC BY 4.0"}]}
        self.put("papers/formatted/SOURCE_MANIFEST.json", json.dumps(ledger).encode())
        self.assertEqual(audit.build_catalog()["file_count"], 2)
        path.write_bytes(b"ALTERED")
        with self.assertRaisesRegex(ValueError, "hash differs"):
            audit.build_catalog()

    def test_stale_catalog_fails_until_intentional_regeneration(self):
        manuscript = self.put("papers/example.md", b"Original")
        with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["audit", "--write"]):
            self.assertEqual(audit.main(), 0)
        with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["audit"]):
            self.assertEqual(audit.main(), 0)
        manuscript.write_bytes(b"Reviewed revision")
        with contextlib.redirect_stderr(io.StringIO()), patch("sys.argv", ["audit"]):
            self.assertEqual(audit.main(), 1)

    def test_nearby_license_is_reported_without_inventing_grant(self):
        self.put("artifacts/example/LICENSE", b"MIT License\nSynthetic notice")
        self.put("artifacts/example/reference.py", b"print('synthetic')\n")
        record = next(record for record in audit.build_catalog()["files"] if record["path"].endswith("reference.py"))
        self.assertEqual(record["nearby_notices"], ["artifacts/example/LICENSE"])
        self.assertNotIn("license", record)


if __name__ == "__main__":
    unittest.main()
