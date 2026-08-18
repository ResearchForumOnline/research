#!/usr/bin/env python3
"""Create a text-free metadata snapshot from the repository source index."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent; repo=ROOT.parents[1]
d=json.loads((repo/"data/research-forum-source-index.json").read_text(encoding="utf-8"))
keep=("id","title","url","starter","text_sha256","word_count","support_authored","likely_spam","third_party","publication_lane")
out={"schema":"researchforum.redacted-source-metadata.v1","generated_from":d.get("generated_at"),"source_count":len(d["sources"]),"sources":[{k:s.get(k) for k in keep} for s in d["sources"]]}
(ROOT/"frozen-source-metadata.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(f"wrote {len(out['sources'])} text-free metadata records")
