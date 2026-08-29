# -*- coding: utf-8 -*-
"""Repair line 207 of shopify_validate.py.

The line was written through a shell heredoc, which ate the backslash escape
and left an unterminated string. Rewritten without any backslash at all.
"""
import ast

P = 'shopify_validate.py'
lines = open(P, encoding='utf-8').read().split('\n')
target = None
for i, line in enumerate(lines):
    if '_rel = _os.path.relpath(_p, R).replace(' in line:
        target = i
        break

if target is None:
    print('line not found — nothing to repair')
else:
    lines[target] = '    _rel = _os.path.relpath(_p, R).replace(chr(92), chr(47))'
    src = '\n'.join(lines)
    ast.parse(src)
    open(P, 'w', encoding='utf-8').write(src)
    print(f'repaired line {target + 1}; file parses')
