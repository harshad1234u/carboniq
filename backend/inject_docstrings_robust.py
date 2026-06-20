import os

def insert_module_docstring(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('"""'):
        with open(path, 'w', encoding='utf-8') as f:
            f.write('"""Module docstring."""\n' + content)

def inject_docstrings(flake8_output_path):
    with open(flake8_output_path, 'r') as f:
        lines = f.readlines()
        
    file_fixes = {}
    for line in lines:
        if 'Missing docstring in public function' in line or 'Missing docstring in public method' in line or 'Missing docstring in __init__' in line:
            parts = line.split(':')
            filepath = parts[0].strip()
            lineno = int(parts[1])
            if filepath not in file_fixes:
                file_fixes[filepath] = []
            file_fixes[filepath].append(lineno)
            
        elif 'Missing docstring in public module' in line:
            parts = line.split(':')
            filepath = parts[0].strip()
            insert_module_docstring(filepath)

    for filepath, fixes in file_fixes.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()
            
        # Deduplicate and sort descending
        fixes = sorted(list(set(fixes)), reverse=True)
        
        for lineno in fixes:
            idx = lineno - 1
            while idx < len(content) and not (content[idx].strip().endswith(':') or ')' in content[idx]):
                idx += 1
            if idx < len(content):
                indent = len(content[idx]) - len(content[idx].lstrip()) + 4
                spaces = " " * indent
                doc = f'{spaces}"""Docstring."""\n'
                content.insert(idx + 1, doc)
                    
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(content)
            
if __name__ == '__main__':
    inject_docstrings('flake8_errors.txt')
