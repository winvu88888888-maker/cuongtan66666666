import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('            if auth_html: final_parts.append(auth_html)\n', '')

target = '            return "\\n".join(final_parts)'
replacement = '''            if auth_html: final_parts.insert(0, auth_html)
            return "\\n".join(final_parts)'''

text = text.replace(target, replacement)

with open('free_ai_helper.py', 'w', encoding='utf-8') as f:
    f.write(text)
