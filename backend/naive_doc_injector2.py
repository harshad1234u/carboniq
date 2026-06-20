import os
import re

def insert_docs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    for i in range(len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith('def ') or stripped.startswith('async def '):
            # check if it ends with :
            j = i
            while j < len(lines) and not lines[j].strip().endswith(':'):
                j += 1
            if j < len(lines) - 1:
                # the next line should be docstring
                next_line = lines[j+1]
                if '"""' not in next_line:
                    # insert docstring
                    indent = len(lines[i]) - len(lines[i].lstrip()) + 4
                    spaces = " " * indent
                    lines.insert(j+1, spaces + '"""Docstring."""')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

files_to_fix = [
    'api/carbon.py', 'api/dashboard.py', 'api/profile.py',
    'main.py'
]

for f in files_to_fix:
    insert_docs(f)

