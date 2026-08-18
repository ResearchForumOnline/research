#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
for n in ("audit_simulator.py","recursive_adaptation.py"): subprocess.run([sys.executable,str(r/n)],check=True,stdout=subprocess.DEVNULL)
print("bio-inspired formula audit and bounded recurrence checks: ok")
