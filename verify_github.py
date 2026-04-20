# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read the downloaded GitHub source
with open(r'C:\Users\GHC\.gemini\antigravity\brain\b3d16ba9-8bcf-4da6-af39-1a01c97cacf5\.system_generated\steps\140\content.md', 'r', encoding='utf-8') as f:
    t = f.read()

checks = [
    'PHASE D: KẾT LUẬN THỐNG NHẤT V39.0',
    'PHÁN QUYẾT',
    'VÌ SAO KẾT LUẬN NHƯ VẬY',
    'KHẲNG ĐỊNH',
    'GIẢI PHÁP',
    'LỜI KHUYÊN',
    'KHÔNG override pct',
]

print("=== V39.0 GitHub Deployment Check ===")
for c in checks:
    status = "✅ FOUND" if c in t else "❌ MISSING"
    print(f"  {c}: {status}")

old_override = "pct = min(pct, 40)" in t
print(f"\n  Old pct override removed: {'✅ YES' if not old_override else '❌ NO - STILL EXISTS'}")
print(f"\n=== RESULT: {'ALL GOOD' if not old_override else 'PROBLEM'} ===")
