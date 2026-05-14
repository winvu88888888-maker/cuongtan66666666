import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    text = f.read()

target_remove = '''        auth_warnings, is_fake = self._check_authenticity(chart_data, luc_hao_data)
        
        auth_html = ""
        if is_fake:
            auth_html = f'<div style="background:linear-gradient(135deg,#7f1d1d,#991b1b);padding:16px;border-radius:12px;margin-bottom:16px;border:2px solid #ef4444;box-shadow:0 4px 15px rgba(239,68,68,0.4);"><div style="font-size:1.1em;font-weight:800;color:#fca5a5;margin-bottom:8px;">🚨 NGHIỆM CHỨNG TÍNH CHÂN THỰC (CẢNH BÁO)</div>'
            for w in auth_warnings:
                auth_html += f'<div style="font-size:1em;color:#fee2e2;margin-bottom:6px;">{w}</div>'
            auth_html += '</div>'

'''

target_inject = '''                if parser_dt:
                    if parser_dt != dung_than:
                        self.log_step("V42.9.12 DT Fix", "OVERRIDE", f"Regex DT: {dung_than} -> Parser DT: {parser_dt} ({reason[:60]})")
                        dung_than = parser_dt
                    else:
                        self.log_step("V32.5 Grammar", "INFO", 
                                      f"Parser suggest: {parser_dt} | V35.8 final: {dung_than} | {reason[:60]}")'''

replacement_inject = '''                if parser_dt:
                    if parser_dt != dung_than:
                        self.log_step("V42.9.12 DT Fix", "OVERRIDE", f"Regex DT: {dung_than} -> Parser DT: {parser_dt} ({reason[:60]})")
                        dung_than = parser_dt
                    else:
                        self.log_step("V32.5 Grammar", "INFO", 
                                      f"Parser suggest: {parser_dt} | V35.8 final: {dung_than} | {reason[:60]}")
                
                # V42.9.15: Authenticity Check with Dung Than
                auth_warnings, is_fake = self._check_authenticity(chart_data, luc_hao_data, dung_than=dung_than)
                auth_html = ""
                if is_fake:
                    auth_html = f'<div style="background:linear-gradient(135deg,#7f1d1d,#991b1b);padding:16px;border-radius:12px;margin-bottom:16px;border:2px solid #ef4444;box-shadow:0 4px 15px rgba(239,68,68,0.4);"><div style="font-size:1.1em;font-weight:800;color:#fca5a5;margin-bottom:8px;">🚨 NGHIỆM CHỨNG TÍNH CHÂN THỰC (CẢNH BÁO)</div>'
                    for w in auth_warnings:
                        auth_html += f'<div style="font-size:1em;color:#fee2e2;margin-bottom:6px;">{w}</div>'
                    auth_html += '</div>'
'''

if target_remove in text and target_inject in text:
    text = text.replace(target_remove, '')
    text = text.replace(target_inject, replacement_inject)
    with open('free_ai_helper.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('SUCCESS')
else:
    print('NOT FOUND target_remove:', target_remove in text)
    print('NOT FOUND target_inject:', target_inject in text)
