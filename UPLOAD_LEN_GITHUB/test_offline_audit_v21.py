"""
AUDIT TOÀN DIỆN AI OFFLINE V20.5
=================================
Test 20+ kịch bản câu hỏi → Tìm tất cả điểm yếu, sai, thiếu.
Output: Bảng tổng hợp vấn đề + đề xuất nâng cấp V21.0
"""

import sys
import os
import json
import datetime
import traceback

# Ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from free_ai_helper import FreeAIHelper, _get_truong_sinh, _ngu_hanh_relation, CHI_NGU_HANH, CAN_NGU_HANH, SINH, KHAC, TRUONG_SINH_STAGES, CHI_ORDER

# ═══════════════════════════════════════════════════
# MOCK DATA — Giả lập dữ liệu quẻ thực tế
# ═══════════════════════════════════════════════════

MOCK_CHART_DATA = {
    'can_ngay': 'Giáp',
    'chi_ngay': 'Tý',
    'can_thang': 'Bính',
    'chi_thang': 'Dần',
    'can_nam': 'Ất',
    'chi_nam': 'Tị',
    'can_gio': 'Canh',
    'chi_gio': 'Ngọ',
    'can_thien_ban': {1: 'Ất', 2: 'Kỷ', 3: 'Đinh', 4: 'Bính', 5: 'Mậu', 6: 'Canh', 7: 'Tân', 8: 'Nhâm', 9: 'Quý'},
    'can_dia_ban': {1: 'Nhâm', 2: 'Kỷ', 3: 'Canh', 4: 'Tân', 5: 'Mậu', 6: 'Ất', 7: 'Bính', 8: 'Đinh', 9: 'Giáp'},
    'thien_ban': {1: 'Thiên Bồng', 2: 'Thiên Nhuế', 3: 'Thiên Xung', 4: 'Thiên Phụ', 5: 'Thiên Cầm', 6: 'Thiên Tâm', 7: 'Thiên Trụ', 8: 'Thiên Nhậm', 9: 'Thiên Anh'},
    'nhan_ban': {1: 'Hưu Môn', 2: 'Tử Môn', 3: 'Thương Môn', 4: 'Đỗ Môn', 5: '', 6: 'Khai Môn', 7: 'Kinh Môn', 8: 'Sinh Môn', 9: 'Cảnh Môn'},
    'than_ban': {1: 'Trực Phù', 2: 'Đằng Xà', 3: 'Thái Âm', 4: 'Lục Hợp', 5: '', 6: 'Bạch Hổ', 7: 'Huyền Vũ', 8: 'Cửu Địa', 9: 'Cửu Thiên'},
}

MOCK_LUC_HAO_DATA = {
    'can_ngay': 'Giáp',
    'chi_ngay': 'Tý',
    'chi_thang': 'Dần',
    'dong_hao': [3],
    'ban': {
        'name': 'Thiên Phong Cấu',
        'palace': 'Càn',
        'haos': [
            {'hao': 1, 'luc_than': 'Tử Tôn',   'can_chi': 'Nhâm Tuất', 'ngu_hanh': 'Thổ', 'chi': 'Tuất', 'the_ung': '', 'vuong_suy': 'Hưu'},
            {'hao': 2, 'luc_than': 'Thê Tài',   'can_chi': 'Nhâm Thân', 'ngu_hanh': 'Kim', 'chi': 'Thân', 'the_ung': 'Ứng', 'vuong_suy': 'Tướng'},
            {'hao': 3, 'luc_than': 'Huynh Đệ',  'can_chi': 'Nhâm Ngọ', 'ngu_hanh': 'Hỏa', 'chi': 'Ngọ', 'the_ung': '', 'vuong_suy': 'Suy'},
            {'hao': 4, 'luc_than': 'Quan Quỷ',  'can_chi': 'Tân Dậu',  'ngu_hanh': 'Kim', 'chi': 'Dậu', 'the_ung': '', 'vuong_suy': 'Tướng'},
            {'hao': 5, 'luc_than': 'Phụ Mẫu',   'can_chi': 'Tân Hợi',  'ngu_hanh': 'Thủy', 'chi': 'Hợi', 'the_ung': 'Thế', 'vuong_suy': 'Vượng'},
            {'hao': 6, 'luc_than': 'Thê Tài',   'can_chi': 'Tân Sửu',  'ngu_hanh': 'Thổ', 'chi': 'Sửu', 'the_ung': '', 'vuong_suy': 'Hưu'},
        ]
    },
    'bien': {
        'name': 'Thiên Sơn Độn',
        'palace': 'Càn',
        'haos': [
            {'hao': 1, 'luc_than': 'Tử Tôn',   'can_chi': 'Nhâm Tuất', 'ngu_hanh': 'Thổ', 'chi': 'Tuất'},
            {'hao': 2, 'luc_than': 'Thê Tài',   'can_chi': 'Nhâm Thân', 'ngu_hanh': 'Kim', 'chi': 'Thân'},
            {'hao': 3, 'luc_than': 'Huynh Đệ',  'can_chi': 'Bính Thân', 'ngu_hanh': 'Kim', 'chi': 'Thân'},
            {'hao': 4, 'luc_than': 'Quan Quỷ',  'can_chi': 'Tân Dậu',  'ngu_hanh': 'Kim', 'chi': 'Dậu'},
            {'hao': 5, 'luc_than': 'Phụ Mẫu',   'can_chi': 'Tân Hợi',  'ngu_hanh': 'Thủy', 'chi': 'Hợi'},
            {'hao': 6, 'luc_than': 'Thê Tài',   'can_chi': 'Tân Sửu',  'ngu_hanh': 'Thổ', 'chi': 'Sửu'},
        ]
    }
}

