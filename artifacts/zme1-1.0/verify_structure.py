#!/usr/bin/env python3
"""Dependency-free structural checks; intentionally performs no decryption."""
import base64, json, sys
from pathlib import Path

PROFILES = {"ZSHIELD-PBKDF2-AESGCM-1", "ZMATH-PBKDF2-HKDF-AESGCM-2", "ZMATH-PBKDF2-HKDF-AESGCM-QPUFACTOR-3"}

def b64(value):
    return base64.b64decode(value, validate=True)

def check(c):
    errors=[]
    try:
        h=c["header"]; p=h["payload"]; k=h["kdf"]; a=h["cipher"]; ct=b64(c["ciphertext"])
        if h.get("format")!="ZME1" or h.get("version")!=1 or h.get("profile") not in PROFILES: errors.append("unsupported identity")
        if not isinstance(k.get("iterations"), int) or not 600000 <= k["iterations"] <= 1200000: errors.append("KDF work outside bounds")
        if len(b64(k["salt"]))!=16 or len(b64(a["iv"]))!=12: errors.append("salt or IV length invalid")
        if a.get("name")!="AES-256-GCM" or a.get("tagLength")!=128: errors.append("cipher profile invalid")
        if not isinstance(p.get("size"), int) or not 0 <= p["size"] <= 50*1024*1024: errors.append("payload size outside bounds")
        elif len(ct)!=p["size"]+16: errors.append("ciphertext length disagrees with authenticated size")
    except Exception as e: errors.append("malformed structure: "+type(e).__name__)
    return errors

def main(path):
    vectors=json.loads(Path(path).read_text(encoding="utf-8")); unexpected=0
    for v in vectors:
        errors=check(v["container"]); observed="PASS" if not errors else "FAIL"; ok=observed==v["expected"]; unexpected += not ok
        print(f"{v['name']}: expected={v['expected']} observed={observed} [{'ok' if not errors else '; '.join(errors)}]")
    print(f"summary: {len(vectors)-unexpected}/{len(vectors)} expectations matched")
    return unexpected != 0

if __name__=="__main__": sys.exit(main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name("structural-vectors.json")))
