#!/usr/bin/env python3
import json, sys
from pathlib import Path
model=json.loads(Path(__file__).with_name("layer-model.json").read_text(encoding="utf-8"))
errors=[]
ids=[x["id"] for x in model["layers"]]
if len(ids)!=len(set(ids)): errors.append("duplicate layer")
if set(model["terminal_decisions"])!={"protected","standard_visible","deny"}: errors.append("terminal decisions changed")
for layer in model["layers"]:
    if not layer.get("must_not_imply"): errors.append(f"missing negative boundary: {layer['id']}")
print("PASS: six distinct layers carry explicit negative boundaries" if not errors else "FAIL: "+"; ".join(errors))
print("PASS: protected, standard-visible, and deny are distinct terminal decisions" if not errors else "")
sys.exit(bool(errors))
