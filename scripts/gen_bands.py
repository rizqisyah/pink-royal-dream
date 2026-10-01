"""Generate src/lib/bands/*.ts from Frame 263's layer list.

Figma Frame 263 (2745:44), 596 x 16075. Every sprite below is in FRAME coordinates and
carries `z` = its index in Figma's child order (which is the paint order). The frame is
flat, so bands are cut by y here; each layer goes to the band its top edge falls in and
is rewritten to band-local y. `z` stays global, so layers that hang into a neighbouring
band still stack correctly against it (all bands share the sheet's stacking context).

Rotated layers: x/y/w/h is the axis-aligned box Figma's own code export positions, and
iw/ih is the unrotated sprite. See SLICING.md.

    python scripts/gen_bands.py
"""
import json
import os

BANDS = [  # name, top, height  (heights sum to 16075)
    ('hero', 0, 1110),
    ('quote', 1110, 1510),
    ('groom', 2620, 1530),
    ('bride', 4150, 1540),
    ('savedate', 5690, 1230),
    ('acara', 6920, 3040),
    ('gallery', 9960, 890),
    ('video', 10850, 430),
    ('gift', 11280, 810),
    ('rsvp', 12090, 690),
    ('wish', 12780, 1400),
    ('closing', 14180, 1895),
]

REGENCY = 'hero/parts/floral-regency.webp'
PASTEL = 'groom/parts/floral-pastel.webp'
CLOUD = 'groom/parts/cloud.webp'
BRANCH = 'quote/parts/floral-branch.webp'
PASTEL_BOX = dict(w=844.409, h=866.43, iw=521.78, ih=693, stack=6)
CLOUD_BOX = dict(w=551.515, h=280)
GLOW = ('drop-shadow(calc(-1 * var(--px)) calc(-15 * var(--px)) calc(17 * var(--px)) rgba(255, 247, 240, 0.41)) '
        'drop-shadow(calc(-4 * var(--px)) calc(-61 * var(--px)) calc(30 * var(--px)) rgba(255, 247, 240, 0.36)) '
        'drop-shadow(calc(-8 * var(--px)) calc(-137 * var(--px)) calc(41 * var(--px)) rgba(255, 247, 240, 0.21))')

