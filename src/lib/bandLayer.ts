/** One sliced sprite of the body frame, placed in band-local design px. */
export type BandLayer = {
  /** Global Figma child order — bands share one stacking context, so this is comparable across them. */
  z: number
  id: string
  src: string
  /**
   * The layer's on-screen box: for a rotated layer this is its axis-aligned bounding box
   * (what Figma's own code export positions), not the unrotated node size.
   */
  x: number
  y: number
  w: number
  h: number
  /** Opacity, when the design fades this layer. Absent means 1. */
  a?: number
  /** `mix-blend-mode`. Absent means `normal`. */
  b?: string
  /** Optional mask image URL to clip the layer sprite, stretched to the layer box. */
  mask?: string
  /** Optional CSS object-position (e.g. 'center top') */
  objectPosition?: string

  /*
   * ---- This theme only ----
   * The base slices every node to its own pre-rotated export. This design reuses a
   * handful of illustrations dozens of times (one floral 12x, another 14x at six
   * stacked fills), so it ships each source image once and recreates the node's
   * transform here instead — about 3 MB of art rather than ~120 near-duplicate exports.
   * Any layer carrying one of these renders as a box with the sprite inside it.
   */
  /** Unrotated sprite size, centred in the box. Defaults to w/h. */
  iw?: number
  ih?: number
  /** Degrees, clockwise, about the sprite's centre. */
  rotate?: number
  flipX?: boolean
  flipY?: boolean
  /** Sprite drawn at w%/h% of the sprite box, offset l%/t%, and clipped to it. */
  crop?: { w: number; h: number; l: number; t: number }
  radius?: number
  /** 'fill' stretches the sprite to its box, as Figma's stretched image fills do. */
  fit?: 'cover' | 'fill'
  /** The same fill painted n times — Figma stacks fills to deepen a semi-transparent image. */
  stack?: number
  /** A mask with its own size and offset inside the sprite box (Figma mask groups). */
  maskBox?: { src: string; x: number; y: number; w: number; h: number }
  /** CSS `filter`, e.g. a drop-shadow glow. */
  filter?: string
  /**
   * Admin-set zoom & focus for a photo (theme_override.foto_*_transform), x/y in %, as in
   * envelope-red: cover-fit, positioned at x% y%, scaled about that point — inside the
   * sprite box, so the box (and any mask on it) stays put while the photo moves.
   */
  zoom?: PhotoTransform
}

export type PhotoTransform = { scale: number; x: number; y: number }
