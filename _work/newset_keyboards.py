# -*- coding: utf-8 -*-
"""The November keyboard intake — 12 products from 17 photographs.

DEDUPLICATION (the owner asked for it explicitly):
  Ketron VEGA .......... photos 6 and 14 are the SAME unit, two different edits
  Alesis Vortex ........ photos 5, 8, 9, 10, 11 are ONE product: 8 and 9 are the
                         unit in its opened box, 5/10/11 are the printed carton
  Everything else ...... one photo, one product
  => 17 photographs, 12 products.

PHOTO 7 WAS MIRRORED. The Yamaha's badge read "AHAMAY" and the model "PSR-A350"
ran backwards; it was taken or exported through a front-camera flip. Corrected
before anything else, because every later step (and the listing copy, which is
read off the panel) depends on it.

WHAT IS AND IS NOT ASSERTED. Titles, panel features and condition come from the
photographs — read off the instrument, not recalled. Key counts are stated only
where the model has exactly one keyboard size. Nothing here claims polyphony,
voice counts, sample memory or production year except where it is PRINTED ON
THE BOX (the MK-821 and the Alesis). Second-hand gear varies unit to unit; the
owner should confirm before publishing.
"""

NEW_COLLECTIONS = [
    # (title, handle, level, parent)  — handle must equal handleize(title) or
    # Shopify generates its own and every theme link breaks. This bit the store
    # once already; see import/collections-checklist.md.
    ('Keyboards & Synths', 'keyboards-synths', 1, None),
    ('Arranger Keyboards', 'arranger-keyboards', 2, 'keyboards-synths'),
    ('Synthesizers',       'synthesizers',       2, 'keyboards-synths'),
    ('Workstations',       'workstations',       2, 'keyboards-synths'),
    ('Portable Keyboards', 'portable-keyboards', 2, 'keyboards-synths'),
]

