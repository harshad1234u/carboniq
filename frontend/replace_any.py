import os

def replace_any(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('catch (err: any)', 'catch (err)')
    content = content.replace('input: any', 'input: unknown')
    content = content.replace('rec: any', 'rec: unknown')
    content = content.replace('value: any', 'value: number')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('d:/code_placed/git_carbon/frontend/src'):
    for f in files:
        if f.endswith('.ts') or f.endswith('.tsx'):
            replace_any(os.path.join(root, f))
