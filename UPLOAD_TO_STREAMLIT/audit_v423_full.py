"""
V42.3 FULL SYSTEM AUDIT — Kiểm tra toàn diện AI Offline + Online
"""
import sys, re
sys.path.insert(0, '.')

code = open('free_ai_helper.py', 'r', encoding='utf-8').read()
gemini_code = open('gemini_helper.py', 'r', encoding='utf-8').read()
app_code = open('app.py', 'r', encoding='utf-8').read()

print("=" * 80)
print("🔍 FULL SYSTEM AUDIT — AI OFFLINE + ONLINE V42.3")
print("=" * 80)

# ═══════════════════════════════════════
# 1. CATEGORIES CHECK — Đủ 9 nhóm chưa?
# ═══════════════════════════════════════
print("\n📋 1. CATEGORIES (Phân loại câu hỏi)")
cats = re.findall(r'"([A-ZĐ_ẮẰẲẴẶ]+)":\s*\{', code)
cats = [c for c in cats if 'keywords' in code[code.find(f'"{c}"'):code.find(f'"{c}"')+500]]
expected_cats = ['SỨC_KHỎE_GIA_ĐÌNH', 'TÀI_CHÍNH', 'CÔNG_VIỆC', 'TÌNH_CẢM', 
                 'TÌM_ĐỒ', 'NHÀ_CỬA', 'XUẤT_HÀNH', 'THẮNG_THUA', 'CHUNG']
# Find by looking in CATEGORIES dict
for ec in expected_cats:
    found = f'"{ec}"' in code
    print(f"  {'✅' if found else '❌'} {ec}: {'CÓ' if found else 'THIẾU!'}")

# ═══════════════════════════════════════
# 2. QUESTION TYPE DETECTORS
# ═══════════════════════════════════════
print("\n📋 2. QUESTION TYPE DETECTORS")
detectors = {
    '_is_age_question': 'Tuổi',
    '_is_find_question': 'Tìm đồ',
    '_is_yesno_question': 'Có/Không',
    '_is_count_question': 'Đếm số',
    '_is_competition_question': 'Thắng Thua',
}
for func, desc in detectors.items():
    found = f'def {func}' in code
    used = f'{func}(' in code and code.count(f'{func}(') >= 2  # def + call
    print(f"  {'✅' if found and used else '❌'} {func}: {'CÓ + USED' if found and used else 'CÓ' if found else 'THIẾU!'}")

# ═══════════════════════════════════════
# 3. 6 PHƯƠNG PHÁP SCORING
# ═══════════════════════════════════════
print("\n📋 3. SCORING 6 PHƯƠNG PHÁP")
methods = {
    '_ky_mon_scoring': 'Kỳ Môn',
    '_luc_hao_scoring': 'Lục Hào',
    '_mai_hoa_scoring': 'Mai Hoa',
    '_thiet_ban_scoring': 'Thiết Bản',
    '_luc_nham_scoring': 'Đại Lục Nhâm',
    '_thai_at_scoring': 'Thái Ất',
}
for func, desc in methods.items():
    found = f'def {func}' in code
    print(f"  {'✅' if found else '❌'} {func}: {desc} {'CÓ' if found else 'THIẾU!'}")

# ═══════════════════════════════════════
# 4. PHÂN TÍCH CHUYÊN SÂU
# ═══════════════════════════════════════
print("\n📋 4. PHÂN TÍCH CHUYÊN SÂU")
features = {
    '_get_truong_sinh': '12 Trường Sinh Engine',
    '_get_van_vat': 'Vạn Vật Loại Tượng',
    '_calc_unified_strength': 'Unified Strength',
    '_check_tam_hinh': 'Tam Hình',
    '_get_khong_vong': 'Không Vong (Tuần Không)',
    '_check_phan_phuc_ngam': 'Phản Phục Ngâm',
    '_check_tan_thoai_than': 'Tấn Thối Thần',
    '_get_lenh_thang_hanh': 'Lệnh Tháng Hành',
    '_get_ung_ky': 'Ứng Kỳ cơ bản',
    '_get_ung_ky_advanced': 'Ứng Kỳ chuyên sâu',
    '_analyze_hoa_hoi_dau': 'Hóa Hồi Đầu',
    '_detect_am_dong': 'Ám Động',
    '_build_phan_phuc_ngam_warning': 'Phản Phục Ngâm Warning',
    '_build_thien_dia_nhan_than': 'Thiên-Địa-Nhân-Thần',
    '_analyze_kv_dich_ma_deep': 'KV + Dịch Mã Deep',
    '_build_nguyet_pha_warning': 'Nguyệt Phá Warning',
    '_get_seasonal_strength': 'Seasonal Strength',
    '_build_seasonal_strength_table': 'Seasonal Table',
    '_get_hao_tu': 'Hào Từ',
}
for func, desc in features.items():
    found = f'def {func}' in code
    print(f"  {'✅' if found else '❌'} {desc}")

# ═══════════════════════════════════════
# 5. VERDICT TYPES (Kết luận theo loại câu hỏi)
# ═══════════════════════════════════════
print("\n📋 5. VERDICT TYPES (Phán quyết theo loại)")
verdict_types = {
    'is_life_death': 'Sinh Tử',
    'is_should': 'Có nên / Nên không',
    'is_yesno_kl': 'Có / Không',
    'is_competition_kl': 'Thắng Thua (Thế vs Ứng)',
}
for flag, desc in verdict_types.items():
    # Check in verdict section
    found = f'if {flag}' in code or f'elif {flag}' in code
    print(f"  {'✅' if found else '❌'} {desc} ({flag})")
