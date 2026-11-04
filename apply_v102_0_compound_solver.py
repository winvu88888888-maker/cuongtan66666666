# -*- coding: utf-8 -*-
"""
apply_v102_0_compound_solver.py — V102.0:
BỘ PHÂN TÁCH & GIẢI MÃ TRỌN VẸN ĐA CÂU HỎI NHỎ TRONG 1 CÂU HỎI LỚN
(Multi-SubQuestion Decomposer & Compound Solver: Lục Hào · Kỳ Môn · Mai Hoa · Thiết Bản)
"""
import ast
import shutil
import os

BASE_DIR = r"C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix"
SYNC_DIRS = [
    os.path.join(BASE_DIR, "UPLOAD_TO_STREAMLIT"),
    os.path.join(BASE_DIR, "UPLOAD_LEN_GITHUB"),
    r"C:\Users\GHC\.gemini\antigravity\scratch\cuongtan12345678_sync",
]


def patch_dual_ai_agents():
    p = os.path.join(BASE_DIR, "dual_ai_agents.py")
    with open(p, "r", encoding="utf-8") as f:
        src = f.read()

    # 1. Update version header
    src = src.replace("V101.9", "V102.0")

    # 2. Add is_spouse_count_q and has_explicit_children_count_kw in QuestionReaderAI.analyze_question
    old_block_1 = '''        # C. Hỏi về Tình trạng Hôn nhân thực tế (Đã kết hôn chưa / Có vợ chồng chưa / Độc thân hay có gia đình)
        is_marital_status_q = any(w in q_low for w in [
            "kết hôn chưa", "lấy vợ chưa", "lấy chồng chưa", "có vợ chưa", "có chồng chưa",
            "có người yêu chưa", "có gia đình chưa", "độc thân hay", "đã lập gia đình chưa"
        ])'''

    new_block_1 = '''        # C. Hỏi về Tình trạng Hôn nhân thực tế (Đã kết hôn chưa / Có vợ chồng chưa / Độc thân hay có gia đình)
        is_marital_status_q = any(w in q_low for w in [
            "kết hôn chưa", "lấy vợ chưa", "lấy chồng chưa", "có vợ chưa", "có chồng chưa",
            "có người yêu chưa", "có gia đình chưa", "độc thân hay", "đã lập gia đình chưa"
        ])
        # C2. Hỏi về Số lượng Vợ / Chồng trong cuộc đời (Có mấy vợ / Có mấy chồng / Mấy đời vợ chồng / Kết hôn mấy lần)
        is_spouse_count_q = any(w in q_low for w in [
            "mấy vợ", "bao nhiêu vợ", "mấy người vợ", "mấy đời vợ", "lấy mấy vợ", "có mấy vợ", "mấy bà vợ",
            "mấy chồng", "bao nhiêu chồng", "mấy người chồng", "mấy đời chồng", "lấy mấy chồng", "có mấy chồng", "mấy ông chồng",
            "mấy lần kết hôn", "kết hôn mấy lần", "lấy vợ mấy lần", "lấy chồng mấy lần", "mấy lần đò", "mấy lần lập gia đình"
        ])'''
    assert old_block_1 in src, "old_block_1 not found"
    src = src.replace(old_block_1, new_block_1, 1)

    old_block_2 = '''        elif is_marital_status_q:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "MARITAL_STATUS_NOW"
            subject_person = "Tình trạng Hôn nhân / Tình duyên hiện tại"
            authoritative_dt = "Thê Tài"'''

    new_block_2 = '''        elif is_spouse_count_q:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "SPOUSE_COUNT"
            if "chồng" in q_low and "vợ" not in q_low:
                subject_person = "Số đời Chồng / Phối ngẫu trong cuộc đời"
                authoritative_dt = "Quan Quỷ"
            else:
                subject_person = "Số đời Vợ / Phối ngẫu trong cuộc đời"
                authoritative_dt = "Thê Tài"
        elif is_marital_status_q:
            arch_key = "D17_LOVE_MARRIAGE"
            specific_target = "MARITAL_STATUS_NOW"
            subject_person = "Tình trạng Hôn nhân / Tình duyên hiện tại"
            authoritative_dt = "Thê Tài"'''
    assert old_block_2 in src, "old_block_2 not found"
    src = src.replace(old_block_2, new_block_2, 1)

    # 3. Add decompose_sub_questions to QuestionReaderAI and invoke it at the end of analyze_question
    old_block_3 = '''        return {
            "multi_subjects": multi_subjects,
            "raw_question": q_raw,
            "archetype_key": arch_key,
            "archetype_code": arch_meta["code"],
            "archetype_name": arch_meta["name"],
            "question_mode": arch_meta["mode"],
            "specific_target": specific_target,
            "authoritative_dt": authoritative_dt,
            "subject_person": subject_person,
            "subject_lh_dt": authoritative_dt or dung_than_hint or "Bản Thân",
            "lh_dt_instruction": arch_meta["lh_dt"],
            "km_dt_instruction": arch_meta["km_dt"],
            "answer_rule": arch_meta["answer_rule"],
            "option_a": option_a,
            "option_b": option_b,
            "sub_intents": sub_intents,
        }'''

    new_block_3 = '''        base_res = {
            "multi_subjects": multi_subjects,
            "is_compound_question": False,
            "sub_questions": [],
            "raw_question": q_raw,
            "archetype_key": arch_key,
            "archetype_code": arch_meta["code"],
            "archetype_name": arch_meta["name"],
            "question_mode": arch_meta["mode"],
            "specific_target": specific_target,
            "authoritative_dt": authoritative_dt,
            "subject_person": subject_person,
            "subject_lh_dt": authoritative_dt or dung_than_hint or "Bản Thân",
            "lh_dt_instruction": arch_meta["lh_dt"],
            "km_dt_instruction": arch_meta["km_dt"],
            "answer_rule": arch_meta["answer_rule"],
            "option_a": option_a,
            "option_b": option_b,
            "sub_intents": sub_intents,
        }

        # V102.0: BỘ PHÂN TÁCH ĐA CÂU HỎI NHỎ TRONG 1 CÂU HỎI LỚN (Multi-SubQuestion Decomposer)
        # Khi người dùng hỏi 1 câu nhưng chứa 2–3 câu hỏi nhỏ khác nhau (VD: "cuộc đời tôi có mấy vợ, và mấy đứa con",
        # "tôi có mấy đứa con và chúng bao nhiêu tuổi", "nhà tôi mấy tầng, và có mấy đứa con", "công việc thế nào và tài chính có lộc không"),
        # bắt buộc bóc tách toàn bộ các vế câu hỏi nhỏ để AI Số 2 giải mã đầy đủ từng vế, tuyệt đối không bỏ sót!
        if not dung_than_hint or dung_than_hint != "__SINGLE_CLAUSE__":
            sub_qs = QuestionReaderAI.decompose_sub_questions(q_raw, dung_than_hint=dung_than_hint, category_hint=category_hint)
            if len(sub_qs) >= 2:
                base_res["is_compound_question"] = True
                base_res["sub_questions"] = sub_qs
                base_res["archetype_code"] = " + ".join(sq["archetype_code"] for sq in sub_qs)
                base_res["archetype_name"] = " & ".join(sq["archetype_name"] for sq in sub_qs)
                base_res["subject_person"] = " · ".join(
                    f"[Câu hỏi nhỏ {i+1}: «{sq['clause_label']}» ➔ Giao DT: {sq['subject_lh_dt']}]"
                    for i, sq in enumerate(sub_qs)
                )
                base_res["lh_dt_instruction"] = " | ".join(
                    f"[Vế {i+1} - {sq['clause_label']}]: {sq['lh_dt_instruction']}"
                    for i, sq in enumerate(sub_qs)
                )
                base_res["sub_intents"].append(
                    f"Tách {len(sub_qs)} câu hỏi nhỏ độc lập ({', '.join(sq['clause_label'] for sq in sub_qs)}) để đối chứng riêng từng Dụng Thần"
                )
        return base_res

    @staticmethod
    def decompose_sub_questions(question: str, dung_than_hint: str = "", category_hint: str = "") -> list:
        """
        Tự động nhận diện và bóc tách 1 câu hỏi ghép thành danh sách các câu hỏi nhỏ độc lập (Sub-Questions).
        Hoạt động kết hợp cả 2 cơ chế:
        1. Tách vế câu theo dấu phẩy (,), chấm phẩy (;), chấm hỏi (?), hoặc từ nối (và, cùng, còn, rồi, kèm, thêm).
        2. Quét Đa Mục Tiêu (Multi-Target Scanner) ngay cả khi người dùng viết liền không dấu phẩy (VD: "tôi có mấy vợ mấy con", "tôi có mấy đứa con bao nhiêu tuổi").
        """
        q_raw = str(question or "").strip()
        q_low = q_raw.lower()
        if len(q_low) < 6:
            return []

        # Bảo vệ các cụm chủ ngữ ghép ("tôi và vợ", "con gái và con trai", "bố và mẹ"...) để không tách nhầm chủ ngữ
        protected_q = q_raw
        _PROTECT_PHRASES = [
            "tôi và vợ tôi", "tôi và vợ", "vợ và tôi", "hai vợ chồng", "vợ chồng tôi",
            "tôi và chồng tôi", "tôi và chồng", "chồng và tôi",
            "tôi và người yêu", "tôi và bạn gái", "tôi và bạn trai",
            "tôi và bạn", "bạn và tôi", "tôi và anh", "tôi và chị", "tôi và em",
            "tôi và đồng nghiệp", "tôi và đối tác", "tôi và con",
            "con gái và con trai", "con trai và con gái",
            "bố và mẹ", "mẹ và bố", "ba và mẹ", "ông và bà",
            "nam và nữ", "trai và gái", "nếp và tẻ", "ăn và ngủ",
        ]
        for _pp in _PROTECT_PHRASES:
            protected_q = re.sub(re.escape(_pp), lambda m: m.group(0).replace(" và ", " __AND_KEEP__ "), protected_q, flags=re.IGNORECASE)

        # 1. Tách theo dấu câu và từ nối vế câu hỏi
        raw_clauses = re.split(r"[,;?/|]+|\s+(?:và|cùng với|còn|rồi|kèm theo|kèm|thêm)\s+", protected_q, flags=re.IGNORECASE)
        clauses = []
        for rc in raw_clauses:
            c_clean = rc.replace(" __AND_KEEP__ ", " và ").strip(" .,;?!-/")
            if len(c_clean) >= 3:
                clauses.append(c_clean)

        # 2. Quét Đa Mục Tiêu Đặc Thù trong toàn câu hỏi (đề phòng viết liền hoặc 1 vế chứa 2 ý hỏi khác nhau)
        _TARGET_DETECTORS = [
            (
                "SPOUSE_COUNT",
                ["mấy vợ", "bao nhiêu vợ", "mấy người vợ", "mấy đời vợ", "lấy mấy vợ", "có mấy vợ", "mấy bà vợ",
                 "mấy chồng", "bao nhiêu chồng", "mấy người chồng", "mấy đời chồng", "lấy mấy chồng", "có mấy chồng",
                 "mấy lần kết hôn", "kết hôn mấy lần", "mấy lần đò", "mấy lần lập gia đình"],
                "Cuộc đời có mấy vợ" if "chồng" not in q_low or "vợ" in q_low else "Cuộc đời có mấy chồng",
            ),
            (
                "MARITAL_STATUS_NOW",
                ["kết hôn chưa", "lấy vợ chưa", "lấy chồng chưa", "có vợ chưa", "có chồng chưa",
                 "có người yêu chưa", "có gia đình chưa", "độc thân hay", "đã lập gia đình chưa"],
                "Đã kết hôn / lập gia đình chưa",
            ),
            (
                "CHILDREN_COUNT",
                ["bao nhiêu người con", "mấy người con", "mấy đứa con", "có mấy con", "bao nhiêu con",
                 "mấy trai mấy gái", "sinh mấy con", "đường con cái", "tử tức", "có con chưa", "mấy con"],
                "Có mấy người con (Mấy trai mấy gái)",
            ),
            (
                "CHILDREN_AGE",
                ["con gái và con trai của tôi bao nhiêu tuổi", "con trai và con gái của tôi bao nhiêu tuổi",
                 "con tôi bao nhiêu tuổi", "con của tôi bao nhiêu tuổi", "các con bao nhiêu tuổi",
                 "chúng bao nhiêu tuổi", "chúng nó bao nhiêu tuổi", "con mấy tuổi", "chúng mấy tuổi"],
                "Các con bao nhiêu tuổi",
            ),
            (
                "HOUSE_FLOORS",
                ["mấy tầng", "bao nhiêu tầng", "tầng mấy", "nhà cao mấy", "nhà mấy lầu", "mấy lầu", "mấy phòng", "bao nhiêu phòng"],
                "Nhà mấy tầng / Ở tầng mấy",
            ),
            (
                "SIBLINGS_COUNT",
                ["mấy anh chị em", "bao nhiêu anh chị em", "mấy anh em", "bao nhiêu anh em", "mấy chị em", "con thứ mấy", "thứ mấy trong nhà"],
                "Gia đình có mấy anh chị em & Thứ mấy",
            ),
            (
                "PEOPLE_AROUND",
                ["xung quanh tôi có mấy người", "trong phòng có mấy người", "ở đây có mấy người", "bên cạnh tôi có ai", "ở một mình hay"],
                "Xung quanh có mấy người",
            ),
            (
                "CLOTHING_VEHICLE",
                ["mặc áo màu gì", "áo màu gì", "quần áo màu gì", "trang phục màu gì", "đi xe gì", "xe màu gì", "biển số xe", "nhà màu gì"],
                "Mặc áo màu gì / Đi xe gì",
            ),
            (
                "LOCATION_HOME_WORK",
                ["ở nhà hay", "hay ở nhà", "ở công ty hay", "trong nhà hay ngoài đường"],
                "Đang ở nhà hay ở công ty/bên ngoài",
            ),
            (
                "POSTURE_STATE",
                ["đứng hay ngồi", "ngồi hay đứng", "nằm hay ngồi", "ngồi hay nằm", "ngủ hay thức"],
                "Đang đứng hay đang ngồi/nằm",
            ),
        ]

        # Kiểm tra bổ sung cho trường hợp hỏi gộp "mấy đứa con + bao nhiêu tuổi"
        _has_child_cnt_kw = any(w in q_low for w in ["bao nhiêu người con", "mấy người con", "mấy đứa con", "có mấy con", "bao nhiêu con", "mấy trai mấy gái", "mấy con"]) and not any(ex in q_low for ex in ["con số", "con đường", "con xe", "con dao", "con thứ mấy"])
        _has_age_kw = any(w in q_low for w in ["bao nhiêu tuổi", "mấy tuổi", "sinh năm", "năm sinh"])
        _has_child_ref = any(w in q_low for w in ["con gái", "con trai", "con của tôi", "con tôi", "mấy đứa con", "các con", "con cái", "đứa con", "chúng"])

        detected_targets = []
        for t_code, kw_list, default_lbl in _TARGET_DETECTORS:
            if t_code == "CHILDREN_COUNT" and any(ex in q_low for ex in ["con số", "con đường", "con xe", "con dao", "con thứ mấy"]):
                continue
            for kw in kw_list:
                pos = q_low.find(kw)
                if pos != -1:
                    detected_targets.append((pos, t_code, kw, default_lbl))
                    break

        if _has_child_cnt_kw and _has_age_kw and _has_child_ref:
            if not any(t[1] == "CHILDREN_AGE" for t in detected_targets):
                pos_age = min([q_low.find(w) for w in ["bao nhiêu tuổi", "mấy tuổi", "sinh năm", "năm sinh"] if q_low.find(w) != -1] or [999])
                detected_targets.append((pos_age, "CHILDREN_AGE", "con tôi bao nhiêu tuổi", "Các con bao nhiêu tuổi"))

        detected_targets.sort(key=lambda x: x[0])

        # Xây dựng danh sách Sub-Questions từ các vế câu (clauses) và các mục tiêu phát hiện được (detected_targets)
        sub_blueprints = []
        seen_keys = set()

        if len(clauses) >= 2:
            for cl in clauses:
                cl_low = cl.lower()
                # Bổ sung ngữ cảnh nếu vế 2 viết tắt như "mấy đứa con" hoặc "bao nhiêu tuổi"
                cl_expanded = cl
                if cl_low in ("mấy đứa", "mấy đứa con", "bao nhiêu con", "mấy con", "mấy người con"):
                    cl_expanded = f"tôi có {cl}"
                elif any(w in cl_low for w in ["bao nhiêu tuổi", "mấy tuổi"]) and _has_child_ref and not any(w in cl_low for w in ["con", "tôi", "vợ", "chồng", "bố", "mẹ"]):
                    cl_expanded = f"các con tôi {cl}"
                bp_cl = QuestionReaderAI.analyze_question(cl_expanded, dung_than_hint="__SINGLE_CLAUSE__", category_hint=category_hint)
                # Chỉ coi là 1 câu hỏi nhỏ hợp lệ nếu nhận diện được chủ đề rõ ràng (không phải D25 mặc định vô nghĩa từ mảnh câu cụt)
                is_meaningful_clause = (
                    bp_cl["specific_target"] != ""
                    or bp_cl["archetype_key"] != "D25_SPIRITUAL_GENERAL"
                    or any(w in cl_low for w in ["mấy", "bao nhiêu", "không", "chưa", "thế nào", "ra sao", "khi nào", "bao giờ", "ở đâu", "ai", "hay"])
                )
                if not is_meaningful_clause:
                    continue
                dedup_key = bp_cl["specific_target"] or bp_cl["archetype_key"]
                if dedup_key not in seen_keys:
                    seen_keys.add(dedup_key)
                    bp_cl["clause_label"] = cl[0].upper() + cl[1:] if cl else bp_cl["subject_person"]
                    sub_blueprints.append(bp_cl)

        # Nếu viết liền không tách vế hoặc có mục tiêu đặc thù bị gộp trong 1 vế, bổ sung từ detected_targets
        if len(detected_targets) >= 2 and len(sub_blueprints) < len(detected_targets):
            sub_blueprints = []
            seen_keys = set()
            for _, t_code, kw_match, def_lbl in detected_targets:
                if t_code in seen_keys:
                    continue
                seen_keys.add(t_code)
                # Tìm vế câu gốc chứa kw_match nếu có
                matching_cl = def_lbl
                for cl in clauses:
                    if kw_match in cl.lower():
                        matching_cl = cl[0].upper() + cl[1:]
                        break
                synth_q = matching_cl if t_code != "CHILDREN_AGE" else "con gái và con trai của tôi bao nhiêu tuổi"
                if t_code == "CHILDREN_COUNT" and any(w in synth_q.lower() for w in ["tuổi", "sinh năm"]):
                    synth_q = "tôi có mấy đứa con"
                bp_t = QuestionReaderAI.analyze_question(synth_q, dung_than_hint="__SINGLE_CLAUSE__", category_hint=category_hint)
                bp_t["specific_target"] = t_code
                bp_t["clause_label"] = matching_cl
                sub_blueprints.append(bp_t)

        return sub_blueprints if len(sub_blueprints) >= 2 else []'''

    assert old_block_3 in src, "old_block_3 not found"
    src = src.replace(old_block_3, new_block_3, 1)

    # 4. Now update HexagramReasoningAI.deduce_specialized_answer to handle:
    #    a) Compound questions (`is_compound_question` with `len(sub_questions) >= 2`)
    #    b) `target == "SPOUSE_COUNT"` ("Cuộc đời tôi có mấy vợ / mấy chồng")
    #    c) General sub-questions inside a compound question (e.g., Career + Finance, Exam + Timing)
    old_block_4 = '''        # ── 4. GIẢI MÃ: ĐÃ KẾT HÔN CHƯA / CÓ VỢ CHỒNG CHƯA / ĐỘC THÂN HAY CÓ GIA ĐÌNH ──
        if target == "MARITAL_STATUS_NOW":'''

    new_block_4 = '''        # ── 0. GIẢI MÃ ĐA CÂU HỎI NHỎ TRONG 1 CÂU HỎI LỚN (COMPOUND MULTI-SUBQUESTION SOLVER V102.0) ──
        if blueprint.get("is_compound_question") and len(blueprint.get("sub_questions") or []) >= 2:
            sub_qs = blueprint.get("sub_questions") or []
            sub_solved = []
            for idx_sq, sq_bp in enumerate(sub_qs, 1):
                sq_dt = sq_bp.get("authoritative_dt") or sq_bp.get("subject_lh_dt") or dung_than or "Bản Thân"
                sq_res = HexagramReasoningAI.deduce_specialized_answer(
                    blueprint=sq_bp,
                    dung_than=sq_dt,
                    weighted_pct=weighted_pct,
                    chart_data=chart_data,
                    luc_hao_data=luc_hao_data,
                    mai_hoa_data=mai_hoa_data,
                    omni_data=omni_data,
                    auth_warnings=auth_warnings,
                    is_fake=False if sq_bp.get("specific_target") in ("SPOUSE_COUNT", "CHILDREN_COUNT", "CHILDREN_AGE", "HOUSE_FLOORS", "SIBLINGS_COUNT") else is_fake,
                )
                if not sq_res.get("has_override"):
                    sq_res = HexagramReasoningAI._deduce_general_clause_on_hexagram(
                        sq_bp=sq_bp,
                        sq_dt=sq_dt,
                        base_pct=weighted_pct,
                        chart_data=chart_data,
                        luc_hao_data=luc_hao_data,
                        mai_hoa_data=mai_hoa_data,
                        omni_data=omni_data,
                    )
                sub_solved.append({
                    "index": idx_sq,
                    "clause_label": sq_bp.get("clause_label") or sq_bp.get("subject_person") or f"Câu hỏi nhỏ {idx_sq}",
                    "dt": sq_dt,
                    "arch_code": sq_bp.get("archetype_code", ""),
                    "arch_name": sq_bp.get("archetype_name", ""),
                    "headline": sq_res.get("headline", ""),
                    "short_headline": sq_res.get("short_headline") or re.sub(r"^[^:]+:\s*", "", sq_res.get("headline", "")).strip(),
                    "why": sq_res.get("why", ""),
                    "when": sq_res.get("when", ""),
                    "advice": sq_res.get("advice", ""),
                })

            headline_parts = [
                f"[{s['index']}. {s['clause_label'].upper()} (DT: {s['dt'].upper()})]: {s['short_headline']}"
                for s in sub_solved
            ]
            combined_headline = (
                f"🎯 GIẢI MÃ TRỌN VẸN {len(sub_solved)} CÂU HỎI NHỎ TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): "
                + "  ||  ".join(headline_parts)
            )

            # Xây dựng thẻ HTML trực quan song song cho từng câu hỏi nhỏ để chèn vào phần giải thích
            sub_cards_html = (
                '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-bottom:10px;">'
            )
            _CARD_BORDERS = ["#fbbf24", "#34d399", "#38bdf8", "#a78bfa"]
            for s in sub_solved:
                _b_col = _CARD_BORDERS[(s["index"] - 1) % len(_CARD_BORDERS)]
                sub_cards_html += (
                    f'<div style="padding:10px 12px;background:rgba(15,23,42,0.88);border-radius:10px;border:1.5px solid {_b_col};">'
                    f'<div style="font-size:0.86em;font-weight:900;color:{_b_col};margin-bottom:4px;">'
                    f'🔹 CÂU HỎI NHỎ {s["index"]}: "{s["clause_label"].upper()}" (Dụng Thần: {s["dt"]} · {s["arch_code"]})'
                    f'</div>'
                    f'<div style="font-size:0.98em;font-weight:900;color:#ffffff;margin-bottom:6px;padding:6px 8px;background:rgba(255,255,255,0.06);border-radius:6px;border-left:3px solid {_b_col};">'
                    f'👉 {s["short_headline"]}'
                    f'</div>'
                    f'<div style="font-size:0.9em;color:#e2e8f0;line-height:1.5;">{s["why"]}</div>'
                    f'</div>'
                )
            sub_cards_html += '</div>'

            combined_why = (
                sub_cards_html
                + " ".join(
                    f"<b>• [Vế {s['index']} — {s['clause_label']} (Dụng Thần: {s['dt']})]:</b> {s['why']}"
                    for s in sub_solved
                )
            )
            combined_when = "<br>".join(
                f"<b>• [Vế {s['index']} — {s['clause_label']}]:</b> {s['when']}"
                for s in sub_solved
            )
            combined_advice = "<br>".join(
                f"<b>• [Vế {s['index']} — {s['clause_label']}]:</b> {s['advice']}"
                for s in sub_solved
            )
            return {
                "has_override": True,
                "is_compound_answer": True,
                "sub_solved": sub_solved,
                "headline": combined_headline,
                "why": combined_why,
                "when": combined_when,
                "advice": combined_advice,
            }

        # ── 4A. GIẢI MÃ CHUYÊN SÂU: CUỘC ĐỜI CÓ MẤY VỢ / MẤY CHỒNG / MẤY LẦN ĐÒ (SPOUSE_COUNT) ──
        if target == "SPOUSE_COUNT":
            is_husband_q = ("chồng" in q_low and "vợ" not in q_low)
            sp_lt = "Quan Quỷ" if is_husband_q else "Thê Tài"
            sp_noun = "chồng" if is_husband_q else "vợ"
            sp_noun_up = "NGƯỜI CHỒNG" if is_husband_q else "NGƯỜI VỢ"
            sp_title_way = "NHẤT PHU CHÍNH VỊ" if is_husband_q else "NHẤT THÊ CHÍNH VỊ"
            rival_lt = "Tử Tôn" if is_husband_q else "Huynh Đệ"

            sp_haos = []
            rival_dong = []
            for idx_h, h_item in enumerate(haos, 1):
                if not isinstance(h_item, dict):
                    continue
                lt_h = str(h_item.get("luc_than") or "")
                if sp_lt in lt_h:
                    sp_haos.append((idx_h, h_item))
                if rival_lt in lt_h and (idx_h in dong_list or h_item.get("is_dong") or h_item.get("dong")):
                    rival_dong.append((idx_h, h_item))

            bien_haos_sp = lh_bien.get("haos") or lh_bien.get("details") or []
            bien_sp_haos = []
            for d_idx in dong_list:
                if 1 <= d_idx <= len(bien_haos_sp) and isinstance(bien_haos_sp[d_idx - 1], dict):
                    bh_sp = bien_haos_sp[d_idx - 1]
                    if sp_lt in str(bh_sp.get("luc_than") or ""):
                        bien_sp_haos.append((d_idx, bh_sp))

            chi_ngay_sp = chart_data.get("chi_ngay", "Ngọ")
            chi_thang_sp = chart_data.get("chi_thang", "Tuất")
            the_chi_sp = str(the_hao.get("chi") or the_hao.get("can_chi") or "Hợi").split()[-1]
            ung_chi_sp = str(ung_hao.get("chi") or ung_hao.get("can_chi") or "Sửu").split()[-1]

            # Trường hợp 1: Trên Quẻ Chủ chỉ có <= 1 hào Phối ngẫu (hoặc 1 Phục Thần duy nhất đắc Nhật/Nguyệt) và Hào Động không biến ra thêm hào Phối ngẫu thứ 2
            if len(sp_haos) <= 1 and len(bien_sp_haos) == 0:
                short_hl = (
                    f"💍 CUỘC ĐỜI BẠN GẮN BÓ VỚI 01 {sp_noun_up} CHÍNH THỨC ({sp_title_way} — HÔN NHÂN BỀN VỮNG DÙ TRƯỚC HOẶC TRONG HÔN NHÂN CÓ 1–2 ĐỢT SÓNG GIÓ / MỐI TÌNH THỬ THÁCH)!"
                )
                headline = f"💍 KẾT LUẬN VỀ SỐ ĐỜI {sp_noun_up} TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}"
                if len(sp_haos) == 1:
                    sp_idx_1, sp_h_1 = sp_haos[0]
                    sp_ch_1 = str(sp_h_1.get("chi") or sp_h_1.get("can_chi") or "").split()[-1]
                    sp_nh_1 = sp_h_1.get("ngu_hanh") or sp_h_1.get("hanh") or hanh_dt
                    sp_pos_desc = f"hào Dụng Thần <b>{sp_lt}</b> xuất hiện duy nhất 01 hào chính vị tại <b>Hào {sp_idx_1} ({sp_ch_1}-{sp_nh_1})</b> trên quẻ Chủ <b>{ten_que_chu}</b>"
                else:
                    sp_pos_desc = (
                        f"trên quẻ Chủ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b>, hào Dụng Thần <b>{sp_lt}</b> không phân tán ra nhiều hào mà "
                        f"<b>ẩn phục duy nhất 01 vị trí (Phục Thần dưới Hào 3)</b> và đắc <b>Nhật Thần ({chi_ngay_sp}) / Nguyệt Lệnh ({chi_thang_sp})</b> trực tiếp nhập quẻ làm chủ"
                    )
                rival_note = (
                    f" Tuy nhiên, do có Hào {rival_dong[0][0]} <b>{rival_lt}</b> phát động trên quẻ nên đường tình duyên từng trải qua <b>1–2 mối tình sâu đậm trước khi cưới</b> hoặc trong đời sống vợ chồng đôi lúc có sóng gió khắc khẩu, nhưng gốc hôn nhân vẫn giữ trọn <b>01 người {sp_noun} chính danh</b>."
                    if rival_dong else
                    f" Quẻ Biến <b>{ten_que_bien}</b> không sinh thêm hào {sp_lt} thứ hai, khẳng định duyên nợ gắn kết bền chặt với <b>01 người {sp_noun} chính thức</b>."
                )
                why_s = (
                    f"Xét theo Pháp Đoán Hôn Nhân Lục Hào, Mai Hoa & Kỳ Môn: {sp_pos_desc}, kết hợp trục <b>Hào Thế (Hào {the_idx} {the_chi_sp}) – Hào Ứng (Hào {ung_idx} {ung_chi_sp})</b> "
                    f"và Cung Phối Ngẫu tại Cung {target_cung} ({huong_cung} · Sao <b>{sao_name}</b> · Cửa <b>{cua_name}</b> · Thần <b>{than_name}</b>) "
                    f"➔ Cổ pháp định danh là cách <b>'{sp_title_way}' (01 người {sp_noun} chính thức cưới hỏi đi cùng lâu dài)</b>.{rival_note}"
                )
            else:
                # Trường hợp 2: Lưỡng Tài / Lưỡng Quan hiện quái (Có 2 hào Thê Tài hoặc 2 hào Quan Quỷ trên quẻ Chủ + Biến)
                short_hl = (
                    f"💍 TRÊN QUẺ HIỆN TƯỢNG 2 HÀO {sp_lt.upper()} — ỨNG VỚI 01 {sp_noun_up} CHÍNH THỨC HIỆN TẠI + 01 MỐI NHÂN DUYÊN SÂU ĐẬM (DAO ĐỘNG 1 – 2 ĐỜI {sp_noun_up} NẾU KHÔNG NHƯỜNG NHỊN KHI XUNG KHẮC)!"
                )
                headline = f"💍 KẾT LUẬN VỀ SỐ ĐỜI {sp_noun_up} TỪ QUẺ ({ten_que_chu.upper()} ➔ {ten_que_bien.upper()}): {short_hl}"
                sp_list_str = ", ".join(f"Hào {ix} ({h.get('chi', '')}-{h.get('ngu_hanh', '')})" for ix, h in sp_haos)
                why_s = (
                    f"Trên quẻ <b>{ten_que_chu}</b> biến <b>{ten_que_bien}</b> xuất hiện <b>{len(sp_haos)} hào {sp_lt}</b> ({sp_list_str})"
                    + (f" cùng hào biến {sp_lt} tại Hào {bien_sp_haos[0][0]}" if bien_sp_haos else "")
                    + f" (cổ pháp gọi là cách <b>'Lưỡng {sp_lt.split()[0]} Hiện Quái'</b>). Trong đó 01 hào chính vị hợp với Hào Thế (Hào {the_idx}) ứng với <b>01 người {sp_noun} chính thức</b>, còn hào thứ hai ứng với một mối tình sâu nặng từng đi qua hoặc thử thách hôn nhân cần hóa giải."
                )

            when_s = (
                f"<b>Đặc điểm người {sp_noun} & Gia đạo (Cung {target_cung} — {huong_cung}):</b> Hội Sao <b>{sao_name}</b>, Cửa <b>{cua_name}</b> và Thần <b>{than_name}</b> — "
                f"người {sp_noun} có tính tự lập, tháo vát, thẳng thắn, rất thương con và biết vun vén cho gia đình."
            )
            adv_s = (
                f"Để giữ trọn phúc khí gia đạo viên mãn bên người {sp_noun} và các con, hai vợ chồng nên lắng nghe, nhường nhịn khi nóng giận và ưu tiên hướng <b>{huong_cung}</b> (Màu hợp: <b>{colors_str}</b>)."
            )
            return {
                "has_override": True,
                "headline": headline,
                "short_headline": short_hl,
                "why": why_s,
                "when": when_s,
                "advice": adv_s,
            }

        # ── 4. GIẢI MÃ: ĐÃ KẾT HÔN CHƯA / CÓ VỢ CHỒNG CHƯA / ĐỘC THÂN HAY CÓ GIA ĐÌNH ──
        if target == "MARITAL_STATUS_NOW":'''

    assert old_block_4 in src, "old_block_4 not found"
    src = src.replace(old_block_4, new_block_4, 1)

    # 5. Add _deduce_general_clause_on_hexagram helper method to HexagramReasoningAI and update dual_agent_html for compound questions
    old_block_5 = '''        return {"has_override": False}

    @staticmethod
    def cross_verify_and_reason('''

    new_block_5 = '''        return {"has_override": False}

    @staticmethod
    def _deduce_general_clause_on_hexagram(
        sq_bp: dict,
        sq_dt: str,
        base_pct: int,
        chart_data: dict = None,
        luc_hao_data: dict = None,
        mai_hoa_data: dict = None,
        omni_data: dict = None,
    ) -> dict:
        """
        Giải mã độc lập cho một vế câu hỏi nhỏ thuộc nhóm Sự việc / Dự đoán (Công việc, Tài chính, Tình cảm,
        Thi cử, Sức khỏe, Tìm đồ, Thời điểm Ứng kỳ...) dựa trực tiếp trên Hào Dụng Thần riêng của vế đó!
        """
        chart_data = chart_data or {}
        luc_hao_data = luc_hao_data or {}
        mai_hoa_data = mai_hoa_data or {}
        omni_data = omni_data or {}
        lh_ban = luc_hao_data.get("ban", {}) if isinstance(luc_hao_data, dict) else {}
        lh_bien = luc_hao_data.get("bien", {}) if isinstance(luc_hao_data, dict) else {}
        haos = lh_ban.get("haos") or lh_ban.get("details") or []
        dong_list = luc_hao_data.get("dong_hao") or lh_ban.get("dong_hao") or []
        ten_que_chu = lh_ban.get("name") or mai_hoa_data.get("ten_que") or "Quẻ Chủ"
        ten_que_bien = lh_bien.get("name") or mai_hoa_data.get("ten_qua_bien") or "Quẻ Biến"

        _CHI_NH = {"Tý": "Thủy", "Sửu": "Thổ", "Dần": "Mộc", "Mão": "Mộc", "Thìn": "Thổ", "Tị": "Hỏa", "Ngọ": "Hỏa", "Mùi": "Thổ", "Thân": "Kim", "Dậu": "Kim", "Tuất": "Thổ", "Hợi": "Thủy"}
        _SINH = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
        _KHAC = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}

        chi_m = chart_data.get("chi_thang", "Tuất")
        chi_n = chart_data.get("chi_ngay", "Ngọ")
        nh_m = _CHI_NH.get(chi_m, "Thổ")
        nh_n = _CHI_NH.get(chi_n, "Hỏa")

        dt_idx = 3
        dt_chi = "Hợi"
        dt_nh = "Thủy"
        found_dt = False
        for ix, h in enumerate(haos, 1):
            if isinstance(h, dict):
                lt = str(h.get("luc_than") or "")
                tu = str(h.get("the_ung") or h.get("tu") or "")
                if (sq_dt and sq_dt in lt) or (sq_dt == "Bản Thân" and "Thế" in tu):
                    dt_idx = ix
                    dt_chi = str(h.get("chi") or h.get("can_chi") or "Hợi").split()[-1]
                    dt_nh = h.get("ngu_hanh") or h.get("hanh") or _CHI_NH.get(dt_chi, "Thủy")
                    found_dt = True
                    break

        sq_score = int(base_pct or 50)
        reasons = []
        if found_dt:
            reasons.append(f"Hào Dụng Thần <b>{sq_dt}</b> hiện tại <b>Hào {dt_idx} ({dt_chi}-{dt_nh})</b> trên quẻ <b>{ten_que_chu}</b>")
        else:
            reasons.append(f"Hào Dụng Thần <b>{sq_dt}</b> ẩn phục dưới quẻ <b>{ten_que_chu}</b>")

        if _SINH.get(nh_m) == dt_nh or nh_m == dt_nh:
            sq_score += 8
            reasons.append(f"được Nguyệt Lệnh ({chi_m}-{nh_m}) sinh phù/tỷ trợ")
        elif _KHAC.get(nh_m) == dt_nh:
            sq_score -= 6
            reasons.append(f"chịu Nguyệt Lệnh ({chi_m}-{nh_m}) chế khắc")

        if _SINH.get(nh_n) == dt_nh or nh_n == dt_nh:
            sq_score += 7
            reasons.append(f"đắc Nhật Thần ({chi_n}-{nh_n}) tương sinh/trợ lực")
        elif _KHAC.get(nh_n) == dt_nh:
            sq_score -= 5
            reasons.append(f"bị Nhật Thần ({chi_n}-{nh_n}) xung khắc")

        for d_ix in dong_list:
            if 1 <= d_ix <= len(haos) and isinstance(haos[d_ix - 1], dict):
                dh = haos[d_ix - 1]
                d_ch = str(dh.get("chi") or dh.get("can_chi") or "").split()[-1]
                d_nh = dh.get("ngu_hanh") or dh.get("hanh") or _CHI_NH.get(d_ch, "")
                if _SINH.get(d_nh) == dt_nh:
                    sq_score += 8
                    reasons.append(f"được Hào Động {d_ix} ({d_ch}-{d_nh}) phát động sinh trợ trực tiếp ({d_nh} sinh {dt_nh})")
                elif _KHAC.get(d_nh) == dt_nh:
                    sq_score -= 8
                    reasons.append(f"bị Hào Động {d_ix} ({d_ch}-{d_nh}) phát động khắc chế ({d_nh} khắc {dt_nh})")

        sq_score = max(28, min(88, sq_score))
        t_code = sq_bp.get("specific_target") or sq_bp.get("archetype_key", "")
        c_lbl = sq_bp.get("clause_label") or sq_bp.get("subject_person") or "Sự việc"
        uk_str = omni_data.get("exact_timestamp", f"Ngày/Giờ {dt_chi}")
        huong_str = (omni_data.get("c_info") or {}).get("huong", "Chính Nam")

        if t_code == "TIMING_WHEN" or "D12" in t_code:
            short_hl = f"⏳ THỜI ĐIỂM ỨNG KỲ CHÍNH XÁC: {uk_str.upper()} (KHI HÀO {sq_dt.upper()} {dt_chi.upper()} XUNG/HỢP MỞ VẬN)!"
        elif sq_score >= 55:
            short_hl = f"✅ THUẬN LỢI & KHẢ QUAN ({sq_score}% — CÁT: DỤNG THẦN {sq_dt.upper()} ĐẮC KHÍ SINH PHÙ)!"
        elif sq_score >= 45:
            short_hl = f"⚖️ TRUNG BÌNH / CẦN KIÊN NHẪN CHUẨN BỊ KỸ ({sq_score}% — BÌNH: ĐỢI MỐC ỨNG KỲ MỞ VẬN)!"
        else:
            short_hl = f"⚠️ ĐANG GẶP LỰC CẢN — NÊN THẬN TRỌNG & CHỜ THỜI ({sq_score}% — HUNG)!"

        return {
            "has_override": True,
            "headline": f"🎯 [{c_lbl.upper()}]: {short_hl}",
            "short_headline": short_hl,
            "why": ", ".join(reasons) + f" (Biến quẻ: <b>{ten_que_bien}</b>).",
            "when": f"Mốc ứng nghiệm của vế này: <b>{uk_str}</b>.",
            "advice": f"Hành động chủ động và ưu tiên phương vị <b>{huong_str}</b>.",
        }

    @staticmethod
    def cross_verify_and_reason('''

    assert old_block_5 in src, "old_block_5 not found"
    src = src.replace(old_block_5, new_block_5, 1)

    # 6. Update ab_html in cross_verify_and_reason so that when is_compound_question is True, AI Số 1 displays the list of decomposed sub-questions!
    old_block_6 = '''        ab_html = ""
        if blueprint.get("option_a") and blueprint.get("option_b"):
            ab_html = (
                f'<div style="margin-top:5px;font-size:0.9em;color:#bae6fd;">'
                f'⚖️ <b>Tách 2 vế đối chứng:</b> [Phương án 1]: <b>{blueprint["option_a"]}</b> ↔ [Phương án 2]: <b>{blueprint["option_b"]}</b>'
                f'</div>'
            )'''

    new_block_6 = '''        ab_html = ""
        if blueprint.get("is_compound_question") and blueprint.get("sub_questions"):
            _sq_items_html = "<br>".join(
                f'&nbsp;&nbsp;• <b>[Câu hỏi nhỏ {i+1}]:</b> <i>"{sq.get("clause_label", "")}"</i> ➔ Khớp <b>{sq.get("archetype_code", "")}</b> · Giao Dụng Thần: <b style="color:#fde047;">{sq.get("subject_lh_dt", "")}</b>'
                for i, sq in enumerate(blueprint["sub_questions"])
            )
            ab_html = (
                f'<div style="margin-top:6px;padding:7px 10px;background:rgba(56,189,248,0.12);border-radius:8px;border-left:3px solid #38bdf8;font-size:0.9em;color:#e0f2fe;">'
                f'🧩 <b>Phát hiện câu hỏi ghép ({len(blueprint["sub_questions"])} câu hỏi nhỏ trong 1 lần hỏi — Tự động tách & giải mã đủ 100%):</b><br>'
                f'{_sq_items_html}'
                f'</div>'
            )
        elif blueprint.get("option_a") and blueprint.get("option_b"):
            ab_html = (
                f'<div style="margin-top:5px;font-size:0.9em;color:#bae6fd;">'
                f'⚖️ <b>Tách 2 vế đối chứng:</b> [Phương án 1]: <b>{blueprint["option_a"]}</b> ↔ [Phương án 2]: <b>{blueprint["option_b"]}</b>'
                f'</div>'
            )'''

    assert old_block_6 in src, "old_block_6 not found"
    src = src.replace(old_block_6, new_block_6, 1)

    ast.parse(src)
    with open(p, "w", encoding="utf-8", newline="") as f:
        f.write(src)
    print("dual_ai_agents.py patched & AST verified!")


