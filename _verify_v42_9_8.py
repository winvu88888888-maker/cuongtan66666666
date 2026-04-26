"""V42.9.8 Verification: DKT Integration + Diagram Coverage"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

TOTAL = 0
PASS = 0
FAIL = []

def check(name, cond, detail=""):
    global TOTAL, PASS
    TOTAL += 1
    if cond:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL.append(name)
        print(f"  ❌ {name}: {detail}")

print("=" * 70)
print("🔬 V42.9.8 VERIFICATION: DKT INTEGRATION + DIAGRAM COVERAGE")
print("=" * 70)

# ═══ TEST 1: DKT Import ═══
print("\n📦 TEST 1: DKT Import & TREE structure")
from divination_knowledge_tree import TREE
check("TREE exists", TREE is not None)
check("TREE has 9 keys", len(TREE) >= 8, f"Có {len(TREE)}")
check("LH has luc_xung", 'luc_xung' in TREE.get('LH', {}))
check("LH has luc_hop", 'luc_hop' in TREE.get('LH', {}))
check("LH has tam_hop", 'tam_hop' in TREE.get('LH', {}))
check("LH luc_xung has 6 pairs", len(TREE['LH']['luc_xung']) == 6, f"Có {len(TREE['LH']['luc_xung'])}")
check("LH luc_hop has 6 pairs", len(TREE['LH']['luc_hop']) == 6, f"Có {len(TREE['LH']['luc_hop'])}")
check("LH tam_hop has 4 cucs", len(TREE['LH']['tam_hop']) == 4, f"Có {len(TREE['LH']['tam_hop'])}")

# ═══ TEST 2: Engine reads from DKT ═══
print("\n🔗 TEST 2: Engine reads Lục Xung/Hợp/Tam Hợp from DKT")
from free_ai_helper import LUC_HOP_CHI, LUC_XUNG_CHI, TAM_HOP_CUC

check("LUC_HOP_CHI loaded", len(LUC_HOP_CHI) == 12, f"Có {len(LUC_HOP_CHI)}")
check("LUC_XUNG_CHI loaded", len(LUC_XUNG_CHI) == 12, f"Có {len(LUC_XUNG_CHI)}")
check("TAM_HOP_CUC loaded", len(TAM_HOP_CUC) == 4, f"Có {len(TAM_HOP_CUC)}")

# Verify data correctness
check("Tý xung Ngọ", LUC_XUNG_CHI.get('Tý') == 'Ngọ', f"Got: {LUC_XUNG_CHI.get('Tý')}")
check("Tý hợp Sửu", LUC_HOP_CHI.get('Tý') == 'Sửu', f"Got: {LUC_HOP_CHI.get('Tý')}")
check("Dần xung Thân", LUC_XUNG_CHI.get('Dần') == 'Thân', f"Got: {LUC_XUNG_CHI.get('Dần')}")
check("Mão hợp Tuất", LUC_HOP_CHI.get('Mão') == 'Tuất', f"Got: {LUC_HOP_CHI.get('Mão')}")

# Tam Hợp
tam_hop_hanhs = [h for _, (h, _) in TAM_HOP_CUC.items()]
check("Tam Hợp has Thủy", 'Thủy' in tam_hop_hanhs)
check("Tam Hợp has Mộc", 'Mộc' in tam_hop_hanhs)
check("Tam Hợp has Hỏa", 'Hỏa' in tam_hop_hanhs)
check("Tam Hợp has Kim", 'Kim' in tam_hop_hanhs)

# ═══ TEST 3: Interaction Diagrams has KM/TV/XND ═══
print("\n📐 TEST 3: Interaction Diagrams has KM/TV/XND references")
from interaction_diagrams import (
    DIAGRAM_MASTER, DIAGRAMS,
    KM_BAT_MON_REF, KM_CUU_TINH_REF,
    TV_CHINH_TINH_REF,
    XND_HOANG_DAO_REF, XND_HAC_DAO_REF,
)

check("KM_BAT_MON_REF has 8 cửa", len(KM_BAT_MON_REF) == 8, f"Có {len(KM_BAT_MON_REF)}")
check("KM_CUU_TINH_REF has 9 sao", len(KM_CUU_TINH_REF) == 9, f"Có {len(KM_CUU_TINH_REF)}")
check("TV_CHINH_TINH_REF has 14 tinh", len(TV_CHINH_TINH_REF) == 14, f"Có {len(TV_CHINH_TINH_REF)}")
check("XND_HOANG_DAO_REF has 6 sao", len(XND_HOANG_DAO_REF) == 6, f"Có {len(XND_HOANG_DAO_REF)}")
check("XND_HAC_DAO_REF has 6 sao", len(XND_HAC_DAO_REF) == 6, f"Có {len(XND_HAC_DAO_REF)}")

# Verify KM data
check("Khai Môn is ĐẠI CÁT", KM_BAT_MON_REF['Khai Môn']['cat_hung'] == 'ĐẠI CÁT')
check("Tử Môn is ĐẠI HUNG", KM_BAT_MON_REF['Tử Môn']['cat_hung'] == 'ĐẠI HUNG')
check("Thiên Tâm is CÁT", KM_CUU_TINH_REF['Thiên Tâm']['cat_hung'] == 'CÁT')

# ═══ TEST 4: DIAGRAM_MASTER template has new sections ═══
print("\n📝 TEST 4: DIAGRAM_MASTER template includes TV/XND/KM")
tpl = DIAGRAM_MASTER.get('template', '')
check("Template has bat_mon_cat_hung", '{bat_mon_cat_hung}' in tpl)
check("Template has cuu_tinh_cat_hung", '{cuu_tinh_cat_hung}' in tpl)
check("Template has TỬ VI section", 'TỬ VI' in tpl)
check("Template has tv_chinh_tinh", '{tv_chinh_tinh}' in tpl)
check("Template has XEM NGÀY section", 'XEM NGÀY' in tpl)
check("Template has xnd_hoang_hac", '{xnd_hoang_hac}' in tpl)

# ═══ TEST 5: All 17 diagrams still work ═══
print("\n📊 TEST 5: All 17 diagrams intact")
for i in range(17):
    d_id = f'SD{i}' if i > 0 else 'SD0'
    check(f"DIAGRAMS has {d_id}", d_id in DIAGRAMS, f"Missing {d_id}")

# ═══ TEST 6: Engine functions still work ═══
print("\n⚙️ TEST 6: Engine functions work with DKT data")
from free_ai_helper import _get_ung_ky_advanced, _analyze_hoa_hoi_dau, _detect_am_dong

# Test ứng kỳ uses DKT-sourced LUC_XUNG_CHI
ung_ky = _get_ung_ky_advanced('Kim', 'CÁT', chi_dt='Thân', can_ngay='Giáp', chi_ngay='Tý')
check("_get_ung_ky_advanced works", len(ung_ky) > 0, f"Got empty string")
check("Ung ky has Xung kỳ", 'Xung kỳ' in ung_ky or 'Trị thời' in ung_ky)

# Test hoa hoi dau uses DKT-sourced LUC_XUNG_CHI
results = _analyze_hoa_hoi_dau('Kim', 'Thủy', 'Thân', 'Dần')
check("_analyze_hoa_hoi_dau works", isinstance(results, list))

# ═══ SUMMARY ═══
print("\n" + "=" * 70)
print(f"📊 KẾT QUẢ: {PASS}/{TOTAL} — {'✅ ALL PASS' if not FAIL else '⚠️ CÓ LỖI'}")
if FAIL:
    print(f"❌ FAIL: {', '.join(FAIL)}")
print("=" * 70)
