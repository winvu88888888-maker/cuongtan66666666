# -*- coding: utf-8 -*-
"""Scan all version numbers in free_ai_helper.py"""
import re
from collections import Counter

with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Find all V version numbers
versions = re.findall(r'V(\d+\.?\d*[a-z]?)', content)
vc = Counter(versions)

def ver_key(v):
    parts = v.rstrip('abcdefgh').split('.')
    try:
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
        suffix = v[len('.'.join(parts)):]
        return (major, minor, suffix)
    except:
        return (0, 0, v)

sorted_versions = sorted(vc.items(), key=lambda x: ver_key(x[0]), reverse=True)

print('=== TOP 30 VERSION REFERENCES ===')
for v, count in sorted_versions[:30]:
    print(f'  V{v}: {count}x')

print(f'\nHIGHEST VERSION: V{sorted_versions[0][0]}')
print(f'Total unique versions: {len(vc)}')

# Find version numbers in USER-VISIBLE output (headers, titles shown to user)
print('\n=== VERSIONS IN USER-VISIBLE OUTPUT ===')
for i, line in enumerate(lines, 1):
    # Lines that append to output
    if 'append' in line or 'final_parts' in line:
        m = re.search(r'V\d+\.?\d*[a-z]?', line)
        if m:
            ver = m.group()
            snippet = line.strip()[:150]
            print(f'  Line {i}: {ver} — {snippet}')

# Find version numbers in docstrings/titles at top
print('\n=== VERSION IN FILE HEADER ===')
for i in range(min(15, len(lines))):
    m = re.search(r'V\d+\.?\d*[a-z]?', lines[i])
    if m:
        print(f'  Line {i+1}: {m.group()} — {lines[i].strip()[:120]}')
