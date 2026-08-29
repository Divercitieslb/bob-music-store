# -*- coding: utf-8 -*-
"""New products identified from the WhatsApp drop.

Each entry: sku -> dict(cand=[indices into cand.json], title, type, vendor,
tags, body, seo). Candidate indices refer to the reviewed contact sheets.

EXTRA_IMAGES attaches a WhatsApp photo to a product that is already listed
(a second angle, or the unit next to its box).
DUPES are photos of items already in the catalogue - not imported.
"""

# candidate index -> existing SKU it is simply another photo of
EXTRA_IMAGES = {
    7:  'PA-33',    # Joyo JT-01 tuner, boxed
    17: 'PA-28',    # MDR-7 reverb pedal, unit
    22: 'GEAR-13',  # mpm PS15 sustain pedal, unit
    31: 'PA-29',    # Mooer GE100, on stand
    6:  'ACC-09',   # Paolo Soprani, top-down detail
}

# candidate indices that duplicate an existing photo outright
DUPES = {69: 'DRM-38', 70: 'DRM-37', 71: 'DRM-42', 72: 'DRM-53', 73: 'GEAR-21'}

NEW = {}


def P(sku, cand, title, type_, vendor, tags, body, **kw):
    NEW[sku] = dict(cand=cand, title=title, type=type_, vendor=vendor,
                    tags=tags, body=body, **kw)


# ---------------------------------------------------------------- guitars
P('GTR-25', [0], 'Warlock-Style Electric Guitar — Gloss Blue, Sharp-Horn Body',
  'Electric Guitar', 'Unbranded',
  'electric guitar, metal guitar, warlock, pointed body, blue, rock',
  'A pointed "warlock" style electric guitar in gloss blue — the shape metal and hard-rock players reach for. '
  'Twin humbuckers, bolt-on neck with a rosewood-look fingerboard and dot inlays, three-way selector with volume '
  'and tone, and a fixed bridge with through-body stringing that keeps tuning steady under heavy playing.')

P('GTR-26', [1], 'Warlock-Style Electric Bass — 4-String, Satin Black',
  'Bass Guitar', 'Unbranded',
  'bass guitar, electric bass, 4-string, metal bass, warlock, black',
  'A four-string electric bass built on the same aggressive pointed body as the warlock guitars, finished in satin '
  'black. Long-scale bolt-on neck, split/single pickup pairing with volume and tone controls, and a solid bridge '
  'with individual saddle adjustment. A stage-ready bass for rock and metal players who want the look to match.')

P('GTR-27', [2], 'Flying V Electric Guitar — Gloss Red',
  'Electric Guitar', 'Unbranded',
  'electric guitar, flying v, v-shape, red, rock, metal',
  'A classic V-shape electric guitar in gloss red with cream binding. Twin humbuckers deliver thick rhythm tone and '
  'a cutting lead voice, the bolt-on neck gives easy upper-fret access, and the through-body bridge holds tuning. '
  'The V body sits naturally against the leg when seated and looks unmistakable on stage.')

P('GTR-28', [3], 'Beast-Style Electric Guitar — Gloss Black, Multi-Point Body',
  'Electric Guitar', 'Unbranded',
  'electric guitar, metal guitar, beast, pointed body, black, rock',
  'An extreme multi-point "beast" body in gloss black — one of the most striking shapes on the wall. Twin humbuckers '
  'with three-way switching, bolt-on neck with dot-inlaid fingerboard, and a fixed bridge. Built for players who want '
  'maximum stage presence with a straightforward, reliable electric platform underneath.')

# ---------------------------------------------------------------- wind
P('WND-06', [33, 4], 'Mendini by Cecilio Alto Saxophone — Black Lacquer with Gold Keys, Full Outfit',
  'Saxophone', 'Mendini by Cecilio',
  'saxophone, alto sax, mendini, cecilio, black lacquer, student sax, wind, outfit',
  'A Mendini by Cecilio alto saxophone in black lacquer with contrasting gold-lacquer keywork — a genuinely handsome '
  'student horn. Supplied as a complete outfit in its fitted hard case: mouthpiece with ligature and cap, neck strap, '
  'cleaning cloth and swab, cork grease, a pack of reeds and a clip-on chromatic tuner. Ribbed construction, adjustable '
  'thumb rest and leather pads with metal resonators. Everything a starting player needs in one box.')

