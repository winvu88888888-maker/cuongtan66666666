# -*- coding: utf-8 -*-
"""
V128.0 — BỘ TỰ HỌC & HIỆU CHỈNH TRỌNG SỐ THỰC NGHIỆM 4 PHƯƠNG PHÁP (ADAPTIVE BAYESIAN CALIBRATION)
===================================================================================================
Tuân thủ tuyệt đối QUY TẮC 1 (BẢO MẬT TUYỆT ĐỐI):
- TUYỆT ĐỐI KHÔNG lưu câu hỏi, văn bản, thời gian cá nhân hay bất kỳ dữ liệu nhận dạng nào của người dùng.
- Chỉ lưu duy nhất ma trận hệ số toán học ẩn danh (4 con số thực trong khoảng [0.80, 1.25]) cho 4 phương pháp
  (Mai Hoa · Kỳ Môn · Lục Hào · Thiết Bản) theo mã dạng câu hỏi (D1..D25) để tự tinh chỉnh độ nhạy thực chiến.
"""

import json
import os
from typing import Dict, Any

_CALIB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "method_weights_v128.json")
_METHODS = ("mai_hoa", "ky_mon", "luc_hao", "thiet_ban")
_MIN_MULT = 0.80
_MAX_MULT = 1.25
_LR = 0.04

_MEM_STATE: Dict[str, Any] = {
    "version": "V128.0",
    "total_feedback": 0,
    "correct_feedback": 0,
    "global_mult": {m: 1.0 for m in _METHODS},
    "by_arch": {},
}
_LOADED = False


