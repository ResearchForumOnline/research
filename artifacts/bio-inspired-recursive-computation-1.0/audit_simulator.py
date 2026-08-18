#!/usr/bin/env python3
"""Independent semantic audit of the frozen Genetic Adaptation formula."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def h(x): return 1 if x>0 else 0
def g(xs,y=0,Q=1,b1=1,b2=1,alpha=0,beta=0,gamma=0,eta=1,theta=1,lam=0):
    xs=[xs] if isinstance(xs,(int,float)) else list(xs); out=[]
    for x in xs:
        arg=b1+eta*Q*x
        if arg<=0: arg=1e-12
        out.append(b2*math.log(arg)*math.exp(lam*x)*(1+alpha*h(-x)+beta*h(x)+gamma*math.exp(-theta*Q*x*x)))
    return out
def main():
    findings={}
    findings["y_is_invariant"]=g([-.5,0,.5],y=-999)==g([-.5,0,.5],y=999)
    findings["independent_not_recursive"]=g([.5,-.5])==[g(.5)[0],g(-.5)[0]]
    findings["invalid_log_inputs_collapse"]=g(-2)==g(-200)
    findings["zero_step_differs_from_sides"]=g(0,alpha=.5,beta=.7)!=g(1e-9,alpha=.5,beta=.7)
    overflow=False
    try: g(1000,lam=1)
    except OverflowError: overflow=True
    findings["large_growth_can_overflow"]=overflow
    out={"schema":"researchforum.genetic-formula-audit.v1","implementation_boundary":"independent exact mirror","findings":findings,"all_findings_reproduced":all(findings.values())}
    (ROOT/"simulator-audit-results.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2)); raise SystemExit(0 if all(findings.values()) else 1)
if __name__=="__main__": main()