P('WND-07', [30], 'Pan Flute Pair — Curved Bamboo, Student Sizes',
  'Pan Flute', 'Handmade',
  'pan flute, panpipes, bamboo, folk, wind, handmade, world instrument',
  'A pair of curved bamboo pan flutes bound with cane and cord in the traditional way. The graduated pipes give a '
  'clear, breathy tone that sits beautifully in folk and world music, and the curved arrangement puts every pipe '
  'within easy reach of the lips. No keys, no reeds — just breath and a row of tuned pipes.')

P('WND-08', [32], 'Brass Bugle on Wooden Display Base — Polished Lacquer',
  'Bugle', 'Unbranded',
  'bugle, brass, horn, display, decorative, wind, collectible',
  'A polished brass bugle mounted on a turned wooden base. The classic single-coil cavalry shape with a flared bell '
  'and a fitted mouthpiece — playable for calls and fanfares, and equally at home as a display piece on a shelf or '
  'counter. The lacquered finish keeps the brass bright with minimal polishing.')

P('WND-09', [34], 'Large Curved Pan Flute — Wide-Bore Bamboo, Concert Size',
  'Pan Flute', 'Handmade',
  'pan flute, panpipes, bamboo, concert, folk, wind, handmade',
  'A large concert-size pan flute with a deep curve and a wide row of bamboo pipes, giving a much fuller and lower '
  'voice than the student sizes. The pipes are bound and lacquered, with the curve set so the whole range stays under '
  'the player\'s lips in one sweep. A serious folk instrument with real projection.')

P('WND-10', [35], 'Reed Ney / Kaval Set — Assorted Keys, Natural Cane',
  'Ney', 'Handmade',
  'ney, kaval, reed flute, cane, arabic, turkish, wind, world instrument, set',
  'A set of natural cane reed flutes in assorted keys — the ney of Arabic and Turkish music, played by directing '
  'breath across the rim rather than through a fipple. Each pipe is cut and burnished by hand, so the grain and colour '
  'vary from piece to piece. Sold as the set pictured; ask us if you need a specific key on its own.')

P('WND-11', [36], 'Bamboo Ney Flutes with Fitted Mouthpieces — Pair',
  'Ney', 'Handmade',
  'ney, reed flute, bamboo, mouthpiece, arabic, turkish, wind, world instrument',
  'A pair of bamboo ney flutes fitted with turned mouthpieces, which make the instrument far easier to sound than a '
  'bare-rim ney — a good route in for players coming from recorder or Western flute. Bound at the joints for stability '
  'and finished by hand, with the warm, airy tone the ney is loved for.')

P('WND-12', [37], 'Silver-Plated Concert Flute — C Foot, with Case',
  'Flute', 'Unbranded',
  'flute, concert flute, silver plated, student flute, orchestral, wind',
  'A silver-plated concert flute in C with closed-hole keywork — the standard student configuration, and the easiest '
  'route into orchestral and band playing. Offset G, C foot joint, and drawn tone holes. Supplied with its case, '
  'cleaning rod and cloth. Set up and checked before it leaves the shop.')

P('WND-13', [38], 'Silver-Plated Concert Flute — Student Model, Second Unit',
  'Flute', 'Unbranded',
  'flute, concert flute, silver plated, student flute, orchestral, wind',
  'A second silver-plated student concert flute in C, closed-hole with an offset G. Light, even key action and a '
  'responsive headjoint that speaks easily for a beginner. Comes with case and cleaning rod. Ideal as a school or '
  'second instrument.')

