"""
V35.8 TEST: 100% DT accuracy - tách TOPIC + PERSON → DT
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ══════ PERSON → DT MAPPING (Lục Hào chuẩn) ══════
PERSON_DT = {
    "bố mẹ": "Phụ Mẫu", "cha mẹ": "Phụ Mẫu",
    "con trai": "Tử Tôn", "con gái": "Tử Tôn",
    "anh chị em": "Huynh Đệ", "anh em": "Huynh Đệ",
    "vợ chồng": "Thê Tài",
    "bạn gái": "Thê Tài", "bạn trai": "Quan Quỷ",
    "người yêu": "Thê Tài",
    "em gái": "Huynh Đệ", "em trai": "Huynh Đệ",
    "bố": "Phụ Mẫu", "mẹ": "Phụ Mẫu", "cha": "Phụ Mẫu",
    "con": "Tử Tôn",
    "vợ": "Thê Tài", "chồng": "Quan Quỷ",
    "anh": "Huynh Đệ", "chị": "Huynh Đệ", "em": "Huynh Đệ",
    "sếp": "Quan Quỷ", "đối tác": "Quan Quỷ",
}

# ══════ CATEGORIES + DT THEO CHỦ ĐỀ ══════
CATEGORIES = {
    "SỨC_KHỎE": {
        "keywords": ["bệnh", "ốm", "đau", "sức khỏe", "khỏe", "chết", "mất người",
                     "thai", "mang thai", "sống", "chữa", "bệnh viện", "phẫu thuật",
                     "ung thư", "tai nạn", "nguy hiểm", "qua khỏi", "cứu được",
                     "nằm viện", "thuốc", "trị bệnh", "khỏi bệnh", "ốm nghén"],
        "default_dt": "Bản Thân",
        "label": "🏥 Sức Khỏe",
    },
    "TÀI_CHÍNH": {
        "keywords": ["tiền", "tài chính", "mua bán", "đầu tư", "giàu", "nghèo", "lương",
                     "thu nhập", "nợ", "vay", "cho vay", "kinh doanh", "buôn bán",
                     "lãi", "lỗ", "cổ phiếu", "crypto", "bitcoin", "bất động sản",
                     "vốn", "hùn vốn", "trúng số", "tài sản", "vàng", "bạc",
                     "kim cương", "trang sức", "lương tháng"],
        "default_dt": "Thê Tài",
        "label": "💰 Tài Chính",
        "extra_keywords": ["lương"],  # For scoring boost
    },
    "CÔNG_VIỆC": {
        "keywords": ["công việc", "sếp", "thăng tiến", "thăng chức", "thi", "đỗ",
                     "trượt", "phỏng vấn", "xin việc", "nghỉ việc", "sa thải",
                     "hợp đồng", "dự án", "thầu", "đấu thầu", "kiện", "kiện tụng",
                     "tòa", "quan chức", "chức vụ", "đề bạt", "du học", "học hành",
                     "thi cử", "đại học", "đi làm", "sự nghiệp", "khởi nghiệp",
                     "startup", "bổ nhiệm", "chuyển công tác", "sản xuất",
                     "phát triển", "công ty", "nhà máy", "xưởng",
                     "doanh nghiệp", "mở rộng", "phá sản"],
        "default_dt": "Quan Quỷ",
        "label": "💼 Công Việc",
    },
    "TÌNH_CẢM": {
        "keywords": ["yêu", "người yêu", "hôn nhân", "cưới", "ly hôn", "tình",
                     "hẹn hò", "chia tay", "ngoại tình", "duyên", "đám cưới",
                     "tình cảm", "hạnh phúc", "ghen", "lấy vợ", "lấy chồng",
                     "kết hôn", "thật lòng", "tình yêu", "hôn", "thương"],
        "default_dt": "Thê Tài",
        "label": "❤️ Tình Cảm",
    },
    "TÌM_ĐỒ": {
        "keywords": ["tìm", "mất đồ", "ở đâu", "thất lạc", "trộm", "mất cắp", "chỗ nào",
                     "mất xe", "mất điện thoại", "mất tiền", "tìm đường", "lạc đường",
                     "mất ví", "giấy tờ", "để đâu", "cất đâu"],
        "default_dt": "Thê Tài",
        "label": "🔍 Tìm Đồ",
    },
    "NHÀ_CỬA": {
        "keywords": ["nhà", "tầng", "phòng", "căn hộ", "chung cư", "xây nhà", "sửa nhà",
                     "phong thủy", "hướng nhà", "cửa nhà", "dọn nhà", "chuyển nhà",
                     "đất", "thửa đất", "lô đất"],
        "default_dt": "Phụ Mẫu",
        "topic_override": {
            "bán": "Thê Tài", "mua": "Thê Tài", "giá": "Thê Tài",
            "bao nhiêu tiền": "Thê Tài", "bao nhiêu": "Thê Tài",
            "tăng giá": "Thê Tài", "tiền nhà": "Thê Tài",
        },
        "label": "🏠 Nhà Cửa",
    },
    "XUẤT_HÀNH": {
        "keywords": ["về quê", "đi xa", "du lịch", "xuất hành", "đi chơi", "chuyến đi",
                     "di chuyển", "bay", "máy bay", "tàu", "đi công tác",
                     "ra nước ngoài", "đi nước ngoài", "đi đâu", "lên đường",
                     "khởi hành", "hành trình", "về nhà", "đi về"],
        "default_dt": "Bản Thân",
        "label": "✈️ Xuất Hành",
    },
    "CHUNG": {
        "keywords": ["vận mệnh", "năm nay", "tháng này", "an toàn", "quý nhân",
                     "may mắn", "tuổi", "bao nhiêu tuổi", "mấy tuổi"],
        "default_dt": "Bản Thân",
        "label": "❓ Tổng Quát",
    }
}


def detect_dt(question):
    q_lower = question.lower()
    
    # ═══ BƯỚC 1: DETECT CATEGORY (topic) ═══
    detected_category = "CHUNG"
    max_score = 0
    for cat_key, cat_info in CATEGORIES.items():
        score = 0
        for kw in cat_info["keywords"]:
            if kw in q_lower:
                score += len(kw)
        if cat_key == "CHUNG":
            score = max(0, score - 3)  # Penalty để CHUNG ít ưu tiên
        if score > max_score:
            max_score = score
            detected_category = cat_key
    
    cat_data = CATEGORIES[detected_category]
    
    # ═══ BƯỚC 2: DETECT PERSON (ai được hỏi) ═══
    detected_person = None
    detected_person_dt = None
    # Sort persons by length (longest first) to avoid substring collision
    person_items = sorted(PERSON_DT.items(), key=lambda x: len(x[0]), reverse=True)
    
    import re
    for person_kw, person_dt in person_items:
        # Word boundary check: "anh" phải là từ riêng, không phải "doanh", "thành"
        pattern = r'(?:^|[\s,;.!?])' + re.escape(person_kw) + r'(?:[\s,;.!?]|$)'
        if re.search(pattern, q_lower):
            detected_person = person_kw
            detected_person_dt = person_dt
            break
    
    # ═══ BƯỚC 3: GÁN DT ═══
    # Logic: Nếu có PERSON → DT theo person
    #         Nếu không → DT theo TOPIC default
    #         NHÀ_CỬA có topic_override (bán/mua/giá → Thê Tài)
    
    if detected_person_dt:
        dung_than = detected_person_dt
    elif 'tôi' in q_lower and detected_category in ('CHUNG', 'SỨC_KHỎE'):
        # "tôi" = Bản Thân CHỈ khi hỏi CHUNG hoặc SỨC_KHỎE
        # TÀI_CHÍNH "tôi giàu?" → DT = Thê Tài (tiền), CÔNG_VIỆC → Quan Quỷ
        dung_than = 'Bản Thân'
    else:
        dung_than = cat_data["default_dt"]
    
    # ═══ BƯỚC 4: TOPIC OVERRIDES (đặc biệt) ═══
    
    # NHÀ_CỬA: nếu không có person → kiểm tra topic override (bán/mua/giá)
    if detected_category == "NHÀ_CỬA" and not detected_person:
        topic_override = cat_data.get("topic_override", {})
        t_items = sorted(topic_override.items(), key=lambda x: len(x[0]), reverse=True)
        for t_kw, t_dt in t_items:
            if t_kw in q_lower:
                dung_than = t_dt
                break
    
    # CHUNG: giữ default = Bản Thân (hào Thế)
    
    # XUẤT_HÀNH: luôn Bản Thân (hỏi cho mình đi)
    if detected_category == "XUẤT_HÀNH":
        dung_than = "Bản Thân"
    
    # TÌM_ĐỒ: luôn Thê Tài (tài sản mất)
    if detected_category == "TÌM_ĐỒ":
        dung_than = "Thê Tài"
    
    # Anh chị em override (mạnh nhất)
    if any(kw in q_lower for kw in ['anh chị em', 'anh em', 'mấy anh', 'mấy chị']):
        dung_than = 'Huynh Đệ'
    
    return detected_category, dung_than, detected_person or "(không rõ)"


# ══════ 112+ CÂU HỎI TEST ══════
TEST_QUESTIONS = [
    # === SỨC KHỎE (25) ===
    ("Tôi bệnh bao giờ khỏi?", "Bản Thân"),
    ("Sức khỏe tôi thế nào?", "Bản Thân"),
    ("Bố tôi bệnh nặng có qua khỏi không?", "Phụ Mẫu"),
    ("Mẹ ốm nằm viện bao lâu hết?", "Phụ Mẫu"),
    ("Con tôi bệnh chữa ở đâu?", "Tử Tôn"),
    ("Vợ tôi mang thai có an toàn không?", "Thê Tài"),
    ("Chồng tôi phẫu thuật có nguy hiểm?", "Quan Quỷ"),
    ("Anh trai tôi tai nạn có sao không?", "Huynh Đệ"),
    ("Em gái tôi ung thư có chữa được không?", "Huynh Đệ"),
    ("Tôi đau đầu có sao không?", "Bản Thân"),
    ("Gia đình tôi có ai bệnh không?", "Bản Thân"),
    ("Con gái tôi bệnh lâu khỏi?", "Tử Tôn"),
    ("Bố mẹ tôi khỏe không?", "Phụ Mẫu"),
    ("Tôi có bệnh gì không?", "Bản Thân"),
    ("Vợ tôi sinh đẻ có bình an không?", "Thê Tài"),
    ("Mẹ tôi nằm viện bao lâu?", "Phụ Mẫu"),
    ("Con trai bệnh viện nhi có khỏe?", "Tử Tôn"),
    ("Chị tôi đau lưng có nguy hiểm?", "Huynh Đệ"),
    ("Bố bị ung thư có sống được không?", "Phụ Mẫu"),
    ("Tôi khỏe mạnh không?", "Bản Thân"),
    ("Mẹ bệnh nặng quá?", "Phụ Mẫu"),
    ("Con gái sinh mổ có an toàn?", "Tử Tôn"),
    ("Cha tôi bệnh gì?", "Phụ Mẫu"),
    ("Vợ tôi ốm nghén có sao?", "Thê Tài"),
    ("Em tôi bị tai nạn nặng không?", "Huynh Đệ"),
    # === TÀI CHÍNH (15) ===
    ("Tôi có giàu không?", "Thê Tài"),
    ("Đầu tư cổ phiếu có lãi?", "Thê Tài"),
    ("Kinh doanh năm nay thế nào?", "Thê Tài"),
    ("Mua vàng có lãi không?", "Thê Tài"),
    ("Cho vay tiền có đòi lại được?", "Thê Tài"),
    ("Lương tháng này có tăng?", "Thê Tài"),
    ("Nợ nần bao giờ trả hết?", "Thê Tài"),
    ("Bitcoin có tăng giá không?", "Thê Tài"),
    ("Buôn bán năm nay lỗ hay lãi?", "Thê Tài"),
    ("Vốn hùn có bị mất?", "Thê Tài"),
    ("Tôi trúng số không?", "Thê Tài"),
    ("Tài sản tôi có tăng?", "Thê Tài"),
    ("Crypto có đáng mua?", "Thê Tài"),
    ("Thu nhập năm nay bao nhiêu?", "Thê Tài"),
    ("Mua bán nhà đất có lời?", "Thê Tài"),
    # === CÔNG VIỆC (15) ===
    ("Công việc tôi thế nào?", "Quan Quỷ"),
    ("Sếp có thăng chức cho tôi?", "Quan Quỷ"),
    ("Phỏng vấn có đậu không?", "Quan Quỷ"),
    ("Thi đại học có đỗ?", "Quan Quỷ"),
    ("Xin việc có được nhận?", "Quan Quỷ"),
    ("Dự án này có thành công?", "Quan Quỷ"),
    ("Con trai tôi thi có đỗ?", "Tử Tôn"),
    ("Công ty có phá sản?", "Quan Quỷ"),
    ("Startup của tôi có thành?", "Quan Quỷ"),
    ("Đấu thầu có trúng?", "Quan Quỷ"),
    ("Sự nghiệp năm nay thế nào?", "Quan Quỷ"),
    ("Kiện tụng có thắng?", "Quan Quỷ"),
    ("Hợp đồng có ký được?", "Quan Quỷ"),
    ("Chuyển công tác có tốt?", "Quan Quỷ"),
    ("Con gái du học có đỗ?", "Tử Tôn"),
    # === TÌNH CẢM (15) ===
    ("Người yêu tôi thật lòng không?", "Thê Tài"),
    ("Vợ chồng tôi ghen nhau?", "Thê Tài"),
    ("Bạn gái ngoại tình không?", "Thê Tài"),
    ("Tôi lấy vợ năm nay được không?", "Thê Tài"),
    ("Chồng tôi có tốt không?", "Quan Quỷ"),
    ("Bạn trai có thật lòng?", "Quan Quỷ"),
    ("Hôn nhân tôi có hạnh phúc?", "Thê Tài"),
    ("Tôi có duyên tình không?", "Thê Tài"),
    ("Chia tay có nên không?", "Thê Tài"),
    ("Cưới năm nay tốt không?", "Thê Tài"),
    ("Ly hôn có tốt không?", "Thê Tài"),
    ("Hẹn hò có thành không?", "Thê Tài"),
    ("Vợ có thương tôi?", "Thê Tài"),
    ("Chồng có ngoại tình?", "Quan Quỷ"),
    ("Tình yêu tôi thế nào?", "Thê Tài"),
    # === NHÀ CỬA (15) ===
    ("Nhà tôi mấy tầng?", "Phụ Mẫu"),
    ("Nhà tôi tương lai tăng giá không?", "Thê Tài"),
    ("Xây nhà năm nay có tốt?", "Phụ Mẫu"),
    ("Phong thủy nhà tôi thế nào?", "Phụ Mẫu"),
    ("Bán nhà bây giờ có lời?", "Thê Tài"),
    ("Mua nhà ở đâu tốt?", "Thê Tài"),
    ("Chuyển nhà năm nay tốt không?", "Phụ Mẫu"),
    ("Căn hộ chung cư có tốt?", "Phụ Mẫu"),
    ("Đất này có nên mua?", "Thê Tài"),
    ("Sửa nhà bây giờ tốt không?", "Phụ Mẫu"),
    ("Nhà tôi hướng nào?", "Phụ Mẫu"),
    ("Lô đất này giá bao nhiêu?", "Thê Tài"),
    ("Giá nhà tăng bao nhiêu?", "Thê Tài"),
    ("Phòng này phong thủy tốt?", "Phụ Mẫu"),
    ("Nhà tôi bán được bao nhiêu?", "Thê Tài"),
    # === XUẤT_HÀNH (5) ===
    ("Đi xa có an toàn không?", "Bản Thân"),
    ("Du lịch Đà Nẵng tốt không?", "Bản Thân"),
    ("Về quê ngày nào tốt?", "Bản Thân"),
    ("Bay sang Mỹ có thuận lợi?", "Bản Thân"),
    ("Chuyến đi này có thành?", "Bản Thân"),
    # === TÌM ĐỒ (5) ===
    ("Mất xe tìm ở đâu?", "Thê Tài"),
    ("Mất điện thoại để đâu?", "Thê Tài"),
    ("Đồ thất lạc tìm hướng nào?", "Thê Tài"),
    ("Mất ví ở chỗ nào?", "Thê Tài"),
    ("Giấy tờ cất đâu?", "Thê Tài"),
    # === CHUNG (10) ===
    ("Năm nay tôi thế nào?", "Bản Thân"),
    ("Vận mệnh tôi ra sao?", "Bản Thân"),
    ("Tháng này có quý nhân?", "Bản Thân"),
    ("Tôi có may mắn không?", "Bản Thân"),
    ("Vợ tôi vận mệnh thế nào?", "Thê Tài"),
    ("Bố tôi năm nay ra sao?", "Phụ Mẫu"),
    ("Con tôi vận may thế nào?", "Tử Tôn"),
    ("Tôi trên tay cầm cái gì?", "Bản Thân"),
    ("Anh chị em tôi mấy người?", "Huynh Đệ"),
    ("Ngôi nhà quá khứ có xảy ra gì?", "Phụ Mẫu"),
    # === HỖN HỢP — câu khó (12) ===
    ("Vợ tôi bệnh có khỏi không?", "Thê Tài"),
    ("Bố mẹ tôi có khỏe không?", "Phụ Mẫu"),
    ("Con gái thi đại học đỗ không?", "Tử Tôn"),
    ("Công việc vợ tôi thế nào?", "Thê Tài"),
    ("Sếp tôi có tốt không?", "Quan Quỷ"),
    ("Tôi nên đầu tư vàng hay crypto?", "Thê Tài"),
    ("Tiền nhà trả bao lâu?", "Thê Tài"),
    ("Con dâu mang thai có an toàn?", "Tử Tôn"),
    ("Bố tôi sự nghiệp thế nào?", "Phụ Mẫu"),
    ("Mẹ tôi kinh doanh có lãi?", "Phụ Mẫu"),
    ("Vợ tôi có ngoại tình không?", "Thê Tài"),
    ("Chồng tôi có tiền không?", "Quan Quỷ"),
]

# RUN TEST
print("=" * 100)
print(f"{'CÂU HỎI':<45} {'KỲ VỌNG':<15} {'THỰC TẾ':<15} {'KQ':<8} {'CATEGORY':<15} {'PERSON'}")
print("=" * 100)

pass_count = 0
fail_count = 0
dt_stats = {}
fail_list = []

for question, expected_dt in TEST_QUESTIONS:
    cat, actual_dt, person = detect_dt(question)
    ok = actual_dt == expected_dt
    status = "✅" if ok else "❌"
    if ok:
        pass_count += 1
    else:
        fail_count += 1
        fail_list.append((question, expected_dt, actual_dt, cat, person))
    
    dt_stats[actual_dt] = dt_stats.get(actual_dt, 0) + 1
    q_short = question[:42] + "..." if len(question) > 42 else question
    print(f"{q_short:<45} {expected_dt:<15} {actual_dt:<15} {status:<8} {cat:<15} {person}")

print("=" * 100)
print(f"\n📊 KẾT QUẢ: {pass_count} PASS / {fail_count} FAIL / {len(TEST_QUESTIONS)} TOTAL ({pass_count*100//len(TEST_QUESTIONS)}%)")

if fail_list:
    print(f"\n❌ CHI TIẾT FAIL:")
    for q, exp, act, cat, person in fail_list:
        print(f"   Q: {q}")
        print(f"   Expected={exp}, Got={act}, Cat={cat}, Person={person}")
        print()

print(f"\n📈 DT PHÂN BỐ:")
for dt, cnt in sorted(dt_stats.items(), key=lambda x: -x[1]):
    pct = cnt * 100 // len(TEST_QUESTIONS)
    bar = "█" * (pct // 2)
    print(f"   {dt:<15}: {cnt:>3} câu ({pct:>2}%) {bar}")
