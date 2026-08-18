#!/usr/bin/env python3
"""Deterministic classical reference evaluator for a small claim graph."""
import hashlib, itertools, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def evaluate(data, selected):
    s=set(selected); rows={c["id"]:c for c in data["claims"]}; cost=sum(rows[i]["cost"] for i in s)
    feasible=cost<=data["budget"] and all(a not in s or b in s for a,b in data["dependencies"]) and all(not({a,b}<=s) for a,b in data["contradictions"])
    base=sum(rows[i]["utility"]-data["risk_weight"]*rows[i]["risk"] for i in s)
    bonus=data["support_bonus"]*sum(1 for a,b in data["supports"] if a in s and b in s)
    return {"feasible":feasible,"score":round(base+bonus,6),"cost":cost}
def exact(data):
    ids=[c["id"] for c in data["claims"]]; candidates=[]; evaluated=0
    for n in range(len(ids)+1):
        for subset in itertools.combinations(ids,n):
            evaluated+=1; result=evaluate(data,subset)
            if result["feasible"]: candidates.append((result["score"],-result["cost"],subset,result))
    score,_,subset,result=max(candidates)
    return {"selected":list(subset),"score":score,"cost":result["cost"],"subsets_evaluated":evaluated,"feasible_subsets":len(candidates)}
def greedy(data):
    rows={c["id"]:c for c in data["claims"]}; ordered=sorted(rows,key=lambda i:(-(rows[i]["utility"]-data["risk_weight"]*rows[i]["risk"])/rows[i]["cost"],i)); selected=[]; changed=True
    while changed:
        changed=False
        for i in ordered:
            if i not in selected and evaluate(data,selected+[i])["feasible"]: selected.append(i); changed=True
    result=evaluate(data,selected)
    return {"selected":sorted(selected),"score":result["score"],"cost":result["cost"],"order":ordered}
def main():
    path=ROOT/"claim-graph-instance.json"; data=json.loads(path.read_text(encoding="utf-8")); e=exact(data); g=greedy(data)
    out={"schema":"researchforum.claim-graph-result.v1","algorithm_boundary":"classical-only","instance_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"exact":e,"greedy":g,"greedy_to_exact_ratio":round(g["score"]/e["score"],6)}
    (ROOT/"test-results.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8"); print(json.dumps(out,indent=2))
if __name__=="__main__": main()
