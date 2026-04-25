# -*- coding: utf-8 -*-
"""V42.9: Fix output — remove duplicates, clean competition, hide VẠN VẬT for competition"""

with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lines 12928 to 13146 (1-indexed) = 12927 to 13145 (0-indexed)
# This is the entire offline-only output assembly section

new_block = r'''            if not _offline_short_answer:
                # V42.9: SMART HEADER — detect loại câu hỏi để trả lời đúng kiểu
                _q_lower_off2 = question.lower()
                _is_competition_off = _is_competition_question(question)
                _is_what_off2 = any(k in _q_lower_off2 for k in ['cái gì', 'loại gì', 'sản xuất gì', 'làm gì', 'sản phẩm gì',
                    'buôn bán gì', 'kinh doanh gì', 'nghề gì', 'ngành gì', 'gì vậy', 'gì đây',
                    'bán gì', 'trồng gì', 'nuôi gì', 'mua gì', 'bằng gì', 'sản xuất cái'])
                _is_where_off2 = any(k in _q_lower_off2 for k in ['ở đâu', 'hướng nào', 'phương nào', 'chỗ nào', 'nơi nào'])
                _is_when_off2 = any(k in _q_lower_off2 for k in ['khi nào', 'bao giờ', 'lúc nào', 'thời điểm'])
                
                if _is_competition_off:
                    # V42.9: COMPETITION — Extract kết quả thắng/thua
                    _side_a, _side_b = _extract_two_sides(question)
                    # Tính điểm Thế vs Ứng từ Lục Hào factors
                    _the_score = 0
                    _ung_score = 0
                    for _f in (v23_lh_factors or []):
                        if '+' in str(_f):
                            try:
                                import re as _re_comp
                                _m = _re_comp.search(r'\+(\d+)', str(_f))
                                if _m: _the_score += int(_m.group(1))
                            except: _the_score += 3
                        elif '-' in str(_f):
                            try:
                                import re as _re_comp2
                                _m2 = _re_comp2.search(r'-(\d+)', str(_f))
                                if _m2: _ung_score += int(_m2.group(1))
                            except: _ung_score += 3
                    
                    _net = _the_score - _ung_score
                    if _net > 3:
                        _offline_short_answer = f"⚽ {_side_a} THẮNG ✅ (Chênh: +{_net})"
                    elif _net < -3:
                        _offline_short_answer = f"⚽ {_side_b} THẮNG ✅ (Chênh: {_net})"
                    else:
                        _offline_short_answer = f"⚽ HÒA ⚖️ — {_side_a} ≈ {_side_b} (Chênh: {_net:+d})"
                elif _is_what_off2:
                    _LT_HANH_OFF3 = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc'}
                    _hanh_off3 = _LT_HANH_OFF3.get(dung_than, 'Thổ')
                    _HANH_SP2 = {'Kim': 'Kim loại/Máy móc/Linh kiện', 'Mộc': 'Gỗ/Vải/Nông sản/Giấy', 
                                 'Thủy': 'Nước/Chất lỏng/Hải sản/Hóa chất', 'Hỏa': 'Điện tử/Năng lượng/Thực phẩm', 
                                 'Thổ': 'Gạch/Gốm sứ/Vật liệu XD/Nông sản'}
                    _offline_short_answer = f"🔮 Hành {_hanh_off3}: {_HANH_SP2.get(_hanh_off3, '?')} ({weighted_pct}%)"
                elif _is_where_off2:
                    _LT_HANH_OFF4 = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc'}
                    _hanh_off4 = _LT_HANH_OFF4.get(dung_than, 'Thổ')
                    _HANH_HUONG2 = {'Kim': 'HƯỚNG TÂY', 'Mộc': 'HƯỚNG ĐÔNG', 'Thủy': 'HƯỚNG BẮC', 'Hỏa': 'HƯỚNG NAM', 'Thổ': 'TRUNG TÂM'}
                    _offline_short_answer = f"🧭 {_HANH_HUONG2.get(_hanh_off4, '?')} (Hành {_hanh_off4}) — {weighted_pct}%"
                elif _is_when_off2:
                    try:
                        from xem_ngay_dep import _jdn as _jdn_h2
                        import datetime as _dt_h2
                        _LT2 = {'Quan Quỷ': 'Kim', 'Thê Tài': 'Thổ', 'Tử Tôn': 'Hỏa', 'Phụ Mẫu': 'Thủy', 'Huynh Đệ': 'Mộc', 'Bản Thân': 'Thổ'}
                        _h2 = _LT2.get(dung_than, 'Thổ')
                        _UKC2 = {'Kim': [8,9], 'Mộc': [2,3], 'Thủy': [0,11], 'Hỏa': [6,5], 'Thổ': [4,10,1,7]}
                        _SINH2 = {'Kim': 'Thổ', 'Mộc': 'Thủy', 'Thủy': 'Kim', 'Hỏa': 'Mộc', 'Thổ': 'Hỏa'}
                        _tc2 = _UKC2.get(_h2, [4]) if weighted_pct >= 55 else _UKC2.get(_SINH2.get(_h2, 'Thổ'), [4])
                        _CHIS2 = ['Tý','Sửu','Dần','Mão','Thìn','Tị','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi']
                        _CANS2 = ['Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Quý']
                        _CGW2 = {'Tý':'23h-1h','Sửu':'1h-3h','Dần':'3h-5h','Mão':'5h-7h','Thìn':'7h-9h','Tị':'9h-11h',
                                 'Ngọ':'11h-13h','Mùi':'13h-15h','Thân':'15h-17h','Dậu':'17h-19h','Tuất':'19h-21h','Hợi':'21h-23h'}
                        _td2 = _dt_h2.date.today()
                        _nd2 = None
                        for _o2 in range(1, 200):
                            _dd2 = _td2 + _dt_h2.timedelta(days=_o2)
                            _jj2 = _jdn_h2(_dd2.day, _dd2.month, _dd2.year)
                            _cc2 = (_jj2 + 1) % 12
                            if _cc2 in _tc2:
                                _cn2 = _CANS2[(_jj2 + 9) % 10]
                                _chn2 = _CHIS2[_cc2]
                                _TW2 = ['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật']
                                _tw2 = _TW2[_dd2.weekday()]
                                _gt2 = _CGW2.get(_chn2, '')
                                _nd2 = f"📆 {_dd2.day:02d}/{_dd2.month:02d}/{_dd2.year} ({_tw2}) lúc {_gt2} — ngày {_cn2} {_chn2} (còn {_o2} ngày)"
                                break
                        _offline_short_answer = _nd2 or f"⏳ Xem Ứng Kỳ chi tiết bên dưới ({weighted_pct}%)"
                    except Exception:
                        _offline_short_answer = f"⏳ Xem Ứng Kỳ chi tiết bên dưới ({weighted_pct}%)"
                elif overall_short in ('CÁT', 'ĐẠI CÁT'):
                    _offline_short_answer = f"{v_icon} CÓ — THUẬN LỢI ({weighted_pct}%)"
                elif overall_short in ('HUNG', 'ĐẠI HUNG'):
                    _offline_short_answer = f"{v_icon} KHÔNG — BẤT LỢI ({weighted_pct}%)"
                else:
                    _offline_short_answer = f"{v_icon} CẦN CÂN NHẮC — {overall_short} ({weighted_pct}%)"
            
            # === V42.0: CẢNH BÁO PHẢN/PHỤC NGÂM ===
            try:
                _ppn_warning = _build_phan_phuc_ngam_warning(chart_data, luc_hao_data)
                if _ppn_warning:
                    final_parts.append(_ppn_warning)
            except Exception:
                pass
            
            # === V42.1: CẢNH BÁO NGUYỆT PHÁ ===
            try:
                _lh_dt_chi_np2 = ''
                _lh_chi_thang_np2 = ''
                if luc_hao_data:
                    _lh_haos_np2 = luc_hao_data.get('ban', {}).get('haos', luc_hao_data.get('haos', []))
                    _lh_chi_thang_np2 = luc_hao_data.get('chi_thang', '')
                    if _lh_haos_np2 and dung_than:
                        for _h_np2 in _lh_haos_np2:
                            if _h_np2.get('luc_than', '') == dung_than:
                                _lh_dt_chi_np2 = _h_np2.get('chi', '')
                                break
                    if _lh_dt_chi_np2 and _lh_chi_thang_np2:
                        _, _np_html_offline = _build_nguyet_pha_warning(
                            _lh_dt_chi_np2, _lh_chi_thang_np2,
                            dung_than_name=dung_than or 'Dụng Thần'
                        )
                        if _np_html_offline:
                            final_parts.append(_np_html_offline)
            except Exception:
                pass
            
            # ═══════════════════════════════════════════════════════════
            # V42.9: Ô XANH LÁ — KẾT LUẬN AI OFFLINE (DUY NHẤT)
            # ═══════════════════════════════════════════════════════════
            _evidence_html = ""
            if _offline_evidence:
                _evidence_html = '<div style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.2);">'
                for _ev in _offline_evidence:
                    _evidence_html += f'<div style="font-size:1em;color:#d1fae5;margin:4px 0;">{_ev}</div>'
                _evidence_html += '</div>'
            
            # V42.9: Competition → thêm chi tiết 2 đội vào header
            _comp_detail_html = ""
            _is_comp_final = _is_competition_question(question)
            if _is_comp_final:
                _sa, _sb = _extract_two_sides(question)
                _comp_detail_html = (
                    f'<div style="margin-top:14px;padding:14px;background:rgba(0,0,0,0.2);border-radius:10px;">'
                    f'<div style="font-size:1.15em;color:#6ee7b7;font-weight:700;margin-bottom:8px;">📊 Phương pháp: Thế vs Ứng</div>'
                    f'<div style="color:#d1fae5;font-size:1.05em;">• Lục Hào: Thế = {_sa}, Ứng = {_sb}</div>'
                    f'<div style="color:#d1fae5;font-size:1.05em;">• Kỳ Môn: Nhật Can (Chủ = {_sa}), Thời Can (Khách = {_sb})</div>'
                    f'<div style="color:#d1fae5;font-size:1.05em;">• Mai Hoa: Thể Quái = {_sa}, Dụng Quái = {_sb}</div>'
                    f'</div>'
                )
            
            final_parts.append(
                f'<div style="background:linear-gradient(135deg,#064e3b,#065f46);padding:28px;border-radius:16px;margin:16px 0;border:3px solid #34d399;box-shadow:0 4px 25px rgba(52,211,153,0.4);">'
                f'<div style="font-size:1.2em;font-weight:700;color:#6ee7b7;margin-bottom:10px;">🖥️ KẾT LUẬN AI OFFLINE — THIÊN CƠ ĐẠI SƯ V42.9</div>'
                f'<div style="font-size:2em;font-weight:900;color:#ffffff;line-height:1.3;margin-bottom:8px;">{_offline_short_answer}</div>'
                f'<div style="font-size:1.05em;color:#a7f3d0;">📊 Điểm: <b>{weighted_pct}%</b> | DT: <b>{dung_than}</b> | KM: {ky_mon_verdict} | LH: {luc_hao_verdict} | MH: {mai_hoa_verdict}</div>'
                + _comp_detail_html
                + _evidence_html
                + f'</div>'
            )
            final_parts.append("")
            
            # ═══════════════════════════════════════════════════════════
            # V42.9: 1 COLLAPSE DUY NHẤT — TẤT CẢ chi tiết
            # KHÔNG có section nào hiển thị bên ngoài collapse
            # ═══════════════════════════════════════════════════════════
            final_parts.append("\n<details>")
            final_parts.append(f"<summary><b>📖 XEM CHI TIẾT PHÂN TÍCH AI OFFLINE (nhấn để mở)</b></summary>\n")
            
            # 1. Protocol 27 bước (NẾU CÓ)
            if v38_protocol_text:
                final_parts.append(v38_protocol_text)
            else:
                final_parts.append(f"## {v_icon} KẾT LUẬN: {overall_short} (Điểm Tổng Hợp: {weighted_pct}%)")
            
            # 2. Thám tử kiểm chứng + Câu trả lời
            if direct_answer:
                final_parts.append(f"\n### 🔍 THÁM TỬ KIỂM CHỨNG + CÂU TRẢ LỜI")
                final_parts.append(direct_answer)
            
            # 3. VẠN VẬT CỤ THỂ (CHỈ cho câu hỏi KHÔNG PHẢI competition)
            if not _is_comp_final:
                vv_cu_the_kl = _get_van_vat_cu_the(hanh_dt_v22, unified_v22.get('tier_key', 'TRUNG_BÌNH') if unified_v22 else 'TRUNG_BÌNH')
                if vv_cu_the_kl and hanh_dt_v22:
                    final_parts.append(f"\n### 🎯 VẠN VẬT CỤ THỂ ({hanh_dt_v22} × {unified_v22['tier_data']['cap'] if unified_v22 else '?'})")
                    final_parts.append(f"- 🔮 **Đồ vật:** {vv_cu_the_kl.get('do_vat', '?')}")
                    final_parts.append(f"- 🏠 **Nhà cửa:** {vv_cu_the_kl.get('nha_cua', '?')}")
                    final_parts.append(f"- 🧑 **Người:** {vv_cu_the_kl.get('nguoi', '?')}")
                    final_parts.append(f"- 🏥 **Bệnh:** {vv_cu_the_kl.get('benh', '?')}")
            
            # 4. V31 Sơ đồ Master
            if v31_master_diagram:
                final_parts.append(f"\n### 🏆 SĐ MASTER: DỤNG THẦN → SUY VƯỢNG → VẠN VẬT")
                final_parts.append(f"```")
                final_parts.append(v31_master_diagram)
                final_parts.append(f"```")
                final_parts.append(f"**📊 CÔNG THỨC:** {v31_master_info.get('formula_detail', '?')}")
                final_parts.append(f"**🎯 KẾT LUẬN MASTER:** {v31_master_info.get('conclusion', '?')}")
            
            # 5. V31 Sơ đồ câu hỏi
            if v31_question_diagram and v31_diagram_id != 'SD0':
                final_parts.append(f"\n### 📐 CHÚ GIẢI: {v31_question_info.get('diagram_name', 'Sơ Đồ')}")
                final_parts.append(f"```")
                final_parts.append(v31_question_diagram)
                final_parts.append(f"```")
                final_parts.append(f"**📊 CÔNG THỨC:** {v31_question_info.get('formula', '?')}")
                final_parts.append(f"**🎯 KẾT LUẬN:** {v31_question_info.get('conclusion', '?')}")
            
            # 6. V32.5: Sơ đồ tương tác 6PP
            try:
                v325_interaction = self._build_factor_interaction_map(
                    chart_data=chart_data,
                    luc_hao_data=luc_hao_data,
                    mai_hoa_data=mai_hoa_data,
                    dung_than=dung_than,
                    hanh_dt=hanh_dt_v22,
                    question=question,
                    km_verdict=ky_mon_verdict or 'BÌNH',
                    lh_verdict=luc_hao_verdict or 'BÌNH',
                    mh_verdict=mai_hoa_verdict or 'BÌNH',
                    ln_verdict=luc_nham_verdict or 'BÌNH',
                    ta_verdict=thai_at_verdict or 'BÌNH'
                )
                if v325_interaction:
                    final_parts.append("\n### 🔮 SƠ ĐỒ TƯƠNG TÁC 6PP CHI TIẾT")
                    final_parts.append(v325_interaction)
            except Exception as e:
                self.log_step("V32.5", "INTERACTION_ERR", str(e)[:100])
            
            # 7. Thống kê yếu tố
            all_factors = v24_km_factors + v23_lh_factors + v24_mh_factors + v24_tb_factors + v24_ln_factors + v24_ta_factors
            if all_factors:
                final_parts.append(f"\n### 📋 THỐNG KÊ CHI TIẾT CÁC YẾU TỐ ({len(all_factors)})")
                for f in all_factors:
                    if '+' in f:
                        final_parts.append(f"- ✅ **THUẬN LỢI:** {f}")
                    elif '-' in f:
                        final_parts.append(f"- ⚠️ **BẤT LỢI:** {f}")
                    else:
                        final_parts.append(f"- ℹ️ **THÔNG TIN:** {f}")
            
            # 8. V26.2: Full offline output (gốc)
            if offline_full_output:
                final_parts.append("\n---")
                final_parts.append(offline_full_output)
            
            final_parts.append("\n</details>")
            final_parts.append(f"\n💡 Để dùng AI thông minh hơn, nhập API Key tại [Google AI Studio](https://aistudio.google.com/).")
            return "\n".join(final_parts)
'''

# Build new lines
before = lines[:12927]  # Lines 1-12927 (0-indexed 0-12926)
after = lines[13146:]   # Lines 13147+ (0-indexed 13146+)

new_lines = before + [new_block + '\n'] + after

print(f"Original: {len(lines)} lines")
print(f"New: {len(new_lines)} lines")
print(f"Removed: {13146 - 12927} lines from original")
print(f"Added: {new_block.count(chr(10))} lines of new code")

with open('free_ai_helper.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ DONE — file saved!")