P('WND-14', [39], 'Ney Reed Flute — Single, Wrapped Grip',
  'Ney', 'Handmade',
  'ney, reed flute, cane, arabic, turkish, wind, world instrument, handmade',
  'A single cane ney with a bound and wrapped grip at the playing position, which protects the cane and steadies the '
  'hand. Traditional seven-hole layout (six front, one thumb). Played at an angle across the rim, it gives the breathy, '
  'vocal tone that carries so much of Arabic and Sufi music.')

P('WND-15', [40], 'Soprano Recorders in C — Cream, Three-Piece (Set of 3)',
  'Recorder', 'Unbranded',
  'recorder, soprano recorder, school recorder, student, wind, set, beginner',
  'Three cream soprano recorders in C, three-piece construction with a tapered bore and German fingering. Joints are '
  'greased and fit snugly so tuning can be adjusted at the head. The obvious first wind instrument for a child — '
  'cheap to replace, easy to clean, and genuinely in tune.')

P('WND-16', [41], 'Hand-Painted Soprano Recorders — Blue, Red & Green (Set of 3)',
  'Recorder', 'Handmade',
  'recorder, soprano recorder, hand painted, colourful, student, wind, set, gift',
  'Three soprano recorders finished by hand in blue, red and green with painted floral panels and contrasting tips. '
  'They play as properly as the plain ones — three-piece, in C, with a clean fipple — but they look like something '
  'worth keeping. A good gift for a child starting out.')

P('WND-17', [42], 'Soprano Recorder Assortment — Wood & Coloured, Boxed Selection',
  'Recorder', 'Unbranded',
  'recorder, soprano recorder, assortment, student, wind, set, boxed',
  'A mixed selection of soprano recorders — natural wood and painted finishes — supplied with original sleeves and '
  'boxes. Sizes and colours as pictured. A practical bundle for a school, a teacher, or anyone equipping a group of '
  'beginners at once.')

P('WND-18', [43], 'Wooden Soprano Recorders — Natural & Two-Tone (Set of 3)',
  'Recorder', 'Handmade',
  'recorder, soprano recorder, wooden recorder, natural wood, student, wind, set',
  'Three wooden soprano recorders in natural and two-tone finishes. Wood gives a warmer, rounder tone than plastic and '
  'a slightly softer response under the fingers — the step up a player makes once they are past the first year. '
  'Three-piece with turned decorative rings and greased joints.')

# ---------------------------------------------------------------- percussion
_DARB = [
    ('DRM-56', 5,  'Blue & Magenta Diamond Mosaic',
     'a vivid cobalt-blue ground with magenta and white diamond columns running the full height of the shell'),
    ('DRM-57', 58, 'Cream Rosette Medallions & Honeycomb Neck',
     'cream mother-of-pearl mosaic with two large rosette medallions on the bowl and a fine honeycomb lattice down the waist'),
    ('DRM-58', 59, 'Monochrome Diamond Lattice',
     'a dense black-and-white diamond lattice covering the entire shell, one of the crispest geometric patterns in the set'),
    ('DRM-59', 60, 'Cream Snowflake & Star Motifs',
     'a pale cream ground scattered with small black snowflake and star motifs, with banded borders at the head and foot'),
    ('DRM-60', 61, 'Stone Cream with Diagonal Colour Stripe',
     'a stone-cream mosaic with a single diagonal stripe of red, blue and gold tesserae sweeping across the waist'),
    ('DRM-61', 62, 'Cream with Blue & Red Diamond Column',
     'a cream shell with a central column of blue, red and gold diamonds framed by fine black borders'),
    ('DRM-62', 63, 'Red & Black Checkerboard with Circle Medallions',
     'a bold red and black checkerboard band above a row of circular medallions on a cream ground'),
    ('DRM-63', 64, 'Cream with Blue & Gold Flower Medallions',
     'a cream mosaic centred on large blue and gold flower medallions, with a fine chequered rim band'),
    ('DRM-64', 65, 'Teal Crackle Lacquer',
     'a turquoise crackle-lacquer finish over a pale ground, giving a weathered ceramic look with no mosaic at all'),
    ('DRM-65', 66, 'Gloss Black, Plain Lacquer',
     'a plain gloss black lacquer with no ornament — the quiet one, and the one working players tend to pick'),
    ('DRM-66', 67, 'Cream with Deep Red Rosettes',
     'a cream ground with large deep-red rosette medallions and a wide patterned collar at the head'),
    ('DRM-67', 68, 'Cream Arrow Panels & Star Lattice',
     'cream mosaic with tall arrow-shaped panels rising from the foot and a star lattice across the bowl'),
]
for sku, ci, name, desc in _DARB:
    P(sku, [ci], f'Mosaic Darbuka — {name}', 'Darbuka', 'Handmade',
      'darbuka, doumbek, tabla, arabic percussion, mosaic, hand drum, percussion, middle eastern',
      f'A hand-decorated darbuka (doumbek) with {desc}. Cast aluminium shell with a tuneable synthetic head and a '
      'bolt-tuned rim, so it holds pitch through changes in humidity — the reason these travel and gig so well. '
      'The mosaic is applied and finished by hand, so no two shells are ever identical.')

