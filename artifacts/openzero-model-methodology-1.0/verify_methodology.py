import argparse, hashlib, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEX = re.compile(r"^[0-9a-f]{64}$")

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

def final_prompt(row):
    return next(m["content"] for m in reversed(row["messages"]) if m["role"] == "user")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--curated-dir", type=Path)
    args = p.parse_args()
    m = json.loads((HERE / "methodology-manifest.json").read_text(encoding="utf-8"))
    assert sum(s["rows"] for s in m["sources"]) == m["input_rows"]
    assert m["train"] + m["eval"] == m["accepted"]
    assert m["accepted"] + sum(m["rejected"].values()) == m["input_rows"]
    hashes = [s["sha256"] for s in m["sources"]] + [x["sha256"] for x in m["outputs"].values()]
    assert all(HEX.fullmatch(h) for h in hashes)
    if args.curated_dir:
        train_path, eval_path = args.curated_dir / "train.jsonl", args.curated_dir / "eval.jsonl"
        train, evaluation = rows(train_path), rows(eval_path)
        assert len(train) == m["train"] and len(evaluation) == m["eval"]
        assert digest(train_path) == m["outputs"]["train"]["sha256"]
        assert digest(eval_path) == m["outputs"]["eval"]["sha256"]
        assert {final_prompt(r) for r in train}.isdisjoint(final_prompt(r) for r in evaluation)
        print("PASS: private split counts, hashes, and final-prompt isolation verified")
    print("PASS: methodology manifest arithmetic and SHA-256 syntax verified")

if __name__ == "__main__":
    main()
