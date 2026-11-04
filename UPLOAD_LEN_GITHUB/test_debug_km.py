# -*- coding: utf-8 -*-
"""Debug KM Scoring"""
import sys
sys.path.insert(0, '.')
from free_ai_helper import FreeAIHelper

ai = FreeAIHelper()

# Get chart data via answer flow
_captured = {}
_orig = ai._try_online_ai
def _mock(question, chart_data=None, mai_hoa_data=None, luc_hao_data=None, topic=None, offline_analysis_data=None):
    _captured['cd'] = chart_data
    _captured['mh'] = mai_hoa_data
    _captured['lh'] = luc_hao_data
    _captured['od'] = offline_analysis_data
    return None
ai._try_online_ai = _mock
ai.answer_question("Mua nha nam nay tot khong?")

cd = _captured.get('cd', {})
od = _captured.get('od', {})
mh = _captured.get('mh', {})
lh = _captured.get('lh', {})

print("=== KM SCORING DEBUG ===")
print(f"dung_than from od: {od.get('dung_than')}")
print(f"can_thien_ban: {cd.get('can_thien_ban')}")

# Try KM scoring directly
dung_than = od.get('dung_than', 'Phu Mau')
try:
    s, summary, factors = ai._ky_mon_scoring(cd, dung_than)
    print(f"\nKM Scoring OK: s={s}, factors={len(factors)}")
    for f in factors:
        print(f"  {f}")
except Exception as e:
    print(f"\nKM Scoring ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Check Mai Hoa data
print("\n=== MAI HOA DATA ===")
for k in ['ten', 'ten_que', 'ten_thuong', 'ten_ha', 'thuong_quai', 'ha_quai', 
           'hanh_thuong', 'hanh_ha', 'ho_quai', 'bien_quai', 'tuong', 'nghia',
           'ho_quai_ten', 'bien_quai_ten', 'the_dung']:
    print(f"  {k}: {mh.get(k, 'MISSING')}")
# Show all keys
print(f"\n  ALL KEYS: {list(mh.keys())[:30]}")

# Check Luc Hao data
print("\n=== LUC HAO DATA ===")
for k in ['ten_que', 'ten', 'ten_thuong', 'ten_ha', 'hanh_thuong', 'hanh_ha',
           'chi_thang', 'chi_ngay', 'ngu_hanh', 'que_chu', 'the_vi', 'ung_vi']:
    print(f"  {k}: {lh.get(k, 'MISSING')}")
ban = lh.get('ban', {})
print(f"\n  ban keys: {list(ban.keys())[:10]}")
haos = ban.get('haos', ban.get('details', []))
if haos:
    print(f"  haos count: {len(haos)}")
    for i, h in enumerate(haos):
        print(f"    hao[{i}]: {h.get('luc_than','?')} {h.get('chi','?')} {h.get('ngu_hanh','?')} {h.get('the_ung','')}")
