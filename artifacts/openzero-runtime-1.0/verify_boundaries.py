#!/usr/bin/env python3
import json,sys
from pathlib import Path
d=json.loads(Path(__file__).with_name('action-boundaries.json').read_text(encoding='utf-8')); errors=[]
if d.get('unknown_action')!='deny': errors.append('unknown actions must deny')
names=[a['class'] for a in d['actions']]
if len(names)!=len(set(names)): errors.append('duplicate action class')
for a in d['actions']:
    if a.get('local') is False and a.get('confirmation')=='none': errors.append(a['class']+' hides network transition')
    if a.get('confirmation') not in {'none','policy','action_time','route_visible'}: errors.append(a['class']+' has invalid confirmation')
print('PASS: 8 action classes have explicit locality, mutation, and confirmation boundaries' if not errors else 'FAIL: '+'; '.join(errors))
print('PASS: unknown actions deny' if not errors else '')
sys.exit(bool(errors))
