# -*- coding: utf-8 -*-
import sys, json
sys.path.insert(0, '.')
from luc_hao_kinh_dich import lap_qua_luc_hao

r = lap_qua_luc_hao(2026, 4, 16, 11)

print("=== TOP KEYS ===")
for k in sorted(r.keys()):
    v = r[k]
    t = type(v).__name__
    if t == 'dict':
        print(f"  {k}: dict({len(v)})")
    elif t == 'list':
        print(f"  {k}: list({len(v)})")
    else:
        print(f"  {k}: {str(v)[:80]}")

# Bien (Biến quẻ)
bien = r.get('bien', {})
if bien:
    print("\n=== BIEN KEYS ===")
    for k in sorted(bien.keys()):
        print(f"  {k}: {type(bien[k]).__name__}")

# Hao details
ban = r.get('ban', {})
haos = ban.get('haos', [])
print(f"\n=== {len(haos)} HAOS ===")
for h in haos:
    mv = 'DONG' if h.get('is_moving') else 'tinh'
    lt = h.get('luc_than', '?')
    cc = h.get('can_chi', '?')
    nh = h.get('ngu_hanh', '?')
    st = h.get('strength', '?')
    mk = h.get('marker', '')
    print(f"  Hao{h['hao']}: {lt:12s} {cc:10s} {nh:5s} {st:8s} {mv} {mk}")

print(f"\ndong_hao: {r.get('dong_hao')}")
print(f"the_ung: {json.dumps(r.get('the_ung', {}), ensure_ascii=False)}")
print(f"phuc_than: {json.dumps(r.get('phuc_than', {}), ensure_ascii=False)[:200]}")
print(f"conclusion: {json.dumps(r.get('conclusion', {}), ensure_ascii=False)[:200]}")

# MH
print("\n\n=== MAI HOA ===")
try:
    from mai_hoa_dich_so import lap_que_mai_hoa
    mh = lap_que_mai_hoa(2026, 4, 16, 11)
    if mh and isinstance(mh, dict):
        for k in sorted(mh.keys()):
            v = mh[k]
            t = type(v).__name__
            if t in ('dict', 'list'):
                print(f"  {k}: {t}({len(v)})")
            else:
                print(f"  {k}: {str(v)[:80]}")
except Exception as e:
    print(f"MH Error: {e}")
