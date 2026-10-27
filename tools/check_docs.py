#!/usr/bin/env python3
"""Check repository-local Markdown targets without network access."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
for path in root.rglob('*.md'):
    if '.git' in path.parts:
        continue
    content = path.read_text()
    if re.search(r'[\u4e00-\u9fff]', content):
        errors.append(f'{path.relative_to(root)}: expected English documentation')
    for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', content):
        target = match.group(1).split('#')[0]
        if not target or '://' in target or target.startswith('mailto:'):
            continue
        if not (path.parent / target).exists():
            errors.append(f'{path.relative_to(root)}: missing target {target}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print('Local Markdown links and English-documentation checks passed.')
