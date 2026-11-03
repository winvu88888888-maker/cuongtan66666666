"""
LUC HAO EXPERT AI - Chuyên Gia Lục Hào Kinh Dịch (V100.1 Deep Focus)
Luận giải quẻ Lục Hào thực chiến từ đúng hào Dụng Thần (kể cả Phục Thần ẩn tàng), Hào Thế, Hào Ứng, Lục Thú & Hào Động.
"""

LUC_THAN = {
    "Phụ Mẫu": {"tuong": "Cha mẹ, Bề trên, Giấy tờ, Nhà cửa, Đất đai, Xe cộ, Trường học", "hanh_dong": "Che chở, Pháp lý, Văn thư"},
    "Huynh Đệ": {"tuong": "Anh chị em, Bạn bè, Đồng nghiệp, Đối thủ cạnh tranh", "hanh_dong": "Tranh đoạt, Chia sẻ, Hao tài"},
    "Tử Tôn": {"tuong": "Con cái, Hậu bối, Thuốc men, Bác sĩ, Nguồn vốn sinh tài, Bình an", "hanh_dong": "Giải họa, Khắc Quan Quỷ, Sinh Thê Tài"},
    "Thê Tài": {"tuong": "Vợ, Bạn gái, Tiền bạc, Lợi nhuận, Tài sản, Đồ vật sở hữu", "hanh_dong": "Dưỡng mệnh, Sinh Quan, Khắc Phụ Mẫu"},
    "Quan Quỷ": {"tuong": "Chồng, Bạn trai, Công việc, Chức vụ, Cấp trên, Bệnh tật, Kẻ gian", "hanh_dong": "Quản thúc, Áp lực, Danh vị"},
    "Bản Thân": {"tuong": "Chính người hỏi (Hào Thế)", "hanh_dong": "Chủ thể hành sự"}
}

NGU_HANH_SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
NGU_HANH_KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}

LUC_THU_MEANING = {
    "Thanh Long": "Hỷ tín, chân thành, chính đáng, tốt lành",
    "Chu Tước": "Lời nói, tin tức, tranh luận hoặc giấy tờ",
    "Câu Trần": "Chậm trễ, vướng bận, gắn kết lâu dài hoặc đất đai",
    "Đằng Xà": "Lo âu, nghi ngờ, tâm sự rối ren hoặc biến động bất ngờ",
    "Bạch Hổ": "Áp lực mạnh, nóng nảy, bệnh tật hoặc quyết liệt",
    "Huyền Vũ": "Tâm sự giấu kín, mờ ám, lạnh nhạt hoặc thất thoát ngầm",
}


