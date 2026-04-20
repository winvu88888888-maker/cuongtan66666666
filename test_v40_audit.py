"""AUDIT V40: Kiểm tra TOÀN DIỆN luận giải AI Online + AI Offline
- Kiểm tra data nào đang được truyền vào
- Kiểm tra output có đủ phần không
- So sánh Online vs Offline
"""
import sys, json, re
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper

ai = FreeAIHelper()

question = "Mua nhà năm nay có tốt không?"
print("=" * 80)
print(f"AUDIT: {question}")
print("=" * 80)

# Monkey-patch để capture offline_analysis_data
_captured_data = {}
_original_try = ai._try_online_ai

def _mock_try(question, chart_data=None, mai_hoa_data=None, luc_hao_data=None, topic=None, offline_analysis_data=None):
    _captured_data['offline_analysis_data'] = offline_analysis_data
    _captured_data['chart_data'] = chart_data
    _captured_data['luc_hao_data'] = luc_hao_data
    _captured_data['mai_hoa_data'] = mai_hoa_data
    # Gọi thật nhưng sẽ fail vì không có API key → OK, ta chỉ cần capture data
    return _original_try(question, chart_data, mai_hoa_data, luc_hao_data, topic, offline_analysis_data)

ai._try_online_ai = _mock_try

result = ai.answer_question(question)

print(f"\n{'=' * 80}")
print("PHẦN 1: KIỂM TRA DỮ LIỆU ĐẦU VÀO (offline_analysis_data)")
print("=" * 80)

od = _captured_data.get('offline_analysis_data', {})
if not od:
    print("  ❌ KHÔNG CÓ offline_analysis_data!")
else:
    # Kiểm tra từng field
    REQUIRED_FIELDS = {
        # Core verdicts
        'dung_than': 'Dụng Thần',
        'category_label': 'Nhóm câu hỏi',
        'ky_mon_verdict': 'KM Verdict',
        'ky_mon_reason': 'KM Reason',
        'luc_hao_verdict': 'LH Verdict', 
        'luc_hao_reason': 'LH Reason',
        'mai_hoa_verdict': 'MH Verdict',
        'mai_hoa_reason': 'MH Reason',
        'luc_nham_verdict': 'LN Verdict',
        'luc_nham_reason': 'LN Reason',
        'thai_at_verdict': 'TA Verdict',
        'thai_at_reason': 'TA Reason',
        # Factors (V26.2)
        'v23_lh_factors': 'LH Factors (chi tiết)',
        'v24_km_factors': 'KM Factors (chi tiết)',
        'v24_mh_factors': 'MH Factors (chi tiết)',
        'v24_tb_factors': 'TB Factors (chi tiết)',
        'v24_ln_factors': 'LN Factors (chi tiết)',
        'v24_ta_factors': 'TA Factors (chi tiết)',
        # Scoring
        'v16_lh_score': 'LH Score',
        'v16_mh_score': 'MH Score',
        'v16_tb_score': 'TB Score',
        'v16_ln_score': 'LN Score',
        'v16_ta_score': 'TA Score',
        # V15 Analysis
        'v15_bt_score': 'BT Score (cung BT)',
        'v15_dt_score': 'DT Score (cung DT)',
        'v15_timeline': 'Timeline (xu hướng)',
        'v15_timing': 'Timing (ứng kỳ)',
        # V17 Routing
        'v17_routing': 'Method Routing',
        'v17_primary_method': 'PP Chính',
        'v17_primary_verdict': 'PP Chính Verdict',
        # V18 Detective
        'v18_detective': 'Thám Tử Kiểm Chứng',
        # V22 Unified
        'v22_unified_strength': 'Lực Lượng Tổng Hợp',
        # V31 Diagrams
        'v31_master_diagram': 'SĐ Master',
        'v31_question_diagram': 'SĐ Câu hỏi',
        'v31_diagram_id': 'Diagram ID',
        'v31_master_conclusion': 'Master Conclusion',
        # Impact
        'impact_evidence': 'Impact Evidence',
        'unified_narrative': 'Unified Narrative',
        # Full report
        'full_offline_report': 'Full Offline Report',
    }
    
    present = 0
    missing = 0
    empty = 0
    
    for field, label in REQUIRED_FIELDS.items():
        val = od.get(field)
        if val is None:
            print(f"  ❌ MISSING: {label} ({field})")
            missing += 1
        elif isinstance(val, str) and len(val) == 0:
            print(f"  ⚠️ EMPTY:   {label} ({field})")
            empty += 1
        elif isinstance(val, list) and len(val) == 0:
            print(f"  ⚠️ EMPTY[]: {label} ({field}) — 0 items")
            empty += 1
        elif isinstance(val, dict) and len(val) == 0:
            print(f"  ⚠️ EMPTY{{}}: {label} ({field})")
            empty += 1
        else:
            size = len(val) if isinstance(val, (str, list, dict)) else str(val)[:30]
            print(f"  ✅ OK:      {label} = {size if isinstance(size, int) else size}")
            present += 1
    
    print(f"\n  TỔNG: {present} OK, {missing} MISSING, {empty} EMPTY / {len(REQUIRED_FIELDS)} fields")