MOCK_MAI_HOA_DATA = {
    'thuong_quai': 'Càn',
    'ha_quai': 'Tốn',
    'dong_hao': 3,
    'bien_quai': {'thuong': 'Càn', 'ha': 'Cấn'},
    'the_quai': 'Tốn',
    'dung_quai': 'Càn',
    'the_hanh': 'Mộc',
    'dung_hanh': 'Kim',
    'ho_quai': {'thuong': 'Càn', 'ha': 'Chấn'},
    'tuong': 'Gió dưới trời, tản khắp nơi',
    'nghia': 'Gặp gỡ, hội ngộ, duyên lành',
    'interpretation': 'Trên trời dưới gió, gặp gỡ tình cờ, cơ hội bất ngờ',
}

# ═══════════════════════════════════════════════════
# CÁC CÂU HỎI TEST — Bao phủ tất cả loại
# ═══════════════════════════════════════════════════
TEST_QUESTIONS = [
    # Nhóm 1: CÓ/KHÔNG — Cần CÂU TRẢ LỜI CÁT/HUNG rõ ràng
    {"q": "Tôi có nên mua nhà bây giờ không?", "expected_type": "yes_no", "expected_topic": "TÀI_CHÍNH", "expected_dt": "Thê Tài"},
    {"q": "Có nên đầu tư bitcoin lúc này được không?", "expected_type": "yes_no", "expected_topic": "TÀI_CHÍNH", "expected_dt": "Thê Tài"},
    {"q": "Tôi có thể thăng chức năm nay không?", "expected_type": "yes_no", "expected_topic": "CÔNG_VIỆC", "expected_dt": "Quan Quỷ"},
    {"q": "Thi đại học có đỗ không?", "expected_type": "yes_no", "expected_topic": "CÔNG_VIỆC", "expected_dt": "Quan Quỷ"},
    
    # Nhóm 2: SỨC KHỎE — Cần phân biệt bệnh nhẹ vs nguy hiểm
    {"q": "Bố tôi bệnh nặng có qua khỏi không?", "expected_type": "health", "expected_topic": "SỨC_KHỎE", "expected_dt": "Phụ Mẫu"},
    {"q": "Mẹ tôi ốm có nên phẫu thuật?", "expected_type": "health", "expected_topic": "SỨC_KHỎE", "expected_dt": "Phụ Mẫu"},
    {"q": "Sức khỏe tôi năm nay thế nào?", "expected_type": "health", "expected_topic": "SỨC_KHỎE", "expected_dt": "Bản Thân"},
    
    # Nhóm 3: TÌNH CẢM
    {"q": "Người yêu tôi có thật lòng không?", "expected_type": "emotion", "expected_topic": "TÌNH_CẢM", "expected_dt": "Thê Tài"},
    {"q": "Tôi có nên cưới người này?", "expected_type": "emotion", "expected_topic": "TÌNH_CẢM", "expected_dt": "Thê Tài"},
    
    # Nhóm 4: TÌM ĐỒ — Cần HƯỚNG + VỊ TRÍ
    {"q": "Tôi mất điện thoại ở đâu?", "expected_type": "find", "expected_topic": "TÌM_ĐỒ", "expected_dt": "Thê Tài"},
    {"q": "Chìa khóa xe tôi để chỗ nào?", "expected_type": "find", "expected_topic": "TÌM_ĐỒ", "expected_dt": "Thê Tài"},
    
    # Nhóm 5: SỐ LƯỢNG — Cần CON SỐ cụ thể
    {"q": "Tôi có mấy anh chị em?", "expected_type": "count", "expected_topic": "SỨC_KHỎE", "expected_dt": "Huynh Đệ"},
    {"q": "Năm nay tôi có bao nhiêu cơ hội kiếm tiền?", "expected_type": "count", "expected_topic": "TÀI_CHÍNH", "expected_dt": "Thê Tài"},
    
    # Nhóm 6: THỜI GIAN — Cần DỰ ĐOÁN KHI NÀO
    {"q": "Khi nào tôi được thăng chức?", "expected_type": "when", "expected_topic": "CÔNG_VIỆC", "expected_dt": "Quan Quỷ"},
    {"q": "Bao giờ tôi lấy vợ?", "expected_type": "when", "expected_topic": "TÌNH_CẢM", "expected_dt": "Thê Tài"},
    
    # Nhóm 7: TỔNG QUÁT — Khó phân loại
    {"q": "Vận mệnh tôi năm nay thế nào?", "expected_type": "general", "expected_topic": "CHUNG", "expected_dt": "Bản Thân"},
    {"q": "Có quý nhân giúp tôi không?", "expected_type": "general", "expected_topic": "CHUNG", "expected_dt": "Bản Thân"},
    {"q": "Đi xe hôm nay có an toàn không?", "expected_type": "yes_no", "expected_topic": "CHUNG", "expected_dt": "Bản Thân"},
    
    # Nhóm 8: CÂU HỎI KHÓ — Edge cases
    {"q": "Bố mất chưa?", "expected_type": "health", "expected_topic": "SỨC_KHỎE", "expected_dt": "Phụ Mẫu"},
    {"q": "Con trai có đi du học được không?", "expected_type": "yes_no", "expected_topic": "CÔNG_VIỆC", "expected_dt": "Tử Tôn"},
]

