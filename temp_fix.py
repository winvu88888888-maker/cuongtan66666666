import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''        auth_warnings, is_fake = self._check_authenticity(chart_data, luc_hao_data)
        
        sections = []'''

replacement1 = '''        auth_warnings, is_fake = self._check_authenticity(chart_data, luc_hao_data)
        
        auth_html = ""
        if is_fake:
            auth_html = f'<div style="background:linear-gradient(135deg,#7f1d1d,#991b1b);padding:16px;border-radius:12px;margin-bottom:16px;border:2px solid #ef4444;box-shadow:0 4px 15px rgba(239,68,68,0.4);"><div style="font-size:1.1em;font-weight:800;color:#fca5a5;margin-bottom:8px;">🚨 NGHIỆM CHỨNG TÍNH CHÂN THỰC (CẢNH BÁO)</div>'
            for w in auth_warnings:
                auth_html += f'<div style="font-size:1em;color:#fee2e2;margin-bottom:6px;">{w}</div>'
            auth_html += '</div>'

        sections = []'''

target2 = '''        if online_result:
            # V31.0: AI Online + Sơ Đồ Tương Tác
            final_parts = []'''

replacement2 = '''        if online_result:
            # V31.0: AI Online + Sơ Đồ Tương Tác
            final_parts = []
            if auth_html: final_parts.append(auth_html)'''

target3 = '''        else:
            # AI Online không khả dụng   Hiện KẾT LUẬN trực tiếp, offline chi tiết ẩn sau
            
            overall_short = 'ĐẠI CÁT'
            v_icon = '🌟'
            if weighted_pct >= 65:
                overall_short = 'ĐẠI CÁT'
                v_icon = '🌟'
            elif weighted_pct >= 55:
                overall_short = 'CÁT'
                v_icon = '✅'
            elif weighted_pct >= 45:
                overall_short = 'BÌNH'
                v_icon = '⚠️'
            elif weighted_pct >= 35:
                overall_short = 'HUNG'
                v_icon = '❌'
            else:
                overall_short = 'ĐẠI HUNG'
                v_icon = '💀'
            
            final_parts = []'''

replacement3 = '''        else:
            # AI Online không khả dụng   Hiện KẾT LUẬN trực tiếp, offline chi tiết ẩn sau
            
            overall_short = 'ĐẠI CÁT'
            v_icon = '🌟'
            if weighted_pct >= 65:
                overall_short = 'ĐẠI CÁT'
                v_icon = '🌟'
            elif weighted_pct >= 55:
                overall_short = 'CÁT'
                v_icon = '✅'
            elif weighted_pct >= 45:
                overall_short = 'BÌNH'
                v_icon = '⚠️'
            elif weighted_pct >= 35:
                overall_short = 'HUNG'
                v_icon = '❌'
            else:
                overall_short = 'ĐẠI HUNG'
                v_icon = '💀'
            
            final_parts = []
            if auth_html: final_parts.append(auth_html)'''

text = text.replace(target1, replacement1)
text = text.replace(target2, replacement2)
text = text.replace(target3, replacement3)

with open('free_ai_helper.py', 'w', encoding='utf-8') as f:
    f.write(text)
