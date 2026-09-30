"""Verify and bundle the explicit, previously public formatted-paper allowlist."""
import hashlib
import json
from pathlib import Path
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'papers' / 'formatted'


def main():
    ledger = json.loads((SOURCE / 'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
    assert ledger['file_count'] == 22 and ledger['unique_papers'] == 11
    paths = []
    for record in ledger['files']:
        path = SOURCE / record['path']
        assert path.parent == SOURCE and path.suffix in {'.pdf', '.docx'}
        assert path.is_file() and not path.is_symlink()
        content = path.read_bytes()
        assert len(content) == record['bytes']
        assert hashlib.sha256(content).hexdigest() == record['sha256'], path.name
        assert (ROOT / record['public_manuscript']).is_file()
        paths.append(path)
    assert len(set(paths)) == 22
    paths += [SOURCE / 'README.md', SOURCE / 'SOURCE_MANIFEST.json', ROOT / 'docs/PROJECT_PRESERVATION.md']
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    target = output / 'formatted-research-papers-20260930.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(paths):
            info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), (2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_suffix('.zip.sha256').write_text(f'{digest}  {target.name}\n', encoding='ascii')
    print(f'Verified 22 original documents. Built {target.name}, SHA-256 {digest}')


if __name__ == '__main__':
    main()