# ---------------------------------------------------------------- audio & studio
P('PA-36', [14], 'HiPower AR-50 Professional Dynamic Headset Microphone',
  'Microphone', 'HiPower',
  'microphone, headset microphone, dynamic, hands free, presentation, vocal',
  'A dynamic headset microphone on an adjustable over-ear frame — hands free for presenters, fitness instructors, '
  'worship leaders and performers who need to move. Cardioid capsule for good rejection of stage spill, foam windshield '
  'included, and a standard jack termination. Supplied sealed on its retail card.')

P('PA-37', [15], 'Lavalier Clip-On Microphone — Smartphone & Camera Compatible',
  'Microphone', 'Unbranded',
  'microphone, lavalier, lapel mic, clip on, smartphone, content creation, video',
  'A clip-on lavalier microphone for phones, tablets and cameras — the quickest way to make spoken-word video sound '
  'far better than the built-in mic. Omnidirectional capsule on a long cable with a sprung lapel clip and windshield. '
  'Works with iOS and Android handsets, laptops and most compact cameras.')

P('PA-38', [16], 'Coron Phaser Effects Pedal — Orange',
  'Effects Pedal', 'Coron',
  'effects pedal, phaser, guitar pedal, modulation, stompbox, coron',
  'A compact analogue-voiced phaser in a bright orange enclosure with Depth, Rate and Feedback controls plus a level '
  'trim — enough range to go from a slow, syrupy sweep to a fast, vocal warble. True stompbox format with a metal '
  'footswitch and standard in/out jacks.')

P('PA-39', [18], 'Fender Two-Button Footswitch — Channel Select & Reverb',
  'Footswitch', 'Fender',
  'footswitch, fender, channel select, reverb, amplifier accessory, pedal',
  'A genuine Fender two-button footswitch for channel selection and reverb, in the ribbed chrome-and-black housing. '
  'Fits the many Fender combos and heads that use the two-button jack, freeing you to switch clean-to-drive and kick '
  'reverb in and out without leaving the mic.')

P('PA-40', [19], 'Carlsbro Single Footswitch with Captive Cable',
  'Footswitch', 'Carlsbro',
  'footswitch, carlsbro, amplifier accessory, channel switch, pedal',
  'A single-button Carlsbro footswitch on a captive cable — the standard latching switch for channel or effect '
  'selection on Carlsbro amplifiers and many other makes using a mono jack. Steel housing with a rubber base so it '
  'stays where you put it.')

P('PA-41', [21], 'Five-Button Footswitch Controller — DIN Connection',
  'Footswitch', 'Unbranded',
  'footswitch, 5 button, din, amplifier accessory, keyboard, controller',
  'A five-way footswitch controller on a multi-pin DIN cable, numbered 1 to 5 — for amplifiers, keyboard arrangers and '
  'rack units that need more than simple channel switching. Long captive lead, low-profile steel chassis and clearly '
  'marked switches you can find in the dark.')

