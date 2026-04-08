import os, re

BASE = r'c:\Users\arira\Desktop\NijamVhai\mockups\v2'
SCRIPT_TAG = '<script src="_theme.js"></script>'

files = [
    '01-dashboard.html',
    '02-companies.html',
    '03-order-detail.html',
    '04-new-order.html',
    '05-sample-revision.html',
    '06-pi.html',
    '07-lc-tracker.html',
    '08-challan.html',
]

for fname in files:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already injected
    if SCRIPT_TAG in content:
        print(f'Already has script: {fname}')
        continue

    # Inject before </body>
    if '</body>' in content:
        content = content.replace('</body>', f'{SCRIPT_TAG}\n</body>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Injected: {fname}')
    else:
        print(f'WARNING: no </body> found in {fname}')

print('DONE inject')