# ═══════════════════════════════════════════════════
# AUDIT FUNCTIONS
# ═══════════════════════════════════════════════════

def audit_truong_sinh_engine():
    """Test 1: Kiểm tra 12 Trường Sinh cho tất cả 60 tổ hợp"""
    print("\n" + "="*80)
    print("AUDIT 1: 12 TRƯỜNG SINH ENGINE")
    print("="*80)
    
    issues = []
    hanh_list = ['Mộc', 'Hỏa', 'Kim', 'Thủy', 'Thổ']
    
    for hanh in hanh_list:
        stages_found = []
        for chi in CHI_ORDER:
            stage, explain = _get_truong_sinh(hanh, chi)
            if stage:
                stages_found.append((chi, stage))
            else:
                issues.append(f"❌ _get_truong_sinh('{hanh}', '{chi}') = None")
        
        # Check: tất cả 12 stages đều xuất hiện
        stage_names = [s for _, s in stages_found]
        for expected in TRUONG_SINH_STAGES:
            if expected not in stage_names:
                issues.append(f"❌ Hành {hanh}: Thiếu giai đoạn '{expected}'")
        
        # Hiển thị tóm tắt
        print(f"\n  {hanh}:")
        for chi, stage in stages_found:
            print(f"    {chi:4s} → {stage}")
    
    # Issue: Không có power score
    issues.append("⚠️ _get_truong_sinh() chỉ trả về (name, text) — KHÔNG CÓ POWER SCORE (%)")
    issues.append("⚠️ Không phân biệt Dương/Âm (ví dụ: Giáp Mộc thuận vs Ất Mộc nghịch)")
    issues.append("⚠️ Không mapping sang đặc tính vật (kích thước, mới/cũ...)")
    
    print(f"\n  📋 Issues: {len(issues)}")
    for i in issues:
        print(f"    {i}")
    return issues