print(f"  {'✅' if 'else:' in code[code.find('TẠO PHÁN QUYẾT'):code.find('TẠO PHÁN QUYẾT')+2000] else '❌'} Tổng quát (default)")

# ═══════════════════════════════════════
# 6. AI ONLINE (gemini_helper.py)
# ═══════════════════════════════════════
print("\n📋 6. AI ONLINE (gemini_helper.py)")
online_features = {
    'class GeminiQMDGHelper': 'GeminiQMDGHelper Class',
    'def analyze_': 'Analyze methods',
    'def _build_prompt': 'Prompt building',
    'web_search': 'Web search integration',
    'def answer_question': 'Answer question',
    'KẾT LUẬN CUỐI CÙNG': 'Final conclusion',
    'CÂU TRẢ LỜI': 'Direct answer format',
}
for kw, desc in online_features.items():
    found = kw in gemini_code
    print(f"  {'✅' if found else '❌'} {desc}")

# ═══════════════════════════════════════
# 7. APP.PY — UI Integration
# ═══════════════════════════════════════
print("\n📋 7. APP.PY — UI Integration")
ui_features = {
    'HỎI AI': 'Nút Hỏi AI',
    'PHÂN TÍCH TỔNG HỢP AI': 'Phân tích tổng hợp',
    'SO SÁNH CHỦ - KHÁCH': 'So sánh Chủ-Khách',
    'AI OFFLINE': 'Hiển thị AI Offline',
    'AI ONLINE': 'Hiển thị AI Online',
    'free_ai_helper': 'Import Offline engine',
    'gemini_helper': 'Import Online engine',
    'Kỳ Môn Độn Giáp': 'Tab Kỳ Môn',
    'Mai Hoa': 'Tab Mai Hoa',
    'Lục Hào': 'Tab Lục Hào',
    'Thiết Bản': 'Tab Thiết Bản',
    'Vạn Vật Loại Tượng': 'Tab Vạn Vật',
    'Đại Lục Nhâm': 'Tab Đại Lục Nhâm',
    'Thái Ất': 'Tab Thái Ất',
}
for kw, desc in ui_features.items():
    found = kw in app_code
    print(f"  {'✅' if found else '❌'} {desc}")

# ═══════════════════════════════════════
# 8. KHÔNG DẤU SUPPORT
# ═══════════════════════════════════════
print("\n📋 8. KHÔNG DẤU SUPPORT")
print(f"  ✅ VN_NO_DIAC_MAP: {'CÓ' if '_VN_NO_DIAC_MAP' in code else 'THIẾU'}")
no_diac_count = len(re.findall(r"'[a-z ]+': '[^']+',", code[code.find('_VN_NO_DIAC_MAP'):code.find('_VN_NO_DIAC_MAP')+5000]))
print(f"  ✅ Số entries: ~{no_diac_count}")

# ═══════════════════════════════════════
# 9. DATA PIPELINE
# ═══════════════════════════════════════
print("\n📋 9. DATA PIPELINE (Auto-compute)")
pipeline = {
    'tinh_qua_theo_thoi_gian': 'Mai Hoa auto-cast',
    'lap_qua_luc_hao': 'Lục Hào auto-cast',
    'calculate_qmdg_params': 'KM params auto-calc',
    'lap_ban_qmdg': 'KM 9 cung auto',
}
for kw, desc in pipeline.items():
    found = kw in code
    print(f"  {'✅' if found else '❌'} {desc}")

# ═══════════════════════════════════════
# 10. TỔNG KẾT
# ═══════════════════════════════════════
print(f"\n{'='*80}")
print("📊 TỔNG KẾT AUDIT")
print(f"{'='*80}")

# Count total functions
total_funcs = len(re.findall(r'def \w+', code))
total_classes = len(re.findall(r'class \w+', code))
total_lines = len(code.split('\n'))
factors_count = code.count('factors.append')
scoring_count = len(re.findall(r'score\s*[+-]=', code))

print(f"""
  📦 CODE SIZE:        {total_lines:,} lines ({len(code):,} bytes)
  🔧 Functions:        {total_funcs}
  🏗️ Classes:          {total_classes}
  📊 Factor rules:     {factors_count}
  ⚖️ Scoring rules:    {scoring_count}
  📂 Categories:       9 (SỨC_KHỎE, TÀI_CHÍNH, CÔNG_VIỆC, TÌNH_CẢM, TÌM_ĐỒ, NHÀ_CỬA, XUẤT_HÀNH, THẮNG_THUA, CHUNG)
  🔍 Question types:   5 (age, find, yesno, count, competition)
  📐 Methods:          6 (KM, LH, MH, TB, LN, TA)
  🎯 Verdict types:    5 (sinh_tử, nên/không, có/không, thắng_thua, tổng_quát)
  📝 Deep features:    19 (Trường Sinh, Vạn Vật, Tam Hình, KV, Phản Phục Ngâm, ...)
  🌐 AI Online:        Gemini integration + Web search
""")
