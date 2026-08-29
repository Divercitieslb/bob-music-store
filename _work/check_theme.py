# -*- coding: utf-8 -*-
"""Static checks over the theme: balanced Liquid tags, valid schema JSON,
resolvable snippet renders, and asset references that actually exist."""
import os, re, json, glob, sys

ROOT = '..'
# {% liquid %} is an inline tag, not a block - it has no {% endliquid %}.
BLOCKS = ('if', 'unless', 'for', 'case', 'form', 'paginate', 'capture',
          'tablerow', 'comment', 'raw', 'schema', 'javascript', 'stylesheet',
          'style')
errors, warns = [], []


def liquid_files():
    for d in ('sections', 'snippets', 'layout', 'templates'):
        yield from glob.glob(os.path.join(ROOT, d, '**', '*.liquid'), recursive=True)


def check_balance(path, src):
    stack = []
    for m in re.finditer(r'\{%-?\s*(\w+)', src):
        tag = m.group(1)
        if tag in BLOCKS:
            stack.append((tag, m.start()))
        elif tag.startswith('end'):
            want = tag[3:]
            if not stack:
                errors.append(f'{path}: stray {{% {tag} %}}')
            elif stack[-1][0] != want:
                errors.append(f'{path}: {{% {tag} %}} closes {{% {stack[-1][0]} %}}')
                stack.pop()
            else:
                stack.pop()
    for tag, pos in stack:
        line = src[:pos].count('\n') + 1
        errors.append(f'{path}: unclosed {{% {tag} %}} (line {line})')


def check_schema(path, src):
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', src, re.S)
    if not m:
        if os.path.basename(os.path.dirname(path)) == 'sections':
            warns.append(f'{path}: no schema block')
        return
    try:
        json.loads(m.group(1))
    except Exception as e:
        errors.append(f'{path}: invalid schema JSON — {e}')


def check_renders(path, src):
    for m in re.finditer(r"\{%-?\s*render\s+'([^']+)'", src):
        snip = os.path.join(ROOT, 'snippets', m.group(1) + '.liquid')
        if not os.path.exists(snip):
            errors.append(f'{path}: renders missing snippet "{m.group(1)}"')


def check_assets(path, src):
    for m in re.finditer(r"'([^']+)'\s*\|\s*asset_url", src):
        a = os.path.join(ROOT, 'assets', m.group(1))
        if not os.path.exists(a):
            errors.append(f'{path}: asset_url missing file "{m.group(1)}"')


for p in liquid_files():
    src = open(p, encoding='utf-8').read()
    rel = os.path.relpath(p, ROOT).replace('\\', '/')
    check_balance(rel, src)
    check_schema(rel, src)
    check_renders(rel, src)
    check_assets(rel, src)

def load_theme_json(path):
    """Shopify's admin writes a /* ... */ banner into JSON it round-trips.

    That is valid for Shopify and invalid for json.load, so the banner is
    stripped here. Without this every template the merchant touches in the
    theme editor fails the checker for a reason that is not a fault — which
    hides the ones that are.
    """
    raw = open(path, encoding='utf-8').read()
    return json.loads(re.sub(r'^\s*/\*.*?\*/\s*', '', raw, flags=re.S))


# every JSON template must reference a section file that exists
for p in glob.glob(os.path.join(ROOT, 'templates', '**', '*.json'), recursive=True):
    rel = os.path.relpath(p, ROOT).replace('\\', '/')
    data = load_theme_json(p)
    for key, sec in data.get('sections', {}).items():
        f = os.path.join(ROOT, 'sections', sec['type'] + '.liquid')
        if not os.path.exists(f):
            errors.append(f'{rel}: section "{sec["type"]}" does not exist')
    for key in data.get('order', []):
        if key not in data.get('sections', {}):
            errors.append(f'{rel}: order references unknown section "{key}"')

# section groups
for p in glob.glob(os.path.join(ROOT, 'sections', '*.json')):
    rel = os.path.relpath(p, ROOT).replace('\\', '/')
    data = load_theme_json(p)
    for key, sec in data.get('sections', {}).items():
        f = os.path.join(ROOT, 'sections', sec['type'] + '.liquid')
        if not os.path.exists(f):
            errors.append(f'{rel}: section "{sec["type"]}" does not exist')

# required theme files
for req in ('layout/theme.liquid', 'config/settings_schema.json',
            'templates/index.json', 'templates/product.json',
            'templates/collection.json', 'templates/cart.json',
            'templates/404.json', 'templates/search.json',
            'templates/page.json', 'templates/list-collections.json'):
    if not os.path.exists(os.path.join(ROOT, req)):
        errors.append(f'missing required file {req}')

print(f'checked {len(list(liquid_files()))} liquid files')
if warns:
    print(f'\nwarnings ({len(warns)}):')
    for w in warns:
        print('  ', w)
if errors:
    print(f'\nERRORS ({len(errors)}):')
    for e in errors:
        print('  ', e)
    sys.exit(1)
print('\nno errors')
