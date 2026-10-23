#!/usr/bin/env python3
"""Inventory only Git-tracked public research and verify its published bytes.

This does not crawl the author's computer, fetch data, inspect credentials, or
decide whether material is scientifically valid or legally publishable.
SPDX-License-Identifier: MIT
Copyright (c) 2026 Shafaet Brady Hussain
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "PUBLIC_RESEARCH_CATALOG.json"
SCHEMA = "research-public-catalog.v1"


def tracked_research_paths():
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "papers", "artifacts", "sources", "data"],
        cwd=ROOT, check=True, capture_output=True,
    )
    return sorted(path.decode("utf-8") for path in result.stdout.split(b"\0") if path)


def frontmatter(text):
    """Read only simple published scalar frontmatter; no YAML dependencies."""
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}
    result = {}
    for line in lines[1:]:
        if line == "---":
            break
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def build_catalog():
    records = []
    paths = tracked_research_paths()
    path_set = set(paths)
    for relative in paths:
        path = ROOT / relative
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(ROOT):
            raise ValueError(f"Tracked research file is absent or unsafe: {relative}")
        payload = path.read_bytes()
        if relative.startswith("papers/formatted/"):
            category = "formatted-manuscript" if path.suffix in {".pdf", ".docx"} else "archive-metadata"
        elif relative.startswith("papers/"):
            category = "manuscript" if path.suffix == ".md" else "manuscript-companion"
        elif relative.startswith("artifacts/"):
            category = "reproducibility-artifact"
        elif relative.startswith("sources/"):
            category = "source-ledger"
        else:
            category = "public-data-or-metadata"
        record = {
            "path": relative,
            "category": category,
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        }
        if path.suffix == ".md":
            metadata = frontmatter(payload.decode("utf-8-sig"))
            for key in ("title", "author", "date", "license"):
                if metadata.get(key):
                    record[key] = metadata[key]
        # Report actual nearby notices without inferring grants from publicity.
        notices = []
        for parent in path.parents:
            if parent == ROOT:
                break
            for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "NOTICE"):
                candidate = (parent / name).relative_to(ROOT).as_posix()
                if candidate in path_set:
                    notices.append(candidate)
        if notices:
            record["nearby_notices"] = sorted(set(notices))
        records.append(record)
    manifest_relative = "papers/formatted/SOURCE_MANIFEST.json"
    if manifest_relative in path_set:
        manifest = json.loads((ROOT / manifest_relative).read_text(encoding="utf-8"))
        by_path = {record["path"]: record for record in records}
        for source in manifest["files"]:
            relative = "papers/formatted/" + source["path"]
            record = by_path[relative]
            if record["sha256"] != source["sha256"] or record["bytes"] != source["bytes"]:
                raise ValueError(f"Original formatted-manuscript hash differs: {relative}")
            record["archive_recorded_rights"] = source["document_rights"]
            record["archive_rights_evidence"] = source.get("license_evidence_path")
    return {
        "schema": SCHEMA,
        "scope": "Git-tracked papers, artifacts, sources and data in this public repository only",
        "integrity_boundary": "Hashes describe bytes; they do not establish scientific validity, ownership, peer review or privacy clearance",
        "rights_boundary": "Read LICENSE.md, file declarations, nearby notices and docs/OPEN_RESEARCH.md; no rights are inferred from public visibility alone",
        "current_rights_notice": "LICENSE.md",
        "counts": dict(sorted(Counter(record["category"] for record in records).items())),
        "file_count": len(records),
        "files": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Regenerate the public catalog after reviewing intended changes")
    arguments = parser.parse_args()
    try:
        catalog = build_catalog()
        serialized = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
        if arguments.write:
            CATALOG.write_text(serialized, encoding="utf-8", newline="\n")
        elif not CATALOG.is_file() or CATALOG.read_text(encoding="utf-8") != serialized:
            print("FAIL: public research catalog differs. Review changed files, then run with --write.", file=sys.stderr)
            return 1
        print(f"PASS: {catalog['file_count']} tracked public research files; formatted originals match their source manifest.")
        for category, count in catalog["counts"].items():
            print(f"  {category}: {count}")
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
