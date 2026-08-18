#!/usr/bin/env python3
import json,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(r/"benchmark_corpus.py")],check=True,stdout=subprocess.DEVNULL)
d=json.loads((r/"benchmark-results.json").read_text()); assert d["records"]==134 and d["synthetic_rule_test"]["cases"]==12 and d["boundary"].startswith("title-signal")
print("corpus structure and claim-risk triage benchmark: ok")