P('PA-42', [24], 'Carlsbro GLX Three-Button Footswitch',
  'Footswitch', 'Carlsbro',
  'footswitch, carlsbro, glx, 3 button, amplifier accessory',
  'The three-button Carlsbro GLX footswitch with status LEDs above each switch, on a long captive cable. Designed for '
  'the GLX amplifier range to select channels and engage effects, with the LEDs telling you what is live at a glance.')

P('PA-43', [25], 'BOSS CH-1 Super Chorus Pedal',
  'Effects Pedal', 'BOSS',
  'effects pedal, boss, ch-1, super chorus, chorus, modulation, stompbox',
  'The BOSS CH-1 Super Chorus — the stereo chorus that defined the sound on countless records. E.Level, EQ, Rate and '
  'Depth controls take it from a gentle shimmer to a deep, glassy swirl, and the stereo outputs open the sound right '
  'up through two amps. Built in the famously indestructible BOSS compact enclosure.')

P('PA-44', [26], 'BOSS RC-2 Loop Station',
  'Effects Pedal', 'BOSS',
  'effects pedal, boss, rc-2, loop station, looper, stompbox, recording',
  'The BOSS RC-2 Loop Station — up to 16 minutes of stereo recording across 11 memories, with undo/redo, a built-in '
  'rhythm guide and Auto Recording that starts the moment you play. Everything runs from one footswitch, so it works '
  'as a practice tool, a writing pad and a full one-person live rig.')

P('PA-45', [27], 'Roland GO:MIXER — Audio Mixer for Smartphones',
  'Audio Interface', 'Roland',
  'audio interface, roland, go mixer, smartphone, recording, content creation, mixer',
  'The Roland GO:MIXER connects guitars, mics, keyboards and line sources straight into a smartphone for clean, '
  'multi-input recording — no adapters, no computer. Up to nine inputs mixed with physical knobs, powered by the phone '
  'itself, and small enough to live in a gig bag. The tool for musicians making video.')

P('PA-46', [28], 'Kelfar Technologies AK-2 Pro MIDI Wind / Breath Controller',
  'MIDI Controller', 'Kelfar Technologies',
  'midi controller, wind controller, breath controller, kelfar, ak-2 pro, arabic music, quarter tone',
  'The Kelfar AK-2 Pro breath controller — a Lebanese-made MIDI wind instrument with a world-scale tuning panel, so '
  'quarter-tones and Arabic maqam scales are available directly from the front panel. Breath-driven expression into any '
  'MIDI sound module, with per-note tuning buttons across the octave. Rare, and genuinely built for this repertoire.')

P('PA-47', [44], 'ZQS6137 Wireless Portable Speaker — 6.5" Super Bass',
  'Speaker', 'Unbranded',
  'speaker, portable speaker, bluetooth, wireless, party speaker, pa, rechargeable',
  'A 6.5-inch rechargeable party speaker with Bluetooth, USB and card playback, an LED-lit grille and a carry handle. '
  'Loud enough for a garden, a classroom or a small function, and it runs off its internal battery for hours. Supplied '
  'boxed with charging lead and remote.')

P('PA-48', [45, 46], 'Joyo JPA882 Acoustic & Outdoor Guitar Amplifier — Rechargeable',
  'Amplifier', 'Joyo',
  'amplifier, guitar amp, acoustic amp, joyo, jpa882, battery powered, busking, portable, pa',
  'The Joyo JPA882 is a rechargeable acoustic and outdoor amplifier built for busking and small events. Two instrument '
  'inputs and two microphone channels each with their own volume and two-band EQ, plus master reverb, delay and an '
  'activator control. Battery powered with a carry handle — a complete little PA you can pick up in one hand.')

P('PA-49', [47], 'Laney GC-60A Acoustic Guitar Combo Amplifier — Stereo Chorus',
  'Amplifier', 'Laney',
  'amplifier, guitar amp, acoustic amp, laney, gc-60a, combo, stereo chorus, used',
  'The Laney GC-60A acoustic combo — separate Electro and Acoustic channels each with their own EQ, plus onboard '
  'stereo chorus and a dedicated microphone input with its own controls. Designed so a singer-guitarist can run the '
  'whole show from one box. A well-regarded British-designed amp, in good working order.')

