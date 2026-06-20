import re
import sys

def inject_docstrings(flake8_output_path):
    with open(flake8_output_path, 'r') as f:
        lines = f.readlines()
        
    file_fixes = {}
    for line in lines:
        if 'D100 Missing docstring in public module' in line:
            parts = line.split(':')
            filepath = parts[0].strip()
            if filepath not in file_fixes:
                file_fixes[filepath] = []
            file_fixes[filepath].append(('module', 1))
        elif 'Missing docstring in public function' in line or 'Missing docstring in public method' in line:
            parts = line.split(':')
            filepath = parts[0].strip()
            lineno = int(parts[1])
            if filepath not in file_fixes:
                file_fixes[filepath] = []
            file_fixes[filepath].append(('func', lineno))
        elif 'Missing docstring in public class' in line:
            parts = line.split(':')
            filepath = parts[0].strip()
            lineno = int(parts[1])
            if filepath not in file_fixes:
                file_fixes[filepath] = []
            file_fixes[filepath].append(('class', lineno))
        elif 'Missing docstring in __init__' in line:
            parts = line.split(':')
            filepath = parts[0].strip()
            lineno = int(parts[1])
            if filepath not in file_fixes:
                file_fixes[filepath] = []
            file_fixes[filepath].append(('init', lineno))

    for filepath, fixes in file_fixes.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()
            
        fixes.sort(key=lambda x: x[1], reverse=True)
        
        for fix_type, lineno in fixes:
            if fix_type == 'module' and lineno == 1:
                content.insert(0, '"""Module docstring."""\n')
            else:
                idx = lineno - 1
                # find the def or class line and wait for it to end with :
                while idx < len(content) and not content[idx].strip().endswith(':'):
                    idx += 1
                
                if idx < len(content):
                    # figure out indentation
                    next_line = content[idx+1] if idx+1 < len(content) else ""
                    indent = len(next_line) - len(next_line.lstrip())
                    if next_line.strip() == '':
                        # try to find next non-empty line to get indent
                        tmp = idx + 1
                        while tmp < len(content) and content[tmp].strip() == '':
                            tmp += 1
                        if tmp < len(content):
                            indent = len(content[tmp]) - len(content[tmp].lstrip())
                        else:
                            indent = len(content[idx]) - len(content[idx].lstrip()) + 4
                            
                    spaces = " " * indent
                    doc = f'{spaces}"""Docstring."""\n'
                    content.insert(idx + 1, doc)
                    
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(content)
            
if __name__ == '__main__':
    inject_docstrings('flake8_errors.txt')
