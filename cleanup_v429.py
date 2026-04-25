# -*- coding: utf-8 -*-
"""V42.9 CLEANUP: Loại bỏ trùng lặp triệt để trong output pipeline

PHÁT HIỆN:
1. direct_answer nằm TRONG offline_full_output (line 12337-12338)
   → Khi collapse gom cả 2 → direct_answer xuất hiện 2 LẦN
   
2. v38_protocol_text có VẠN VẬT + Ứng Kỳ + CHUỖI BẰNG CHỨNG
   offline_full_output CŨNG CÓ VẠN VẬT + Ứng Kỳ + CHUỖI BẰNG CHỨNG
   → Trùng lặp

FIX:
1. Bỏ direct_answer khỏi sections[] → offline_full_output không chứa THÁM TỬ nữa
2. Bỏ KẾT LUẬN THỐNG NHẤT khỏi sections[] → đã có trong v38_protocol_text
3. Output collapse = v38_protocol_text (CHÍNH) + offline_full_output (CHI TIẾT 5PP)
   → Không cần direct_answer riêng vì v38 đã có phần KẾT LUẬN + THÁM TỬ
"""
import re

with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

changes = 0

# ═══ FIX 1: Bỏ direct_answer khỏi sections[] ═══
# Line 12335-12338: sections.append THÁM TỬ + direct_answer
# → Loại bỏ để offline_full_output không chứa THÁM TỬ (đã có trong v38)
old_block = '''        # V34.7: HIỂN THỊ direct_answer (Thám Tử + Câu trả lời linh hoạt)
        if direct_answer:
            sections.append(f"\\n### 🔍 THÁM TỬ KIỂM CHỨNG + CÂU TRẢ LỜI")
            sections.append(direct_answer)'''

new_block = '''        # V42.9: direct_answer KHÔNG gom vào sections nữa
        # → Tránh trùng lặp khi offline_full_output + v38 cùng hiện trong collapse
        # direct_answer sẽ được sử dụng riêng trong output assembly'''

if old_block in content:
    content = content.replace(old_block, new_block)
    changes += 1
    print(f"✅ FIX 1: Bỏ direct_answer khỏi sections[] (tránh trùng trong offline_full_output)")
else:
    print(f"❌ FIX 1: Không tìm thấy block cần thay")

# ═══ FIX 2: Bỏ KẾT LUẬN THỐNG NHẤT khỏi sections[] ═══
# Line 12343: sections.append "KẾT LUẬN THỐNG NHẤT" + unified_narrative
# → Đã có trong v38_protocol_text (phần V. KẾT LUẬN CHÍNH THỨC)
old_ket_luan = '''        # ========================================
        # KẾT LUẬN THỐNG NHẤT (V11.0)
        # ========================================
        sections.append(f"\\n### 🏆 KẾT LUẬN THỐNG NHẤT")
        
        unified_narrative = self._build_unified_narrative(
            question=question,
            dung_than=dung_than,
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            ky_mon_verdict=ky_mon_verdict,
            luc_hao_verdict=luc_hao_verdict,
            mai_hoa_verdict=mai_hoa_verdict,
            ky_mon_reason=ky_mon_reason,
            luc_hao_reason=luc_hao_reason,
            mai_hoa_reason=mai_hoa_reason,
            impact_evidence=impact_evidence,
            luc_nham_verdict=luc_nham_verdict,
            luc_nham_reason=luc_nham_reason,
            thai_at_verdict=thai_at_verdict,
            thai_at_reason=thai_at_reason,
            final_pct=weighted_pct,
            lh_factors=v23_lh_factors,
            km_factors=v24_km_factors,
            mh_factors=v24_mh_factors
        )
        sections.append(unified_narrative)'''

new_ket_luan = '''        # V42.9: KẾT LUẬN THỐNG NHẤT đã được tính trong v38_protocol_text
        # (phần V. KẾT LUẬN CHÍNH THỨC) → không cần duplicate ở đây
        unified_narrative = self._build_unified_narrative(
            question=question,
            dung_than=dung_than,
            chart_data=chart_data,
            luc_hao_data=luc_hao_data,
            mai_hoa_data=mai_hoa_data,
            ky_mon_verdict=ky_mon_verdict,
            luc_hao_verdict=luc_hao_verdict,
            mai_hoa_verdict=mai_hoa_verdict,
            ky_mon_reason=ky_mon_reason,
            luc_hao_reason=luc_hao_reason,
            mai_hoa_reason=mai_hoa_reason,
            impact_evidence=impact_evidence,
            luc_nham_verdict=luc_nham_verdict,
            luc_nham_reason=luc_nham_reason,
            thai_at_verdict=thai_at_verdict,
            thai_at_reason=thai_at_reason,
            final_pct=weighted_pct,
            lh_factors=v23_lh_factors,
            km_factors=v24_km_factors,
            mh_factors=v24_mh_factors
        )
        # unified_narrative vẫn tính nhưng KHÔNG append vào sections
        # → Dùng cho offline_analysis_data gửi AI Online'''

if old_ket_luan in content:
    content = content.replace(old_ket_luan, new_ket_luan)
    changes += 1
    print(f"✅ FIX 2: Bỏ KẾT LUẬN THỐNG NHẤT duplicate khỏi sections[]")
else:
    print(f"❌ FIX 2: Không tìm thấy block KẾT LUẬN THỐNG NHẤT")

# ═══ FIX 3: Trong OFFLINE-ONLY output, bỏ direct_answer riêng (đã có trong v38) ═══
# Tìm block trong offline-only collapse assembly
old_offline_da = '''            # 2. Thám tử kiểm chứng + Câu trả lời
            if direct_answer:
                final_parts.append(f"\\n### 🔍 THÁM TỬ KIỂM CHỨNG + CÂU TRẢ LỜI")
                final_parts.append(direct_answer)'''

new_offline_da = '''            # V42.9: THÁM TỬ đã nằm trong offline_full_output
            # KHÔNG append direct_answer riêng → tránh trùng lặp'''

if old_offline_da in content:
    content = content.replace(old_offline_da, new_offline_da)
    changes += 1
    print(f"✅ FIX 3: Bỏ direct_answer riêng trong offline-only collapse")
else:
    print(f"❌ FIX 3: Không tìm thấy direct_answer trong offline-only collapse")

# ═══ FIX 4: Trong ONLINE flow collapse, bỏ direct_answer riêng ═══
old_online_da = '''            if direct_answer:
                final_parts.append(f"\\n### 🔍 THÁM TỬ KIỂM CHỨNG + CÂU TRẢ LỜI")
                final_parts.append(direct_answer)
            # V42.9 FIX: LUÔN include offline_full_output'''

new_online_da = '''            # V42.9: THÁM TỬ đã nằm trong offline_full_output → không append riêng
            # V42.9 FIX: LUÔN include offline_full_output'''

if old_online_da in content:
    content = content.replace(old_online_da, new_online_da)
    changes += 1
    print(f"✅ FIX 4: Bỏ direct_answer riêng trong online flow collapse")
else:
    print(f"❌ FIX 4: Không tìm thấy direct_answer trong online collapse")

# Save
with open('free_ai_helper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'='*60}")
print(f"Tổng: {changes} thay đổi đã áp dụng")
print(f"{'='*60}")
