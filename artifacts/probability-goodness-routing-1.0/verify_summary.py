#!/usr/bin/env python3
import json,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(r/"audit_goodness.py")],check=True,stdout=subprocess.DEVNULL)
d=json.loads((r/"test-results.json").read_text()); assert len(d["cases"])==8 and d["all_findings_reproduced"]
print("Probability-of-Goodness mirror and metamorphic audit: ok")
