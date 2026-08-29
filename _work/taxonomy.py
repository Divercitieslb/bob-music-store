# -*- coding: utf-8 -*-
"""Bob Music Store catalogue taxonomy.

Seven families -> collections. Every product Type maps to exactly one leaf
collection; the family collection is derived from that. Collection membership
is expressed as tags so Shopify smart collections can be built with a single
"tag is equal to" rule each.
"""

# leaf handle -> (leaf title, family handle, family title)
LEAF = {}
FAMILY = {}


def fam(handle, title, leaves):
    FAMILY[handle] = title
    for h, t, types in leaves:
        LEAF[h] = (t, handle, types)


fam('guitars', 'Guitars & Bass', [
    ('acoustic-guitars',  'Acoustic Guitars',  ['Acoustic Guitar']),
    ('classical-guitars', 'Classical Guitars', ['Classical Guitar']),
    ('electric-guitars',  'Electric Guitars',  ['Electric Guitar']),
    ('bass-guitars',      'Bass Guitars',      ['Bass Guitar']),
    ('kids-guitars',      "Kids' Guitars",     ['Toy Instrument']),
])

fam('oud', 'Oud', [
    ('oud-instruments', 'Oud', ['Oud']),
])

fam('percussion', 'Percussion', [
    ('darbuka',      'Darbuka',              ['Darbuka']),
    ('frame-drums',  'Riq & Frame Drums',    ['Frame Drum']),
    ('bass-drums',   'Tabl & Bass Drums',    ['Bass Drum']),
    ('drum-kits',    'Drum Kits & Bongos',   ['Drum Kit', 'Bongos', 'Glockenspiel']),
    ('drum-heads',   'Drum Heads',           ['Drum Head', 'Packaging / Collectible']),
])

fam('accordions', 'Accordions', [
    ('piano-accordions',  'Piano Accordions',  ['Piano Accordion']),
    ('button-accordions', 'Button Accordions', ['Button Accordion']),
])

fam('violins-wind', 'Violins & Wind', [
    ('violins',           'Violins',            ['Violin']),
    ('electric-violins',  'Electric Violins',   ['Electric Violin']),
    ('flutes-ney',        'Flutes & Ney',       ['Flute', 'Ney', 'Pan Flute']),
    ('recorders',         'Recorders',          ['Recorder']),
    ('saxophones-brass',  'Saxophones & Brass', ['Saxophone', 'Bugle']),
])

fam('audio-studio', 'Audio & Studio', [
    ('microphones',      'Microphones',        ['Microphone']),
    ('amplifiers',       'Amplifiers',         ['Amplifier']),
    ('speakers-pa',      'Speakers & PA',      ['Speaker']),
    ('effects-pedals',   'Effects Pedals',     ['Effects Pedal']),
    ('studio-recording', 'Studio & Recording', ['Studio Equipment', 'Audio Interface', 'DJ Mixer']),
    ('midi-controllers', 'MIDI Controllers',   ['MIDI Controller']),
    ('footswitches',     'Footswitches',       ['Footswitch']),
])

fam('accessories', 'Strings & Accessories', [
    ('guitar-strings',      'Guitar Strings',        ['Guitar Strings']),
    ('oud-saz-strings',     'Oud & Saz Strings',     ['Oud Strings', 'Saz Strings', 'Instrument Strings', 'Ukulele Strings']),
    ('violin-bass-strings', 'Violin & Bass Strings', ['Violin Strings', 'Bass Strings']),
    ('guitar-straps',       'Straps',                ['Guitar Strap']),
    ('stands',              'Stands',                ['Music Stand', 'Microphone Stand']),
    ('tuners-pickups',      'Tuners & Pickups',      ['Tuner', 'Pickup', 'Capo']),
    ('cases-care',          'Cases & Care',          ['Case', 'Rosin', 'Cable', 'Accessory']),
])

# type -> leaf handle
TYPE_TO_LEAF = {}
for h, (t, fh, types) in LEAF.items():
    for ty in types:
        TYPE_TO_LEAF[ty] = h

# ---------------------------------------------------------------- features
FEATURE = {
    'arabic-instruments': 'Arabic Instruments',
    'vintage-collectible': 'Vintage & Collectible',
    'new-arrivals': 'New Arrivals',
    'beginner': 'Beginner & Student',
}

ARABIC_TYPES = {
    'Oud', 'Darbuka', 'Frame Drum', 'Bass Drum', 'Oud Strings',
    'Saz Strings', 'Instrument Strings', 'Ney',
}

