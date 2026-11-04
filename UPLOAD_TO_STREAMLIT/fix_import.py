import os
p = os.path.join(os.path.dirname(__file__), 'app.py')
with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    stripped = line.rstrip('\r\n')
    if 'try:\\r\\n' in stripped and 'from google import genai' in stripped:
        # Replace this broken line with proper multiline
        new_lines.append('try:\n')
        new_lines.append('    from google import genai\n')
        new_lines.append('except ImportError:\n')
        new_lines.append('    genai = None\n')
    else:
        new_lines.append(line)

with open(p, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("FIXED!")
