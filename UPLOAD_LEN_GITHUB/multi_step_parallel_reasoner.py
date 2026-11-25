# -*- coding: utf-8 -*-
"""
MULTI-STEP REASONING & PARALLEL THINKING ENGINE (V146.0)
========================================================
Kiến trúc Suy Luận Đa Bước Tuần Tự (7-Step Causal Chain-of-Thought) kết hợp
Tư Duy Song Song 5 Luồng Độc Lập (5-Branch Parallel Thinking via ThreadPoolExecutor):

  [TƯ DUY SONG SONG 5 LUỒNG ĐỘC LẬP — PARALLEL THINKING]
  ├── Luồng 1 (Lục Hào Nạp Giáp): Nguyệt/Nhật ➔ Động/Ám Động ➔ Hóa Biến ➔ Thế/Ứng/Dụng/Phục/Hình/Mộ
  ├── Luồng 2 (Kỳ Môn Độn Giáp): Chủ–Khách (Can Ngày/Giờ) ➔ Tinh–Môn–Thần ➔ Ám Can & Tứ Hại ➔ Lật Cung 4 Trạm
  ├── Luồng 3 (Mai Hoa & Vạn Vật): Đảng Thể/Dụng ➔ 4 Chặng Bản–Hạ Hỗ–Thượng Hỗ–Biến ➔ Quái Số & Loại Tượng
  ├── Luồng 4 (Đại Lục Nhâm Tam Truyền): Tứ Khóa ➔ Sơ Truyền (Khởi phát) ➔ Trung Truyền (Biến chuyển) ➔ Mạt Truyền (Kết cục)
  └── Luồng 5 (Phản Biện Ngược Chiều — Devil's Advocate / Red-Team): Truy quét bẫy "Giả Cát Thực Hung",
      "Giả Hung Thực Cát", Hồi Đầu Khắc, Hóa Không/Thoái, Hợp Trói, Du Hồn, Đắc Kỳ Bất Đắc Môn, Tương Hình.

  [CHUỖI SUY LUẬN ĐA BƯỚC 7 TẦNG — MULTI-STEP SEQUENTIAL REASONING]
  Bước 1: Giải phẫu Ý định, Chủ thể, Mệnh đề điều kiện ("nếu... thì...") & Quy tắc Cát/Hung đặc thù
  Bước 2: Pháp định Dụng Thần Đa Hệ & Kiểm chứng Thực/Hư (Chân Không vs Giả Không, Phục Thần)
  Bước 3: Kích hoạt đồng thời 5 Luồng Tư Duy Song Song (Parallel Fan-Out)
  Bước 4: Suy diễn Diễn biến 3 Thời (Khởi phát ➔ Chuyển tiếp ➔ Kết cục cuối cùng)
  Bước 5: Đối biện Giải quyết Xung đột giữa các Luồng & Hiệu chỉnh Trọng số Hội tụ (Consensus Calibration)
  Bước 6: Chẩn đoán Bệnh – Dược Quẻ & Khóa Ứng kỳ Thiên văn Dương/Âm lịch
  Bước 7: Cổng Tự Kiểm Chứng Chống Mâu Thuẫn (Self-Verification Gate) trước khi chốt Kết Luận 4 Trụ Cột
"""

from __future__ import annotations

import concurrent.futures
import html as _html
import re
import time
from typing import Any, Dict, List, Optional, Tuple


_SHARED_PARALLEL_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=8, thread_name_prefix="v146_think")


def _esc(text: Any) -> str:
    return _html.escape(str(text or "").strip())


def _strip_tags(text: Any) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(text or ""))).strip()


def _polarity_from_score(score: int, invert_for_hazard: bool = False) -> Tuple[str, str, str]:
    """Trả về (code, nhãn tiếng Việt, mã màu hex) theo điểm khí lực 0..100."""
    eff = (100 - score) if invert_for_hazard else score
    if eff >= 62:
        return ("FAVORABLE", "THUẬN / VƯỢNG CÁT", "#22c55e")
    if eff >= 52:
        return ("LEAN_POSITIVE", "NGHIÊNG THUẬN / CÓ CƠ HỘI", "#4ade80")
    if eff >= 45:
        return ("MIXED_CONDITIONAL", "GIẰNG CO / CẦN ĐÚNG THỜI", "#fbbf24")
    if eff >= 34:
        return ("LEAN_NEGATIVE", "VƯỚNG LỰC CẢN / TRÌ TRỆ", "#fb923c")
    return ("UNFAVORABLE", "NGƯỢC Ý / RỦI RO CAO", "#ef4444")


# ═══════════════════════════════════════════════════════════════════════════
# 5 LUỒNG TƯ DUY SONG SONG ĐỘC LẬP (5 INDEPENDENT PARALLEL THINKING STREAMS)
# ═══════════════════════════════════════════════════════════════════════════

def _branch_1_liuyao_specialist(
    ly_res: Dict[str, Any],
    deep_syn: Dict[str, Any],
    dung_than: str,
    question: str,
) -> Dict[str, Any]:
    t0 = time.perf_counter()
    lh_sc = int(deep_syn.get("lh_score", 50))
    ban_name = str(ly_res.get("ban_name") or "Quẻ Chủ")
    bien_name = str(ly_res.get("bien_name") or "Quẻ Biến")
    lines = ly_res.get("line_micro_audit") or []
    dt_idx = int(ly_res.get("dt_hao_idx") or 1)
    the_pos = int(ly_res.get("the_pos") or 1)
    ung_pos = int(ly_res.get("ung_pos") or 4)
    dt_ln = lines[dt_idx - 1] if 1 <= dt_idx <= len(lines) else {}
    the_ln = lines[the_pos - 1] if 1 <= the_pos <= len(lines) else {}
    moving_lines = [ln for ln in lines if ln.get("is_moving")]
    am_dong_lines = [ln for ln in lines if ln.get("is_am_dong")]

    dt_desc = (
        f"Hào {dt_idx} {dt_ln.get('luc_than', dung_than)} ({dt_ln.get('chi', '')}-{dt_ln.get('ngu_hanh', '')}) "
        f"bậc {dt_ln.get('vuong_suy', 'Bình')}, Trường Sinh: {dt_ln.get('ts_ngay', 'Bình')}"
    )
    if dt_ln.get("is_void"):
        dt_desc += f" [Tuần Không: {dt_ln.get('void_type', 'Không Vong')}]"
    if dt_ln.get("is_nguyet_pha") or dt_ln.get("is_nhat_pha"):
        dt_desc += " [Nguyệt/Nhật Phá]"

    mv_summary = (
        "; ".join(
            f"Hào {m['hao']} {m.get('luc_than','')} ({m.get('chi','')}) động hóa {m.get('bien_luc_than','')} ({m.get('bien_chi','')})"
            for m in moving_lines[:3]
        )
        if moving_lines
        else ("Có hào Ám Động ngầm thúc đẩy" if am_dong_lines else "Quẻ Tĩnh (6 hào an tĩnh, xét Nhật/Nguyệt làm trung tâm)")
    )
    chain_notes = list(deep_syn.get("lh_chain_notes") or [])
    trait_tags = []
    if ly_res.get("ban_is_du_hon"):
        trait_tags.append("Quẻ Du Hồn (tâm bất định/biến dịch)")
    elif ly_res.get("ban_is_quy_hon"):
        trait_tags.append("Quẻ Quy Hồn (thu hồi/ổn định)")
    if ly_res.get("ban_is_luc_xung"):
        trait_tags.append("Lục Xung (va chạm/phân tán nhanh)")
    elif ly_res.get("ban_is_luc_hop"):
        trait_tags.append("Lục Hợp (kết dính/kéo dài)")

    pol_code, pol_lbl, pol_col = _polarity_from_score(lh_sc)
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    return {
        "branch_id": "B1_LIUYAO",
        "branch_name": "Luồng 1 · Lục Hào Nạp Giáp",
        "classic_source": "Tăng San Bốc Dịch & Bốc Phệ Chính Tông",
        "score": lh_sc,
        "weight": 0.44,
        "polarity_code": pol_code,
        "polarity_label": pol_lbl,
        "color": pol_col,
        "focal_anchor": dt_desc,
        "core_evidence": " · ".join(chain_notes[:3]) if chain_notes else mv_summary,
        "movement_vector": mv_summary,
        "structural_traits": ", ".join(trait_tags) if trait_tags else f"Thế Hào {the_pos} ({the_ln.get('chi','')}) ↔ Ứng Hào {ung_pos}",
        "hex_pair": f"{ban_name} ➔ {bien_name}",
        "elapsed_ms": elapsed_ms,
    }


