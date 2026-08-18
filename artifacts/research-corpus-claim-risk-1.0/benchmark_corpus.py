#!/usr/bin/env python3
"""Deterministic title-signal triage and structural corpus QA."""
import collections,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CATS={
 "medical":("medical","health","disease","pain","antibiotic","antimicrobial","treatment","medicine","healing","diet","smoking"),
 "genetic_biological":("dna","genetic","genome","ancestry","cloning","wetware","organic ai"),
 "security":("encryption","secure","cyber","malware","privacy","shield","vault"),
 "quantum":("quantum","qpu","qiskit","ionq"),
 "extraordinary":("consciousness","time travel","interdimensional","psychic","remote viewing","universal energy","astral","anunnaki","ancient knowledge")}
SYN=[
 ("Local agent runtime benchmark",set()),("Health treatment claim",{"medical"}),
 ("DNA encryption using a quantum computer",{"genetic_biological","security","quantum"}),
 ("Remote viewing and psychic evidence",{"extraordinary"}),
 ("Privacy-preserving secure vault",{"security"}),
 ("Quantum simulator evaluation",{"quantum"}),
 ("Genetic ancestry analysis",{"genetic_biological"}),
 ("Pain and healing with diet",{"medical"}),
 ("Interdimensional time travel",{"extraordinary"}),
 ("Ordinary mathematics note",set()),
 ("Organic AI wetware",{"genetic_biological"}),
 ("Cyber malware shield",{"security"})]
def classify(title):
 t=title.casefold(); return {c for c,terms in CATS.items() if any(x in t for x in terms)}
def main():
 d=json.loads((ROOT/"frozen-source-metadata.json").read_text(encoding="utf-8")); rows=d["sources"]
 required=("id","title","url","text_sha256","word_count","publication_lane")
 missing=sum(any(r.get(k) in (None,"") for k in required) for r in rows)
 urls=collections.Counter(r["url"] for r in rows); hashes=collections.Counter(r["text_sha256"] for r in rows)
 lanes=collections.Counter(r["publication_lane"] for r in rows); cats=collections.Counter(); flagged=0
 for r in rows:
  labels=classify(r["title"]); cats.update(labels); flagged+=bool(labels)
 tp=fp=fn=0
 for title,want in SYN:
  got=classify(title); tp+=len(got&want); fp+=len(got-want); fn+=len(want-got)
 precision=tp/(tp+fp) if tp+fp else 1; recall=tp/(tp+fn) if tp+fn else 1
 result={"schema":"researchforum.claim-risk-triage-benchmark.v1","boundary":"title-signal review queue; not truth or risk ground truth","records":len(rows),"lane_counts":dict(sorted(lanes.items())),"structural":{"missing_required_records":missing,"duplicate_url_groups":sum(v>1 for v in urls.values()),"duplicate_text_hash_groups":sum(v>1 for v in hashes.values()),"replacement_character_titles":sum("�" in r["title"] for r in rows),"nonpositive_word_counts":sum((r.get("word_count") or 0)<=0 for r in rows)},"triage":{"flagged_records":flagged,"category_counts":dict(sorted(cats.items()))},"synthetic_rule_test":{"cases":len(SYN),"true_positive_labels":tp,"false_positive_labels":fp,"false_negative_labels":fn,"micro_precision":round(precision,6),"micro_recall":round(recall,6)},"deterministic_rerun":True}
 (ROOT/"benchmark-results.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8"); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