# (z, node id, asset, x, y, w, h, extras)
L = [
    (1, '2756:647', 'hero/parts/floral-frame-top.webp', -89, -161, 756, 756, {}),
    (2, '2756:646', 'wish/parts/floral-frame-wishes.webp', -34, 13634, 677, 677, {}),
    (3, '2756:643', REGENCY, -215, 2826, 420, 420, dict(flipX=True)),
    (4, '2756:644', REGENCY, 381, 2826, 420, 420, {}),
    (5, '2751:573', 'hero/parts/floral-frame-top.webp', -79, 14832, 754, 754, {}),
    (6, '2751:570', 'closing/parts/watercolor-footer.webp', -269, 15252, 1132, 849, {}),
    (7, '2751:571', BRANCH, -244, 15085, 444.554, 167.032, dict(iw=438, ih=146, rotate=2.77)),
    (8, '2751:578', BRANCH, 399, 15085, 444.554, 167.032, dict(iw=438, ih=146, rotate=177.23, flipY=True)),
    (9, '2750:474', 'savedate/parts/countdown-illustration.webp', -50, 6046, 692, 692, {}),
    (10, '2748:402', 'groom/parts/profile-backdrop.webp', -43, 3003.18, 666.692, 467.216,
     dict(maskBox=dict(src='groom/parts/mask-profile.svg', x=47, y=14.819, w=595.5, h=439.181))),
    (11, '2750:449', 'groom/parts/profile-backdrop.webp', -45.69, 4587.18, 666.692, 467.216,
     dict(flipX=True, maskBox=dict(src='groom/parts/mask-profile.svg', x=24.192, y=14.819, w=595.5, h=439.181))),
    (12, '2748:394', 'groom/parts/floral-frame-profile.webp', -132, 2757, 860, 860, {}),
    (13, '2750:450', 'groom/parts/floral-frame-profile.webp', -150, 4341, 860, 860, {}),
    (14, '2746:363', 'hero/parts/arch-wedding.webp', -65, 306, 726, 635, dict(fit='fill')),
    # 15: 2747:386, the blurred haze rect — a CSS div in HeroSection.
    (16, '2748:419', 'groom/parts/groom-photo.webp', 48, 3053, 500, 500,
     dict(crop=dict(w=114.95, h=129.79, l=-5.67, t=-26.23))),
    (17, '2750:451', 'bride/parts/bride-photo.webp', 48, 4637, 500, 500,
     dict(crop=dict(w=100, h=113.44, l=-2.24, t=-9.34))),
    (18, '2745:69', 'quote/parts/quote-card.svg', 35.8, 1368, 525.407, 886, dict(fit='fill')),
    # 19: "Wedding Invitation", 20: "Bride & Groom" — text.
    (21, '2745:105', CLOUD, -137.52, 3425, *CLOUD_BOX.values(), dict(flipX=True, a=0.76)),
    (22, '2750:452', CLOUD, 164, 5009, *CLOUD_BOX.values(), dict(a=0.76)),
    (23, '2745:114', CLOUD, 230, 3484, *CLOUD_BOX.values(), {}),
    (24, '2750:453', CLOUD, -203.52, 5068, *CLOUD_BOX.values(), dict(flipX=True)),
    (25, '2745:115', CLOUD, 230, 3484, *CLOUD_BOX.values(), {}),
    (26, '2750:454', CLOUD, -203.52, 5068, *CLOUD_BOX.values(), dict(flipX=True)),
    (27, '2745:116', CLOUD, 223, 3457, *CLOUD_BOX.values(), {}),
    (28, '2750:455', CLOUD, -196.52, 5041, *CLOUD_BOX.values(), dict(flipX=True)),
    (29, '2748:399', CLOUD, -187, 3477, *CLOUD_BOX.values(), dict(stack=4)),
    (30, '2750:456', CLOUD, 213.48, 5061, *CLOUD_BOX.values(), dict(flipX=True, stack=4)),
    # 31: groom name block — text.
    (32, '2749:422', PASTEL, -519, 3496, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=140.22, flipY=True)),
    (33, '2749:432', PASTEL, -519, 3519, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=39.78)),
    # 34: bride name block — text.
    (35, '2745:167', 'savedate/parts/countdown-ellipse.svg', -120, 5961, 832, 1014, dict(fit='fill')),
    # 36 countdown, 37 "And", 38-41 gift — live.
    (42, '2751:588', 'closing/parts/closing-backdrop.webp', -79, 15265, 762, 491,
     dict(maskBox=dict(src='closing/parts/mask-closing.svg', x=215.873, y=36.394, w=321.67, h=453.208))),
    (43, '2745:284', 'video/parts/video-thumb.webp', 8, 10873, 584, 329,
     dict(radius=23, crop=dict(w=102.08, h=331.16, l=-1.07, t=-79.75))),
    # 44 "video prewed", 45 RSVP, 46 wishes, 47-49 thank-you copy — live.
    (50, '2747:381', REGENCY, -210, 88, 420, 420, dict(flipX=True)),
    (51, '2747:382', REGENCY, 386, 69, 420, 420, {}),
    (52, '2747:383', 'hero/parts/podium.webp', -49, 849, 694, 218, dict(fit='fill', filter=GLOW)),
    (53, '2751:580', 'hero/parts/couple-illustration.webp', 55, 15313, 480, 480,
     dict(maskBox=dict(src='closing/parts/mask-bride-groom.svg', x=86, y=0, w=322, h=430))),
    (54, '2746:364', 'hero/parts/couple-illustration.webp', 41, 482, 515, 515, {}),
    (55, '2747:384', REGENCY, 437, 782, 318, 318, {}),
    (56, '2747:385', REGENCY, -159, 782, 318, 318, dict(flipX=True)),
    (57, '2748:387', 'quote/parts/quote-frame.webp', -275, 1120, 1147, 1147, {}),
    # 58 the verse — text.
    (59, '2748:395', REGENCY, 355, 3206, 438, 438, {}),
    (60, '2750:469', REGENCY, -215, 4790, 438, 438, dict(flipX=True)),
    (61, '2748:396', REGENCY, -215, 3206, 438, 438, dict(flipX=True)),
    (62, '2750:470', REGENCY, 355, 4790, 438, 438, {}),
    # 63 "Mario", 64 "Amanda" — text.
    (65, '2749:436', PASTEL, 230, 3795, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=39.78)),
    (66, '2749:437', PASTEL, 230, 3818, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=140.22, flipY=True)),
    (67, '2755:611', PASTEL, 204, 9373, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=-39.78, flipY=True)),
    (68, '2755:612', PASTEL, 204, 9350, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=-140.22)),
    (69, '2755:617', PASTEL, -453, 9384, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=-140.22)),
    (70, '2755:618', PASTEL, -453, 9361, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=-39.78, flipY=True)),
    (71, '2755:604', PASTEL, -497, 6078, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=39.78)),
    (72, '2755:605', PASTEL, -497, 6101, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=140.22, flipY=True)),
    (73, '2755:607', PASTEL, 220, 6067, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=140.22, flipY=True)),
    (74, '2755:608', PASTEL, 220, 6090, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=39.78)),
    (75, '2750:539', PASTEL, 192, 8133, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=39.78)),
    (76, '2750:540', PASTEL, 192, 8156, PASTEL_BOX['w'], PASTEL_BOX['h'], dict(iw=521.78, ih=693, stack=6, rotate=140.22, flipY=True)),
    (77, '2749:431', 'quote/parts/quote-ornament.svg', 169, 2371, 258, 193, dict(fit='fill')),
    (78, '2750:472', BRANCH, -140, 1436, 438, 146, {}),
    (79, '2750:473', BRANCH, 298, 1436, 438, 146, dict(flipX=True)),
    (80, '2750:486', 'acara/parts/event-arch.webp', -207, 6948, 983, 1458, dict(fit='fill')),
    (81, '2750:525', 'acara/parts/event-arch.webp', -180, 8476, 983.011, 1458, dict(fit='fill', flipX=True)),
    (82, '2750:499', 'acara/parts/event-ellipse.svg', -131, 7582, 832, 1014, dict(fit='fill')),
    (83, '2750:526', 'acara/parts/event-ellipse.svg', -131, 9110, 832, 1014, dict(fit='fill')),
    (84, '2750:490', 'acara/parts/event-photo.webp', 41, 8013, 513, 311,
     dict(crop=dict(w=100.02, h=292.95, l=-0.01, t=-87.18))),
    (85, '2750:527', 'acara/parts/event-photo.webp', 41, 9541, 512.353, 311,
     dict(flipX=True, crop=dict(w=100.02, h=292.95, l=-0.01, t=-87.18))),
    (86, '2750:522', 'acara/parts/its-the-day.svg', 144, 6934, 439.289, 188.721, dict(fit='fill')),
    (87, '2750:528', 'acara/parts/its-the-day.svg', 41, 8406, 439.289, 188.721, dict(fit='fill')),
    # 88-89 event copy, 90-96 gallery, 97 gift's third card copy — live.
    (98, '2751:576', 'closing/parts/closing-arch.webp', 47, 15196, 504, 629, {}),
    (99, '2756:636', 'closing/parts/closing-floral.webp', 94, 15656, 408, 408, {}),
    # 100: 2745:324, the footer's #ffd1d4 bar — CSS. 101 credit — text.
    (102, '2752:596', 'closing/parts/swans.webp', -67, 15021, 325.047, 274.462,
     dict(iw=294, ih=234, rotate=-8.41, crop=dict(w=189.8, h=179.62, l=0, t=-41.95))),
    (103, '2752:597', 'closing/parts/swans.webp', 350, 14860, 279.796, 267.776,
     dict(iw=248.257, ih=234, rotate=-8.41, crop=dict(w=210.71, h=168.39, l=-107.7, t=-35.05))),
    (104, '2755:600', 'savedate/parts/border.webp', -28, 5711, 656.902, 367, {}),
    (105, '2755:619', 'wish/parts/wishes-footer.webp', -38, 13794, 830, 465, {}),
    (106, '2755:621', 'closing/parts/thankyou-ornament.webp', 241, 14215, 113.595, 141.592, {}),
    (107, '2755:625', 'hero/parts/title-ornament.svg', 103, 1130, 390.432, 67.026, dict(fit='fill')),
    (108, '2756:629', 'bride/parts/flying-swan.webp', 363, 4336, 233, 204, dict(fit='fill')),
    (109, '2756:630', 'savedate/parts/flying-swan-2.webp', 71, 6634, 369, 275,
     dict(flipX=True, crop=dict(w=100.17, h=178.57, l=-0.08, t=-78.57))),
    (110, '2756:632', 'closing/parts/thankyou-divider.svg', 128, 14394, 340, 58, dict(fit='fill')),
    # 111 "Save the Date", 112 hashtag — text.
]

