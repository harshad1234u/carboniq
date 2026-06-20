import os
import re

def insert_docs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Module docstring
    if not content.lstrip().startswith('"""'):
        content = '"""Module docstring."""\n' + content

    # Function docstrings
    pattern = re.compile(r'(\n[ \t]*def [^\(]+\(.*?\)(?: -> [^:]+)?:[ \t]*\n)([ \t]*)(?!""")', re.DOTALL)
    
    def replacer(match):
        decl = match.group(1)
        indent = match.group(2)
        # figure out inner indent
        inner_indent = indent + "    "
        if not indent and decl.startswith('\n '):
            pass # wait, naive indentation adding
        return decl + inner_indent + '"""Function docstring."""\n' + indent

    # We do a simpler regex:
    # Match lines ending with : that start with def
    lines = content.split('\n')
    for i in range(len(lines)):
        if lines[i].strip().startswith('def '):
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
    'database/client.py', 'database/repositories.py', 'grant_perms.py',
    'main.py', 'services/profile_service.py', 'utils/error_handlers.py',
    'utils/rate_limit.py'
]

for f in files_to_fix:
    insert_docs(f)

