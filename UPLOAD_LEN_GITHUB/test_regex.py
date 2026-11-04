import re

_s = """
<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);padding:22px;border-radius:14px;border-left:6px solid #22c55e;margin:12px 0;">
<span style="font-size:1.3em;font-weight:900;color:#c4b5fd;">🔮 PHÂN TÍCH VẠN VẬT: "nhà tôi có mấy anh chị em , các anh chị em tôi đang làm nghề gì , bao nhiêu tuổi"</span><br><br>
<span style="font-size:1.15em;font-weight:800;color:#22c55e;">📦 Hành Hỏa → 🔥 ĐIỆN TỬ, công nghệ, ánh sáng</span><br><br>
<span style="color:#e2e8f0;font-size:1.05em;">
- <b>Lĩnh vực (DT Huynh Đệ):</b> ANH EM, BẠN BÈ<br>
</span><br><br>
<span style="color:#22c55e;font-weight:700;">📊 Mức chất lượng: TRUNG BÌNH (51%)</span>
</div>
"""

_s_spaced = _s.replace('<br>', ' ').replace('</div>', ' ')
_clean_s = re.sub(r'<[^>]+>', '', _s_spaced)
_ans = _clean_s.replace('**', '').replace('#', '').strip()
if 'CÂU TRẢ LỜI:' in _ans: _ans = _ans.replace('CÂU TRẢ LỜI:', '').strip()
print('ANS:')
print(_ans)