# Chi tiết factors
print(f"\n{'=' * 80}")
print("PHẦN 2: CHI TIẾT FACTORS (Dữ liệu thô từ mỗi PP)")
print("=" * 80)

for fname, label in [
    ('v23_lh_factors', 'LỤC HÀO'),
    ('v24_km_factors', 'KỲ MÔN'),
    ('v24_mh_factors', 'MAI HOA'),
    ('v24_tb_factors', 'THIẾT BẢN'),
    ('v24_ln_factors', 'LỤC NHÂM'),
    ('v24_ta_factors', 'THÁI ẤT'),
]:
    factors = od.get(fname, [])
    if not factors:
        print(f"\n  ❌ {label}: KHÔNG CÓ FACTORS!")
    else:
        items = factors if isinstance(factors, list) else [factors]
        total_score = 0
        for f in items:
            m = re.search(r'([+-]\d+)\s*$', str(f))
            if m: total_score += int(m.group(1))
        print(f"\n  ✅ {label}: {len(items)} factors, Σ={total_score:+d}")
        for f in items[:5]:
            print(f"     • {str(f)[:90]}")
        if len(items) > 5:
            print(f"     ... (+{len(items)-5} more)")

# Kiểm tra unified strength
print(f"\n{'=' * 80}")
print("PHẦN 3: LỰC LƯỢNG TỔNG HỢP (V22)")
print("=" * 80)

v22 = od.get('v22_unified_strength', {})
if v22:
    for k, v in v22.items():
        if isinstance(v, dict):
            print(f"  {k}: {len(v)} items")
        else:
            print(f"  {k}: {v}")
else:
    print("  ❌ KHÔNG CÓ v22_unified_strength!")

# Kiểm tra diagrams
print(f"\n{'=' * 80}")
print("PHẦN 4: SƠ ĐỒ TƯƠNG TÁC (V31)")
print("=" * 80)

master = od.get('v31_master_diagram', '')
q_diagram = od.get('v31_question_diagram', '')
print(f"  SĐ Master:   {'✅ ' + str(len(master)) + ' chars' if master else '❌ MISSING'}")
print(f"  SĐ Question:  {'✅ ' + str(len(q_diagram)) + ' chars' if q_diagram else '❌ MISSING'}")
print(f"  Diagram ID:   {od.get('v31_diagram_id', '?')}")
print(f"  Conclusion:   {str(od.get('v31_master_conclusion', ''))[:100]}")

# Kiểm tra chart_data (Kỳ Môn raw)
print(f"\n{'=' * 80}")
print("PHẦN 5: KỲ MÔN RAW DATA (chart_data)")
print("=" * 80)

cd = _captured_data.get('chart_data', {})
if cd and isinstance(cd, dict):
    KM_FIELDS = ['can_ngay', 'chi_ngay', 'can_gio', 'chi_gio', 'can_thang', 'chi_thang',
                 'can_nam', 'tiet_khi', 'cuc', 'don_trung',
                 'can_thien_ban', 'thien_ban', 'nhan_ban', 'than_ban', 'dia_can']
    for f in KM_FIELDS:
        val = cd.get(f)
        if val is None:
            print(f"  ❌ {f}: MISSING")
        elif isinstance(val, dict) and len(val) == 0:
            print(f"  ⚠️ {f}: EMPTY dict")
        else:
            size = len(val) if isinstance(val, dict) else str(val)[:40]
            print(f"  ✅ {f}: {size}")
else:
    print("  ❌ chart_data KHÔNG CÓ!")

# Kiểm tra luc_hao_data raw
print(f"\n{'=' * 80}")
print("PHẦN 6: LỤC HÀO RAW DATA (luc_hao_data)")
print("=" * 80)

