import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        try:
            v31_parsed_questions = v32_parse_question(question)
            print("DEBUG: v31_parsed_questions=", v31_parsed_questions)'''
replacement = '''        try:
            v31_parsed_questions = v32_parse_question(question)'''
text = text.replace(target, replacement)

target2 = '''            # V42.9.15: Authenticity Check with Dung Than
            print("DEBUG: Call _check_authenticity with dung_than=", dung_than)
            auth_warnings, is_fake = self._check_authenticity(chart_data, luc_hao_data, dung_than=dung_than)'''
replacement2 = '''            # V42.9.15: Authenticity Check with Dung Than
            auth_warnings, is_fake = self._check_authenticity(chart_data, luc_hao_data, dung_than=dung_than)'''
text = text.replace(target2, replacement2)

target3 = '''        except Exception as e:
            import traceback
            traceback.print_exc()
            self.log_step("V32.5 Grammar", "ERROR", str(e)[:80])'''
replacement3 = '''        except Exception as e:
            self.log_step("V32.5 Grammar", "ERROR", str(e)[:80])'''
text = text.replace(target3, replacement3)

with open('free_ai_helper.py', 'w', encoding='utf-8') as f:
    f.write(text)