P('PA-50', [48], 'Yada HDT-22 Portable Teaching Amplifier with Wireless Microphone',
  'Speaker', 'Yada',
  'speaker, teaching amplifier, wireless microphone, portable pa, classroom, tour guide, boxed',
  'A portable teaching amplifier with a wireless microphone — the classroom and tour-guide standard. Belt-clip or '
  'handheld transmitter, rechargeable battery, and a shoulder strap so it goes where the teacher goes. Line input for '
  'backing tracks. Supplied boxed and complete.')

P('PA-51', [49], 'Leem KA-1210 Pro Multiple Amplifier — Guitar, Bass & Keyboard Channels',
  'Amplifier', 'Leem',
  'amplifier, combo amp, leem, ka-1210, keyboard amp, bass amp, multi channel, used',
  'The Leem KA-1210 is a genuinely multi-purpose combo — separate guitar/bass and keyboard channels plus two '
  'microphone inputs, each with their own EQ and reverb, feeding one speaker. For rehearsal rooms, churches and '
  'schools that need one amplifier to cover several jobs, it is hard to beat.')

P('PA-52', [50], 'Edison FA-1200 Bluetooth PA Speaker System — Multi-Function',
  'Speaker', 'Edison',
  'speaker, pa speaker, bluetooth, edison, fa-1200, tower speaker, party, boxed',
  'The Edison FA-1200 multi-function Bluetooth speaker and PA system, with LED lighting columns, wireless streaming, '
  'USB and card playback and microphone inputs. Built for parties, functions and small venues. Supplied boxed with its '
  'accessories.')

P('PA-53', [51], 'Elementa Hi-Fi PA Speaker Cabinet — Full-Range Passive',
  'Speaker', 'Elementa',
  'speaker, pa speaker, passive speaker, cabinet, full range, elementa, used',
  'A full-range passive PA cabinet from the Elementa Hi-Fi system, with a perforated metal grille over the driver and '
  'a ported enclosure. Pole-mountable and built to be driven from any standard power amplifier — a straightforward, '
  'solid box for fixed installation or hire stock.')

P('PA-54', [52], 'Epiphone Electar-10 Guitar Practice Amplifier',
  'Amplifier', 'Epiphone',
  'amplifier, guitar amp, practice amp, epiphone, electar 10, combo, used',
  'The Epiphone Electar-10 practice combo — volume, treble and bass, an aux input for playing along and a headphone '
  'socket for silent practice. Compact enough for a bedroom and loud enough for a lesson. A dependable first amplifier '
  'from a name that needs no introduction.')

P('PA-55', [54], 'Audio-Technica AT2020USB Cardioid Condenser Microphone',
  'Microphone', 'Audio-Technica',
  'microphone, condenser microphone, usb microphone, audio technica, at2020usb, podcast, streaming, recording, boxed',
  'The Audio-Technica AT2020USB — the studio condenser that became the default for podcasting, streaming and home '
  'vocal recording. Cardioid pattern for good room rejection, built-in USB converter so it goes straight into a '
  'computer, and the honest, detailed voicing the AT2020 is known for. Supplied boxed with stand mount and tripod.')

P('PA-56', [55], 'Professional Condenser Microphone Kit — Boom Arm, Shock Mount & Pop Filter',
  'Microphone', 'Unbranded',
  'microphone, condenser microphone, recording kit, boom arm, shock mount, pop filter, podcast, streaming, boxed',
  'A complete condenser microphone kit for recording and streaming: large-diaphragm capsule, scissor boom arm, '
  'elastic shock mount, pop filter and cables. Everything needed to get a clean vocal or voice-over take at a desk, '
  'in one box, at a fraction of the cost of buying the parts separately.')