lh = _captured_data.get('luc_hao_data', {})
if lh and isinstance(lh, dict):
    LH_FIELDS = ['ten_que', 'ten_thuong', 'ten_ha', 'hanh_thuong', 'hanh_ha',
                 'ban', 'dong_hao', 'chi_thang', 'chi_ngay']
    for f in LH_FIELDS:
        val = lh.get(f)
        if val is None:
            print(f"  ❌ {f}: MISSING")
        elif isinstance(val, (dict, list)) and len(val) == 0:
            print(f"  ⚠️ {f}: EMPTY")
        else:
            if isinstance(val, dict):
                haos = val.get('haos', val.get('details', []))
                print(f"  ✅ {f}: dict, {len(haos)} hào" if isinstance(haos, list) else f"  ✅ {f}: dict")
            elif isinstance(val, list):
                print(f"  ✅ {f}: {len(val)} items")
            else:
                print(f"  ✅ {f}: {str(val)[:40]}")
else:
    print("  ❌ luc_hao_data KHÔNG CÓ!")

# Kiểm tra mai_hoa_data raw
print(f"\n{'=' * 80}")
print("PHẦN 7: MAI HOA RAW DATA (mai_hoa_data)")
print("=" * 80)

mh = _captured_data.get('mai_hoa_data', {})
if mh and isinstance(mh, dict):
    MH_FIELDS = ['ten', 'ten_que', 'ten_thuong', 'ten_ha', 'thuong_quai', 'ha_quai',
                 'hanh_thuong', 'hanh_ha', 'ho_quai', 'bien_quai', 'tuong', 'nghia']
    for f in MH_FIELDS:
        val = mh.get(f)
        if val is None:
            print(f"  ❌ {f}: MISSING")
        elif isinstance(val, str) and len(val) == 0:
            print(f"  ⚠️ {f}: EMPTY")
        else:
            print(f"  ✅ {f}: {str(val)[:50]}")
else:
    print("  ❌ mai_hoa_data KHÔNG CÓ!")

# Kiểm tra OUTPUT cuối cùng
print(f"\n{'=' * 80}")
print("PHẦN 8: KIỂM TRA OUTPUT CUỐI CÙNG")
print("=" * 80)

if result:
    # Check sections
    SECTIONS = [
        ('AI ONLINE', ['AI ONLINE', '🌐 AI ONLINE']),
        ('AI OFFLINE Protocol 27', ['PROTOCOL 27', 'AI OFFLINE — PROTOCOL']),
        ('AI OFFLINE Detail', ['AI OFFLINE — PHÂN TÍCH']),
        ('PHÁN QUYẾT/KẾT LUẬN', ['📢', 'PHÁN QUYẾT', 'CÂU TRẢ LỜI']),
        ('VÌ SAO', ['📋 VÌ SAO', 'VÌ SAO']),
        ('ỨNG KỲ', ['⏳ ỨNG KỲ', 'ỨNG KỲ']),
        ('GIẢI PHÁP', ['🔧 GIẢI PHÁP', 'GIẢI PHÁP']),
        ('Thám Tử Kiểm Chứng', ['THÁM TỬ KIỂM CHỨNG', '🔍 THÁM TỬ']),
        ('SĐ Master', ['SĐ MASTER', 'DỤNG THẦN → SUY VƯỢNG']),
        ('SĐ Question', ['CHÚ GIẢI', 'SĐ']),
        ('Tam Thời', ['TAM THỜI', '⏰']),
        ('Lục Hào Detail', ['LỤC HÀO', 'Lục Hào']),
        ('Kỳ Môn Detail', ['KỲ MÔN', 'Kỳ Môn']),
        ('Mai Hoa Detail', ['MAI HOA', 'Mai Hoa']),
        ('Đại Lục Nhâm', ['ĐẠI LỤC NHÂM']),
        ('Thái Ất', ['THÁI ẤT']),
        ('Vạn Vật Loại Tượng', ['VẠN VẬT', 'Vạn Vật']),
        ('12 Trường Sinh', ['Trường Sinh', 'TRƯỜNG SINH']),
    ]
    
    for section_name, keywords in SECTIONS:
        found = any(kw in result for kw in keywords)
        count = sum(result.count(kw) for kw in keywords)
        if found:
            print(f"  ✅ {section_name}: FOUND ({count} mentions)")
        else:
            print(f"  ❌ {section_name}: MISSING!")
    
    # Check if Online or Offline only
    has_online = 'AI ONLINE' in result and '🌐' in result
    print(f"\n  Mode: {'AI ONLINE + OFFLINE' if has_online else 'AI OFFLINE ONLY (no API key)'}")
    print(f"  Total output: {len(result)} chars")
else:
    print("  ❌ KHÔNG CÓ OUTPUT!")

print(f"\n{'=' * 80}")
print("AUDIT HOÀN TẤT")
print("=" * 80)