def _load_state() -> Dict[str, Any]:
    global _LOADED, _MEM_STATE
    if _LOADED:
        return _MEM_STATE
    _LOADED = True
    try:
        if os.path.isfile(_CALIB_FILE):
            with open(_CALIB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and isinstance(data.get("global_mult"), dict):
                for m in _METHODS:
                    v = float(data["global_mult"].get(m, 1.0))
                    _MEM_STATE["global_mult"][m] = max(_MIN_MULT, min(_MAX_MULT, round(v, 4)))
                _MEM_STATE["total_feedback"] = int(data.get("total_feedback", 0))
                _MEM_STATE["correct_feedback"] = int(data.get("correct_feedback", 0))
                if isinstance(data.get("by_arch"), dict):
                    clean_arch = {}
                    for ak, md in data["by_arch"].items():
                        if isinstance(ak, str) and ak.startswith("D") and len(ak) <= 32 and isinstance(md, dict):
                            clean_arch[ak] = {
                                m: max(_MIN_MULT, min(_MAX_MULT, round(float(md.get(m, 1.0)), 4)))
                                for m in _METHODS
                            }
                    _MEM_STATE["by_arch"] = clean_arch
    except Exception:
        pass
    return _MEM_STATE


def _save_state() -> None:
    """Lưu duy nhất ma trận hệ số toán học ẩn danh (0% dữ liệu câu hỏi người dùng)."""
    try:
        state = _load_state()
        safe_payload = {
            "version": "V128.0",
            "total_feedback": int(state.get("total_feedback", 0)),
            "correct_feedback": int(state.get("correct_feedback", 0)),
            "global_mult": {
                m: round(float(state["global_mult"].get(m, 1.0)), 4) for m in _METHODS
            },
            "by_arch": {
                ak: {m: round(float(mv.get(m, 1.0)), 4) for m in _METHODS}
                for ak, mv in (state.get("by_arch") or {}).items()
                if isinstance(ak, str) and ak.startswith("D")
            },
        }
        with open(_CALIB_FILE, "w", encoding="utf-8") as f:
            json.dump(safe_payload, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get_calibrated_multipliers(archetype_key: str = "") -> Dict[str, float]:
    """Trả về hệ số hiệu chỉnh thực nghiệm hiện tại của 4 phương pháp cho dạng câu hỏi."""
    state = _load_state()
    g = state.get("global_mult") or {}
    a = (state.get("by_arch") or {}).get(str(archetype_key or ""), {})
    out = {}
    for m in _METHODS:
        gm = float(g.get(m, 1.0))
        am = float(a.get(m, 1.0))
        combined = max(_MIN_MULT, min(_MAX_MULT, round(0.4 * gm + 0.6 * am if a else gm, 4)))
        out[m] = combined
    return out


def _verdict_to_score(verdict_str: str, base_pct: int = 50) -> float:
    u = str(verdict_str or "").upper()
    if "ĐẠI CÁT" in u:
        return 82.0
    if "CÁT" in u:
        return 68.0
    if "ĐẠI HUNG" in u:
        return 22.0
    if "HUNG" in u:
        return 34.0
    return float(base_pct or 50)


def apply_calibrated_weighted_pct(
    base_pct: int,
    archetype_key: str,
    mai_hoa_verdict: str = "",
    ky_mon_verdict: str = "",
    luc_hao_verdict: str = "",
    thiet_ban_verdict: str = "",
) -> int:
    """Điều chỉnh nhẹ điểm tổng hợp theo trọng số thực nghiệm đã học được của 4 phương pháp."""
    state = _load_state()
    if int(state.get("total_feedback", 0)) <= 0:
        return int(base_pct)
    mults = get_calibrated_multipliers(archetype_key)
    scores = {
        "mai_hoa": _verdict_to_score(mai_hoa_verdict, base_pct),
        "ky_mon": _verdict_to_score(ky_mon_verdict, base_pct),
        "luc_hao": _verdict_to_score(luc_hao_verdict, base_pct),
        "thiet_ban": _verdict_to_score(thiet_ban_verdict, base_pct),
    }
    base_weights = {"mai_hoa": 0.28, "luc_hao": 0.30, "ky_mon": 0.27, "thiet_ban": 0.15}
    num = sum(scores[m] * base_weights[m] * mults[m] for m in _METHODS)
    den = sum(base_weights[m] * mults[m] for m in _METHODS)
    emp_score = num / den if den > 0 else float(base_pct)
    blended = round(0.75 * float(base_pct) + 0.25 * emp_score)
    return max(15, min(95, int(blended)))


def record_empirical_feedback(
    archetype_key: str,
    verdicts: Dict[str, str],
    overall_pct: int,
    is_correct: bool,
) -> Dict[str, Any]:
    """
    Cập nhật trọng số Multiplicative-Weights cho 4 phương pháp khi người dùng xác nhận Đúng / Lệch thực tế.
    Không nhận và không lưu câu hỏi của người dùng (Bảo mật tuyệt đối).
    """
    state = _load_state()
    ak = str(archetype_key or "D0_GENERAL").strip()
    if not ak.startswith("D"):
        ak = "D0_GENERAL"
    arch_map = state["by_arch"].setdefault(ak, {m: 1.0 for m in _METHODS})

    overall_pos = int(overall_pct or 50) >= 50
    state["total_feedback"] = int(state.get("total_feedback", 0)) + 1
    if is_correct:
        state["correct_feedback"] = int(state.get("correct_feedback", 0)) + 1

    for m in _METHODS:
        v_str = str((verdicts or {}).get(m, "")).upper()
        if "CÁT" in v_str:
            m_pos = True
        elif "HUNG" in v_str:
            m_pos = False
        else:
            m_pos = overall_pos

        agreed_with_overall = (m_pos == overall_pos)
        # Nếu kết luận tổng ĐÚNG: thưởng cho phương pháp đồng thuận, giảm nhẹ phương pháp ngược chiều.
        # Nếu kết luận tổng LỆCH: thưởng cho phương pháp phản biện đúng, giảm nhẹ phương pháp dẫn sai.
        step_dir = 1.0 if (agreed_with_overall == bool(is_correct)) else -1.0

        arch_map[m] = max(_MIN_MULT, min(_MAX_MULT, round(arch_map[m] + step_dir * _LR, 4)))
        state["global_mult"][m] = max(
            _MIN_MULT,
            min(_MAX_MULT, round(state["global_mult"][m] + step_dir * (_LR * 0.5), 4)),
        )

    # Chuẩn hóa trung bình quanh 1.0 để không bị trôi tổng trọng số
    avg_a = sum(arch_map.values()) / len(_METHODS)
    if avg_a > 0:
        for m in _METHODS:
            arch_map[m] = max(_MIN_MULT, min(_MAX_MULT, round(arch_map[m] / avg_a, 4)))

    _save_state()
    return get_calibration_summary(ak)


def get_calibration_summary(archetype_key: str = "") -> Dict[str, Any]:
    state = _load_state()
    mults = get_calibrated_multipliers(archetype_key)
    total = int(state.get("total_feedback", 0))
    corr = int(state.get("correct_feedback", 0))
    acc_pct = round(100.0 * corr / total, 1) if total > 0 else 0.0
    labels = {
        "mai_hoa": f"Mai Hoa ×{mults['mai_hoa']:.2f}",
        "luc_hao": f"Lục Hào ×{mults['luc_hao']:.2f}",
        "ky_mon": f"Kỳ Môn ×{mults['ky_mon']:.2f}",
        "thiet_ban": f"Thiết Bản ×{mults['thiet_ban']:.2f}",
    }
    return {
        "total_feedback": total,
        "correct_feedback": corr,
        "accuracy_pct": acc_pct,
        "multipliers": mults,
        "badge_str": " · ".join(labels.values()),
    }