class LucHaoExpertAI:
    """Chuyên gia Lục Hào Kinh Dịch — phân tích trực tiếp 6 hào thực tế của quẻ."""

    def __init__(self, gemini_helper=None):
        self.gemini = gemini_helper

    def _infer_dung_than_name(self, topic, explicit_dt=None):
        if explicit_dt and explicit_dt in LUC_THAN:
            return explicit_dt
        q = (topic or "").lower()
        if any(w in q for w in ["vợ", "bạn gái", "người yêu", "tiền", "tài", "lương", "đầu tư", "lời", "lãi", "mua bán", "mất ví", "mất tiền", "mất đồ"]):
            return "Thê Tài"
        if any(w in q for w in ["chồng", "bạn trai", "việc", "sự nghiệp", "thăng chức", "sếp", "kiện"]):
            return "Quan Quỷ"
        if any(w in q for w in ["bố", "mẹ", "cha", "ông", "bà", "nhà", "đất", "hợp đồng", "thi", "học", "giấy tờ"]):
            return "Phụ Mẫu"
        if any(w in q for w in ["con", "thai", "thuốc", "chữa", "bác sĩ"]):
            return "Tử Tôn"
        if any(w in q for w in ["anh", "chị", "em", "bạn bè", "đối thủ"]):
            return "Huynh Đệ"
        return "Bản Thân"

    def analyze_luc_hao(self, luc_hao_data, topic="Chung", dung_than_override=None):
        data = luc_hao_data if isinstance(luc_hao_data, dict) else {}
        ban = data.get("ban", {}) if isinstance(data.get("ban"), dict) else {}
        bien = data.get("bien", {}) if isinstance(data.get("bien"), dict) else {}
        haos = ban.get("haos") or data.get("haos") or ban.get("details") or []
        dong_hao_list = data.get("dong_hao") or []

        dt_name = self._infer_dung_than_name(topic, dung_than_override)
        the_hao = None
        ung_hao = None
        dt_hao = None

        for idx, h in enumerate(haos, 1):
            if not isinstance(h, dict):
                continue
            h_copy = dict(h)
            h_copy.setdefault("hao", h.get("hao", idx))
            tu_str = str(h.get("the_ung", h.get("tu", "")))
            lt_str = str(h.get("luc_than", ""))
            if "Thế" in tu_str:
                the_hao = h_copy
            elif "Ứng" in tu_str:
                ung_hao = h_copy
            if dt_name != "Bản Thân" and lt_str == dt_name and dt_hao is None:
                dt_hao = h_copy

        is_phuc_than = False
        if dt_hao is None:
            if dt_name == "Bản Thân" and the_hao:
                dt_hao = the_hao
            else:
                is_phuc_than = True
                phuc_list = data.get("phuc_than") or ban.get("phuc_than") or []
                phuc_match = None
                if isinstance(phuc_list, list):
                    for pt in phuc_list:
                        if isinstance(pt, dict) and str(pt.get("luc_than", "")) == dt_name:
                            phuc_match = pt
                            break
                dt_hao = phuc_match or {
                    "hao": "Ẩn (Phục Thần)",
                    "chi": "?",
                    "ngu_hanh": "?",
                    "vuong_suy": "Phục Thần (Ẩn)",
                    "luc_thu": ""
                }

        hao_num = dt_hao.get("hao", 1)
        chi = dt_hao.get("chi", dt_hao.get("can_chi", "?"))
        hanh_dt = dt_hao.get("ngu_hanh") or dt_hao.get("hanh") or "?"
        vs = str(dt_hao.get("vuong_suy", "Phục Thần (Ẩn)" if is_phuc_than else "Bình"))
        luc_thu = dt_hao.get("luc_thu", dt_hao.get("luc_than_kd", ""))
        is_dong = (not is_phuc_than) and ((hao_num in dong_hao_list) or bool(dt_hao.get("is_moving") or dt_hao.get("dong")))

        # Tính điểm từ Vượng/Suy thực tế của hào Dụng Thần
        vs_up = vs.upper()
        if is_phuc_than:
            score = 38
        elif "VƯỢNG" in vs_up:
            score = 82
        elif "TƯỚNG" in vs_up:
            score = 72
        elif "HƯU" in vs_up:
            score = 54
        elif "TÙ" in vs_up:
            score = 38
        elif "TỬ" in vs_up or "TUYỆT" in vs_up:
            score = 25
        else:
            score = 52

        # Phân tích tương tác Thế - Ứng & Thế - Dụng Thần
        the_hanh = (the_hao.get("ngu_hanh") or the_hao.get("hanh") or "?") if the_hao else "?"
        ung_hanh = (ung_hao.get("ngu_hanh") or ung_hao.get("hanh") or "?") if ung_hao else "?"
        the_chi = the_hao.get("chi", "?") if the_hao else "?"
        ung_chi = ung_hao.get("chi", "?") if ung_hao else "?"
        the_lt = the_hao.get("luc_thu", "") if the_hao else ""
        ung_lt = ung_hao.get("luc_thu", "") if ung_hao else ""

        rel_str = f"Hào Thế ({the_chi}-{the_hanh}) và Hào Ứng ({ung_chi}-{ung_hanh})"
        if the_hanh != "?" and ung_hanh != "?":
            if NGU_HANH_SINH.get(ung_hanh) == the_hanh:
                rel_str += f": Ứng sinh Thế ({ung_hanh} sinh {the_hanh}) → Đối phương/hoàn cảnh vẫn hướng về và nâng đỡ bạn"
                score += 10
            elif NGU_HANH_SINH.get(the_hanh) == ung_hanh:
                rel_str += f": Thế sinh Ứng ({the_hanh} sinh {ung_hanh}) → Bạn là người nặng lòng, chủ động cho đi/nhường nhịn nhiều hơn"
            elif the_hanh == ung_hanh:
                rel_str += f": Thế Ứng Tỷ Hòa (cùng hành {the_hanh}) → Hai bên đồng điệu, dễ tìm tiếng nói chung"
                score += 6
            elif NGU_HANH_KHAC.get(the_hanh) == ung_hanh:
                rel_str += f": Thế khắc Ứng ({the_hanh} khắc {ung_hanh}) → Bạn nắm quyền chủ động nhưng dễ gây áp lực cho đối phương"
            elif NGU_HANH_KHAC.get(ung_hanh) == the_hanh:
                rel_str += f": Ứng khắc Thế ({ung_hanh} khắc {the_hanh}) → Đối phương đang bất mãn, lạnh nhạt hoặc tạo áp lực lên bạn"
                score -= 10

        score = max(15, min(95, score))
        verdict = "CÁT" if score >= 60 else ("BÌNH" if score >= 45 else "HUNG")
        thu_desc = LUC_THU_MEANING.get(luc_thu, "")
        dong_txt = "ĐỘNG (đang có biến chuyển rõ rệt)" if is_dong else "TĨNH (trạng thái đang giữ nguyên, ít bộc lộ)"

        if is_phuc_than:
            summary = (
                f"Quẻ {ban.get('name', '?')} → {bien.get('name', 'Tĩnh')}: "
                f"Dụng Thần {dt_name} đang ẩn phục (Phục Thần — chưa lộ diện trực tiếp trên 6 hào chính, tâm tư hoặc kết quả còn giấu kín)"
            )
        else:
            summary = (
                f"Quẻ {ban.get('name', '?')} → {bien.get('name', 'Tĩnh')}: "
                f"Dụng Thần {dt_name} tại Hào {hao_num} ({chi} - hành {hanh_dt}), khí lực [{vs}], {dong_txt}"
                + (f", lâm {luc_thu} ({thu_desc})" if luc_thu else "")
            )

        return {
            "dung_than": {"ten": dt_name, "tuong": LUC_THAN.get(dt_name, {}).get("tuong", ""), "ly_do": f"Trọng tâm '{topic}' quy về {dt_name}"},
            "dung_than_status": {
                "hao": hao_num, "can_chi": f"{chi} ({hanh_dt})", "dong": is_dong,
                "strength": vs, "score": score, "mo_ta": summary
            },
            "dong_hao": {
                "so_luong": len(dong_hao_list),
                "danh_sach": dong_hao_list,
                "mo_ta": f"Hào động: {', '.join(str(x) for x in dong_hao_list)}" if dong_hao_list else "Lục hào tĩnh — sự việc âm ỉ bên trong",
                "y_nghia": f"Biến quái: {bien.get('name', 'Không đổi')}"
            },
            "the_ung": {
                "mo_ta": f"Thế Hào {the_hao.get('hao','?') if the_hao else '?'} ({the_chi}) ↔ Ứng Hào {ung_hao.get('hao','?') if ung_hao else '?'} ({ung_chi})",
                "relation": rel_str,
                "quan_he": rel_str,
                "y_nghia": f"Thế lâm {the_lt or '?'} | Ứng lâm {ung_lt or '?'}"
            },
            "bien": {"ten": bien.get("name", "Không đổi"), "y_nghia": f"Xu hướng biến chuyển sang quẻ {bien.get('name', 'Tĩnh')}", "giai_doan": "Kết cục"},
            "thoi_gian": {"so_ngay": hao_num if isinstance(hao_num, int) else 7, "khoang": f"Ứng vào ngày/tháng Địa Chi {chi}", "toc_do": "nhanh" if is_dong else "từ từ", "mo_ta": f"Ứng kỳ tại chi {chi} (Hào {hao_num})"},
            "ket_luan": {
                "diem": score,
                "verdict": verdict,
                "summary": summary,
                "tom_tat": summary,
                "loi_khuyen": rel_str
            }
        }

    def get_detailed_interpretation(self, luc_hao_data, topic="Chung"):
        res = self.analyze_luc_hao(luc_hao_data, topic)
        kl = res["ket_luan"]
        return f"## 📜 LỤC HÀO THỰC CHIẾN: {kl['verdict']} ({kl['diem']}%)\n- {kl['summary']}\n- {res['the_ung']['relation']}"


_expert = None
def get_luc_hao_expert(gemini_helper=None):
    global _expert
    if _expert is None:
        _expert = LucHaoExpertAI(gemini_helper)
    return _expert
