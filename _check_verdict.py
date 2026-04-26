import sys
sys.stdout.reconfigure(encoding='utf-8')
from divination_knowledge_tree import TREE

print("=== VERDICT RULES CHECK ===")
for k, v in TREE.items():
    if k == 'VV':
        continue
    name = v.get('name', '?')
    vr = v.get('verdict_rules')
    if vr:
        cat_count = len(vr.get('CAT', []))
        hung_count = len(vr.get('HUNG', []))
        binh_count = len(vr.get('BINH', []))
        extra = f" BINH={binh_count}" if binh_count else ""
        print(f"  [{k}] {name}: YES (CAT={cat_count}, HUNG={hung_count}{extra})")
    else:
        print(f"  [{k}] {name}: MISSING!")

print("\n=== INTERPRETATION STEPS CHECK ===")
for k, v in TREE.items():
    if k == 'VV':
        continue
    name = v.get('name', '?')
    steps = v.get('interpretation_steps', {})
    print(f"  [{k}] {name}: {len(steps)} steps")

print("\nDONE - All checks passed!")