def audit_ngu_hanh_relations():
    """Test 2: Kiểm tra Ngũ Hành sinh khắc"""
    print("\n" + "="*80)
    print("AUDIT 2: NGŨ HÀNH RELATIONS")
    print("="*80)
    
    issues = []
    hanh_list = ['Mộc', 'Hỏa', 'Thổ', 'Kim', 'Thủy']
    
    for h1 in hanh_list:
        for h2 in hanh_list:
            rel = _ngu_hanh_relation(h1, h2)
            print(f"  {h1:4s} → {h2:4s} = {rel}")
            if rel == "Không xác định":
                issues.append(f"❌ _ngu_hanh_relation('{h1}', '{h2}') = Không xác định")
    
    # Issues
    issues.append("⚠️ _ngu_hanh_relation() chỉ trả text — KHÔNG CÓ điểm số (sinh=+X, khắc=-X)")
    
    print(f"\n  📋 Issues: {len(issues)}")
    for i in issues:
        print(f"    {i}")
    return issues


def audit_question_classification():
    """Test 3: Phân loại câu hỏi"""
    print("\n" + "="*80)
    print("AUDIT 3: PHÂN LOẠI CÂU HỎI (Smart Category)")
    print("="*80)
    
    issues = []
    helper = FreeAIHelper()
    
    for test in TEST_QUESTIONS:
        q = test['q']
        expected_topic = test['expected_topic']
        expected_dt = test['expected_dt']
        
        # Simulate category detection (extract from answer_question logic)
        q_lower = q.lower()
        CATEGORIES = {
            "SỨC_KHỎE_GIA_ĐÌNH": {
                "keywords": ["bệnh", "ốm", "đau", "sức khỏe", "khỏe", "chết", "mất người", "bố", "mẹ", "cha", "ông", "bà", 
                             "con cái", "gia đình", "thai", "mang thai", "sinh", "bố mất", "mẹ mất", "chết chưa",
                             "sống", "chữa", "bệnh viện", "phẫu thuật", "ung thư", "tai nạn", "nguy hiểm"],
                "dung_than": "Phụ Mẫu",
            },
            "TÀI_CHÍNH": {
                "keywords": ["tiền", "tài", "mua", "bán", "đầu tư", "giàu", "nghèo", "lương", "thu nhập", "nợ",
                             "vay", "cho vay", "kinh doanh", "buôn bán", "lãi", "lỗ", "cổ phiếu", "crypto",
                             "bitcoin", "nhà đất", "mua nhà", "bất động sản", "vốn", "hùn vốn", "trúng số",
                             "xe", "xe máy", "ô tô", "xe hơi", "tài sản", "sở hữu", "có mấy", "bao nhiêu",
                             "vàng", "bạc", "kim cương", "trang sức"],
                "dung_than": "Thê Tài",
            },
            "CÔNG_VIỆC": {
                "keywords": ["việc", "công việc", "sếp", "thăng tiến", "thi", "đỗ", "trượt", "phỏng vấn",
                             "xin việc", "nghỉ việc", "sa thải", "hợp đồng", "dự án", "thầu", "đấu thầu",
                             "kiện", "kiện tụng", "tòa", "quan chức", "chức vụ", "đề bạt"],
                "dung_than": "Quan Quỷ",
            },
            "TÌNH_CẢM": {
                "keywords": ["yêu", "người yêu", "vợ", "chồng", "hôn nhân", "cưới", "ly hôn", "tình",
                             "hẹn hò", "chia tay", "ngoại tình", "duyên", "vợ chồng", "đám cưới",
                             "bạn trai", "bạn gái", "tình cảm", "hạnh phúc", "ghen"],
                "dung_than": "Thê Tài",
            },
            "TÌM_ĐỒ": {
                "keywords": ["tìm", "mất đồ", "ở đâu", "thất lạc", "trộm", "mất cắp", "chỗ nào",
                             "mất xe", "mất điện thoại", "mất tiền", "tìm đường", "lạc đường",
                             "mất ví", "mất đồ", "giấy tờ", "hướng nào"],
                "dung_than": "Thê Tài",
            },
            "CHUNG": {"keywords": [], "dung_than": "Bản Thân"},
        }
        
        detected = "CHUNG"
        max_score = 0
        nguoi_keywords = ["bố", "mẹ", "cha", "ông", "bà", "con", "anh", "chị", "em", "vợ", "chồng"]
        has_person = any(nk in q_lower for nk in nguoi_keywords)
        
        for cat_key, cat_info in CATEGORIES.items():
            if cat_key == "CHUNG":
                continue
            score = 0
            for kw in cat_info["keywords"]:
                if kw in q_lower:
                    score += len(kw)
            if cat_key == "TÌM_ĐỒ" and has_person:
                if "ở đâu" not in q_lower and "chỗ nào" not in q_lower and "hướng" not in q_lower:
                    score = 0
            if cat_key == "SỨC_KHỎE_GIA_ĐÌNH" and has_person:
                score += 5
            if score > max_score:
                max_score = score
                detected = cat_key
        
        actual_dt = CATEGORIES[detected]["dung_than"]
        
        # Remap for comparison
        topic_map = {
            "SỨC_KHỎE_GIA_ĐÌNH": "SỨC_KHỎE",
            "TÀI_CHÍNH": "TÀI_CHÍNH",
            "CÔNG_VIỆC": "CÔNG_VIỆC",
            "TÌNH_CẢM": "TÌNH_CẢM",
            "TÌM_ĐỒ": "TÌM_ĐỒ",
            "NHÀ_CỬa": "NHÀ_CỬA",
            "CHUNG": "CHUNG",
        }
        
        mapped = topic_map.get(detected, detected)
        correct_topic = (mapped == expected_topic)
        correct_dt = (actual_dt == expected_dt)
        
        status = "✅" if correct_topic and correct_dt else "❌"
        print(f"  {status} \"{q[:50]:50s}\"")
        print(f"     Expect: {expected_topic:15s} DT={expected_dt:12s}")
        print(f"     Actual: {mapped:15s} DT={actual_dt:12s} (score={max_score})")
        
        if not correct_topic:
            issues.append(f"❌ PHÂN LOẠI SAI: \"{q}\" → Expect={expected_topic}, Got={mapped}")
        if not correct_dt:
            issues.append(f"❌ DỤNG THẦN SAI: \"{q}\" → Expect={expected_dt}, Got={actual_dt}")
    
    # Structural issues
    issues.append("⚠️ 'mua nhà' → TÀI_CHÍNH, nhưng đúng ra nên là NHÀ_CỬA hoặc matched cả 2")
    issues.append("⚠️ Không có category 'HỌC TẬP/THI CỬ' riêng biệt")
    issues.append("⚠️ 'con trai du học' → DT nên là Tử Tôn nhưng hệ thống không tách rõ '+ con'")
    issues.append("⚠️ Category detection chỉ dùng keyword length scoring — thiếu NLP context")
    
    print(f"\n  📋 Issues: {len(issues)}")
    for i in issues:
        print(f"    {i}")
    return issues


