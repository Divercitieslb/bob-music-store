# -*- coding: utf-8 -*-
"""Validate every section schema against Shopify's own rules.

A single rejected schema makes Shopify refuse the whole GitHub sync, and the
failure is silent from the repo side — the push succeeds, the storefront just
never changes. This checks the rules that actually cause rejection.
"""
import json, os, re, sys, glob

R = '..'

VALID_TYPES = {
    # input
    'text', 'textarea', 'number', 'range', 'checkbox', 'radio', 'select',
    'color', 'color_background', 'color_scheme', 'color_scheme_group',
    'font_picker', 'collection', 'collection_list', 'product', 'product_list',
    'blog', 'page', 'link_list', 'url', 'video', 'video_url', 'image_picker',
    'article', 'html', 'liquid', 'richtext', 'inline_richtext', 'text_alignment',
    'metaobject', 'metaobject_list', 'style.layout_panel', 'style.size_panel',
    # sidebar
    'header', 'paragraph',
}
SIDEBAR = {'header', 'paragraph'}

# Setting types Shopify accepts no "default" for.
NO_DEFAULT = {'url', 'image_picker', 'video', 'article', 'page',
              'collection', 'collection_list', 'product', 'product_list',
              'blog', 'metaobject', 'metaobject_list', 'font_picker'}

errors, warns = [], []


def check_settings(where, settings, seen_ids):
    for i, s in enumerate(settings):
        if not isinstance(s, dict):
            errors.append(f'{where}: setting #{i} is not an object'); continue
        t = s.get('type')
        if t is None:
            errors.append(f'{where}: setting #{i} has no "type"'); continue
        if t not in VALID_TYPES:
            errors.append(f'{where}: setting #{i} has invalid type "{t}"'); continue
        if t in SIDEBAR:
            if t == 'header' and 'content' not in s:
                errors.append(f'{where}: header setting #{i} needs "content"')
            continue

        sid = s.get('id')
        if not sid:
            errors.append(f'{where}: setting #{i} (type {t}) has no "id"')
        else:
            if not re.fullmatch(r'[A-Za-z0-9_]+', sid):
                errors.append(f'{where}: id "{sid}" — only letters, digits and underscore are allowed')
            if sid in seen_ids:
                errors.append(f'{where}: duplicate setting id "{sid}"')
            seen_ids.add(sid)

        if 'label' not in s:
            errors.append(f'{where}: setting "{sid}" has no "label"')

        if t == 'select':
            opts = s.get('options')
            if not opts:
                errors.append(f'{where}: select "{sid}" has no options')
            else:
                vals = [o.get('value') for o in opts]
                for o in opts:
                    if 'value' not in o or 'label' not in o:
                        errors.append(f'{where}: select "{sid}" option missing value/label')
                if 'default' in s and s['default'] not in vals:
                    errors.append(f'{where}: select "{sid}" default "{s["default"]}" is not one of its options')

        if t == 'radio':
            opts = s.get('options') or []
            vals = [o.get('value') for o in opts]
            if 'default' in s and s['default'] not in vals:
                errors.append(f'{where}: radio "{sid}" default not in options')

        if t == 'range':
            for k in ('min', 'max', 'step'):
                if k not in s:
                    errors.append(f'{where}: range "{sid}" missing "{k}"')
            if all(k in s for k in ('min', 'max', 'step')):
                mn, mx, st = s['min'], s['max'], s['step']
                if st <= 0:
                    errors.append(f'{where}: range "{sid}" step must be > 0')
                else:
                    steps = (mx - mn) / st
                    if steps != int(steps):
                        errors.append(f'{where}: range "{sid}" ({mn}..{mx} step {st}) does not divide evenly')
                    if steps > 101:
                        errors.append(f'{where}: range "{sid}" has {int(steps)+1} steps — Shopify allows at most 101')
                d = s.get('default')
                if d is not None and not (mn <= d <= mx):
                    errors.append(f'{where}: range "{sid}" default {d} outside {mn}..{mx}')

        # Shopify's "url" setting type takes no default. A schema carrying one
        # is REJECTED and the file is then never written to the theme — the
        # storefront quietly keeps serving the previous version and reports
        # nothing at all. header.liquid was stuck for a whole deploy on this.
        if t in NO_DEFAULT and 'default' in s:
            errors.append(f'{where}: "{sid}" is type {t}, which takes no "default" — '
                          f'Shopify rejects the schema and never writes the file. '
                          f'Fall back in Liquid instead:  assign x = settings.{sid} | default: ...')

        if t == 'checkbox' and 'default' in s and not isinstance(s['default'], bool):
            errors.append(f'{where}: checkbox "{sid}" default must be true/false')

        if t in ('text', 'textarea', 'richtext', 'inline_richtext', 'url', 'html', 'liquid'):
            if 'default' in s and not isinstance(s['default'], str):
                errors.append(f'{where}: "{sid}" default must be a string')

        if t == 'richtext':
            d = s.get('default')
            if isinstance(d, str) and d.strip() and not d.strip().startswith('<'):
                errors.append(f'{where}: richtext "{sid}" default must be wrapped in HTML tags')


