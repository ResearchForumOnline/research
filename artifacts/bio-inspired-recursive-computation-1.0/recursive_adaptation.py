#!/usr/bin/env python3
"""Deterministic bounded recurrence; a software metaphor, not a biological model."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def evolve(initial,target,rate,steps):
    if not 0<rate<=1 or steps<0: raise ValueError("require 0 < rate <= 1 and steps >= 0")
    values=[float(initial)]
    for _ in range(steps): values.append(values[-1]+rate*(target-values[-1]))
    return values
def main():
    values=evolve(0,1,.2,20); closed=[1-(.8**t) for t in range(21)]
    checks={"deterministic":values==evolve(0,1,.2,20),"closed_form":max(abs(a-b) for a,b in zip(values,closed))<1e-12,"bounded":all(0<=x<=1 for x in values),"monotone":all(a<=b for a,b in zip(values,values[1:])),"error_contracts":abs(1-values[-1])<abs(1-values[0])}
    out={"schema":"researchforum.recursive-adaptation.v1","parameters":{"initial":0,"target":1,"rate":.2,"steps":20},"final":values[-1],"checks":checks,"all_checks_pass":all(checks.values())}
    (ROOT/"recurrence-results.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2)); raise SystemExit(0 if all(checks.values()) else 1)
if __name__=="__main__": main()