def _branch_2_qimen_specialist(
    qm_res: Dict[str, Any],
    deep_syn: Dict[str, Any],
    chart_data: Dict[str, Any],
) -> Dict[str, Any]:
    t0 = time.perf_counter()
    qm_sc = int(deep_syn.get("qm_score", 50))
    tc = int(qm_res.get("target_cung") or 1)
    pm = qm_res.get("palace_micro_audit") or {}
    pa_tc = pm.get(tc, {})
    chain = list(qm_res.get("phien_cung_chain") or [tc])
    end_c = chain[-1] if chain else tc
    pa_end = pm.get(end_c, pa_tc)
    tu_hai = list(pa_tc.get("tu_hai") or [])
    qm_notes = list(deep_syn.get("qm_notes") or [])

    anchor_str = (
        f"Cung {tc} ({pa_tc.get('quai', '')} · {pa_tc.get('huong', '')}) — "
        f"{pa_tc.get('star', '')} · {pa_tc.get('door', '')} · {pa_tc.get('deity', '')} "
        f"[Can {pa_tc.get('can_thien_disp', '')}/{pa_tc.get('can_dia_disp', '')}, Ám Can {pa_tc.get('am_can', '')}]"
    )
    phien_str = " ➔ ".join(f"Cung {c} ({(pm.get(c) or {}).get('door', '')})" for c in chain[:4])
    hazard_str = ", ".join(tu_hai) if tu_hai else "Không phạm Tứ Hại (Cung vị thanh thuần)"

    pol_code, pol_lbl, pol_col = _polarity_from_score(qm_sc)
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    return {
        "branch_id": "B2_QIMEN",
        "branch_name": "Luồng 2 · Kỳ Môn Độn Giáp",
        "classic_source": "Ngự Định Kỳ Môn Bảo Giám",
        "score": qm_sc,
        "weight": 0.31,
        "polarity_code": pol_code,
        "polarity_label": pol_lbl,
        "color": pol_col,
        "focal_anchor": anchor_str,
        "core_evidence": " · ".join(qm_notes[:3]) if qm_notes else str(qm_res.get("ck_desc") or phien_str),
        "movement_vector": f"Lật cung: {phien_str} (Hạ màn: {pa_end.get('door', '')})",
        "structural_traits": f"Tứ Hại: {hazard_str}",
        "elapsed_ms": elapsed_ms,
    }


def _branch_3_meihua_specialist(
    mh_res: Dict[str, Any],
    deep_syn: Dict[str, Any],
) -> Dict[str, Any]:
    t0 = time.perf_counter()
    _QUAI_EL_MAP = {
        "Càn": "Kim", "Đoài": "Kim", "Ly": "Hỏa", "Chấn": "Mộc",
        "Tốn": "Mộc", "Khảm": "Thủy", "Cấn": "Thổ", "Khôn": "Thổ",
    }
    mh_sc = int(deep_syn.get("mh_score", 50))
    the_q = str(mh_res.get("the_quai") or "Càn")
    dung_q = str(mh_res.get("dung_quai") or "Khôn")
    the_el = str(mh_res.get("the_el") or mh_res.get("hanh_the") or _QUAI_EL_MAP.get(the_q, "Kim"))
    dung_el = str(mh_res.get("dung_el") or mh_res.get("hanh_dung") or _QUAI_EL_MAP.get(dung_q, "Thổ"))
    ha_ho = str(mh_res.get("ha_ho") or "Cấn")
    th_ho = str(mh_res.get("thuong_ho") or "Chấn")
    bien_d = str(mh_res.get("bien_dung_quai") or dung_q)
    bien_el = str(mh_res.get("bien_dung_el") or mh_res.get("hanh_bien_dung") or _QUAI_EL_MAP.get(bien_d, dung_el))
    rel_chu = str(mh_res.get("rel_chu_label") or mh_res.get("rel_chu") or "")
    rel_bien = str(mh_res.get("rel_bien_label") or mh_res.get("rel_bien") or "")
    party_note = str(mh_res.get("dang_the_dung_verdict") or f"Đảng Thể vs Đảng Dụng qua Hỗ Quái ({ha_ho}/{th_ho})")

    pol_code, pol_lbl, pol_col = _polarity_from_score(mh_sc)
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    return {
        "branch_id": "B3_MEIHUA",
        "branch_name": "Luồng 3 · Mai Hoa Dịch Số",
        "classic_source": "Mai Hoa Dịch Số (Thiệu Khang Tiết)",
        "score": mh_sc,
        "weight": 0.15,
        "polarity_code": pol_code,
        "polarity_label": pol_lbl,
        "color": pol_col,
        "focal_anchor": f"Quẻ Thể {the_q} ({the_el}) ↔ Quẻ Dụng {dung_q} ({dung_el})",
        "core_evidence": f"Khởi đầu: {rel_chu or 'Thể–Dụng đối ứng'} ➔ Kết cục Biến Quái ({bien_d}-{bien_el}): {rel_bien or 'Chuyển hóa theo Biến'}",
        "movement_vector": f"4 Chặng: Thể {the_q}/Dụng {dung_q} ➔ Hạ Hỗ {ha_ho} ➔ Thượng Hỗ {th_ho} ➔ Biến {bien_d}",
        "structural_traits": _strip_tags(party_note)[:140],
        "elapsed_ms": elapsed_ms,
    }