def audit_full_answer(question_idx=0):
    """Test 4: Chạy answer_question() thực tế, phân tích output"""
    print("\n" + "="*80)
    print("AUDIT 4: FULL answer_question() CHẠY THẬT")
    print("="*80)
    
    issues = []
    helper = FreeAIHelper()
    
    test_cases = [
        ("Tôi có nên mua nhà bây giờ không?", "yes_no"),
        ("Bố tôi bệnh nặng có qua khỏi không?", "health"),
        ("Mất điện thoại ở đâu?", "find"),
        ("Tôi có mấy anh chị em?", "count"),
        ("Khi nào tôi được thăng chức?", "when"),
        ("Vận mệnh tôi năm nay thế nào?", "general"),
        ("Người yêu có thật lòng không?", "emotion"),
    ]
    
    for q, q_type in test_cases:
        print(f"\n  {'─'*60}")
        print(f"  📝 Q: {q} (type: {q_type})")
        print(f"  {'─'*60}")
        
        try:
            result = helper.answer_question(
                question=q,
                chart_data=MOCK_CHART_DATA,
                mai_hoa_data=MOCK_MAI_HOA_DATA,
                luc_hao_data=MOCK_LUC_HAO_DATA,
            )
            
            if not result:
                issues.append(f"❌ EMPTY result for \"{q}\"")
                continue
            
            # Analyze output quality
            result_lower = result.lower()
            output_len = len(result)
            
            # Check 1: Có CÂU TRẢ LỜI cụ thể không?
            has_answer = 'câu trả lời' in result_lower
            has_percentage = '%' in result
            has_verdict = any(v in result for v in ['THUẬN LỢI', 'KHÓ KHĂN', 'CÁT', 'HUNG', 'CÂN BẰNG', 'CÓ', 'KHÔNG NÊN'])
            
            # Check 2: Có BƯỚC 5.7 (lượng hóa) không? (chưa có — expected fail)
            has_strength_table = 'LỰC LƯỢNG' in result or 'PHÂN CẤP' in result
            
            # Check 3: Có mapping vạn vật không? (chưa có — expected fail)
            has_van_vat = 'kích thước' in result_lower or 'tình trạng' in result_lower
            
            # Check 4: Output quá dài (>10000 chars) — khó đọc
            too_long = output_len > 10000
            
            status_parts = []
            if has_answer: status_parts.append("✅ Có câu trả lời")
            else: 
                status_parts.append("❌ THIẾU câu trả lời trực tiếp")
                issues.append(f"❌ \"{q}\" — Không có phần 'CÂU TRẢ LỜI'")
            
            if has_percentage: status_parts.append("✅ Có %")
            else:
                status_parts.append("⚠️ Thiếu %")
                issues.append(f"⚠️ \"{q}\" — Không có phần trăm cụ thể")
            
            if has_verdict: status_parts.append("✅ Có verdict")
            else:
                status_parts.append("❌ THIẾU verdict")
                issues.append(f"❌ \"{q}\" — Không có kết luận CÁT/HUNG/BÌNH")
            
            if not has_strength_table:
                issues.append(f"⚠️ \"{q}\" — CHƯA CÓ bảng lượng hóa lực lượng (V21 mới)")
            
            if not has_van_vat:
                issues.append(f"⚠️ \"{q}\" — CHƯA CÓ mapping vạn vật (kích thước/mới cũ)")
            
            if too_long:
                issues.append(f"⚠️ \"{q}\" — Output QUÁ DÀI ({output_len} chars), khó đọc")
            
            print(f"  Output: {output_len} chars")
            print(f"  Result: {' | '.join(status_parts)}")
            
            # Print first 500 chars of conclusion section
            conclusion_start = result.find('KẾT LUẬN')
            if conclusion_start > 0:
                snippet = result[conclusion_start:conclusion_start+500]
                print(f"  Conclusion preview: {snippet[:200]}...")
            
        except Exception as e:
            issues.append(f"❌ CRASH cho \"{q}\": {str(e)}")
            print(f"  ❌ CRASH: {str(e)}")
            traceback.print_exc()
    
    return issues


