"""
V42.9.7 DEEP AUDIT: Kiểm tra AI Offline/Online có ĐỌC + ĐÁNH GIÁ hết 271 yếu tố không
+ Sơ đồ tương tác có lấy đủ không
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("🔬 DEEP AUDIT: AI ĐỌC ĐƯỢC BAO NHIÊU YẾU TỐ TỪ KNOWLEDGE TREE?")
print("=" * 80)

# ═══════════════════════════════════════════
# 1. KIỂM TRA free_ai_helper.py — AI Offline có đọc DKT không?
# ═══════════════════════════════════════════
print("\n" + "=" * 60)
print("📋 [1] AI OFFLINE — free_ai_helper.py ĐỌC Knowledge Tree?")
print("=" * 60)

content = open('free_ai_helper.py', 'r', encoding='utf-8').read()

# Check DKT import
print(f"\n  📥 Import DKT: {'✅ CÓ' if 'from divination_knowledge_tree import TREE as DKT' in content else '❌ KHÔNG'}")
print(f"  📥 DKT usage count: {content.count('DKT[')} lần truy cập trực tiếp")
print(f"  📥 DKT reference: {content.count('DKT')} lần nhắc đến")

# Check từng nhóm yếu tố có được sử dụng trong engine không
FACTOR_GROUPS = {
    # LH factors
    'luc_than': ['Thê Tài', 'Quan Quỷ', 'Phụ Mẫu', 'Huynh Đệ', 'Tử Tôn'],
    'luc_thu': ['Thanh Long', 'Chu Tước', 'Câu Trận', 'Đằng Xà', 'Bạch Hổ', 'Huyền Vũ'],
    'ngu_hanh': ['Kim', 'Mộc', 'Thủy', 'Hỏa', 'Thổ'],
    'luc_xung': ['Tý-Ngọ', 'Sửu-Mùi', 'Dần-Thân', 'Mão-Dậu'],
    'luc_hop': ['Tý-Sửu', 'Dần-Hợi', 'Mão-Tuất'],
    'truong_sinh': ['Trường Sinh', 'Đế Vượng', 'Mộ', 'Tuyệt'],
    'nguyet_kien': ['Nguyệt Kiến', 'Nguyệt Lệnh'],
    'nhat_than': ['Nhật Thần', 'Nhật'],
    'dong_hao': ['Động Hào', 'động'],
    'hoa_hao': ['Hóa Hào', 'Hóa'],
    'khong_vong_lh': ['Tuần Không', 'Không Vong'],
    'nguyet_pha': ['Nguyệt Phá'],
    'phan_ngam': ['Phản Ngâm', 'Phục Ngâm'],
    'am_dong': ['Ám Động', 'ám động'],
    'mo_kho': ['nhập Mộ', 'Mộ Khố'],
    
    # KM factors
    'bat_mon': ['Khai Môn', 'Hưu Môn', 'Sinh Môn', 'Tử Môn', 'Kinh Môn'],
    'cuu_tinh': ['Thiên Bồng', 'Thiên Nhậm', 'Thiên Xung', 'Thiên Tâm'],
    'bat_than': ['Trực Phù', 'Đằng Xà', 'Thái Âm', 'Lục Hợp', 'Bạch Hổ'],
    'tam_ky': ['Ất Kỳ', 'Bính Kỳ', 'Đinh Kỳ', 'Tam Kỳ'],
    'thien_can_km': ['Can Ngày', 'Can Giờ', 'can_ngay', 'can_gio'],
    'dia_chi_km': ['Chi Ngày', 'Chi Giờ', 'chi_ngay', 'chi_gio'],
    'cuu_cung': ['Cung 1', 'Cung', 'cung_'],
    'cach_cuc': ['Cát Cách', 'Hung Cách', 'cách cục'],
    'ma_tinh': ['Mã Tinh', 'Dịch Mã'],
    
    # MH factors
    'the_dung': ['Thể Quái', 'Dụng Quái', 'thể_quái', 'dụng_quái'],
    'sinh_khac_mh': ['Thể sinh Dụng', 'Dụng sinh Thể', 'Thể khắc Dụng', 'Dụng khắc Thể', 'Tỷ Hòa'],
    'bat_quai_mh': ['Càn', 'Đoài', 'Ly', 'Chấn', 'Tốn', 'Khảm', 'Cấn', 'Khôn'],
    'ho_quai': ['Hỗ Quái'],
    'bien_quai': ['Biến Quái'],
    
    # LN factors
    'thien_tuong': ['Thiên Tướng', 'Quý Nhân'],
    'tu_khoa': ['Tứ Khóa', 'Sơ Khóa', 'Trung Khóa', 'Mạt Khóa'],
    'tam_truyen': ['Tam Truyền', 'Sơ Truyền', 'Mạt Truyền'],
    
    # TA factors
    'thai_at': ['Thái Ất', 'thai_at'],
    'bat_tuong': ['Bát Tướng', 'bat_tuong'],
    
    # TV factors
    'chinh_tinh': ['Tử Vi', 'Thiên Cơ', 'Thái Dương', 'Vũ Khúc'],
    'phu_tinh': ['Tả Phụ', 'Hữu Bật', 'Văn Xương', 'Lộc Tồn'],
    
    # XND factors
    'hoang_dao': ['Hoàng Đạo', 'Hắc Đạo'],
    'truc_12': ['Kiến', 'Trừ', 'Mãn', 'Bình'],
}

print(f"\n  📊 KIỂM TRA {len(FACTOR_GROUPS)} NHÓM YẾU TỐ:")
found_groups = 0
missing_groups = []
partial_groups = []

for group_name, keywords in FACTOR_GROUPS.items():
    found = sum(1 for kw in keywords if kw in content)
    total = len(keywords)
    
    if found == total:
        status = "✅ ĐẦY ĐỦ"
        found_groups += 1
    elif found > 0:
        status = f"🟡 THIẾU ({found}/{total})"
        partial_groups.append((group_name, found, total))
        found_groups += 0.5
    else:
        status = f"❌ KHÔNG ĐỌC"
        missing_groups.append(group_name)
    
    print(f"    {status} — {group_name}: {found}/{total} keywords found")

# ═══════════════════════════════════════════
# 2. SCORING METHODS — Có dùng đủ yếu tố?
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print(f"📈 [2] SCORING METHODS — Có đánh giá đủ yếu tố?")
print(f"{'='*60}")

SCORING_CHECKS = {
    '_luc_hao_scoring': {
        'Nguyệt sinh': 'Nguyệt' in content and 'sinh' in content,
        'Nhật sinh/khắc': 'Nhật' in content,
        'Động Hào': 'Động' in content and 'Hào' in content,
        'Hóa Hào': 'Hóa' in content,
        'Tuần Không': 'Tuần Không' in content or 'tuan_khong' in content,
        'Nguyệt Phá': 'Nguyệt Phá' in content or 'nguyet_pha' in content,
        'Phản Ngâm': 'Phản Ngâm' in content or 'phan_ngam' in content,
        'Ám Động': 'Ám Động' in content or 'am_dong' in content,
        '12 Trường Sinh': 'Trường Sinh' in content,
        'Mộ Khố': 'Mộ' in content and ('Khố' in content or 'nhập Mộ' in content),
        'Lục Thú': 'Thanh Long' in content or 'luc_thu' in content,
        'Lục Xung': 'Lục Xung' in content or 'xung' in content,
        'Lục Hợp': 'Lục Hợp' in content or 'hop' in content,
    },
    '_ky_mon_scoring': {
        'Bát Môn': 'Bát Môn' in content or 'bat_mon' in content,
        'Cửu Tinh': 'Cửu Tinh' in content or 'cuu_tinh' in content,
        'Bát Thần': 'Bát Thần' in content or 'bat_than' in content,
        'Tam Kỳ': 'Tam Kỳ' in content or 'tam_ky' in content,
        'Cách Cục': 'Cách' in content or 'cach_cuc' in content,
        'Thiên Can': 'can_ngay' in content or 'Can Ngày' in content,
        'Cung sinh/khắc': 'cung' in content and ('sinh' in content or 'khắc' in content),
    },
    '_mai_hoa_scoring': {
        'Thể/Dụng': 'thể' in content.lower() or 'the_quai' in content,
        'Sinh Khắc': 'sinh' in content and 'khắc' in content,
        'Hỗ Quái': 'Hỗ' in content or 'ho_quai' in content,
        'Biến Quái': 'Biến' in content or 'bien_quai' in content,
    },
}

for method, checks in SCORING_CHECKS.items():
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    pct = int(passed / total * 100)
    print(f"\n  📊 {method}: {passed}/{total} ({pct}%)")
    for check_name, ok in checks.items():
        print(f"    {'✅' if ok else '❌'} {check_name}")

# ═══════════════════════════════════════════
# 3. AI ONLINE — Gemini nhận đủ data không?
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print(f"🤖 [3] AI ONLINE (Gemini) — Nhận đủ data?")
print(f"{'='*60}")

online_checks = {
    'offline_analysis_data sent': 'offline_analysis_data' in content,
    'unified_narrative sent': 'unified_narrative' in content,
    'weighted_pct sent': 'weighted_pct' in content,
    'verdicts sent': 'ky_mon_verdict' in content and 'luc_hao_verdict' in content,
    'lh_factors sent': 'lh_factors' in content or 'v23_lh_factors' in content,
    'km_factors sent': 'km_factors' in content or 'v24_km_factors' in content,
    'direct_answer sent': 'direct_answer' in content,
    'impact_evidence sent': 'impact_evidence' in content,
}
for name, ok in online_checks.items():
    print(f"  {'✅' if ok else '❌'} {name}")

# ═══════════════════════════════════════════
# 4. SƠ ĐỒ TƯƠNG TÁC — Có tham chiếu đủ?
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print(f"📊 [4] SƠ ĐỒ TƯƠNG TÁC — Tham chiếu yếu tố?")
print(f"{'='*60}")

try:
    diag_content = open('interaction_diagrams.py', 'r', encoding='utf-8').read()
    
    DIAGRAM_FACTOR_CHECKS = {
        'Kỳ Môn (Bát Môn/Cửu Tinh)': any(k in diag_content for k in ['Bát Môn', 'Cửu Tinh', 'bat_mon', 'ky_mon']),
        'Lục Hào (Dụng Thần/Lục Thân)': any(k in diag_content for k in ['Dụng Thần', 'Lục Thân', 'luc_hao']),
        'Mai Hoa (Thể/Dụng)': any(k in diag_content for k in ['Thể Quái', 'Dụng Quái', 'mai_hoa', 'Mai Hoa']),
        'Đại Lục Nhâm': any(k in diag_content for k in ['Lục Nhâm', 'luc_nham']),
        'Thái Ất': any(k in diag_content for k in ['Thái Ất', 'thai_at']),
        'Thiết Bản': any(k in diag_content for k in ['Thiết Bản', 'thiet_ban']),
        'Tử Vi': any(k in diag_content for k in ['Tử Vi', 'tu_vi']),
        'Xem Ngày': any(k in diag_content for k in ['Xem Ngày', 'xem_ngay']),
        '12 Trường Sinh': any(k in diag_content for k in ['Trường Sinh', 'truong_sinh']),
        'Ngũ Hành Sinh Khắc': any(k in diag_content for k in ['Ngũ Hành', 'sinh_khac', 'Sinh Khắc']),
        'Vạn Vật Loại Tượng': any(k in diag_content for k in ['Vạn Vật', 'van_vat']),
        'Conflict Detection': any(k in diag_content for k in ['xung_dot', 'Xung Đột', 'conflict']),
    }
    
    for name, ok in DIAGRAM_FACTOR_CHECKS.items():
        print(f"  {'✅' if ok else '❌'} {name}")
        
except Exception as e:
    print(f"  ❌ Cannot read interaction_diagrams.py: {e}")

# ═══════════════════════════════════════════
# 5. DKT INTEGRATION — Tree dùng ở đâu?
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print(f"🌳 [5] DKT (Knowledge Tree) — Thực tế dùng ở đâu?")
print(f"{'='*60}")

import re
dkt_usages = re.findall(r"DKT\[(['\"][^'\"]+['\"])\]", content)
dkt_keys = set()
for u in dkt_usages:
    dkt_keys.add(u.strip("'\""))

print(f"  📊 DKT được truy cập {len(dkt_usages)} lần")
print(f"  📊 Các key: {', '.join(sorted(dkt_keys)) if dkt_keys else 'KHÔNG CÓ'}")

# Check nếu DKT chỉ import nhưng không thực sự dùng sâu
dkt_deep = content.count("DKT.get(") + content.count("DKT[")
print(f"  📊 Deep access (DKT.get + DKT[]): {dkt_deep} lần")

if dkt_deep < 5:
    print(f"\n  ⚠️ CẢNH BÁO: DKT chỉ được truy cập {dkt_deep} lần!")
    print(f"     → AI Offline có thể KHÔNG đọc đủ yếu tố từ Knowledge Tree")
    print(f"     → Cần tích hợp DKT sâu hơn vào scoring/analysis functions")

# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════
print(f"\n{'='*80}")
print(f"📊 TÓM TẮT DEEP AUDIT")
print(f"{'='*80}")
print(f"  ❌ Nhóm YẾU TỐ AI KHÔNG ĐỌC: {len(missing_groups)}")
for mg in missing_groups:
    print(f"     → {mg}")
print(f"  🟡 Nhóm THIẾU MỘT PHẦN: {len(partial_groups)}")
for pg in partial_groups:
    print(f"     → {pg[0]}: {pg[1]}/{pg[2]}")
print(f"  ✅ Nhóm ĐẦY ĐỦ: {int(found_groups)}/{len(FACTOR_GROUPS)}")
print(f"{'='*80}")
