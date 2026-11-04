# -*- coding: utf-8 -*-
"""Replace V33.0 → V34.0 across all relevant files."""
import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')

base = os.path.dirname(__file__)
files_to_update = [
    'free_ai_helper.py',
    'interaction_diagrams.py',
    'app.py',
]

total_replaced = 0
for fname in files_to_update:
    fpath = os.path.join(base, fname)
    if not os.path.exists(fpath):
        print(f"⚪ {fname}: not found, skip")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = content.count('V33.0') + content.count('V33')
    
    # Replace version strings
    new_content = content.replace('V33.0', 'V34.0')
    new_content = new_content.replace('V33.1', 'V34.0')
    new_content = new_content.replace('V33', 'V34')
    
    # Count actual replacements
    actual = content.count('V33.0') + content.count('V33.1') + content.count('V33')
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ {fname}: {actual} replacements")
        total_replaced += actual
    else:
        print(f"⚪ {fname}: no changes")

print(f"\n✅ Total: {total_replaced} replacements across {len(files_to_update)} files")