def audit_scoring_system():
    """Test 5: Kiểm tra hệ thống scoring hiện tại"""
    print("\n" + "="*80)
    print("AUDIT 5: SCORING SYSTEM")
    print("="*80)
    
    issues = []
    helper = FreeAIHelper()
    
    # Test _luc_hao_scoring
    try:
        score, summary = helper._luc_hao_scoring(MOCK_LUC_HAO_DATA, 'Thê Tài')
        print(f"  LH score (Thê Tài): {score} → {summary}")
    except Exception as e:
        issues.append(f"❌ _luc_hao_scoring CRASH: {e}")
        print(f"  ❌ LH: {e}")
    
    try:
        score, summary = helper._luc_hao_scoring(MOCK_LUC_HAO_DATA, 'Quan Quỷ')
        print(f"  LH score (Quan Quỷ): {score} → {summary}")
    except Exception as e:
        issues.append(f"❌ _luc_hao_scoring CRASH: {e}")
    
    try:
        score, summary = helper._luc_hao_scoring(MOCK_LUC_HAO_DATA, 'Bản Thân')
        print(f"  LH score (Bản Thân): {score} → {summary}")
    except Exception as e:
        issues.append(f"❌ _luc_hao_scoring CRASH: {e}")
    
    # Test _mai_hoa_scoring
    try:
        score, summary = helper._mai_hoa_scoring(MOCK_MAI_HOA_DATA)
        print(f"  MH score: {score} → {summary}")
    except Exception as e:
        issues.append(f"❌ _mai_hoa_scoring CRASH: {e}")
        print(f"  ❌ MH: {e}")
    
    # Test _thiet_ban_scoring
    try:
        score, summary = helper._thiet_ban_scoring(MOCK_CHART_DATA, MOCK_LUC_HAO_DATA, MOCK_MAI_HOA_DATA)
        print(f"  TB score: {score} → {summary}")
    except Exception as e:
        issues.append(f"❌ _thiet_ban_scoring CRASH: {e}")
        print(f"  ❌ TB: {e}")
    
    # Test _luc_nham_scoring
    try:
        score, summary = helper._luc_nham_scoring(MOCK_CHART_DATA)
        print(f"  LN score: {score} → {summary}")
    except Exception as e:
        issues.append(f"❌ _luc_nham_scoring CRASH: {e}")
        print(f"  ❌ LN: {e}")
    
    # Test _thai_at_scoring
    try:
        score, summary = helper._thai_at_scoring(MOCK_CHART_DATA)
        print(f"  TA score: {score} → {summary}")
    except Exception as e:
        issues.append(f"❌ _thai_at_scoring CRASH: {e}")
        print(f"  ❌ TA: {e}")
    
    # Structural issues
    issues.append("⚠️ Score = raw integer, KHÔNG normalize thành % (0-100)")
    issues.append("⚠️ Mỗi PP dùng thang điểm KHÁC nhau (LH: ±40, KM: ±30...) — KHÔNG SO SÁNH ĐƯỢC")
    issues.append("⚠️ Score KHÔNG liên kết với 12 Trường Sinh power")
    issues.append("⚠️ Score KHÔNG mapping sang vạn vật (kích thước, tuổi, con người)")
    issues.append("⚠️ THIẾU: Niên Chi, Thời Chi ảnh hưởng — chỉ có Nguyệt và Nhật")
    
    print(f"\n  📋 Issues: {len(issues)}")
    for i in issues:
        print(f"    {i}")
    return issues