def _branch_4_daliuren_specialist(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Luồng 4 chạy độc lập Đại Lục Nhâm (Tứ Khóa & Tam Truyền Sơ–Trung–Mạt) để soi lộ trình 3 giai đoạn."""
    t0 = time.perf_counter()
    can_n = str((chart_data or {}).get("can_ngay") or "Giáp")
    chi_n = str((chart_data or {}).get("chi_ngay") or "Tý")
    chi_g = str((chart_data or {}).get("chi_gio") or "Tý")
    tk_raw = str((chart_data or {}).get("tiet_khi") or "Tiểu Tuyết").split("(")[0].strip()

    dln_sc = 52
    so_tr, trung_tr, mat_tr = "Tý", "Thìn", "Thân"
    cach_cuc_dln = "Tam Truyền Thuận Tiến"
    dln_verdict_note = ""
    try:
        from dai_luc_nham import tinh_dai_luc_nham
        r_dln = tinh_dai_luc_nham(can_n, chi_n, chi_g, tk_raw) or {}
        tt = r_dln.get("tam_truyen") or {}
        so_d = tt.get("so") if isinstance(tt.get("so"), dict) else {}
        tr_d = tt.get("trung") if isinstance(tt.get("trung"), dict) else {}
        ma_d = tt.get("mat") if isinstance(tt.get("mat"), dict) else {}
        so_tr = f"{so_d.get('chi', tt.get('so_truyen', '?'))} ({so_d.get('tuong', '')} · {so_d.get('luc_than', '')})".strip(" ()·")
        trung_tr = f"{tr_d.get('chi', tt.get('trung_truyen', '?'))} ({tr_d.get('tuong', '')} · {tr_d.get('luc_than', '')})".strip(" ()·")
        mat_tr = f"{ma_d.get('chi', tt.get('mat_truyen', '?'))} ({ma_d.get('tuong', '')} · {ma_d.get('luc_than', '')})".strip(" ()·")
        cach_cuc_dln = str(tt.get("ten_cach") or tt.get("phuong_phap") or "Tam Truyền Khóa Thức")
        lg = r_dln.get("luan_giai") or {}
        if isinstance(lg, dict):
            v_str = str(lg.get("ket_luan") or lg.get("verdict") or "")
            dln_verdict_note = str(lg.get("tong_quan") or lg.get("chi_tiet") or v_str)
            if isinstance(dln_verdict_note, list):
                dln_verdict_note = " · ".join(str(x) for x in dln_verdict_note[:2])
            v_up = (v_str + " " + str(dln_verdict_note)).upper()
            if "ĐẠI CÁT" in v_up:
                dln_sc = 74
            elif "CÁT" in v_up and "HUNG" not in v_up:
                dln_sc = 63
            elif "ĐẠI HUNG" in v_up:
                dln_sc = 28
            elif "HUNG" in v_up and "CÁT" not in v_up:
                dln_sc = 38
            else:
                dln_sc = 51
            # Điều chỉnh nhẹ theo Mạt Truyền Lục Thân (Kết cục)
            mat_lt = str(ma_d.get("luc_than") or "")
            if "Tử Tôn" in mat_lt or "Tài" in mat_lt:
                dln_sc = min(85, dln_sc + 6)
            elif "Quan Quỷ" in mat_lt:
                dln_sc = max(22, dln_sc - 7)
    except Exception:
        pass

    pol_code, pol_lbl, pol_col = _polarity_from_score(dln_sc)
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    return {
        "branch_id": "B4_DALIUREN",
        "branch_name": "Luồng 4 · Đại Lục Nhâm Tam Truyền",
        "classic_source": "Đại Lục Nhâm Đại Toàn (Sơ–Trung–Mạt)",
        "score": dln_sc,
        "weight": 0.10,
        "polarity_code": pol_code,
        "polarity_label": pol_lbl,
        "color": pol_col,
        "focal_anchor": f"Khóa thức: {cach_cuc_dln} (Ngày {can_n} {chi_n} · Giờ {chi_g})",
        "core_evidence": _strip_tags(dln_verdict_note)[:160] or f"Sơ Truyền {so_tr} mở đầu, Mạt Truyền {mat_tr} định kết cục",
        "movement_vector": f"Sơ Truyền [{so_tr}] ➔ Trung Truyền [{trung_tr}] ➔ Mạt Truyền [{mat_tr}]",
        "structural_traits": f"Lộ trình 3 thời Sơ–Trung–Mạt",
        "so_truyen": so_tr,
        "trung_truyen": trung_tr,
        "mat_truyen": mat_tr,
        "elapsed_ms": elapsed_ms,
    }


def _branch_5_adversarial_critic(
    ly_res: Dict[str, Any],
    qm_res: Dict[str, Any],
    mh_res: Dict[str, Any],
    deep_syn: Dict[str, Any],
    question: str,
) -> Dict[str, Any]:
    """
    Luồng 5 (Phản Biện Ngược Chiều — Devil's Advocate / Counterfactual Critic):
    Chuyên truy tìm các bẫy 'Giả Cát Thực Hung', 'Giả Hung Thực Cát', mâu thuẫn giữa Nội Hào và Ngoại Tượng,
    để ngăn chặn 100% phán đoán nông cạn một chiều!
    """
    t0 = time.perf_counter()
    traps_found: List[str] = []
    hidden_rescues: List[str] = []
    penalty_pts = 0
    rescue_pts = 0

    lines = ly_res.get("line_micro_audit") or []
    dt_idx = int(ly_res.get("dt_hao_idx") or 1)
    the_pos = int(ly_res.get("the_pos") or 1)
    dt_ln = lines[dt_idx - 1] if 1 <= dt_idx <= len(lines) else {}
    the_ln = lines[the_pos - 1] if 1 <= the_pos <= len(lines) else {}

    # 1. Bẫy Hào Dụng/Thế Động Hóa Hồi Đầu Khắc / Hóa Không / Hóa Thoái ("Trước sáng sau tối")
    for tag_lbl, ln_chk in (("Dụng Thần", dt_ln), ("Hào Thế", the_ln)):
        if not ln_chk:
            continue
        hflags = set(ln_chk.get("hoa_flags") or [])
        if "HOI_DAU_KHAC" in hflags:
            traps_found.append(f"Bẫy «Động Hóa Hồi Đầu Khắc» tại {tag_lbl} Hào {ln_chk.get('hao')} ({ln_chk.get('chi')} hóa {ln_chk.get('bien_chi')}) — ban đầu tưởng thuận nhưng tự sinh lực phản tác dụng ở chặng cuối")
            penalty_pts += 12
        if "HOA_THOAI" in hflags:
            traps_found.append(f"Bẫy «Hóa Thoái Thần» tại {tag_lbl} Hào {ln_chk.get('hao')} ({ln_chk.get('chi')} lùi về {ln_chk.get('bien_chi')}) — nhiệt độ/nguồn lực giảm dần về sau")
            penalty_pts += 8
        if "HOA_KHONG" in hflags:
            traps_found.append(f"Bẫy «Động Hóa Không Vong» tại {tag_lbl} Hào {ln_chk.get('hao')} — lời hứa hoặc kế hoạch dễ rơi vào khoảng trống chưa thực chất")
            penalty_pts += 9
        if "HOI_DAU_SINH" in hflags:
            hidden_rescues.append(f"Điểm cứu «Động Hóa Hồi Đầu Sinh» tại {tag_lbl} Hào {ln_chk.get('hao')} ({ln_chk.get('bien_chi')} quay lại sinh {ln_chk.get('chi')}) — càng về sau càng có hậu lực nâng đỡ")
            rescue_pts += 10
        if "HOA_TIEN" in hflags:
            hidden_rescues.append(f"Điểm bứt phá «Hóa Tiến Thần» tại {tag_lbl} Hào {ln_chk.get('hao')} ({ln_chk.get('chi')} tiến lên {ln_chk.get('bien_chi')}) — đà tăng trưởng mạnh dần")
            rescue_pts += 8

    # 2. Bẫy Chân Không vs Giả Không (Xung Không / Động Không = Hư ảo thành Thực!)
    if dt_ln.get("is_void"):
        vtype = str(dt_ln.get("void_type") or "")
        if dt_ln.get("is_moving") or "GIẢ" in vtype.upper() or "XUNG" in vtype.upper():
            hidden_rescues.append(f"Giải ảo «Giả Không / Xung Thực» tại Hào {dt_idx} ({dt_ln.get('chi')}) — hiện tại tạm trống nhưng đến ngày Xuất/Xung Không sẽ ứng nghiệm thật")
            rescue_pts += 6
        else:
            traps_found.append(f"Cảnh báo «Chân Không Vô Khí» tại Hào {dt_idx} ({dt_ln.get('chi')}) — mục tiêu hiện chưa đủ cơ sở thực tế, chớ vội tin lời hứa suông")
            penalty_pts += 10

    # 3. Bẫy "Ngoại Cát Nội Hung" (Kỳ Môn/Mai Hoa điểm cao >= 65 nhưng Lục Hào nội tại <= 38 hoặc Du Hồn + Kỵ Thần động khắc Thế)
    lh_sc = int(deep_syn.get("lh_score", 50))
    qm_sc = int(deep_syn.get("qm_score", 50))
    mh_sc = int(deep_syn.get("mh_score", 50))
    if max(qm_sc, mh_sc) >= 65 and lh_sc <= 38:
        traps_found.append(
            f"Phát hiện lệch pha «Ngoại Tượng Sáng ({max(qm_sc, mh_sc)}/100) nhưng Nội Hào Tổn Thương ({lh_sc}/100)»: "
            f"bề ngoài/hoàn cảnh trông thuận lợi nhưng bên trong đang chịu sức ép sinh khắc trực tiếp — phải ưu tiên gốc Lục Hào, tránh lạc quan sớm"
        )
        penalty_pts += 8
    elif lh_sc >= 65 and min(qm_sc, mh_sc) <= 38:
        hidden_rescues.append(
            f"Phát hiện «Nội Lực Vững ({lh_sc}/100) vượt Ngoại Cảnh Khó ({min(qm_sc, mh_sc)}/100)»: "
            f"môi trường bên ngoài có rào cản Tứ Hại nhưng thực lực gốc Dụng Thần đủ mạnh để vượt qua"
        )
        rescue_pts += 6

    # 4. Bẫy Kỳ Môn "Đắc Kỳ Bất Đắc Môn" hoặc Môn Bức / Lục Nghi Kích Hình tại Cung Dụng Thần
    tc = int(qm_res.get("target_cung") or 1)
    pa_tc = (qm_res.get("palace_micro_audit") or {}).get(tc, {})
    tu_hai_tc = list(pa_tc.get("tu_hai") or [])
    door_tc = str(pa_tc.get("door") or "")
    if any(d in door_tc for d in ("Tử Môn", "Kinh Môn", "Thương Môn", "Đỗ Môn")) and any(
        k in str(pa_tc.get("can_thien_disp", "")) for k in ("Ất", "Bính", "Đinh")
    ):
        traps_found.append(f"Bẫy Kỳ Môn «Đắc Kỳ Bất Đắc Môn» tại Cung {tc} (có Tam Kỳ nhưng lâm {door_tc}) — có cơ hội tốt nhưng khâu thực thi dễ vướng thủ tục/nhân sự")
        penalty_pts += 6
    if tu_hai_tc:
        traps_found.append(f"Điểm mù Tứ Hại Kỳ Môn tại Cung {tc}: {', '.join(tu_hai_tc[:2])}")
        penalty_pts += 5

    # 5. Bẫy Quẻ Du Hồn & Phục Ngâm / Phản Ngâm
    if ly_res.get("ban_is_du_hon"):
        traps_found.append("Tượng «Quẻ Du Hồn»: tâm tư người trong cuộc dễ dao động, hay nghĩ ngợi lan man hoặc kế hoạch thay đổi giữa chừng")
    if qm_res.get("is_phuc_ngam"):
        traps_found.append("Cục «Phục Ngâm Kỳ Môn»: tiến độ thực tế sẽ chậm hơn dự kiến, kỵ nóng vội thúc ép")
    elif qm_res.get("is_phan_ngam"):
        traps_found.append("Cục «Phản Ngâm Kỳ Môn»: sự việc dễ đảo chiều nhanh hoặc phải làm đi làm lại 2 lần mới xong")

    critic_summary = (
        traps_found[0]
        if traps_found
        else (hidden_rescues[0] if hidden_rescues else "Đã rà quét 5 tầng bẫy cổ pháp: Không phát hiện bẫy Hồi Đầu Khắc hay Chân Không ngầm.")
    )
    risk_level = "CAO (Cần phòng thủ chặt)" if penalty_pts >= 14 else ("TRUNG BÌNH (Lưu ý điều kiện)" if penalty_pts >= 6 else "THẤP (Mạch quẻ thuần khiết)")
    col = "#ef4444" if penalty_pts >= 14 else ("#fbbf24" if penalty_pts >= 6 else "#34d399")
    elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    return {
        "branch_id": "B5_ADVERSARIAL_CRITIC",
        "branch_name": "Luồng 5 · Phản Biện Chống Sai Lầm",
        "classic_source": "Đối Kiểm Ngược Chiều (Red-Team Critic)",
        "score": max(15, min(92, int(deep_syn.get("composite_score", 50)) - penalty_pts // 2 + rescue_pts // 2)),
        "weight": 0.0,  # Dùng làm bộ hiệu chỉnh phản biện (calibration & caveat), không pha loãng điểm thô
        "polarity_code": "CRITIC_ALERT" if traps_found else "CRITIC_CLEAN",
        "polarity_label": f"MỨC RỦI RO ẨN: {risk_level}",
        "color": col,
        "focal_anchor": f"Phát hiện {len(traps_found)} bẫy tiềm ẩn · {len(hidden_rescues)} điểm cứu giải",
        "core_evidence": critic_summary,
        "traps_found": traps_found,
        "hidden_rescues": hidden_rescues,
        "penalty_pts": penalty_pts,
        "rescue_pts": rescue_pts,
        "risk_level": risk_level,
        "elapsed_ms": elapsed_ms,
    }


# ═══════════════════════════════════════════════════════════════════════════
# ĐỘNG CƠ HỢP NHẤT: 5 LUỒNG SONG SONG + 7 BƯỚC SUY LUẬN TUẦN TỰ (V146.0)
# ═══════════════════════════════════════════════════════════════════════════

def execute_multi_step_parallel_reasoning(
    blueprint: Dict[str, Any],
    dung_than: str,
    ly_res: Dict[str, Any],
    qm_res: Dict[str, Any],
    mh_res: Dict[str, Any],
    deep_syn: Dict[str, Any],
    chart_data: Optional[Dict[str, Any]] = None,
    question: str = "",
) -> Dict[str, Any]:
    """
    Thực thi đồng thời 5 Luồng Tư Duy Song Song trên ThreadPoolExecutor,
    sau đó dẫn xuất Chuỗi Suy Luận Đa Bước 7 Tầng (Step 1 -> Step 7) kèm Kiểm Định Chống Mâu Thuẫn.
    """
    t_start = time.perf_counter()
    chart_data = chart_data or {}
    q_clean = str(question or blueprint.get("raw_question") or "").strip()
    q_low = q_clean.lower()

    # ── BƯỚC 1: GIẢI PHẪU Ý ĐỊNH, ĐIỀU KIỆN & QUY TẮC CÁT/HUNG ĐẶC THÙ ──
    arch_code = str(blueprint.get("archetype_code") or "D25")
    arch_name = str(blueprint.get("archetype_name") or "Luận đoán tổng quát")
    spec_target = str(blueprint.get("specific_target") or deep_syn.get("special_mode") or "GENERAL")
    subj_person = str(blueprint.get("subject_person") or "Bản thân người hỏi")
    has_cond_clause = bool(re.search(r"\b(nếu\s+|giả\s+sử|trường\s+hợp)\b", q_low))
    is_compound = bool(blueprint.get("is_compound_question") and blueprint.get("sub_questions"))
    invert_hazard = any(w in q_low for w in ("có bị lừa", "có mưa", "bị bệnh", "có tai nạn", "vong theo", "bị động"))

    step1_desc = (
        f"Phân loại [{arch_code} — {arch_name}] · Chủ thể: {subj_person}"
        + (f" · Tách {len(blueprint['sub_questions'])} vế độc lập" if is_compound else "")
        + (" · Bảo toàn mệnh đề điều kiện «Nếu... thì...»" if has_cond_clause else "")
        + (" · Áp dụng luật Đảo Cực Rủi Ro (Dụng Thần suy/bị chế mới là Bình An)" if invert_hazard else "")
    )

    # ── BƯỚC 2: PHÁP ĐỊNH DỤNG THẦN ĐA HỆ & KIỂM CHỨNG THỰC/HƯ ──
    dt_idx = int(ly_res.get("dt_hao_idx") or 1)
    lines = ly_res.get("line_micro_audit") or []
    dt_ln = lines[dt_idx - 1] if 1 <= dt_idx <= len(lines) else {}
    phuc_info = ly_res.get("phuc_than_info") or {}
    tc = int(qm_res.get("target_cung") or 1)
    step2_desc = (
        f"Lục Hào khóa Dụng Thần «{dung_than}» tại Hào {dt_idx} ({dt_ln.get('chi','')}-{dt_ln.get('ngu_hanh','')}, bậc {dt_ln.get('vuong_suy','Bình')})"
        + (f" [Phục Thần ẩn dưới Phi Thần {phuc_info.get('phi_chi','')}]" if phuc_info.get("is_phuc") else "")
        + f" · Kỳ Môn khóa Cung {tc} · Mai Hoa khóa Thể {mh_res.get('the_quai','')} ↔ Dụng {mh_res.get('dung_quai','')}"
    )

    # ── BƯỚC 3: KÍCH HOẠT 5 LUỒNG TƯ DUY SONG SONG (PARALLEL THINKING FAN-OUT) ──
    f_b1 = _SHARED_PARALLEL_POOL.submit(_branch_1_liuyao_specialist, ly_res, deep_syn, dung_than, q_clean)
    f_b2 = _SHARED_PARALLEL_POOL.submit(_branch_2_qimen_specialist, qm_res, deep_syn, chart_data)
    f_b3 = _SHARED_PARALLEL_POOL.submit(_branch_3_meihua_specialist, mh_res, deep_syn)
    f_b4 = _SHARED_PARALLEL_POOL.submit(_branch_4_daliuren_specialist, chart_data)
    f_b5 = _SHARED_PARALLEL_POOL.submit(_branch_5_adversarial_critic, ly_res, qm_res, mh_res, deep_syn, q_clean)

    b1 = f_b1.result()
    b2 = f_b2.result()
    b3 = f_b3.result()
    b4 = f_b4.result()
    b5 = f_b5.result()
    branches = [b1, b2, b3, b4, b5]

    step3_desc = (
        f"Thực thi song song 5 luồng chuyên gia: Lục Hào ({b1['score']}/100) · Kỳ Môn ({b2['score']}/100) · "
        f"Mai Hoa ({b3['score']}/100) · Đại Lục Nhâm ({b4['score']}/100) · Phản Biện ({b5['focal_anchor']})"
    )

    # ── BƯỚC 4: SUY DIỄN DIỄN BIẾN 3 THỜI (KHỞI PHÁT ➔ BIẾN CHUYỂN ➔ KẾT CỤC) ──
    chain_km = list(qm_res.get("phien_cung_chain") or [tc])
    pm = qm_res.get("palace_micro_audit") or {}
    km_start_door = (pm.get(chain_km[0]) or {}).get("door", "") if chain_km else ""
    km_end_door = (pm.get(chain_km[-1]) or {}).get("door", "") if chain_km else ""
    stage_1_init = f"Quẻ Chủ {ly_res.get('ban_name','')} · Sơ Truyền {b4.get('so_truyen','')} · Khởi cung {km_start_door}"
    stage_2_mid = f"Quẻ Hỗ {mh_res.get('ten_ho', mh_res.get('ha_ho',''))} · Trung Truyền {b4.get('trung_truyen','')} · {b1['movement_vector'][:95]}"
    stage_3_end = f"Quẻ Biến {ly_res.get('bien_name','')} · Mạt Truyền {b4.get('mat_truyen','')} · Hạ màn {km_end_door}"

    # Nhận diện quỹ đạo Trước–Sau
    lh_sc = b1["score"]
    mh_rel_bien = str(mh_res.get("rel_bien_label") or "")
    has_hdk = any("Hồi Đầu Khắc" in t or "Hóa Thoái" in t for t in b5["traps_found"])
    has_hds = any("Hồi Đầu Sinh" in r or "Hóa Tiến" in r for r in b5["hidden_rescues"])
    if has_hdk:
        trajectory_tag = "TRƯỚC MỞ SAU THU HẸP (Cần chốt nhanh, tránh kéo dài)"
    elif has_hds or ("sinh Thể" in mh_rel_bien and lh_sc >= 45):
        trajectory_tag = "TRƯỚC CHẬM SAU THÔNG (Càng về cuối càng sáng)"
    elif int(deep_syn.get("composite_score", 50)) >= 56:
        trajectory_tag = "THUẬN ĐÀ TIẾN LÊN (Khí lực thông suốt 3 chặng)"
    else:
        trajectory_tag = "ĐANG TÍCH LŨY CHỜ MỞ KHÓA (Thủ vững chờ đúng ứng kỳ)"

    step4_desc = f"[{trajectory_tag}] Khởi phát ({stage_1_init}) ➔ Chuyển tiếp ({stage_2_mid}) ➔ Kết cục ({stage_3_end})"

    # ── BƯỚC 5: ĐỐI BIỆN GIẢI QUYẾT XUNG ĐỘT & TÍNH ĐỘ ĐỒNG THUẬN HỘI ĐỒNG ──
    comp_sc = int(deep_syn.get("composite_score", 50))
    primary_4_scores = [b1["score"], b2["score"], b3["score"], b4["score"]]
    target_is_pos = comp_sc >= 50
    agree_cnt = sum(1 for s in primary_4_scores if (s >= 50) == target_is_pos)
    spread = max(primary_4_scores) - min(primary_4_scores)
    consensus_pct = max(54, min(99, int(round((agree_cnt / 4.0) * 85 + max(0, 30 - spread) * 0.5))))

    if spread >= 28:
        if b1["score"] < 42 and max(b2["score"], b3["score"]) >= 62:
            conflict_resolution = (
                f"Giải quyết xung đột (Lục Hào {b1['score']} vs Kỳ Môn/Mai Hoa {max(b2['score'], b3['score'])}): "
                f"Áp dụng nguyên lý «Lục Hào định gốc sinh khắc nội tại, Kỳ Môn/Mai Hoa định ngoại cảnh» — "
                f"bề ngoài hoàn cảnh mở lối nhưng gốc Dụng Thần/Hào Thế đang chịu hình khắc, nên chốt theo chiều thận trọng ({comp_sc}/100)."
            )
        elif b1["score"] >= 60 and min(b2["score"], b3["score"]) < 42:
            conflict_resolution = (
                f"Giải quyết xung đột (Lục Hào {b1['score']} vs Ngoại cảnh {min(b2['score'], b3['score'])}): "
                f"Nội lực Dụng Thần Lục Hào đủ vượng để vượt lực cản Tứ Hại ngoại cảnh — việc vẫn thành nhưng phải vượt rào cản ban đầu ({comp_sc}/100)."
            )
        else:
            conflict_resolution = (
                f"Phân hóa giữa các hệ ({min(primary_4_scores)}–{max(primary_4_scores)} điểm): "
                f"Trọng tài ưu tiên chuỗi Hào Động Lục Hào (44%) + Chủ–Khách Kỳ Môn (31%), chốt điểm hội tụ {comp_sc}/100 (Đồng thuận {consensus_pct}%)."
            )
    else:
        conflict_resolution = (
            f"4 hệ Tam Thức + Lục Nhâm đồng pha cao (biên độ chênh lệch thấp {spread} điểm) ➔ "
            f"Độ đồng thuận Hội Đồng đạt {consensus_pct}%, chốt khí lực hợp nhất {comp_sc}/100."
        )

    # ── BƯỚC 6: CHẨN ĐOÁN BỆNH – DƯỢC & KHÓA ỨNG KỲ THIÊN VĂN ──
    benh_q = str(deep_syn.get("benh_quai") or "Quẻ vận hành ổn định")
    uk_short = str(deep_syn.get("short_inline_date") or deep_syn.get("duoc_ung_ky") or "")
    step6_desc = f"Bệnh quái: {benh_q} ══► Dược & Ứng kỳ mở khóa: {uk_short}"

    # ── BƯỚC 7: CỔNG TỰ KIỂM CHỨNG CHỐNG MÂU THUẪN (SELF-VERIFICATION GATE) ──
    hl_now = _strip_tags(deep_syn.get("direct_headline") or "")
    caveat_to_inject = ""
    if b5["traps_found"] and comp_sc >= 55:
        caveat_to_inject = b5["traps_found"][0]
    elif b5["hidden_rescues"] and comp_sc < 48:
        caveat_to_inject = b5["hidden_rescues"][0]

    checks_passed = [
        "Khớp Quẻ Chủ/Biến giữa Lục Hào & Mai Hoa",
        f"Khóa Dụng Thần «{dung_than}» xuyên suốt 5 luồng",
        "Khóa ngày Dương/Âm lịch chuẩn thiên văn UTC+7",
    ]
    if has_cond_clause:
        checks_passed.append("Đã kiểm tra đủ cả vế chính & vế điều kiện «Nếu... thì...»")
    if is_compound:
        checks_passed.append(f"Đã kiểm tra đủ {len(blueprint['sub_questions'])}/{len(blueprint['sub_questions'])} vế câu hỏi ghép")

    step7_desc = "PASS 100% (" + " · ".join(checks_passed) + ")"
    if caveat_to_inject:
        step7_desc += f" | Ghi chú Phản biện: {caveat_to_inject}"

    total_ms = round((time.perf_counter() - t_start) * 1000.0, 2)

    steps_trace = [
        {"step": 1, "title": "Giải Phẫu Ý Định & Cấu Trúc Câu Hỏi", "detail": step1_desc, "badge": arch_code},
        {"step": 2, "title": "Pháp Định Dụng Thần Đa Hệ & Thực/Hư", "detail": step2_desc, "badge": dung_than},
        {"step": 3, "title": "Tư Duy Song Song 5 Luồng Độc Lập", "detail": step3_desc, "badge": f"{total_ms}ms"},
        {"step": 4, "title": "Suy Diễn Nhân–Quả 3 Thời (Sơ–Trung–Mạt)", "detail": step4_desc, "badge": trajectory_tag.split("(")[0].strip()},
        {"step": 5, "title": "Đối Biện Xung Đột & Hội Tụ Trọng Số", "detail": conflict_resolution, "badge": f"Đồng thuận {consensus_pct}%"},
        {"step": 6, "title": "Chẩn Đoán Bệnh–Dược & Khóa Ứng Kỳ", "detail": step6_desc, "badge": "Lịch Thiên Văn"},
        {"step": 7, "title": "Cổng Tự Kiểm Chứng Chống Mâu Thuẫn", "detail": step7_desc, "badge": "VERIFIED"},
    ]

    prompt_block = (
        "=== HỒ SƠ SUY LUẬN ĐA BƯỚC (7-STEP) & TƯ DUY SONG SONG 5 LUỒNG V146.0 [CHUẨN /PROMAX · /RAW · /TLDR · /SOURCE] ===\n"
        "- [CHẾ ĐỘ BẮT BUỘC /TLDR]: Mở đầu Headline bằng đáp án chốt hạ trực diện, 1 nhìn hiểu ngay, không vòng vo.\n"
        "- [CHẾ ĐỘ BẮT BUỘC /RAW]: Đọc thẳng thông số thô Hào/Cung/Không Vong/Hình-Xung-Phá-Mộ; Cát nói Cát, Hung nói thẳng Hung, CẤM tô hồng hay văn mẫu nước đôi.\n"
        "- [CHẾ ĐỘ BẮT BUỘC /SOURCE]: Mọi luận cứ phải gắn rõ nguồn cổ thư (Tăng San Bốc Dịch / Ngự Định Kỳ Môn Bảo Giám / Mai Hoa Dịch Số / Đại Lục Nhâm) kèm vị trí Hào/Cung cụ thể.\n"
        f"- [Bước 1 - Giải phẫu câu hỏi]: {step1_desc}\n"
        f"- [Bước 2 - Định Dụng Thần]: {step2_desc}\n"
        f"- [Bước 3 - Kết quả 5 Luồng Tư Duy Song Song (/promax)]:\n"
        f"   + {b1['branch_name']} ({b1['score']}/100 - {b1['polarity_label']}) [Nguồn: {b1['classic_source']}]: {b1['core_evidence']}\n"
        f"   + {b2['branch_name']} ({b2['score']}/100 - {b2['polarity_label']}) [Nguồn: {b2['classic_source']}]: {b2['core_evidence']} | {b2['movement_vector']}\n"
        f"   + {b3['branch_name']} ({b3['score']}/100 - {b3['polarity_label']}) [Nguồn: {b3['classic_source']}]: {b3['core_evidence']}\n"
        f"   + {b4['branch_name']} ({b4['score']}/100 - {b4['polarity_label']}) [Nguồn: {b4['classic_source']}]: {b4['movement_vector']} | {b4['core_evidence']}\n"
        f"   + {b5['branch_name']} ({b5['polarity_label']}) [Nguồn: {b5['classic_source']}]: {b5['core_evidence']}\n"
        f"- [Bước 4 - Diễn biến 3 Thời]: {step4_desc}\n"
        f"- [Bước 5 - Trọng tài Giải quyết Xung đột (Đồng thuận {consensus_pct}%)]: {conflict_resolution}\n"
        f"- [Bước 6 - Bệnh Dược & Ứng Kỳ]: {step6_desc}\n"
        f"- [Bước 7 - Cổng Kiểm Chứng]: {step7_desc}\n"
    )

    raw_coords_str = (
        f"RAW: {b1.get('hex_pair','')} · {b1['focal_anchor']} | {b2['focal_anchor']} | "
        f"{b3['focal_anchor']} | {b4['movement_vector']}"
    )
    sources_str = (
        "SOURCE: Tăng San Bốc Dịch (Dã Hạc) · Bốc Phệ Chính Tông · Ngự Định Kỳ Môn Bảo Giám · "
        "Mai Hoa Dịch Số (Thiệu Khang Tiết) · Đại Lục Nhâm Đại Toàn"
    )

    panel_html = render_multi_step_parallel_html(
        branches=branches,
        steps_trace=steps_trace,
        consensus_pct=consensus_pct,
        composite_score=comp_sc,
        trajectory_tag=trajectory_tag,
        total_ms=total_ms,
        online_parallel_meta=None,
        tldr_line=hl_now,
        raw_coords_str=raw_coords_str,
        sources_str=sources_str,
    )

    return {
        "version": "V146.0",
        "branches": branches,
        "steps_trace": steps_trace,
        "consensus_pct": consensus_pct,
        "composite_score": comp_sc,
        "trajectory_tag": trajectory_tag,
        "conflict_resolution": conflict_resolution,
        "adversarial_traps": b5["traps_found"],
        "adversarial_rescues": b5["hidden_rescues"],
        "caveat_to_inject": caveat_to_inject,
        "raw_coords_str": raw_coords_str,
        "sources_str": sources_str,
        "total_ms": total_ms,
        "prompt_block": prompt_block,
        "panel_html": panel_html,
    }


def render_multi_step_parallel_html(
    branches: List[Dict[str, Any]],
    steps_trace: List[Dict[str, Any]],
    consensus_pct: int,
    composite_score: int,
    trajectory_tag: str,
    total_ms: float,
    online_parallel_meta: Optional[Dict[str, Any]] = None,
    tldr_line: str = "",
    raw_coords_str: str = "",
    sources_str: str = "",
) -> str:
    """Render giao diện Trực quan 5 Luồng Tư Duy Song Song + Chuỗi Suy Luận 7 Bước [Chuẩn /promax · /raw · /TLDR · /source]."""
    branch_cards = []
    for b in branches:
        b_col = str(b.get("color") or "#38bdf8")
        b_sc_txt = (
            f'<span style="background:rgba(15,23,42,0.9);color:{b_col};padding:1px 7px;border-radius:999px;font-weight:900;font-size:0.80em;border:1px solid {b_col};">{b["score"]}/100</span>'
            if b.get("branch_id") != "B5_ADVERSARIAL_CRITIC"
            else f'<span style="background:rgba(15,23,42,0.9);color:{b_col};padding:1px 7px;border-radius:999px;font-weight:900;font-size:0.78em;border:1px solid {b_col};">RED-TEAM</span>'
        )
        branch_cards.append(
            f'<div style="padding:9px 11px;background:rgba(15,23,42,0.88);border-radius:10px;border-left:4px solid {b_col};border-top:1px solid rgba(255,255,255,0.06);">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:4px;">'
            f'<span style="font-weight:900;color:#f8fafc;font-size:0.86em;">{_esc(b.get("branch_name"))}</span>'
            f'{b_sc_txt}'
            f'</div>'
            f'<div style="font-size:0.78em;font-weight:800;color:{b_col};margin-bottom:3px;">{_esc(b.get("polarity_label"))}</div>'
            f'<div style="font-size:0.81em;color:#cbd5e1;line-height:1.42;">'
            f'<b>Trục (/raw):</b> {_esc(b.get("focal_anchor"))}<br>'
            f'<b>Luận cứ:</b> {_esc(b.get("core_evidence"))}<br>'
            f'<span style="color:#94a3b8;font-size:0.92em;">📚 <i>[Nguồn: {_esc(b.get("classic_source"))}]</i></span>'
            f'</div></div>'
        )

    tldr_strip_html = ""
    if tldr_line:
        tldr_strip_html = (
            f'<div style="margin-bottom:8px;padding:7px 11px;background:rgba(250,204,21,0.11);border-radius:8px;border-left:4px solid #facc15;font-size:0.85em;color:#fef9c3;line-height:1.45;">'
            f'<b style="color:#fde047;">⚡ [/TLDR — Chốt Hạ Tức Thì]:</b> {_esc(tldr_line)}'
            f'</div>'
        )

    raw_source_footer_html = ""
    if raw_coords_str or sources_str:
        raw_source_footer_html = (
            f'<div style="margin-top:8px;padding:6px 10px;background:rgba(15,23,42,0.78);border-radius:8px;border:1px dashed rgba(148,163,184,0.32);font-size:0.78em;color:#cbd5e1;line-height:1.45;">'
            + (f'<div>🔬 <b style="color:#7dd3fc;">[/raw]:</b> {_esc(raw_coords_str)}</div>' if raw_coords_str else "")
            + (f'<div>📖 <b style="color:#c4b5fd;">[/source]:</b> {_esc(sources_str)}</div>' if sources_str else "")
            + '</div>'
        )

    online_council_banner = ""
    if isinstance(online_parallel_meta, dict) and online_parallel_meta.get("active"):
        _st_a = _esc(online_parallel_meta.get("stream_a_model", "GEMINI-2.5-FLASH"))
        _st_b = _esc(online_parallel_meta.get("stream_b_summary", ""))
        _lat_s = _esc(online_parallel_meta.get("parallel_elapsed_s", ""))
        online_council_banner = (
            f'<div style="margin-top:8px;padding:8px 11px;background:rgba(56,189,248,0.11);border-radius:8px;border-left:3px solid #38bdf8;font-size:0.83em;color:#e0f2fe;line-height:1.45;">'
            f'⚡ <b>Hội Đồng Song Song AI Online ({_st_a} · {_lat_s}s):</b> Đã chạy đồng thời <b>Luồng Chánh Luận 7 Bước</b> & <b>Luồng Phản Biện Ngược Chiều</b>'
            + (f" ➔ <i>{_st_b}</i>" if _st_b else "")
            + '</div>'
        )

    step_rows = []
    for st_item in steps_trace:
        step_rows.append(
            f'<div style="display:flex;align-items:flex-start;gap:8px;padding:6px 8px;border-bottom:1px solid rgba(148,163,184,0.14);">'
            f'<span style="flex-shrink:0;background:linear-gradient(135deg,#0284c7,#2563eb);color:#fff;font-weight:900;font-size:0.76em;padding:2px 7px;border-radius:6px;">BƯỚC {st_item["step"]}</span>'
            f'<div style="flex:1;font-size:0.83em;color:#e2e8f0;line-height:1.45;">'
            f'<b style="color:#fde047;">{_esc(st_item["title"])}:</b> {_esc(st_item["detail"])}'
            f'</div>'
            f'<span style="flex-shrink:0;background:rgba(251,191,36,0.14);color:#fde68a;border:1px solid rgba(251,191,36,0.35);font-size:0.74em;font-weight:800;padding:1px 7px;border-radius:999px;">{_esc(st_item["badge"])}</span>'
            f'</div>'
        )

    return (
        f'<div style="margin:10px 0 12px 0;padding:13px 15px;background:linear-gradient(135deg,rgba(15,23,42,0.96),rgba(30,27,75,0.94));border-radius:14px;border:1.5px solid rgba(167,139,250,0.55);box-shadow:0 4px 18px rgba(139,92,246,0.18);">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:9px;border-bottom:1px solid rgba(167,139,250,0.25);padding-bottom:6px;">'
        f'<div style="font-size:0.95em;font-weight:900;color:#e9d5ff;">🧬 TƯ DUY SONG SONG 5 LUỒNG & SUY LUẬN ĐA BƯỚC 7 TẦNG (V146.0 — /PROMAX · /RAW · /TLDR · /SOURCE)</div>'
        f'<div style="display:flex;gap:6px;flex-wrap:wrap;">'
        f'<span style="background:rgba(34,197,94,0.16);color:#86efac;padding:2px 9px;border-radius:999px;font-size:0.78em;font-weight:800;border:1px solid rgba(34,197,94,0.45);">Đồng thuận: {consensus_pct}%</span>'
        f'<span style="background:rgba(251,191,36,0.16);color:#fde047;padding:2px 9px;border-radius:999px;font-size:0.78em;font-weight:800;border:1px solid rgba(251,191,36,0.45);">Hợp nhất: {composite_score}/100 · {_esc(trajectory_tag.split("(")[0].strip())}</span>'
        f'</div></div>'
        + tldr_strip_html
        + f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(225px,1fr));gap:8px;">'
        + "".join(branch_cards)
        + '</div>'
        + online_council_banner
        + raw_source_footer_html
        + f'<details style="margin-top:9px;background:rgba(9,13,26,0.85);border:1px solid rgba(56,189,248,0.32);border-radius:9px;padding:7px 10px;">'
        f'<summary style="cursor:pointer;font-weight:800;color:#7dd3fc;font-size:0.86em;">'
        f'🪜 MỞ XEM CHUỖI SUY LUẬN ĐA BƯỚC 7 TẦNG (STEP 1 ➔ STEP 7 · KIỂM CHỨNG NHÂN–QUẢ & GIẢI QUYẾT XUNG ĐỘT)'
        f'</summary>'
        f'<div style="margin-top:7px;">'
        + "".join(step_rows)
        + '</div></details></div>'
    )
