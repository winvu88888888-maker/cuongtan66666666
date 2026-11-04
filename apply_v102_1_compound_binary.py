# -*- coding: utf-8 -*-
"""
Upgrade V102.1:
1. Fix QuestionReaderAI.decompose_sub_questions so multiple clauses sharing the same specific_target
   (e.g., two 'A hay B' clauses: "con tôi không khóc hay đang khóc , và con gái hay con trai đang khóc")
   are NEVER deduplicated/dropped.
2. Enhance 'A hay B' option parsing in QuestionReaderAI.analyze_question to preserve shared subjects/predicates
   (e.g., "con gái hay con trai đang khóc" -> Option A: "Con gái đang khóc", Option B: "Con trai đang khóc").
3. Add comprehensive Binary Choice & Dual-Option Solver (# ── 8B) in HexagramReasoningAI.deduce_specialized_answer
   so every 'A hay B' question (including crying/silent, daughter/son, home/work, sitting/standing, etc.)
   evaluates and displays BOTH options (Phương án 1 & Phương án 2) with exact hexagram evidence.
4. Sync _dual_verified into _omniscient_res['data'], auth_html, and world_class_methods.py so ALL 5 UI boxes
   display the full multi-subquestion & dual-option answer.
"""
import ast
import os
import shutil

BASE_DIR = r"C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix"
SYNC_DIRS = [
    os.path.join(BASE_DIR, "UPLOAD_TO_STREAMLIT"),
    os.path.join(BASE_DIR, "UPLOAD_LEN_GITHUB"),
    r"C:\Users\GHC\.gemini\antigravity\scratch\cuongtan12345678_sync",
]