P('PA-57', [56], 'NewRixing NR-6011M Outdoor Wireless Speaker with Twin Microphones',
  'Speaker', 'NewRixing',
  'speaker, portable speaker, bluetooth, wireless microphone, karaoke, party speaker, outdoor, boxed',
  'The NewRixing NR-6011M portable speaker with two wireless microphones — a self-contained karaoke and announcement '
  'rig. Bluetooth 5.0, USB and card playback, FM radio, aux input, LED display and around seven hours of playback from '
  'the internal battery. Shoulder strap included. Supplied boxed and sealed.')

# ---------------------------------------------------------------- accessories
P('GEAR-16', [8], 'KQ-2 Violin & Instrument Piezo Pickup with Volume Control',
  'Pickup', 'Unbranded',
  'pickup, piezo pickup, violin pickup, oud pickup, amplification, accessory, boxed',
  'A clip-on piezo pickup with an inline volume and tone control — the simple way to amplify a violin, oud, saz, '
  'zither or bouzouki without any modification to the instrument. Sticks or clips to the body, runs to a standard '
  'jack, and comes off cleanly when you are done.')

P('GEAR-17', [9], 'Yamaha YT-100 Guitar & Bass Auto Tuner',
  'Tuner', 'Yamaha',
  'tuner, guitar tuner, bass tuner, yamaha, yt-100, chromatic, accessory',
  'The Yamaha YT-100 auto tuner for guitar and bass — LED indication across every string of both instruments, a built-in '
  'microphone for acoustic use and a jack input for electrics. Simple, fast and accurate, from a maker whose tuners '
  'have a long reputation for holding calibration.')

P('GEAR-18', [10], 'Fender FT-004 Clip-On Chromatic Tuner',
  'Tuner', 'Fender',
  'tuner, clip on tuner, chromatic tuner, fender, ft-004, accessory',
  'The Fender FT-004 clip-on chromatic tuner, with a bright colour display on a ball-joint clip that rotates to face '
  'you from any angle. It reads vibration through the headstock, so it tunes accurately in a noisy room where a '
  'microphone tuner cannot. Fits guitar, bass, ukulele, oud and violin.')

P('GEAR-19', [11], 'Maxtone BC-650 Chromatic Tuner — Guitar, Bass & Microphone',
  'Tuner', 'Maxtone',
  'tuner, chromatic tuner, guitar tuner, bass tuner, maxtone, bc-650, accessory',
  'The Maxtone BC-650 chromatic tuner with LED indication for every guitar and bass string, a built-in microphone and '
  'a jack input. Clear per-string markings mean beginners can tune without knowing note names yet — one of the reasons '
  'we keep recommending it for first guitars.')

P('GEAR-20', [12], 'Chromatic Clip-On Tuner with Backlit Display',
  'Tuner', 'Unbranded',
  'tuner, clip on tuner, chromatic tuner, backlit, accessory',
  'A chromatic clip-on tuner with a backlit display and a sprung, rotating clip. Chromatic mode tunes any instrument '
  'to any note, with dedicated guitar, bass, violin and ukulele modes for quicker work. Runs for months on a coin cell '
  'and folds flat against the headstock.')

P('GEAR-21', [13, 73], 'AD-20 Acoustic Guitar Transducer Pickup — Soundhole Mount',
  'Pickup', 'Unbranded',
  'pickup, transducer, acoustic guitar pickup, soundhole pickup, amplification, accessory',
  'The AD-20 transducer pickup mounts inside the soundhole of an acoustic guitar and runs to a standard jack — no '
  'drilling, no permanent fitting, and off again in seconds. A clean, feedback-resistant way to plug an acoustic into '
  'an amp or PA. Supplied sealed on its retail card with cable and fittings.')

P('GEAR-22', [23], 'Microphone Floor Stand — Heavy Round Base, Boxed',
  'Microphone Stand', 'Unbranded',
  'microphone stand, mic stand, floor stand, round base, accessory, boxed',
  'A heavy-duty microphone floor stand with a weighted round base and a telescopic upright — the stable choice for '
  'conference rooms, churches and stages where a tripod would be a trip hazard. Supplied boxed with its mic clip and '
  'standard thread adapter.')

