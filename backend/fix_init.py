import os
for root, dirs, files in os.walk('d:/code_placed/git_carbon/backend'):
    if '.venv' in root or 'venv' in root: continue
    for f in files:
        if f == '__init__.py':
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            if '"""' not in content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write('\"\"\"Initialization module.\"\"\"\n' + content)
