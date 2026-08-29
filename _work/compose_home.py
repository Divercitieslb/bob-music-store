# -*- coding: utf-8 -*-
"""Compose the homepage from every section that was actually built.

scroll-story, stat-band and quote-band were written and then left out of
templates/index.json, so none of them ever rendered. This puts them in and
sets the rhythm: image, type, figures, product, story, quote, product.
"""
import json, collections, os

P = '../templates/index.json'
d = json.load(open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
S = d['sections']

# ---- the pinned scroll sequence: how an instrument reaches the shop --------
S['bench_story'] = collections.OrderedDict([
    ('type', 'scroll-story'),
    ('blocks', collections.OrderedDict([
        ('c1', {'type': 'chapter', 'settings': {
            'default_asset': 'story-shop.jpg',
            'image_alt': 'The shop floor in Beirut',
            'eyebrow': 'One',
            'heading': 'It arrives',
            'text': 'Sometimes in a crate from Cairo, sometimes carried in by the person who made it. Nothing is drop-shipped and nothing is listed from a catalogue photograph.'}}),
        ('c2', {'type': 'chapter', 'settings': {
            'default_asset': 'band-bench.jpg',
            'image_alt': 'The repair bench',
            'eyebrow': 'Two',
            'heading': 'It goes on the bench',
            'text': 'Unboxed and checked. A fret dressed if it needs it, a head brought up to pitch, an action set. Anything that will not come right goes back.'}}),
        ('c3', {'type': 'chapter', 'settings': {
            'default_asset': 'feature-oud.jpg',
            'image_alt': 'An oud being set up by hand',
            'eyebrow': 'Three',
            'heading': 'It gets played',
            'text': 'Every instrument is played before it ships — because a specification tells you nothing about how a bowl responds, and two ouds built from the same drawing never sound the same.'}}),
        ('c4', {'type': 'chapter', 'settings': {
            'default_asset': 'look-oud-wide.jpg',
            'image_alt': 'An oud packed and ready to leave',
            'eyebrow': 'Four',
            'heading': 'It leaves properly packed',
            'text': 'A hard case where the instrument needs one, padded and braced where it does not. Across Lebanon, and further when you ask.',
            'link_label': 'How we work',
            'link_url': '/pages/about'}}),
    ])),
    ('block_order', ['c1', 'c2', 'c3', 'c4']),
    ('settings', {
        'eyebrow': 'From the crate to your hands',
        'heading': 'Four steps, every instrument',
        'text': 'Nothing here reaches a customer without passing the bench.',
        'media_side': 'left',
        'show_index': True,
        'bg': 'section--shell',
    }),
])

# ---- the figures ----------------------------------------------------------
S['figures'] = collections.OrderedDict([
    ('type', 'stat-band'),
    ('blocks', collections.OrderedDict([
        ('f1', {'type': 'figure', 'settings': {
            'value': '268', 'label': 'Instruments in stock', 'note': 'Every one photographed as it is'}}),
        ('f2', {'type': 'figure', 'settings': {
            'value': '42', 'label': 'Collections', 'note': 'Sorted the way a player looks'}}),
        ('f3', {'type': 'figure', 'settings': {
            'value': '81', 'label': 'Arabic instruments', 'note': 'Oud, darbuka, riq, tabl, ney'}}),
        ('f4', {'type': 'figure', 'settings': {
            'value': '31', 'label': 'Vintage & collectible', 'note': 'One of each, exactly'}}),
    ])),
    ('block_order', ['f1', 'f2', 'f3', 'f4']),
    ('settings', {
        'eyebrow': 'The shop in numbers',
        'heading': 'What is on the wall today',
        'count_up': True,
        'default_asset': 'look-darbuka.jpg',
        'overlay': 82,
        'bg': 'section--ink',
    }),
])

# ---- the pull quote -------------------------------------------------------
S['quote'] = collections.OrderedDict([
    ('type', 'quote-band'),
    ('settings', {
        'quote': 'You do not choose an oud from a photograph. You choose it by ear, in a room, with the bowl against your chest.',
        'attribution': 'Bob',
        'role': 'Behind the counter since the shop opened',
        'size': 'large',
        'show_divider': True,
        'show_mark': True,
        'default_asset': 'look-oud.jpg',
        'image_alt': 'An oud on the workbench',
        'media_side': 'right',
        'media_width': 38,
        'cta_label': 'See the ouds',
        'cta_url': '/collections/oud',
        'bg': '',
    }),
])

# give the two split features their line drawings
S['oud_room']['settings']['watermark'] = 'oud-outline'
S['percussion']['settings']['watermark'] = 'darbuka-outline'

# ---- the running order ----------------------------------------------------
# image -> brands -> image grid -> story column -> figures -> product ->
# cinematic band -> quote -> story column -> product -> reasons
d['order'] = [
    'hero',
    'brands',
    'lookbook',
    'oud_room',
    'figures',
    'featured',
    'bench',
    'bench_story',
    'quote',
    'percussion',
    'categories',
    'props',
]

json.dump(d, open(P, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

print('homepage order:')
for i, k in enumerate(d['order'], 1):
    print(f'  {i:2}. {k:14} {S[k]["type"]}')
print(f'\n{len(d["order"])} sections, {len(S)} defined')