# Shopify standard product taxonomy category per family
SHOPIFY_CATEGORY = {
    'guitars':      'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > String Instruments > Guitars',
    'oud':          'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > String Instruments',
    'percussion':   'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Percussion',
    'accordions':   'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Accordions & Concertinas',
    'violins-wind': 'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > String Instruments',
    'audio-studio': 'Arts & Entertainment > Hobbies & Creative Arts > Musical Instrument & Orchestra Accessories',
    'accessories':  'Arts & Entertainment > Hobbies & Creative Arts > Musical Instrument & Orchestra Accessories',
}

# more precise overrides where the family default is too broad
CATEGORY_BY_TYPE = {
    'Violin':           'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > String Instruments > Violins',
    'Electric Violin':  'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > String Instruments > Violins',
    'Flute':            'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Wind Instruments > Flutes',
    'Ney':              'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Wind Instruments > Flutes',
    'Pan Flute':        'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Wind Instruments > Flutes',
    'Recorder':         'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Wind Instruments > Recorders',
    'Saxophone':        'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Wind Instruments > Saxophones',
    'Bugle':            'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Wind Instruments > Brass Instruments',
    'Microphone':       'Arts & Entertainment > Hobbies & Creative Arts > Musical Instrument & Orchestra Accessories > Microphone Stands',
    'Speaker':          'Electronics > Audio > Audio Components > Speakers',
    'Amplifier':        'Arts & Entertainment > Hobbies & Creative Arts > Musical Instrument & Orchestra Accessories > Musical Instrument Amplifiers',
    'Effects Pedal':    'Arts & Entertainment > Hobbies & Creative Arts > Musical Instrument & Orchestra Accessories > Electronic Musical Instrument Accessories',
    'MIDI Controller':  'Arts & Entertainment > Hobbies & Creative Arts > Musical Instrument & Orchestra Accessories > Electronic Musical Instrument Accessories',
    'Piano Accordion':  'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Accordions & Concertinas',
    'Button Accordion': 'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments > Accordions & Concertinas',
}

# rough shipping weights in grams, by type, so checkout can quote a rate
WEIGHT = {
    'Acoustic Guitar': 2600, 'Classical Guitar': 2200, 'Electric Guitar': 3600,
    'Bass Guitar': 4200, 'Toy Instrument': 1200, 'Oud': 2400,
    'Darbuka': 2200, 'Frame Drum': 900, 'Bass Drum': 4500, 'Drum Kit': 22000,
    'Bongos': 3200, 'Glockenspiel': 1400, 'Drum Head': 320,
    'Packaging / Collectible': 120,
    'Piano Accordion': 9500, 'Button Accordion': 6000,
    'Violin': 1600, 'Electric Violin': 2200, 'Recorder': 120,
    'Flute': 1100, 'Ney': 220, 'Pan Flute': 380, 'Saxophone': 5200, 'Bugle': 900,
    'Microphone': 550, 'Amplifier': 12000, 'Speaker': 9000,
    'Effects Pedal': 700, 'Studio Equipment': 2600, 'Audio Interface': 240,
    'DJ Mixer': 3200, 'MIDI Controller': 2400, 'Footswitch': 420,
    'Guitar Strings': 90, 'Oud Strings': 70, 'Saz Strings': 60,
    'Violin Strings': 60, 'Bass Strings': 140, 'Ukulele Strings': 40,
    'Instrument Strings': 60, 'Guitar Strap': 220, 'Music Stand': 1800,
    'Microphone Stand': 2400, 'Tuner': 110, 'Pickup': 180, 'Capo': 70,
    'Case': 900, 'Rosin': 60, 'Cable': 260, 'Accessory': 400,
}


def collections_for(ptype, tags_lower, title_lower):
    """Every collection handle a product belongs to."""
    out = []
    leaf = TYPE_TO_LEAF.get(ptype)
    if leaf:
        out.append(leaf)
        out.append(LEAF[leaf][1])
    if ptype in ARABIC_TYPES:
        out.append('arabic-instruments')
    if 'vintage' in tags_lower or 'vintage' in title_lower or 'used' in title_lower:
        out.append('vintage-collectible')
    if 'student' in title_lower or 'beginner' in tags_lower or "kids" in title_lower or "children" in title_lower:
        out.append('beginner')
    return out


def category_for(ptype):
    if ptype in CATEGORY_BY_TYPE:
        return CATEGORY_BY_TYPE[ptype]
    leaf = TYPE_TO_LEAF.get(ptype)
    if leaf:
        return SHOPIFY_CATEGORY.get(LEAF[leaf][1], '')
    return ''


def title_for(handle):
    if handle in LEAF:
        return LEAF[handle][0]
    if handle in FAMILY:
        return FAMILY[handle]
    return FEATURE.get(handle, handle)