def audit_verdict_logic():
    """Test 6: Kiểm tra logic đưa ra kết luận"""
    print("\n" + "="*80)
    print("AUDIT 6: VERDICT/CONCLUSION LOGIC")
    print("="*80)
    
    issues = []
    
    # Simulate verdict calculation from _build_element_impact_analysis
    test_cases = [
        # (ky_mon, luc_hao, mai_hoa, luc_nham, thai_at, good_ev, bad_ev)
        ('CÁT', 'CÁT', 'CÁT', 'CÁT', 'CÁT', 5, 0),
        ('HUNG', 'HUNG', 'HUNG', 'HUNG', 'HUNG', 0, 5),
        ('CÁT', 'HUNG', 'BÌNH', 'CÁT', 'HUNG', 2, 3),
        ('BÌNH', 'BÌNH', 'BÌNH', 'BÌNH', 'BÌNH', 1, 1),
        ('CÁT', 'CÁT', 'HUNG', 'BÌNH', 'CÁT', 4, 1),
    ]
    
    for km, lh, mh, ln, ta, good, bad in test_cases:
        verdicts = [km, lh, mh, ln, ta]
        cat_count = sum(1 for v in verdicts if v in ['CÁT', 'ĐẠI CÁT'])
        hung_count = sum(1 for v in verdicts if v in ['HUNG', 'ĐẠI HUNG'])
        
        if cat_count > hung_count:
            final = 'CÁT'
            pct = int(50 + (cat_count / max(len(verdicts), 1)) * 30 + (good - bad) * 5)
        elif hung_count > cat_count:
            final = 'HUNG'
            pct = int(50 - (hung_count / max(len(verdicts), 1)) * 30 - (bad - good) * 5)
        else:
            final = 'BÌNH'
            pct = 50 + (good - bad) * 5
        pct = max(5, min(95, pct))
        
        print(f"  KM={km:5s} LH={lh:5s} MH={mh:5s} LN={ln:5s} TA={ta:5s} Good={good} Bad={bad} → {final} {pct}%")
    
    issues.append("❌ % tính bằng CẢM TÍNH: 50 ± (count/5)*30 ± ev*5 — KHÔNG CÓ CĂN CỨ KHOA HỌC")
    issues.append("❌ Verdict chỉ đếm CÁT/HUNG count — KHÔNG xét trọng số PP nào quan trọng hơn")
    issues.append("❌ Khi CÁT=HUNG thì luôn BÌNH — nhưng nếu KM=CÁT(95%) vs LH=HUNG(70%) thì CÁT mới đúng")
    issues.append("❌ % không liên kết đến 12 Trường Sinh / Ngũ Khí / Nguyệt Lệnh")
    issues.append("❌ Không có bảng 'BẰNG CHỨNG' xếp theo thứ tự mạnh→yếu")
    issues.append("❌ Không quy ra đặc tính vật/con người từ %")
    issues.append("⚠️ 'good_ev' và 'bad_ev' đếm bằng keyword match ('sinh', 'khắc..') — dễ false positive")
    
    print(f"\n  📋 Issues: {len(issues)}")
    for i in issues:
        print(f"    {i}")
    return issues


