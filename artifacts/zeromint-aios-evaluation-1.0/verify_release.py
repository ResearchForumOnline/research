import argparse, hashlib, json, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--torrent", type=Path)
    p.add_argument("--live", action="store_true")
    args = p.parse_args()
    e = json.loads((HERE / "release-evidence.json").read_text(encoding="utf-8"))
    assert sum(x["size"] for x in e["parts"]) == e["iso"]["size"]
    assert (e["iso"]["size"] + e["torrent"]["piece_length"] - 1) // e["torrent"]["piece_length"] == e["torrent"]["piece_hash_count"]
    assert all(len(x["sha256"]) == 64 for x in e["parts"] + [e["iso"], e["torrent"]])
    print("PASS: part sizes and torrent piece arithmetic are internally consistent")
    if args.torrent:
        assert args.torrent.stat().st_size == e["torrent"]["size"]
        assert sha256(args.torrent) == e["torrent"]["sha256"]
        print("PASS: torrent size and SHA-256 match")
    if args.live:
        url = "https://api.github.com/repos/ResearchForumOnline/OpenZero/releases/tags/zeromint-os-v1.0"
        req = urllib.request.Request(url, headers={"User-Agent": "zeromint-evidence-verifier/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.load(response)
        assets = {x["name"]: x for x in data["assets"]}
        for expected in e["parts"] + [e["torrent"] | {"name": "ZeroMint_OS_v1.0.torrent"}]:
            actual = assets[expected["name"]]
            assert actual["size"] == expected["size"]
            assert actual.get("digest") == "sha256:" + expected["sha256"]
        print("PASS: live GitHub asset sizes and SHA-256 digests match")

if __name__ == "__main__":
    main()
