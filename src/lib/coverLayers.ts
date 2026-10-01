// Figma Frame 264 (2745:354), 596 x 1183. `z` is Figma child order, which IS the paint
// order; the text nodes in CoverSection.vue carry their own slots in the same sequence.
//
// Rotated layers: x/y/w/h is the axis-aligned box Figma's code export positions and
// iw/ih the unrotated sprite, centred in it. The background illustration (2755:609) is
// not here — it bleeds past the frame and is drawn by CoverSection as the backdrop.
const modules = import.meta.glob('../assets/opening/parts/*.webp', {
  eager: true,
  import: 'default',
}) as Record<string, string>

const parts = Object.fromEntries(
  Object.entries(modules).map(([path, url]) => [path.split('/').pop()!.replace('.webp', ''), url]),
) as Record<string, string>

export type CoverLayer = {
  z: number
  id: string
  /** Empty for a flat plate drawn in CSS (the polaroid's white card). */
  src: string
  x: number
  y: number
  w: number
  h: number
  iw?: number
  ih?: number
  rotate?: number
  flipY?: boolean
  /** CSS filter — Figma's drop shadows on transparent sprites follow their alpha. */
  filter?: string
  /** The whole envelope moves as one piece; the seal lands on it afterwards. */
  part: 'envelope' | 'seal'
}

const SWAN_SHADOW =
  'drop-shadow(calc(4 * var(--px)) calc(-1 * var(--px)) calc(4 * var(--px)) rgba(0,0,0,.25)) ' +
  'drop-shadow(0 calc(4 * var(--px)) calc(4 * var(--px)) rgba(0,0,0,.25))'

export const COVER_LAYERS: CoverLayer[] = [
  { z: 2, id: '2746:370', src: parts['envelope-back'], x: 50.982, y: 271, w: 498.036, h: 479.977, part: 'envelope' },
  { z: 3, id: '2747:372', src: parts['floral'], x: 125, y: 329, w: 457.243, h: 457.243, iw: 357.692, ih: 357.692, rotate: 19.68, part: 'envelope' },
  // 4 "Mario & Amanda", 5 guest block, 6 "Click to open" — text.
  { z: 7, id: '2747:379', src: parts['floral'], x: 66, y: 349, w: 362.872, h: 362.872, iw: 283.965, ih: 283.965, rotate: -19.63, part: 'envelope' },
  { z: 8, id: '2756:650', src: parts['swan'], x: 20, y: 195, w: 436.303, h: 489.703, iw: 302.623, ih: 403.497, rotate: 23.02, filter: SWAN_SHADOW, part: 'envelope' },
  { z: 9, id: '2747:377', src: parts['save-our-date'], x: 179, y: 477, w: 181, h: 174, filter: 'drop-shadow(0 calc(3 * var(--px)) calc(4 * var(--px)) rgba(0,0,0,.6))', part: 'envelope' },
  { z: 10, id: '2756:651', src: '', x: 269, y: 375, w: 216.418, h: 263.748, iw: 150, ih: 227, rotate: 19.24, part: 'envelope' },
  { z: 11, id: '2756:652', src: parts['polaroid-photo'], x: 293.18, y: 395.95, w: 174.977, h: 202.023, iw: 126, ih: 170, rotate: 19.24, part: 'envelope' },
  { z: 12, id: '2756:654', src: parts['floral'], x: 182, y: 443, w: 331.497, h: 331.497, iw: 259.324, ih: 259.324, rotate: 19.68, part: 'envelope' },
  { z: 13, id: '2756:655', src: parts['floral'], x: 3, y: 365, w: 331.497, h: 331.497, iw: 259.324, ih: 259.324, rotate: 160.32, flipY: true, part: 'envelope' },
  { z: 14, id: '2746:368', src: parts['envelope-front'], x: 22, y: 339, w: 553, h: 553, part: 'envelope' },
  { z: 15, id: '2746:371', src: parts['wax-seal'], x: 240, y: 549, w: 120, h: 120, part: 'seal' },
]

export const COVER_BACKDROP = parts['illustration-bg']
/** 2755:609 bleeds past the frame: 867 x 1225 at (-134, -17). */
export const BACKDROP_BOX = { x: -134, y: -17, w: 867, h: 1225 }
export const COVER_W = 596
export const COVER_H = 1183