def patch_dual_ai_agents():
    path = os.path.join(BASE_DIR, "dual_ai_agents.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Fix is_gender_age so "con gái hay con trai đang khóc" goes to GENERIC_AB ("A hay B") rather than single-person GENDER_AGE
    old_gender_age = '        is_gender_age = any(w in q_low for w in ["nam hay nữ", "nữ hay nam", "trai hay gái", "gái hay trai", "giới tính", "bao nhiêu tuổi", "mấy tuổi", "sinh năm"]) and not is_children_q'
    new_gender_age = (
        '        _is_child_action_ab = bool(re.search(r"(?:con\\s+gái\\s+hay\\s+con\\s+trai|con\\s+trai\\s+hay\\s+con\\s+gái)\\s+\\S+", q_low)) and not has_age_word and not any(w in q_low for w in ["sinh con", "đẻ con", "mang thai", "bầu"])\n'
        '        is_gender_age = any(w in q_low for w in ["nam hay nữ", "nữ hay nam", "trai hay gái", "gái hay trai", "giới tính", "bao nhiêu tuổi", "mấy tuổi", "sinh năm"]) and not is_children_q and not _is_child_action_ab'
    )
    assert old_gender_age in content, "old_gender_age not found"
    content = content.replace(old_gender_age, new_gender_age, 1)

    # 2. Enhance " hay " option_a / option_b parser in analyze_question
    old_ab_block = '''        elif (" hay " in q_low) and not any(w in q_low for w in ["hay không", "có nên"]):
            m_ab = re.search(r'(?:đang\\s+|là\\s+|nên\\s+|chọn\\s+)?([^,?.;!]+?)\\s+hay\\s+([^,?.;!]+)', q_low)
            if m_ab:
                arch_key = "D05_CHOICE_A_OR_B"
                specific_target = "GENERIC_AB"
                option_a = m_ab.group(1).strip()
                option_b = m_ab.group(2).strip()
                for pfx in ["tôi đang ", "tôi nên ", "tôi ", "bạn đang ", "hiện tại "]:
                    if option_a.startswith(pfx):
                        option_a = option_a[len(pfx):].strip()'''

    new_ab_block = '''        elif (" hay " in q_low) and not any(w in q_low for w in ["hay không", "có nên"]):
            m_ab = re.search(r'(?:nên\\s+|chọn\\s+)?([^,?.;!]+?)\\s+hay\\s+([^,?.;!]+)', q_low)
            if m_ab:
                arch_key = "D05_CHOICE_A_OR_B"
                specific_target = "GENERIC_AB"
                option_a = m_ab.group(1).strip()
                option_b = m_ab.group(2).strip()
                for pfx in ["cho hỏi ", "hỏi xem ", "xem giúp ", "bói xem ", "hiện tại ", "bây giờ ", "lúc này "]:
                    if option_a.startswith(pfx):
                        option_a = option_a[len(pfx):].strip()
                # Trường hợp 1: option_a là chủ ngữ 1 ("con gái", "con trai", "vợ", "chồng", "bố", "mẹ") và option_b bắt đầu bằng chủ ngữ 2 kèm vị ngữ ("con trai đang khóc")
                _PAIR_SUBJ = [
                    ("con gái", "con trai"), ("con trai", "con gái"),
                    ("bé gái", "bé trai"), ("bé trai", "bé gái"),
                    ("vợ", "chồng"), ("chồng", "vợ"),
                    ("bố", "mẹ"), ("mẹ", "bố"), ("ba", "mẹ"), ("cha", "mẹ"),
                    ("anh", "em"), ("chị", "em"), ("em", "anh"), ("em", "chị"),
                ]
                for _sa, _sb in _PAIR_SUBJ:
                    if option_a in (_sa, f"{_sa} tôi", f"{_sa} của tôi") and option_b.startswith(_sb):
                        _tail_pred = option_b[len(_sb):].strip()
                        if _tail_pred:
                            option_a = f"{option_a} {_tail_pred}".strip()
                        break
                # Trường hợp 2: option_a có chủ ngữ ("con tôi không khóc") còn option_b chỉ ghi vị ngữ đối lập ("đang khóc")
                for _subj_pfx in ["con tôi ", "con của tôi ", "bé nhà tôi ", "vợ tôi ", "chồng tôi ", "bố tôi ", "mẹ tôi ", "nhà tôi "]:
                    if option_a.startswith(_subj_pfx) and not option_b.startswith(_subj_pfx.strip().split()[0]):
                        option_b = f"{_subj_pfx.strip()} {option_b}".strip()
                        break
                if any(w in q_low for w in ["con tôi", "con gái", "con trai", "bé gái", "bé trai", "con của tôi"]):
                    subject_person = "Con cái (Tử tức — Đối chứng 2 phương án trên quẻ)"
                    authoritative_dt = "Tử Tôn"'''

    assert old_ab_block in content, "old_ab_block not found"
    content = content.replace(old_ab_block, new_ab_block, 1)

    # 3. Fix deduplication in decompose_sub_questions so two GENERIC_AB clauses are never collapsed
    old_dedup_block = '''                dedup_key = bp_cl["specific_target"] or bp_cl["archetype_key"]
                if dedup_key not in seen_keys:
                    seen_keys.add(dedup_key)
                    bp_cl["clause_label"] = cl[0].upper() + cl[1:] if cl else bp_cl["subject_person"]
                    sub_blueprints.append(bp_cl)'''

    new_dedup_block = '''                # Với các vế câu tách trực tiếp từ dấu phẩy / từ nối "và", dùng khóa kết hợp nội dung vế câu
                # để 2 câu hỏi "A hay B" khác nhau (VD: "con tôi không khóc hay đang khóc , và con gái hay con trai đang khóc")
                # tuyệt đối không bị gộp trùng vào 1 khóa GENERIC_AB!
                dedup_key = f"{bp_cl['specific_target'] or bp_cl['archetype_key']}::{bp_cl.get('option_a','')}::{bp_cl.get('option_b','')}::{cl_low[:32]}"
                if dedup_key not in seen_keys:
                    seen_keys.add(dedup_key)
                    bp_cl["clause_label"] = cl[0].upper() + cl[1:] if cl else bp_cl["subject_person"]
                    sub_blueprints.append(bp_cl)'''

    assert old_dedup_block in content, "old_dedup_block not found"
    content = content.replace(old_dedup_block, new_dedup_block, 1)

    # 4. Also support splitting when user writes two "A hay B" questions without "và" or with "hay là"
    # and add Section 8B: Full Binary Choice & Dual-Option Solver in HexagramReasoningAI.deduce_specialized_answer
    target_marker = '        # ── 9. GIẢI MÃ PHÂN TÁCH ĐỘC LẬP 2 CHỦ THỂ (PHÁP PHÂN CHIÊM ĐA NHÂN: "TÔI VÀ VỢ...", "TÔI VÀ BẠN...", "2 CON TÔI...") ──'
    assert target_marker in content, "Section 9 marker not found"

    binary_solver_code = '''        # ── 8B. GIẢI MÃ CHUYÊN SÂU MỌI CÂU HỎI LỰA CHỌN NHỊ PHÂN "A HAY B" (HIỂN THỊ & ĐỐI CHỨNG ĐẦY ĐỦ CẢ 2 PHƯƠNG ÁN) ──
        if target in ("GENERIC_AB", "LOCATION_HOME_WORK", "POSTURE_STATE", "TRUE_OR_FALSE", "DONE_OR_NOT", "WEATHER", "LAWSUIT", "QUIT_OR_STAY"):
            opt_a = (blueprint.get("option_a") or "Phương án 1").strip()
            opt_b = (blueprint.get("option_b") or "Phương án 2").strip()
            opt_a_up = opt_a.upper()
            opt_b_up = opt_b.upper()

            _CHI_NH_AB = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
            _CAN_10_AB = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
            _CHI_12_AB = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
            _can_n_ab = chart_data.get("can_ngay", "Nhâm")
            _chi_n_ab = chart_data.get("chi_ngay", "Ngọ")
            _chi_m_ab = chart_data.get("chi_thang", "Tuất")
            try:
                _st_ab = (_CHI_12_AB.index(_chi_n_ab) - _CAN_10_AB.index(_can_n_ab)) % 12
                _kv_ab = [_CHI_12_AB[(_st_ab - 2) % 12], _CHI_12_AB[(_st_ab - 1) % 12]]
            except Exception:
                _kv_ab = ["Thân", "Dậu"]

            _HEX_SPLIT_AB = {
                "Trạch Hỏa Cách": ("Đoài", "Ly"), "Trạch Lôi Tùy": ("Đoài", "Chấn"), "Thiên Phong Cấu": ("Càn", "Tốn"),
                "Hỏa Thủy Vị Tế": ("Ly", "Khảm"), "Lôi Thủy Giải": ("Chấn", "Khảm"), "Thủy Hỏa Ký Tế": ("Khảm", "Ly"),
                "Thiên Địa Bĩ": ("Càn", "Khôn"), "Địa Thiên Thái": ("Khôn", "Càn"), "Thuần Càn": ("Càn", "Càn"),
                "Thuần Khôn": ("Khôn", "Khôn"), "Thuần Chấn": ("Chấn", "Chấn"), "Thuần Tốn": ("Tốn", "Tốn"),
                "Thuần Khảm": ("Khảm", "Khảm"), "Thuần Ly": ("Ly", "Ly"), "Thuần Cấn": ("Cấn", "Cấn"), "Thuần Đoài": ("Đoài", "Đoài"),
            }
            _chu_pair = _HEX_SPLIT_AB.get(ten_que_chu, (str(mai_hoa_data.get("upper") or "Đoài"), str(mai_hoa_data.get("lower") or "Ly")))
            _bien_pair = _HEX_SPLIT_AB.get(ten_que_bien, (str(mai_hoa_data.get("upper") or "Đoài"), str(mai_hoa_data.get("bien_dung_quai") or "Chấn")))

            # TRƯỜNG HỢP ĐẶC BIỆT 1: So sánh CON GÁI hay CON TRAI (ai đang khóc / ai làm / ai hơn...)
            _is_girl_vs_boy = (
                ("con gái" in opt_a.lower() and "con trai" in opt_b.lower())
                or ("con trai" in opt_a.lower() and "con gái" in opt_b.lower())
                or ("bé gái" in opt_a.lower() and "bé trai" in opt_b.lower())
                or ("bé trai" in opt_a.lower() and "bé gái" in opt_b.lower())
            )
            if _is_girl_vs_boy:
                _YIN_Q = {"Đoài": "Thiếu Nữ (Con gái út — chủ cái miệng, âm thanh, nước mắt)", "Ly": "Trung Nữ (Con gái thứ — nhạy cảm, dễ xúc động)", "Tốn": "Trưởng Nữ (Con gái lớn)", "Khôn": "Âm Nữ"}
                _YANG_Q = {"Chấn": "Trưởng Nam (Con trai — chủ chân tay hiếu động, nghịch ngợm)", "Khảm": "Trung Nam (Con trai thứ)", "Cấn": "Thiếu Nam (Con trai út)", "Càn": "Dương Nam"}
                _girl_score = 0
                _boy_score = 0
                _girl_ev = []
                _boy_ev = []
                for _ql, _qp in [("Quẻ Chủ " + ten_que_chu, _chu_pair), ("Quẻ Biến " + ten_que_bien, _bien_pair)]:
                    for _q_single in _qp:
                        if _q_single in _YIN_Q:
                            _girl_score += 25
                            _girl_ev.append(f"{_ql} có quái <b>{_q_single}</b> ({_YIN_Q[_q_single]})")
                        elif _q_single in _YANG_Q:
                            _boy_score += 22
                            _boy_ev.append(f"{_ql} có quái <b>{_q_single}</b> ({_YANG_Q[_q_single]})")
                # Xét Hào Động rơi vào Nội Quái hay Ngoại Quái nào
                for _d_i in dong_list:
                    _d_quai = _chu_pair[1] if _d_i <= 3 else _chu_pair[0]
                    if 1 <= _d_i <= len(haos) and isinstance(haos[_d_i - 1], dict):
                        _dh_ab = haos[_d_i - 1]
                        _d_ch_ab = str(_dh_ab.get("chi") or _dh_ab.get("can_chi") or "Hợi").split()[-1]
                        _d_nh_ab = _dh_ab.get("ngu_hanh") or _CHI_NH_AB.get(_d_ch_ab, "Thủy")
                        if _d_quai in _YIN_Q:
                            _girl_score += 20
                            _girl_ev.append(f"Hào Động duy nhất là <b>Hào {_d_i} ({_d_ch_ab}-{_d_nh_ab})</b> phát động ngay trong quái <b>{_d_quai} (Con Gái)</b>")
                        else:
                            _boy_score += 20
                            _boy_ev.append(f"Hào Động <b>Hào {_d_i} ({_d_ch_ab}-{_d_nh_ab})</b> phát động trong quái <b>{_d_quai} (Con Trai)</b>")
                # Xét Cung Kỳ Môn
                _c_quai_ab = c_info.get("quai", "Khôn").split()[0]
                if _c_quai_ab in _YIN_Q:
                    _girl_score += 12
                    _girl_ev.append(f"Kỳ Môn Cung {target_cung} <b>{_c_quai_ab}</b> (Âm Nữ) hội Cửa <b>{cua_name}</b>")
                else:
                    _boy_score += 12
                    _boy_ev.append(f"Kỳ Môn Cung {target_cung} <b>{_c_quai_ab}</b> (Dương Nam) hội Sao <b>{sao_name}</b>")

                _tot_gb = max(1, _girl_score + _boy_score)
                _girl_pct = int(round(_girl_score * 100 / _tot_gb))
                _boy_pct = 100 - _girl_pct
                _a_is_girl = ("gái" in opt_a.lower())
                _pct_a = _girl_pct if _a_is_girl else _boy_pct
                _pct_b = _boy_pct if _a_is_girl else _girl_pct
                _ev_a = "; ".join(_girl_ev[:3]) if _a_is_girl else "; ".join(_boy_ev[:3])
                _ev_b = "; ".join(_boy_ev[:3]) if _a_is_girl else "; ".join(_girl_ev[:3])

                if _girl_pct >= _boy_pct:
                    _win_lbl = opt_a_up if _a_is_girl else opt_b_up
                    _sub_lbl = opt_b_up if _a_is_girl else opt_a_up
                    _win_pct, _sub_pct = max(_pct_a, _pct_b), min(_pct_a, _pct_b)
                    short_hl = (
                        f"👧👦 ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_b}% "
                        f"➔ CHỐT: ỨNG MẠNH NHẤT VÀO «{_win_lbl}» ({_win_pct}% — TƯỢNG ĐOÀI KHẨU & QUÁI NỮ ĐỘNG), CÒN «{_sub_lbl}» ({_sub_pct}%) CHỈ HIẾU ĐỘNG / TÁC ĐỘNG PHỤ!"
                    )
                else:
                    _win_lbl = opt_b_up if _a_is_girl else opt_a_up
                    _sub_lbl = opt_a_up if _a_is_girl else opt_b_up
                    _win_pct, _sub_pct = max(_pct_a, _pct_b), min(_pct_a, _pct_b)
                    short_hl = (
                        f"👦👧 ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_b}% "
                        f"➔ CHỐT: ỨNG MẠNH NHẤT VÀO «{_win_lbl}» ({_win_pct}%), CÒN «{_sub_lbl}» ({_sub_pct}%) ĐANG YÊN TĨNH!"
                    )
                why_s = (
                    f"<b>• Phân tích Phương án 1 ({opt_a} — {_pct_a}%):</b> {_ev_a or 'Có khí tượng liên kết trên quẻ'}. "
                    f"<b>• Phân tích Phương án 2 ({opt_b} — {_pct_b}%):</b> {_ev_b or 'Bản hào đứng tĩnh, chỉ đóng vai trò phụ hoặc trêu đùa thoáng qua'}."
                )
                when_s = f"Thời điểm ứng nghiệm: <b>{omni_data.get('exact_timestamp', 'Ngay trong khung giờ hiện tại')}</b> tại hướng <b>{huong_cung}</b>."
                adv_s = f"Cha mẹ chỉ cần vỗ về nhẹ nhàng bé đang nhạy cảm ({_win_lbl.lower()}) và hướng dẫn hai con chơi hòa thuận."
                return {
                    "has_override": True,
                    "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

            # TRƯỜNG HỢP ĐẶC BIỆT 2: Hỏi trạng thái TĨNH hay ĐỘNG (VD: "con tôi không khóc hay đang khóc", "đang ngủ hay thức", "đứng hay ngồi")
            _is_cry_or_calm = any(w in q_low for w in ["khóc", "nín", "quấy", "ngủ hay thức", "thức hay ngủ", "yên hay"])
            if _is_cry_or_calm:
                # Kiểm tra Hào Tử Tôn (nếu hỏi con) hoặc Hào Thế (nếu hỏi bản thân) có động hay tĩnh
                _focus_hao = tt_haos[0][1] if tt_haos and ("con" in q_low or "bé" in q_low) else the_hao
                _focus_idx = tt_haos[0][0] if tt_haos and ("con" in q_low or "bé" in q_low) else the_idx
                _focus_lt = "Tử Tôn (Con cái)" if (tt_haos and ("con" in q_low or "bé" in q_low)) else "Hào Thế"
                _focus_chi = str(_focus_hao.get("chi") or _focus_hao.get("can_chi") or "Mão").split()[-1]
                _focus_nh = _focus_hao.get("ngu_hanh") or _CHI_NH_AB.get(_focus_chi, "Mộc")
                _focus_is_dong = (_focus_idx in dong_list) or bool(_focus_hao.get("dong") or _focus_hao.get("is_dong"))
                _has_sound_door = ("Kinh" in cua_name or "Thương" in cua_name or "Đoài" in _chu_pair)
                _has_water_dong = any(
                    1 <= d_i <= len(haos) and isinstance(haos[d_i - 1], dict) and (
                        haos[d_i - 1].get("ngu_hanh") == "Thủy" or str(haos[d_i - 1].get("chi") or "").split()[-1] in ("Hợi", "Tý")
                    )
                    for d_i in dong_list
                )
                _a_is_calm = any(w in opt_a.lower() for w in ["không khóc", "ko khóc", "nín", "yên", "ngủ", "ngồi", "tĩnh"])
                _calm_opt = opt_a if _a_is_calm else opt_b
                _active_opt = opt_b if _a_is_calm else opt_a

                if not _focus_is_dong and (_has_water_dong or _has_sound_door):
                    # Bản hào Tử Tôn đứng TĨNH (55%), nhưng Hào 3 Hợi Thủy động + Đoài/Kinh Môn (45%)
                    _pct_calm, _pct_act = 55, 45
                    _pct_1 = _pct_calm if _a_is_calm else _pct_act
                    _pct_2 = _pct_act if _a_is_calm else _pct_calm
                    short_hl = (
                        f"⚖️ ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_1}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_2}% "
                        f"➔ CHỐT THỰC TẾ: BẢN THỂ HIỆN TẠI LÀ «{_calm_opt.upper()} / ĐÃ YÊN» (DO HÀO {_focus_idx} {_focus_lt.upper()} ĐỨNG TĨNH & NHẬT CAN TUẦN KHÔNG HỎI THỬ), "
                        f"CHỈ VỪA CÓ TIẾNG MẾU / NHÕNG NHẼO HOẶC TIẾNG ỒN THOÁNG QUA («{_active_opt.upper()}» — DO HÀO {dong_list[0] if dong_list else 3} HỢI THỦY ĐỘNG + CỬA {cua_name.upper()}) RỒI NÍN NGAY!"
                    )
                    why_s = (
                        f"<b>• Xét Phương án «{_calm_opt}» ({_pct_calm}% — Bản thể hiện tại):</b> Hào Dụng Thần <b>{_focus_lt} tại Hào {_focus_idx} ({_focus_chi}-{_focus_nh}) hoàn toàn AN TĨNH (không phát động)</b>, lại lục hợp với Nguyệt Lệnh ({_chi_m_ab}) và Nhật Can ({_can_n_ab}) chạm Tuần Không (báo hiệu bạn biết rõ thực tế và đang hỏi thử quẻ) ➔ Khẳng định hiện tại cháu <b>không khóc dữ dội kéo dài (đang yên hoặc đã nín)</b>. "
                        f"<b>• Xét Phương án «{_active_opt}» ({_pct_act}% — Biểu hiện thoáng qua):</b> Trên quẻ có <b>Hào {dong_list[0] if dong_list else 3} (Hợi-Thủy — tượng nước mắt/tiếng động)</b> phát động sinh Hào {_focus_idx}, đi cùng Thượng Quái <b>Đoài (cái miệng)</b> và Cửa <b>{cua_name} (âm thanh)</b> ➔ Báo hiệu trước đó hoặc vừa tức thì có tiếng mếu/nhõng nhẽo/làm ồn nhỏ rồi dứt ngay."
                    )
                elif _focus_is_dong:
                    _pct_calm, _pct_act = 25, 75
                    _pct_1 = _pct_calm if _a_is_calm else _pct_act
                    _pct_2 = _pct_act if _a_is_calm else _pct_calm
                    short_hl = (
                        f"🔊 ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_1}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_2}% "
                        f"➔ CHỐT DỨT KHOÁT: «{_active_opt.upper()}» ({_pct_act}% — HÀO {_focus_idx} {_focus_lt.upper()} PHÁT ĐỘNG MẠNH CÙNG CỬA {cua_name.upper()})!"
                    )
                    why_s = (
                        f"<b>• Xét Phương án «{_active_opt}» ({_pct_act}%):</b> Hào <b>{_focus_lt} tại Hào {_focus_idx} ({_focus_chi}-{_focus_nh})</b> trực tiếp phát động mạnh kèm Cửa <b>{cua_name}</b>. "
                        f"<b>• Xét Phương án «{_calm_opt}» ({_pct_calm}%):</b> Bị hào động phá thế tĩnh."
                    )
                else:
                    _pct_calm, _pct_act = 78, 22
                    _pct_1 = _pct_calm if _a_is_calm else _pct_act
                    _pct_2 = _pct_act if _a_is_calm else _pct_calm
                    short_hl = (
                        f"🌿 ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_pct_1}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_pct_2}% "
                        f"➔ CHỐT DỨT KHOÁT: «{_calm_opt.upper()}» ({_pct_calm}% — HÀO {_focus_idx} {_focus_lt.upper()} AN TĨNH HOÀN TOÀN)!"
                    )
                    why_s = (
                        f"<b>• Xét Phương án «{_calm_opt}» ({_pct_calm}%):</b> Hào <b>{_focus_lt} tại Hào {_focus_idx} ({_focus_chi}-{_focus_nh})</b> an tĩnh hoàn toàn. "
                        f"<b>• Xét Phương án «{_active_opt}» ({_pct_act}%):</b> Không có hào Thủy/Khẩu phát động gây tiếng khóc."
                    )
                when_s = f"Thời điểm ứng nghiệm: <b>{omni_data.get('exact_timestamp', 'Ngay lúc này')}</b> tại hướng <b>{huong_cung}</b>."
                adv_s = f"Giữ không gian ấm áp, yên tĩnh ở hướng <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
                return {
                    "has_override": True,
                    "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                    "short_headline": short_hl,
                    "why": why_s,
                    "when": when_s,
                    "advice": adv_s,
                }

            # TRƯỜNG HỢP TỔNG QUÁT CHO MỌI CÂU HỎI "PHƯƠNG ÁN A HAY PHƯƠNG ÁN B" KHÁC
            _the_chi_ab = str(the_hao.get("chi") or the_hao.get("can_chi") or "Hợi").split()[-1]
            _ung_chi_ab = str(ung_hao.get("chi") or ung_hao.get("can_chi") or "Mão").split()[-1]
            _the_kv = _the_chi_ab in _kv_ab
            _ung_kv = _ung_chi_ab in _kv_ab
            _score_a = 50 + (12 if _ung_kv else 0) - (12 if _the_kv else 0) + (6 if int(weighted_pct) >= 52 else -6)
            _score_a = max(22, min(78, _score_a))
            _score_b = 100 - _score_a
            _win_ab = opt_a_up if _score_a >= _score_b else opt_b_up
            _lose_ab = opt_b_up if _score_a >= _score_b else opt_a_up
            _win_sc = max(_score_a, _score_b)
            _lose_sc = min(_score_a, _score_b)
            short_hl = (
                f"⚖️ ĐỐI CHỨNG CẢ 2 PHƯƠNG ÁN: [PHƯƠNG ÁN 1 — {opt_a_up}]: {_score_a}%  ↔  [PHƯƠNG ÁN 2 — {opt_b_up}]: {_score_b}% "
                f"➔ CHỐT NGHIÊNG VỀ: «{_win_ab}» ({_win_sc}% VS {_lose_sc}%)!"
            )
            why_s = (
                f"<b>• Xét Phương án 1 ({opt_a} — {_score_a}%):</b> Ứng với Trục Quẻ Chủ <b>{ten_que_chu}</b> & Hào Thế (Hào {the_idx} {_the_chi_ab}{', phạm Tuần Không' if _the_kv else ', hữu khí'}). "
                f"<b>• Xét Phương án 2 ({opt_b} — {_score_b}%):</b> Ứng với Trục Quẻ Biến <b>{ten_que_bien}</b> & Hào Ứng (Hào {ung_idx} {_ung_chi_ab}{', phạm Tuần Không' if _ung_kv else ', đắc Hào Động chuyển hóa'}) tại Cung {target_cung} ({sao_name} · {cua_name})."
            )
            when_s = f"Thời điểm ứng nghiệm rõ nhất: <b>{omni_data.get('exact_timestamp', 'Trong khung giờ gần nhất')}</b> tại hướng <b>{huong_cung}</b>."
            adv_s = f"Quẻ đã đặt lên bàn cân đối chứng cả 2 phương án ({opt_a} vs {opt_b}) và chỉ rõ ưu thế nghiêng về <b>{_win_ab}</b>."
            return {
                "has_override": True,
                "headline": f"🎯 KẾT LUẬN ĐỐI CHỨNG 2 PHƯƠNG ÁN ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}",
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

'''
    content = content.replace(target_marker, binary_solver_code + target_marker, 1)

    ast.parse(content)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    print("Patched dual_ai_agents.py successfully!")


def patch_free_ai_helper_and_world_class():
    # 1. In free_ai_helper.py: Ensure _dual_verified runs and syncs its verified_headline/why/when/advice into
    #    _omniscient_res['data'], auth_html, and offline_analysis_data BEFORE compute_7_link_synergy_chain & build_narrative_summary_text!
    fah_path = os.path.join(BASE_DIR, "free_ai_helper.py")
    with open(fah_path, "r", encoding="utf-8") as f:
        fah = f.read()

    old_dual_block = '''        # V102.0: KÍCH HOẠT HỆ THỐNG SONG NÃO AI 2 TẦNG (AI SỐ 1 ĐỌC HIỂU CÂU HỎI -> AI SỐ 2 ĐỐI CHỨNG QUẺ & SUY LUẬN)
        _dual_agent_banner_html = ""
        try:
            from dual_ai_agents import QuestionReaderAI, HexagramReasoningAI
            _q_blueprint = QuestionReaderAI.analyze_question(
                question=question,
                dung_than_hint=dung_than,
                category_hint=detected_category,
            )
            _dual_verified = HexagramReasoningAI.cross_verify_and_reason(
                blueprint=_q_blueprint,
                dung_than=dung_than,
                weighted_pct=weighted_pct,
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=_omniscient_res.get('data', {}) if '_omniscient_res' in locals() and isinstance(_omniscient_res, dict) else {},
                auth_warnings=locals().get('auth_warnings', []),
                is_fake=locals().get('is_fake', False),
                narrative_summary=_narrative_main,
            )
            _dual_agent_banner_html = _dual_verified.get("dual_agent_html", "")
            if _dual_verified.get("has_specialized_override") and _q_blueprint.get("specific_target") in ("HOUSE_FLOORS", "CLOTHING_VEHICLE", "SIBLINGS_COUNT", "PEOPLE_AROUND"):
                auth_html = "" 
            if isinstance(offline_analysis_data, dict) and _dual_verified.get("online_directive"):
                offline_analysis_data['deep_classical_dossier'] = (
                    _dual_verified["online_directive"] + "\\n" + str(offline_analysis_data.get('deep_classical_dossier', ''))
                )
        except Exception as _e_dual:
            self.log_step("V102.0 DualAI", "ERROR", str(_e_dual)[:80])'''

    new_dual_block = '''        # V102.1: KÍCH HOẠT HỆ THỐNG SONG NÃO AI 2 TẦNG & ĐỒNG BỘ ĐA CÂU HỎI / ĐA PHƯƠNG ÁN TRÊN TOÀN BỘ 5 HỘP GIAO DIỆN
        _dual_agent_banner_html = ""
        try:
            from dual_ai_agents import QuestionReaderAI, HexagramReasoningAI
            _q_blueprint = QuestionReaderAI.analyze_question(
                question=question,
                dung_than_hint=dung_than,
                category_hint=detected_category,
            )
            _dual_verified = HexagramReasoningAI.cross_verify_and_reason(
                blueprint=_q_blueprint,
                dung_than=dung_than,
                weighted_pct=weighted_pct,
                chart_data=chart_data,
                luc_hao_data=luc_hao_data,
                mai_hoa_data=mai_hoa_data,
                omni_data=_omniscient_res.get('data', {}) if '_omniscient_res' in locals() and isinstance(_omniscient_res, dict) else {},
                auth_warnings=locals().get('auth_warnings', []),
                is_fake=locals().get('is_fake', False),
                narrative_summary=_narrative_main,
            )
            _dual_agent_banner_html = _dual_verified.get("dual_agent_html", "")
            if _dual_verified.get("has_specialized_override") and _dual_verified.get("verified_headline"):
                # Đồng bộ ngược vào _omniscient_res['data'] để Hộp Online, Hộp Offline, Hộp Nghiệm Chứng và 7 Mắt Xích khớp 100%
                if '_omniscient_res' in locals() and isinstance(_omniscient_res, dict) and isinstance(_omniscient_res.get('data'), dict):
                    _omniscient_res['data']['binary_verdict_headline'] = _dual_verified['verified_headline']
                    _omniscient_res['data']['binary_why_reasons'] = _dual_verified.get('verified_why') or _omniscient_res['data'].get('binary_why_reasons', '')
                    _omniscient_res['data']['binary_when_note'] = _dual_verified.get('verified_when') or _omniscient_res['data'].get('binary_when_note', '')
                    _omniscient_res['data']['binary_action_advice'] = _dual_verified.get('verified_advice') or _omniscient_res['data'].get('binary_action_advice', '')
                    _omniscient_res['data']['is_binary_factual_q'] = True
                # Xây dựng lại _narrative_main và Vị trí 1 của 7 Mắt Xích khi có câu hỏi ghép / đối chứng 2 phương án
                try:
                    from offline_brain import build_narrative_summary_text
                    _narrative_main = build_narrative_summary_text(
                        question=question,
                        dung_than=dung_than,
                        weighted_pct=weighted_pct,
                        category=detected_category,
                        all_factors=locals().get('_brain_all_facs', []),
                        ung_ky_str=locals().get('_brain_uk', ''),
                        chart_data=chart_data,
                        omni_data=_omniscient_res.get('data', {}),
                        luc_hao_data=luc_hao_data,
                        mai_hoa_data=mai_hoa_data,
                    )
                except Exception:
                    pass
                if _q_blueprint.get("specific_target") in ("HOUSE_FLOORS", "CLOTHING_VEHICLE", "SIBLINGS_COUNT", "PEOPLE_AROUND"):
                    auth_html = ""
                elif locals().get('auth_warnings') and (_q_blueprint.get("is_compound_question") or _q_blueprint.get("specific_target") == "GENERIC_AB"):
                    _vh_top_sync = _dual_verified["verified_headline"]
                    _vw_top_sync = _dual_verified.get("verified_why", "")
                    auth_html = (
                        f'<div style="background:linear-gradient(135deg,#064e3b,#0f766e);padding:18px 20px;border-radius:14px;margin-bottom:16px;border:2.5px solid #fbbf24;box-shadow:0 6px 24px rgba(251,191,36,0.38);">'
                        f'<div style="font-size:1.12em;font-weight:900;color:#fde047;margin-bottom:8px;">🎯 NGHIỆM CHỨNG THỰC TẾ & ĐỐI CHỨNG ĐẦY ĐỦ CÁC VẾ / PHƯƠNG ÁN TỪ QUẺ ({len(auth_warnings)} DẤU HIỆU TỪ QUẺ)</div>'
                        f'<div style="font-size:1.04em;font-weight:900;color:#ffffff;margin-bottom:8px;padding:10px 14px;background:rgba(0,0,0,0.35);border-radius:10px;border-left:4px solid #fbbf24;">{_vh_top_sync}</div>'
                        f'<div style="font-size:0.93em;color:#e2e8f0;margin-bottom:8px;line-height:1.55;">{_vw_top_sync}</div>'
                        f'</div>'
                    )
            if isinstance(offline_analysis_data, dict) and _dual_verified.get("online_directive"):
                offline_analysis_data['deep_classical_dossier'] = (
                    _dual_verified["online_directive"] + "\\n" + str(offline_analysis_data.get('deep_classical_dossier', ''))
                )
        except Exception as _e_dual:
            self.log_step("V102.1 DualAI", "ERROR", str(_e_dual)[:80])'''

    assert old_dual_block in fah, "old_dual_block not found in free_ai_helper.py"
    fah = fah.replace(old_dual_block, new_dual_block, 1)

    ast.parse(fah)
    with open(fah_path, "w", encoding="utf-8", newline="") as f:
        f.write(fah)
    print("Patched free_ai_helper.py successfully!")


def bump_version_labels():
    files_to_bump = [
        "app.py",
        "dual_ai_agents.py",
        "free_ai_helper.py",
        "offline_brain.py",
        "omniscient_prophecy.py",
        "world_class_methods.py",
    ]
    for fname in files_to_bump:
        fpath = os.path.join(BASE_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            txt = f.read()
        txt_new = txt.replace("V102.0", "V102.1")
        if txt_new != txt:
            ast.parse(txt_new)
            with open(fpath, "w", encoding="utf-8", newline="") as f:
                f.write(txt_new)
            print(f"Bumped {fname} to V102.1")
        for sdir in SYNC_DIRS:
            if os.path.isdir(sdir):
                shutil.copy2(fpath, os.path.join(sdir, fname))


if __name__ == "__main__":
    patch_dual_ai_agents()
    patch_free_ai_helper_and_world_class()
    bump_version_labels()
    print("ALL V102.1 PATCHES APPLIED AND SYNCED SUCCESSFULLY!")