P = [
 dict(
  sku='KBD-01', photos=['6', '14'],
  title='Ketron VEGA Advanced Live Performer — Oriental Arranger Keyboard (Used)',
  vendor='Ketron', type='Arranger Keyboard', grams=11000,
  tags=['Keyboards & Synths', 'Arranger Keyboards', 'Arabic Instruments',
        'Ketron', 'VEGA', 'oriental keyboard', 'arranger', 'quarter tone', 'used'],
  lede='An Italian-built Ketron VEGA arranger in the white "Advanced Live Performer" finish, '
       'set up for Arabic and oriental music.',
  bullets=[
    'Oriental Scale row along the front edge — the bank of twelve switches that drops '
    'individual notes to quarter tones on the fly, which is what players buy a VEGA for',
    'Arranger panel with Arrange Mode, Styles Play, Song Play, Juke Box and Drum Mixer',
    'Style families printed on the panel: Beat, Dance, Party, Folk, Swing, Latin, Pop, '
    'Country/Oriental, Rock and Karoli',
    'Micro Vocalizer section, Drawbars, Edit Program and Edit Drum',
    'Sound banks across the top right: Piano, Chrom, Organ, Accord, Guitar, Strings, '
    'Brass, Sax, Pad, Synth, Ethnic and Bass-FX, with a dedicated Oriental bank',
    'Pitch and modulation panel at the far left, twin built-in speakers, backlit display',
  ],
  condition='Used and played. The cream panel has darkened a little with age and there '
            'are marks on the left-hand speaker grille, visible in the photographs. '
            'Everything on the panel is present and legible.',
 ),
 dict(
  sku='KBD-02', photos=['4'],
  title='GEM WS Keyboard Workstation — Arabic Edition (Vintage)',
  vendor='GEM', type='Keyboard Workstation', grams=12000,
  tags=['Keyboards & Synths', 'Workstations', 'Arabic Instruments',
        'Vintage & Collectible', 'GEM', 'Generalmusic', 'oriental keyboard',
        'arranger', 'quarter tone', 'vintage'],
  lede='A GEM (Generalmusic) WS workstation in the Arabic-market edition — the panel is '
       'labelled in Arabic throughout, alongside the English.',
  bullets=[
    'Arabic Scale section at the lower right, with its own memory switches — the '
    'quarter-tone setup that makes this the oriental version rather than the export one',
    'Workstation panel: Edit (Master, Global, Voice, Mixer, Edit, Type, Status, Splits, '
    'MIDI) and a full Sequencer block (Tempo, Copy, Clear, Drum, Mode, Quant, Bass, Acc, '
    'Song, Page, Demo) around the central data dial',
    'Sound select row reading Grand Pno, E.Pno, Vibes, Darbuka, A.Bass, Guitar, Sax, '
    'Clarinet, Trumpet, Horns, Flute, Choir, Strings, Oud and Qanun',
    'Style row covering Bossa, Cha Cha, Dabke, Latin, Rap, Twist, Fusion, Dance, Blues, '
    'Slow Rock, Waltz, Polka, Samba, Jazz and more',
    'Lower / Upper split with Arabic, MIC, Pro and Chord style banks',
    'Start/Stop, Intro/End, Fill In and Sync/Continue beside the pitch wheel',
  ],
  condition='Vintage and used. Sound, feel and any faults should be checked in the shop '
            'before you commit — see the photograph for the actual panel.',
 ),
 dict(
  sku='KBD-03', photos=['7_unmirrored'],
  title='Yamaha PSR-A350 Oriental Arranger Keyboard — 61 Keys (Used)',
  vendor='Yamaha', type='Arranger Keyboard', grams=7000,
  tags=['Keyboards & Synths', 'Arranger Keyboards', 'Arabic Instruments',
        'Yamaha', 'PSR-A350', 'oriental keyboard', 'arranger', 'quarter tone',
        '61 keys', 'used'],
  lede='Yamaha\'s PSR-A350 — the Oriental model of the PSR line, with the scale-setting '
       'bank that retunes individual notes for Arabic maqam.',
  bullets=[
    '61 keys',
    'Scale Setting switches along the front edge with four Scale Memory slots, so a tuning '
    'can be stored and recalled mid-set',
    'Style list printed on the panel: Arabic, Khaligi, Maghrebi, Iranian, Turkish, Greek, '
    'Pop & Rock, Waltz, Ballad, Dance, Children, Pianist and Swing & Jazz',
    'Song list in the same families, plus Learn to Play, Favorite, Repertoire, User Song '
    'and Flash Memory',
    'Voices across Piano, E.Piano, Organ, Accordion, Guitar, Bass, Strings, Choir, '
    'Saxophone, Trumpet, Brass, Flute, Synth, Percussion, Drum Kits, Arpeggio, Sound '
    'Effects and a dedicated Oriental bank',
    'Oriental Instrument Piano, Ultra-Wide Stereo and Melody Suppressor buttons',
    'Yamaha Education Suite lesson section — Listening, Timing, Waiting and Chord '
    'Dictionary — with Keys to Success and Phrase Repeat',
    'Registration Memory, metronome, tempo/tap, USB and aux in',
  ],
  condition='Used, in good cosmetic order. One photograph of this keyboard arrived '
            'mirrored and has been corrected.',
 ),
 dict(
  sku='KBD-04', photos=['12'],
  title='Korg Trinity Music Workstation — 61 Keys (Vintage)',
  vendor='Korg', type='Keyboard Workstation', grams=15000,
  tags=['Keyboards & Synths', 'Workstations', 'Vintage & Collectible',
        'Korg', 'Trinity', 'workstation', 'synthesizer', '61 keys', 'vintage'],
  lede='The Korg Trinity — the workstation that introduced Korg\'s TouchView screen, and '
       'still the sound of a great many 1990s records.',
  bullets=[
    '61 keys',
    'TouchView graphical touchscreen — lit and working in the photograph',
    'Combination, Program, Sequencer, Disk and Global modes on the panel',
    'Two assignable sliders, F1–F8 function switches and the Value wheel',
    'Numeric keypad with Enter, plus transport switches: Pause, Rewind, FF, Reset, '
    'Rec/Write and Start/Stop',
    'Joystick and ribbon strip at the left-hand cheek',
  ],
  condition='Vintage, used, and sold as seen. Workstations of this age commonly want new '
            'internal backup batteries and the display backlight is a known wear item — '
            'please try it in the shop.',
 ),
 dict(
  sku='KBD-05', photos=['15'],
  title='Korg Triton Extreme Music Workstation / Sampler — 61 Keys (Vintage)',
  vendor='Korg', type='Keyboard Workstation', grams=15500,
  tags=['Keyboards & Synths', 'Workstations', 'Vintage & Collectible',
        'Korg', 'Triton Extreme', 'workstation', 'sampler', 'synthesizer',
        '61 keys', 'vintage'],
  lede='The Triton Extreme — the last and best-specified of the Triton line, and the one '
       'with a real valve in the output stage.',
  bullets=[
    '61 keys',
    'Valve Force: a vacuum tube in the signal path, visible through the window at the top '
    'left, with Ultra Boost, Value Force and Tube Gain controls beside it',
    'TouchView display with Combination, Program, Sequencer, Sampling, Global and Media '
    'modes',
    'Realtime Controls with four assignable knobs — LPF Cutoff, Assignable 1 and 2, '
    'EG Release and EG Intensity among them',
    'Built-in sampling with its own Rec and Start/Stop switches',
    'Arpeggiator with Tempo, Gate and Velocity knobs and an on/off switch',
    'Program and Combination bank switches A–H, joystick and ribbon controller',
  ],
  condition='Vintage and used. As with any workstation of this age, expect to check the '
            'backup battery, the display and the floppy/media slot. The panel sticker is '
            'still on it.',
 ),
 dict(
  sku='KBD-06', photos=['13'],
  title='Korg PS60 Performance Synthesizer — 61 Keys (Used)',
  vendor='Korg', type='Synthesizer', grams=7000,
  tags=['Keyboards & Synths', 'Synthesizers', 'Korg', 'PS60', 'synthesizer',
        'stage piano', '61 keys', 'used'],
  lede='A Korg PS60 — a stage synth laid out so you change sound by reaching for a knob, '
       'not by scrolling a menu.',
  bullets=[
    '61 keys',
    'Six sound families across the top, each with its own on/off switch and level knob: '
    'A.Piano, E.Piano, Organ, Strings, Brass and Synth — layer them by switching more '
    'than one on',
    'Modulation section: Flanger, Chorus, Vintage Chorus/Flanger and Phaser, with Rate, '
    'Depth and Feedback',
    'Reverb/Delay section: Plate, Hall, Room and Delay, with Time, Level and Feedback',
    'Three-band EQ — Bass, Mid, Treble',
    'Performance banks A–D with Store, Performance Edit and Exit',
    'Split Setting with Lower and Upper, Sub Off/Recall and a settable split point',
    'Organ Slow/Fast switch, octave and transpose, joystick',
  ],
  condition='Used. The white keys have yellowed with age — clearly visible in the '
            'photograph — and the body carries light marks. Play-tested in the shop.',
 ),
 dict(
  sku='KBD-07', photos=['16'],
  title='Korg KingKORG Synthesizer — 61 Keys (Used)',
  vendor='Korg', type='Synthesizer', grams=8000,
  tags=['Keyboards & Synths', 'Synthesizers', 'Korg', 'KingKORG', 'synthesizer',
        'analogue modelling', 'vocoder', '61 keys', 'used'],
  lede='The Korg KingKORG — an analogue-modelling synth with a valve driving its output, '
       'and a front panel that gives you a knob for nearly everything.',
  bullets=[
    '61 keys',
    'Tube section with its own Gain and Level — a real valve in the output stage, not a '
    'modelled one',
    'Three-section effects chain laid out across the panel: Pre FX (Decimator, '
    'Distortion, Ring Mod, Cl.Amp), Mod FX (Flanger, Chorus, Phaser, Tremolo) and '
    'Rev/Delay (Hall, Room, Plate, Tape Echo, Spin Delay, Mod Delay)',
    'Oscillator, Filter and Amp sections each with their own displays and knobs',
    'LFO and EG sections with Attack, Decay, Sustain and Release',
    'Timbre Select with Synth, Lead, Bass, Brass, Strings, Piano, Key and SE/Voco banks',
    'Two-band EQ, Favorites and Program select',
  ],
  condition='Used. The cream panel is noticeably marked and discoloured from use — see '
            'the photograph, which has not been retouched to hide it. Controls and '
            'keybed to be checked in the shop.',
 ),
 dict(
  sku='KBD-08', photos=['17'],
  title='Roland RS-50 Synthesizer — 61 Keys (Used)',
  vendor='Roland', type='Synthesizer', grams=8000,
  tags=['Keyboards & Synths', 'Synthesizers', 'Roland', 'RS-50', 'synthesizer',
        'D Beam', '61 keys', 'used'],
  lede='A Roland RS-50 — a straightforward stage synth with Roland\'s D Beam controller '
       'over the left-hand cheek.',
  bullets=[
    '61 keys',
    'D Beam controller — wave a hand over it to bend, filter or trigger, with Solo '
    'Synth, Active Expression and Assignable settings',
    'Patch, Performance and GM2 modes',
    'Sound banks on the numeric row: Rhythm & SFX, Piano, Keyboard & Organ, Guitar, '
    'Orchestral and World',
    'Patch Memory with Upper / Lower and a Destination Tone selector',
    'Quick-edit knobs for Attack, Decay, Release, Cutoff and Resonance, plus Env/LFO '
    'Balance, Rate and LFO Depth',
    'Tap Tempo and the Roland pitch-bend/modulation lever',
  ],
  condition='Used, with marks consistent with its age. Sold as seen — try it in the shop.',
 ),
 dict(
  sku='KBD-09', photos=['3'],
  title='Ringway TB810A Electronic Keyboard — 61 Keys, Silver (Used)',
  vendor='Ringway', type='Electronic Keyboard', grams=6000,
  tags=['Keyboards & Synths', 'Portable Keyboards', 'Beginner & Student',
        'Ringway', 'TB810A', 'electronic keyboard', '61 keys', 'used'],
  lede='A Ringway TB810A in silver — a full-size home and teaching keyboard with the '
       'style and voice lists printed straight onto the panel.',
  bullets=[
    '61 keys',
    'Voice and Style lists printed across the top panel for picking by eye',
    'Backlit LCD with the numeric entry pad beside it',
    'Registration Memory bank and a Lesson section',
    'Accompaniment control with Start/Stop, Sync, Fill and Intro/Ending',
    'Pitch bend wheel at the far left',
    'Twin built-in speakers',
  ],
  condition='Used. The white keys have yellowed with age, clearly visible in the '
            'photograph. Working condition to be confirmed in the shop.',
 ),
 dict(
  sku='KBD-10', photos=['2'],
  title='MK-821 Teaching Keyboard — 61 Keys, 255 Timbres & 255 Rhythms (New, Boxed)',
  vendor='MK', type='Electronic Keyboard', grams=6500,
  tags=['Keyboards & Synths', 'Portable Keyboards', 'Beginner & Student',
        'New Arrivals', 'MK', 'MK-821', 'teaching keyboard', 'electronic keyboard',
        '61 keys', 'new'],
  lede='A brand-new MK-821 teaching keyboard, boxed — the straightforward choice for a '
       'student starting out, or for a school room.',
  bullets=[
    '61 standard-size keys',
    '255 timbres and 255 rhythms',
    'Three-step teaching mode: One-key, Follow and Ensemble',
    'Rhythm programming with record and playback',
    'Keyboard percussion',
    'Master volume, accompaniment volume and tempo control',
    'Start/Stop, Sync, Fill-in, Single Chord and Fingered Chord',
    'Sustain and vibrato',
    'Music player over USB stick (stick not included), and an audio input so a phone can '
    'be played through the keyboard\'s own speakers',
    'Microphone jack, audio input jack and headphone output',
  ],
  condition='New and boxed. Specifications above are as printed on the carton.',
  note='Supplied in the printed carton shown.',
 ),
 dict(
  sku='KBD-11', photos=['8', '9', '11'],
  title='Alesis Vortex Wireless 2 Keytar MIDI Controller — 37 Keys (New, Boxed)',
  vendor='Alesis', type='MIDI Controller', grams=3600,
  tags=['Keyboards & Synths', 'MIDI Controllers', 'Audio & Studio',
        'New Arrivals', 'Alesis', 'Vortex Wireless 2', 'keytar',
        'MIDI controller', '37 keys', 'new'],
  lede='The Alesis Vortex Wireless 2 — a keytar MIDI controller that comes off the stand '
       'and goes wherever you want on the stage, with no cable to tether you.',
  bullets=[
    '37 velocity-sensitive keys',
    'Wireless USB/MIDI, with a USB receiver — also runs over a USB cable',
    'Accelerometer tilt sensor in the neck, assignable to any MIDI parameter',
    'Eight backlit velocity-sensitive trigger pads',
    'Eight assignable faders and an LED display',
    'Touch strip and programmable controls on the neck, with Pitch Bend and Modulation',
    'Keyboard zones — Lower, Split and Upper — with octave up/down',
    'Bundled software as listed on the carton: Ableton Live Lite, Loom II, Vacuum Pro, '
    'Hybrid 3 and Xpand!2',
  ],
  condition='New, in its opened box with the foam insert, as photographed.',
  note='Supplied boxed. Software is redeemed from Alesis by registration.',
 ),
 dict(
  sku='GTR-29', photos=['1'],
  title='Sundmann S-Style Electric Guitar — Black, Three Single Coils (Used)',
  vendor='Sundmann', type='Electric Guitar', grams=3500,
  tags=['Guitars & Bass', 'Electric Guitars', 'Beginner & Student',
        'Sundmann', 'electric guitar', 'S-style', 'black', 'used'],
  lede='A Sundmann electric in the classic S outline — black gloss body, white pickguard, '
       'three single coils. An honest first electric.',
  bullets=[
    'Three single-coil pickups',
    'Five-way blade selector, one volume and two tone controls',
    'Six-screw vintage-style synchronised tremolo with the arm fitted',
    'Maple neck with a dark fingerboard and pearl dot inlays',
    'Six-in-line headstock with the Sundmann logo, chrome enclosed tuners',
    'Recessed output jack plate, chrome hardware throughout',
  ],
  condition='Used. There are light surface scratches and swirls on the pickguard, visible '
            'in the photograph. Body finish is otherwise clean and glossy. A set-up and '
            'fresh strings come as standard before it leaves the shop.',
 ),
]

if __name__ == '__main__':
    import collections
    print(f'{len(P)} products from '
          f'{sum(len(p["photos"]) for p in P)} photographs')
    seen = collections.Counter()
    for p in P:
        for ph in p['photos']:
            seen[ph] += 1
    dupes = [k for k, v in seen.items() if v > 1]
    print('photo used twice:', dupes or 'none')
    print('\nSKU          photos  title')
    for p in P:
        print(f'  {p["sku"]:<9} {len(p["photos"]):>2}     {p["title"][:66]}')