P('GEAR-23', [29], 'Professional Microphone Stand — Telescopic Boom, Boxed',
  'Microphone Stand', 'Unbranded',
  'microphone stand, mic stand, boom stand, telescopic, accessory, boxed',
  'A professional telescopic boom microphone stand with a folding tripod base — the standard stand for stage, studio '
  'and rehearsal. The boom arm swings and extends to place the capsule exactly where it needs to be, over a kit or in '
  'front of a seated player. Supplied boxed with clip and adapter.')

P('GEAR-24', [53, 57], 'E622 Padded Guitar Strap — Wide Webbing with Leather Ends',
  'Guitar Strap', 'Unbranded',
  'guitar strap, padded strap, strap, accessory, boxed',
  'A wide padded guitar strap on strong webbing with reinforced leather-look ends and a sliding length adjuster. The '
  'padding spreads the weight of a heavier electric or bass across the shoulder, which is what saves your back over a '
  'long set. Boxed, and available in the colours shown.',
  option_name='Colour', option_values=['Black', 'Blue'])

# ---------------------------------------------------------------- strings
P('STR-27', [74], 'IRIN V68 Violin Strings — Cupronickel Wound, Full Set',
  'Violin Strings', 'IRIN',
  'strings, violin strings, irin, v68, cupronickel, 4/4, set',
  'A full set of IRIN V68 violin strings, cupronickel wound over a steel core — bright, stable and quick to settle, '
  'which is exactly what a student or a busy teaching studio wants. Sized for 4/4 and 3/4 instruments with ball ends.')

P('STR-28', [75], "D'Orazio 4-36 Classical Guitar Strings — Silver-Plated Nylon, Normal Tension",
  'Guitar Strings', "D'Orazio",
  'strings, classical guitar strings, nylon strings, d orazio, normal tension, italian, set',
  "A full set of D'Orazio 4-36 classical guitar strings — clear nylon trebles with silver-plated wound basses at "
  'normal tension. Made in Italy by a string house working since 1859, with the warm, round voice that suits Spanish '
  'and Arabic classical repertoire alike.')

P('STR-29', [76], "D'Orazio 4-40 Classical Guitar Strings — Silver-Plated Nylon, Hard Tension",
  'Guitar Strings', "D'Orazio",
  'strings, classical guitar strings, nylon strings, d orazio, hard tension, italian, set',
  "The hard-tension version of the D'Orazio classical set — silver-plated wound basses and clear nylon trebles at a "
  'higher tension for more volume, more attack and a firmer feel under the right hand. The set to reach for if normal '
  'tension feels slack or you play with a heavy touch.')

P('STR-30', [77], "D'Orazio 1-40 Classical Guitar Strings — Clear Nylon, Full Set",
  'Guitar Strings', "D'Orazio",
  'strings, classical guitar strings, nylon strings, clear nylon, d orazio, italian, set',
  "A full D'Orazio 1-40 classical set with clear nylon trebles — bright and clean, with even response across the "
  'fingerboard. Italian-made and consistently well finished, so intonation stays true right up the neck.')

P('STR-31', [78], "D'Orazio 047 Acoustic Guitar Strings — Bronze 80/20, Round Wound",
  'Guitar Strings', "D'Orazio",
  'strings, acoustic guitar strings, bronze strings, 80/20 bronze, d orazio, italian, set',
  "A full set of D'Orazio 047 acoustic guitar strings in 80/20 bronze, round wound — crisp, loud and bright, the "
  'classic bronze voice for strummed rhythm and recording. Italian made, cleanly wound and evenly tensioned across '
  'the set.')

P('PA-58', [20], 'TCO-1 Compressor / Sustainer Pedal — Attack, Sustain & Level',
  'Effects Pedal', 'Coron',
  'effects pedal, compressor, sustainer, guitar pedal, stompbox, vintage, used',
  'A vintage-style compressor and sustainer in a hammered metal enclosure, with Attack, Sustain and Level controls. '
  'Evens out picking dynamics and holds notes far longer than the guitar alone — the pedal behind clean funk chops '
  'and long, singing country bends. Well used, honestly worn, and still doing the job.')
