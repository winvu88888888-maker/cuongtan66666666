import re

helper = open('free_ai_helper.py','r',encoding='utf-8').read()

# Tìm tất cả key trong offline_analysis_data
start = helper.find('offline_analysis_data = {')
end = helper.find("# Gọi AI Online (Gemini)")
od_section = helper[start:end]
keys = re.findall(r"'([^']+)'\s*:", od_section)
print('='*80)
print(f'ONLINE DATA DICT: {len(keys)} trường được gửi cho Gemini')
print('='*80)
for k in keys:
    print(f'  ✅ {k}')

# Kiểm tra tất cả BƯỚC phân tích
print()
print('='*80)
print('CÁC BƯỚC PHÂN TÍCH TRONG OFFLINE OUTPUT')
print('='*80)
buoc_pattern = re.findall(r"(BƯỚC \d+[^\n]{0,60})", helper)
seen = set()
for b in buoc_pattern:
    b_clean = b.strip()
    if b_clean not in seen and len(b_clean) > 8:
        seen.add(b_clean)
        print(f'  📌 {b_clean}')

# Kiểm tra module nào CHƯA được dùng
print()
print('='*80)
print('MODULE BỊ BỎ SÓT (Có file nhưng KHÔNG import)')
print('='*80)
missing_modules = {
    'mai_hoa_v2.py': 'giai_qua() — giải quẻ Mai Hoa chi tiết',
    'qmdg_calc.py': 'calculate_qmdg_params() — tính toán tham số KỲ MÔN',
    'qmdg_advanced_rules.py': 'phan_tich_tim_do_chi_tiet() — phân tích TÌM ĐỒ + MÀU SẮC + KHOẢNG CÁCH',
    'qmdg_inference_rules.py': 'xac_dinh_ke_lay(), tinh_gia_tri_vat() — xác định KẺ LẤY + GIÁ TRỊ VẬT',
    'blind_reading.py': 'blind_read() — đọc mù quẻ (không cần câu hỏi)',
    'iching_integrated_data.py': 'ICHING_HEXAGRAMS — 64 quẻ Kinh Dịch DỮ LIỆU ĐẦY ĐỦ',
    'integrated_knowledge_base.py': 'get_comprehensive_palace_info() — tra cứu cung chi tiết',
    'phan_tich_da_tang.py': 'phan_tich_toan_dien() — phân tích đa tầng + TƯƠNG TÁC GIỮA CUNG',
    'database_tuong_tac.py': 'TUONG_TAC_SAO_MON — bảng tương tác Sao-Môn + QUY TẮC CHỌN DỤNG THẦN',
}
for m, desc in missing_modules.items():
    print(f'  ❌ {m}: {desc}')

# Check thiet_ban_than_toan.json
print()
print('='*80)
print('KIỂM TRA THIẾT BẢN THẦN TOÁN (JSON)')
print('='*80)
import json
try:
    tb = json.load(open('thiet_ban_than_toan.json','r',encoding='utf-8'))
    if isinstance(tb, dict):
        print(f'  ✅ thiet_ban_than_toan.json: {len(tb)} entries')
        print(f'     Keys mẫu: {list(tb.keys())[:5]}')
    elif isinstance(tb, list):
        print(f'  ✅ thiet_ban_than_toan.json: {len(tb)} entries (list)')
except Exception as e:
    print(f'  ❌ Lỗi đọc: {e}')

# Check data gửi cho Gemini prompt có đủ không
print()
print('='*80)
print('KIỂM TRA GEMINI PROMPT ĐÃ CÓ ĐỦ DỮ LIỆU CHƯA')
print('='*80)
prompt_section = helper[helper.find('deep_prompt = ('):helper.find('</reasoning_protocol>')]
checks = {
    'Kỳ Môn verdicts': 'ky_mon_verdict' in prompt_section,
    'Lục Hào verdicts': 'luc_hao_verdict' in prompt_section,
    'Mai Hoa verdicts': 'mai_hoa_verdict' in prompt_section,
    'Đại Lục Nhâm verdicts': 'luc_nham_verdict' in prompt_section,
    'Thái Ất verdicts': 'thai_at_verdict' in prompt_section,
    'V15 BT Score': 'v15_bt_score' in prompt_section,
    'V15 DT Score': 'v15_dt_score' in prompt_section,
    'V16 LH Score': 'v16_lh_score' in prompt_section,
    'V17 Routing': 'v17_routing' in prompt_section,
    'V18 Detective': 'v18_detective' in prompt_section,
    'V22 Unified Strength': 'unified_pct' in prompt_section or 'v22_unified' in prompt_section,
    'Full offline report': 'full_offline_report' in prompt_section,
    'RAG prompt': 'rag_prompt' in prompt_section,
    'Verdict Summary': 'verdict_summary' in prompt_section,
    'Lục Nhâm raw data': 'luc_nham_ctx' in prompt_section,
    'Thái Ất raw data': 'thai_at_ctx' in prompt_section,
    'Khẩu Quyết Lục Hào': 'KHẨU QUYẾT' in prompt_section or 'khẩu quyết' in prompt_section.lower(),
    'Phương pháp Mai Hoa': 'THỂ DỤNG' in prompt_section,
    'Phương pháp Kỳ Môn': '4 TẦNG' in prompt_section,
    'V23 LH factors': 'v23_lh_factors' in od_section,
    'V24 KM factors': 'v24_km_factors' in od_section,
    'V24 MH factors': 'v24_mh_factors' in od_section,
    'V24 TB factors': 'v24_tb_factors' in od_section,
    'V24 LN factors': 'v24_ln_factors' in od_section,
    'V24 TA factors': 'v24_ta_factors' in od_section,
}
for name, ok in checks.items():
    icon = '✅' if ok else '❌'
    print(f'  {icon} {name}')