# ═══════════════════════════════════════════════════
# MAIN — RUN ALL AUDITS
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🔍 AUDIT TOÀN DIỆN AI OFFLINE V20.5 → V21.0             ║")
    print("║  Tìm tất cả điểm yếu, sai, thiếu                         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    all_issues = {}
    
    # Run audits
    all_issues['Trường Sinh'] = audit_truong_sinh_engine()
    all_issues['Ngũ Hành'] = audit_ngu_hanh_relations()
    all_issues['Phân Loại Q'] = audit_question_classification()
    all_issues['Scoring'] = audit_scoring_system()
    all_issues['Verdict'] = audit_verdict_logic()
    all_issues['Full Answer'] = audit_full_answer()
    
    # ═══════════════════════════════════════════════════
    # TỔNG HỢP
    # ═══════════════════════════════════════════════════
    print("\n" + "═"*80)
    print("📊 TỔNG HỢP AUDIT — TẤT CẢ VẤN ĐỀ CẦN SỬA")
    print("═"*80)
    
    total_critical = 0
    total_warning = 0
    
    for category, issues in all_issues.items():
        critical = sum(1 for i in issues if i.startswith('❌'))
        warning = sum(1 for i in issues if i.startswith('⚠️'))
        total_critical += critical
        total_warning += warning
        print(f"\n  [{category}]: {critical} ❌ Critical | {warning} ⚠️ Warning")
        for i in issues:
            if i.startswith('❌'):
                print(f"    {i}")
    
    print(f"\n{'─'*80}")
    print(f"  TỔNG: {total_critical} ❌ CRITICAL | {total_warning} ⚠️ WARNING")
    print(f"{'─'*80}")
    
    # Recommendations
    print("\n" + "═"*80)
    print("💡 KHUYẾN NGHỊ NÂNG CẤP V21.0")
    print("═"*80)
    recs = [
        "1. THÊM TRUONG_SINH_POWER dict — power score 0-100% cho mỗi giai đoạn",
        "2. THÊM STRENGTH_TO_VAN_VAT — mapping % → kích thước/mới cũ/vòng đời con người",
        "3. THÊM _calc_*_strength() cho CẢ 6 PP — normalize về 0-100%",
        "4. SỬA verdict logic — dùng weighted % thay vì count CÁT/HUNG",
        "5. THÊM TIME_INFLUENCE — Niên Chi + Thời Chi vào scoring",
        "6. THÊM bảng PHÂN CẤP YẾU TỐ TÁC ĐỘNG — xếp Mạnh→Yếu",
        "7. SỬA _generate_direct_answer — dùng % làm căn cứ thay vì CÁT/HUNG text",
        "8. THÊM category 'THI CỬ/HỌC TẬP' riêng biệt",
        "9. SỬA Dụng Thần detection — 'con trai du học' → Tử Tôn (hiện lạc sang Quan Quỷ)",
        "10. GIẢM output length — ẩn chi tiết, chỉ hiện kết luận + bảng %",
    ]
    for r in recs:
        print(f"  {r}")
    
    print(f"\n✅ Audit hoàn tất. Tổng {total_critical + total_warning} vấn đề cần giải quyết.")