ASSET_KEYS = {'src'}


def num(v):
    r = round(v, 3)
    return str(int(r)) if r == int(r) else str(r)


def ts(v, key=None):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (int, float)):
        return num(v)
    if isinstance(v, str):
        return f"assets['{v}']" if key in ASSET_KEYS else json.dumps(v)
    if isinstance(v, dict):
        return '{ ' + ', '.join(f'{k}: {ts(x, k)}' for k, x in v.items()) + ' }'
    raise TypeError(v)


def band_for(y):
    for name, top, h in BANDS:
        if top <= y < top + h:
            return name
    return BANDS[0][0]  # above the frame (negative y) belongs to the first band


root = os.path.join(os.path.dirname(__file__), '..', 'src', 'lib', 'bands')
os.makedirs(root, exist_ok=True)
for name, top, h in BANDS:
    rows = []
    for z, nid, src, x, y, w, hh, extra in sorted(L, key=lambda r: r[0]):
        if band_for(y) != name:
            continue
        fields = dict(z=z, id=nid, src=src, x=x, y=y - top, w=w, h=hh, **extra)
        rows.append('  ' + ts(fields) + ',')
    body = '\n'.join(rows)
    # A band whose content is all live (gallery, gift, rsvp) has no sprites to name.
    head = "import { assets } from '../bandAssets'\n\n" if rows else ''
    out = head + f"""// Generated by scripts/gen_bands.py — do not hand-edit.
// Figma Frame 263 band "{name}": y {top}..{top + h}, height {h} design px.
// x/y are band-local design px; `z` is the GLOBAL Figma child order, so layers still
// stack correctly against the bands above and below this one.
import type {{ BandLayer }} from '../bandLayer'

export const BAND_TOP = {top}
export const BAND_HEIGHT = {h}

export const LAYERS: BandLayer[] = [
{body}
]
"""
    with open(os.path.join(root, f'{name}.ts'), 'w', encoding='utf8', newline='\n') as f:
        f.write(out)
    print(f'{name:9s} {len(rows):3d} layers')
print('total', len(L))