for path in sorted(glob.glob(os.path.join(R, 'sections', '*.liquid'))):
    rel = 'sections/' + os.path.basename(path)
    src = open(path, encoding='utf-8').read()
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', src, re.S)
    if not m:
        continue
    try:
        sch = json.loads(m.group(1))
    except Exception as e:
        errors.append(f'{rel}: schema is not valid JSON — {e}')
        continue

    name = sch.get('name')
    if not name:
        errors.append(f'{rel}: schema has no "name"')
    elif len(name) > 25:
        errors.append(f'{rel}: name "{name}" is {len(name)} chars — Shopify allows 25')

    check_settings(rel, sch.get('settings', []), set())

    blocks = sch.get('blocks', [])
    if len(blocks) > 50:
        errors.append(f'{rel}: {len(blocks)} block types declared')
    btypes = set()
    for b in blocks:
        bt = b.get('type')
        if not bt:
            errors.append(f'{rel}: a block has no "type"')
        elif bt in btypes:
            errors.append(f'{rel}: duplicate block type "{bt}"')
        else:
            btypes.add(bt)
        if 'name' not in b and bt != '@app':
            errors.append(f'{rel}: block "{bt}" has no "name"')
        check_settings(f'{rel} block:{bt}', b.get('settings', []), set())

    mb = sch.get('max_blocks')
    if mb is not None and (not isinstance(mb, int) or mb < 1 or mb > 50):
        errors.append(f'{rel}: max_blocks must be 1..50, got {mb}')

    for p in sch.get('presets', []):
        if 'name' not in p:
            errors.append(f'{rel}: a preset has no "name"')
        for pb in p.get('blocks', []):
            if isinstance(pb, dict) and pb.get('type') not in btypes:
                errors.append(f'{rel}: preset references unknown block type "{pb.get("type")}"')

    eo = sch.get('enabled_on') or sch.get('disabled_on')
    if eo and not isinstance(eo, dict):
        errors.append(f'{rel}: enabled_on/disabled_on must be an object')

# settings_schema.json
p = os.path.join(R, 'config', 'settings_schema.json')
try:
    top = json.load(open(p, encoding='utf-8'))
    if not isinstance(top, list):
        errors.append('config/settings_schema.json: must be a list')
    else:
        if not top or top[0].get('name') != 'theme_info':
            errors.append('config/settings_schema.json: first entry must be the theme_info block')
        ids = set()
        for grp in top:
            if grp.get('name') == 'theme_info':
                for k in ('theme_name', 'theme_version', 'theme_author'):
                    if k not in grp:
                        errors.append(f'config/settings_schema.json: theme_info missing {k}')
                continue
            check_settings('config/settings_schema.json', grp.get('settings', []), ids)
except Exception as e:
    errors.append(f'config/settings_schema.json: {e}')

print(f'checked {len(glob.glob(os.path.join(R, "sections", "*.liquid")))} sections')
if warns:
    print(f'\nwarnings ({len(warns)}):')
    for w in warns:
        print('  ', w)
if errors:
    print(f'\nWOULD BE REJECTED BY SHOPIFY ({len(errors)}):')
    for e in errors:
        print('  -', e)
    sys.exit(1)
print('\nno schema errors — Shopify would accept this theme')


# ---------------------------------------------------------------------------
# Inline {% liquid %} blocks are LINE-BASED: one statement per line. Shopify
# rejects the whole file on a syntax error there, and a rejected file is never
# written to the theme — the storefront then reports "Could not find asset",
# which reads like a sync problem rather than a syntax one. This cost several
# hours, so it is checked here.
import glob as _glob, re as _re, os as _os, sys as _sys

_LIQ = _re.compile(r'\{%-?\s*liquid\b(.*?)-?%\}', _re.S)
_TAGS = ('assign', 'echo', 'increment', 'decrement', 'if', 'elsif', 'else',
         'endif', 'unless', 'endunless', 'case', 'when', 'endcase', 'for',
         'endfor', 'break', 'continue', 'cycle', 'tablerow', 'endtablerow',
         'capture', 'endcapture', 'render', 'include', 'layout', 'section',
         'sections', 'form', 'endform', 'paginate', 'endpaginate', 'liquid')

_bad = []
for _p in (_glob.glob(_os.path.join(R, 'sections', '*.liquid'))
           + _glob.glob(_os.path.join(R, 'snippets', '*.liquid'))
           + _glob.glob(_os.path.join(R, 'layout', '*.liquid'))):
    _rel = _os.path.relpath(_p, R).replace(chr(92), chr(47))
    _src = open(_p, encoding='utf-8').read()
    for _m in _LIQ.finditer(_src):
        _base = _src[:_m.start()].count('\n')
        for _i, _line in enumerate(_m.group(1).split('\n')):
            _s = _line.strip()
            if not _s or _s.startswith('#'):
                continue
            _first = _s.split()[0]
            if _first not in _TAGS:
                _bad.append(f'{_rel}:{_base + _i + 1}: "{_first}" is not a Liquid tag — '
                            f'inside {{% liquid %}} every line must start with one')
            if _re.search(r'\bthen\b', _s):
                _bad.append(f'{_rel}:{_base + _i + 1}: "then" is not Liquid — '
                            f'put the statement on its own line:  {_s[:60]}')
            if _s.count('|') and _re.search(r'\|\s*(assign|echo|if|case|when)\b', _s):
                _bad.append(f'{_rel}:{_base + _i + 1}: a tag used as a filter after "|":  {_s[:60]}')

if _bad:
    print(f'\nINVALID {{% liquid %}} SYNTAX — Shopify will reject these files ({len(_bad)}):')
    for _b in _bad:
        print('  -', _b)
    _sys.exit(1)
print('all {% liquid %} blocks are line-valid')