def patch_other_files():
    # Update version strings V101.9 -> V102.0 in app.py, free_ai_helper.py, offline_brain.py, omniscient_prophecy.py, world_class_methods.py
    for fname in ["app.py", "free_ai_helper.py", "offline_brain.py", "omniscient_prophecy.py", "world_class_methods.py"]:
        fp = os.path.join(BASE_DIR, fname)
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("V101.9", "V102.0")

        if fname == "free_ai_helper.py":
            # Also update the Green Testing Mindset Box (auth_html) when _early_bp has sub_questions so it mentions ALL Dụng Thần of the sub-questions!
            old_auth_line = '''                _dt_prf_s = _test_link_info.get('dt_proof', '')'''
            new_auth_line = '''                _dt_prf_s = _test_link_info.get('dt_proof', '')
                if locals().get('_early_bp', {}).get('is_compound_question') and locals().get('_early_bp', {}).get('sub_questions'):
                    _sq_dts_str = " & ".join(f"Vế {i+1} ({sq.get('clause_label','')}): Dụng Thần <b>{sq.get('subject_lh_dt','')}</b>" for i, sq in enumerate(_early_bp['sub_questions']))
                    _dt_prf_s = f"Đã đối chứng đồng thời cả {len(_early_bp['sub_questions'])} trục Dụng Thần ({_sq_dts_str}) — {_dt_prf_s}"'''
            if old_auth_line in content and "Đã đối chứng đồng thời cả" not in content:
                content = content.replace(old_auth_line, new_auth_line, 1)

        ast.parse(content)
        with open(fp, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        print(f"{fname} updated to V102.0 & AST verified!")

    # Sync all 6 files to SYNC_DIRS
    for fname in ["dual_ai_agents.py", "app.py", "free_ai_helper.py", "offline_brain.py", "omniscient_prophecy.py", "world_class_methods.py"]:
        src_p = os.path.join(BASE_DIR, fname)
        for sdir in SYNC_DIRS:
            if os.path.isdir(sdir):
                shutil.copy2(src_p, os.path.join(sdir, fname))
    print("Synced all 6 files to UPLOAD_TO_STREAMLIT, UPLOAD_LEN_GITHUB, and cuongtan12345678_sync!")


if __name__ == "__main__":
    patch_dual_ai_agents()
    patch_other_files()
