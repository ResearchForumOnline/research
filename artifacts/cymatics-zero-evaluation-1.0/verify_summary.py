import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def main():
    s = json.loads((HERE / "evaluation-summary.json").read_text(encoding="utf-8"))
    assert s["manifest"]["count"] == s["manifest"]["unique_ids"] == 3000
    assert sum(s["families"].values()) == 3000
    assert set(s["families"].values()) == {600}
    assert s["svg_xml_pass"] == s["medical_boundary_pass"] == 3000
    r = s["sample_regeneration"]
    assert r["byte_matches"] + r["mismatches"] == r["sampled"] == 25
    assert r["byte_matches"] == 0
    assert s["live"]["manifest_count"] != s["live"]["html_claim_count"]
    assert all(len(x) == 64 for x in (s["manifest"]["sha256"], s["generator_sha256"], s["live"]["bundle_sha256"]))
    print("PASS: corpus arithmetic, negative reproduction result, and live count mismatch are internally consistent")

if __name__ == "__main__":
    main()
