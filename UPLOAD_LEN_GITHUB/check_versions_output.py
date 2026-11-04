# -*- coding: utf-8 -*-
"""Final check: scan output for old version references"""
import sys, re; sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper
h = FreeAIHelper()

r = h.answer_question('u17 viet nam va u17 malaysia doi nao thang', chart_data=None, topic=None)

# Find all V-version references in output
versions_found = re.findall(r'V\d+\.?\d*[a-z]?', r)
from collections import Counter
vc = Counter(versions_found)

print("=== VERSIONS IN OUTPUT ===")
for v, count in sorted(vc.items(), key=lambda x: x[1], reverse=True):
    status = '✅' if v == 'V42' or v.startswith('V42.9') else '⚠️'
    print(f"  {status} {v}: {count}x")

# Check for specific old versions in visible part (before <details>)
splits = r.split('<details>')
visible = splits[0] if splits else r
hidden = '<details>'.join(splits[1:]) if len(splits) > 1 else ''

print("\n=== IN VISIBLE PART (before collapse) ===")
vis_versions = re.findall(r'V\d+\.?\d*[a-z]?', visible)
vis_vc = Counter(vis_versions)
for v, count in sorted(vis_vc.items(), key=lambda x: x[1], reverse=True):
    print(f"  {v}: {count}x")

print("\n=== IN HIDDEN PART (inside collapse) ===")
hid_versions = re.findall(r'V\d+\.?\d*[a-z]?', hidden)
hid_vc = Counter(hid_versions)
for v, count in sorted(hid_vc.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {v}: {count}x")
