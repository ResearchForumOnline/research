#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/"evaluate_claim_graph.py")],check=True,stdout=subprocess.DEVNULL)
r=json.loads((root/"test-results.json").read_text(encoding="utf-8"))
assert r["algorithm_boundary"]=="classical-only" and r["exact"]["subsets_evaluated"]==256 and 0<r["greedy_to_exact_ratio"]<=1
print("claim-graph exact/greedy reproducibility checks: ok")
