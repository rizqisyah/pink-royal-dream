<script setup lang="ts">
import type { BandLayer } from '../../lib/bandLayer'

const props = withDefaults(
  defineProps<{
    layers: BandLayer[]
    /** Layer ids this band draws itself — an API photo standing in for a sliced plate. */
    skip?: string[]
    /** Whether the band has scrolled into view; layers hold still until it has. */
    shown?: boolean
    /** Stagger between layers, back to front. */
    step?: number
  }>(),
  { skip: () => [], shown: true, step: 150 },
)

/*
 * Frame 263 is 596 wide, not the base's 375. The entrance distances below are the
 * base's, authored in 375-frame design px, so they are scaled by K to move the same
 * physical distance on screen.
 */
const FRAME_W = 596
const K = FRAME_W / 375

/** A layer that needs a box: anything the base would have pre-rotated into its export. */
const isBoxed = (l: BandLayer) =>
  !!(l.rotate || l.flipX || l.flipY || l.crop || l.stack || l.maskBox || l.iw || l.ih || l.radius || l.filter)

const px = (v: number) => `calc(${v} * var(--px))`

/*
 * Each layer gets its own entrance, derived from where it sits and how big it is,
 * so the band assembles like a set being built rather than a picture fading up.
 *
 *   - full-bleed backdrops swell in from behind, slowest and first
 *   - anything hugging a side edge sweeps in from off that edge, rotating as it lands
 *   - small foreground props drop in late, overshooting slightly before settling
 *
 * All of it is transform + opacity, so it stays on the compositor.
 */
/*
 * Double quotes, not single: Vite inlines a small SVG as a data URI written with single
 * quotes inside it, so `url('...')` closes early and the mask silently never applies.
 */
const cssUrl = (src: string) => `url("${src}")`

const styleFor = (l: BandLayer, i: number): Record<string, string> => ({
  zIndex: String(l.z),
  left: px(l.x),
  top: px(l.y),
  width: px(l.w),
  height: px(l.h),
  ...(l.mask
    ? {
        WebkitMaskImage: cssUrl(l.mask),
        maskImage: cssUrl(l.mask),
        WebkitMaskSize: '100% 100%',
        maskSize: '100% 100%',
        WebkitMaskRepeat: 'no-repeat',
        maskRepeat: 'no-repeat',
      }
    : {}),
  ...(l.objectPosition ? { objectPosition: l.objectPosition } : {}),
  // Through a custom property, so the entrance's `to` frame lands on the layer's own value.
  '--a': String(l.a ?? 1),
  mixBlendMode: l.b ?? 'normal',
  ...entrance(l, i),
})

/** The sprite inside a boxed layer: its unrotated size, transform, clip and mask. */
const spriteStyle = (l: BandLayer): Record<string, string> => {
  const t: string[] = []
  if (l.rotate) t.push(`rotate(${l.rotate}deg)`)
  if (l.flipX) t.push('scaleX(-1)')
  if (l.flipY) t.push('scaleY(-1)')
  const m = l.maskBox
  return {
    width: px(l.iw ?? l.w),
    height: px(l.ih ?? l.h),
    ...(t.length ? { transform: t.join(' ') } : {}),
    ...(l.crop || l.radius ? { overflow: 'hidden' } : {}),
    ...(l.radius ? { borderRadius: px(l.radius) } : {}),
    ...(l.filter ? { filter: l.filter } : {}),
    ...(m
      ? {
          WebkitMaskImage: cssUrl(m.src),
          maskImage: cssUrl(m.src),
          WebkitMaskSize: `${px(m.w)} ${px(m.h)}`,
          maskSize: `${px(m.w)} ${px(m.h)}`,
          WebkitMaskPosition: `${px(m.x)} ${px(m.y)}`,
          maskPosition: `${px(m.x)} ${px(m.y)}`,
          WebkitMaskRepeat: 'no-repeat',
          maskRepeat: 'no-repeat',
        }
      : {}),
  }
}

const cropStyle = (l: BandLayer): Record<string, string> | undefined =>
  l.crop
    ? { width: `${l.crop.w}%`, height: `${l.crop.h}%`, left: `${l.crop.l}%`, top: `${l.crop.t}%` }
    : undefined

const entrance = (l: BandLayer, i: number) => {
  const isBackdrop = l.w >= FRAME_W * 0.9 && l.h > 200 * K
  const centre = l.x + l.w / 2
  const offLeft = centre < FRAME_W * 0.34
  const offRight = centre > FRAME_W * 0.66
  const small = l.w < 130 * K && l.h < 180 * K

  let tx = 0
  let ty = 44 * K
  let rot = 0
  let scale = 0.86

  if (isBackdrop) {
    ty = 26 * K
    scale = 1.08 // settles inward, so the scene opens up rather than rising
  } else if (offLeft || offRight) {
    const dir = offLeft ? -1 : 1
    tx = dir * 92 * K
    ty = 30 * K
    rot = dir * 7
    scale = 0.92
  } else if (small) {
    ty = -34 * K // drops in from above
    rot = (i % 2 ? 1 : -1) * 9
    scale = 0.7
  }

  return {
    '--tx': `${tx}`,
    '--ty': `${ty}`,
    '--rot': `${rot}deg`,
    '--scale': `${scale}`,
    '--dur': isBackdrop ? '3400ms' : small ? '2100ms' : '2700ms',
    // Backdrops lead; everything in front of them queues up behind, front-most last.
    animationDelay: `${Math.round((isBackdrop ? 0 : 440) + i * stagger())}ms`,
  }
}

const visible = () => props.layers.filter((l) => !props.skip.includes(l.id))

/*
 * Cap the total stagger instead of the per-layer step, so short bands get the full
 * leisurely spacing and long ones tighten up to fit the same window.
 */
const MAX_STAGGER = 2600
const stagger = () => Math.min(props.step, MAX_STAGGER / Math.max(1, visible().length - 1))
</script>

<template>
  <template v-for="(layer, i) in visible()" :key="`${layer.id}:${layer.src}`">
    <div
      v-if="isBoxed(layer)"
      class="band-art band-art--box"
      :class="{ 'is-in': shown }"
      :style="styleFor(layer, i)"
    >
      <div class="band-art__sprite" :style="spriteStyle(layer)">
        <img
          v-for="n in layer.stack ?? 1"
          :key="n"
          class="band-art__img"
          :class="{ 'is-fill': layer.fit === 'fill', 'is-crop': !!layer.crop }"
          :src="layer.src"
          alt=""
          loading="lazy"
          decoding="async"
          :style="cropStyle(layer)"
        />
      </div>
    </div>
    <img
      v-else
      class="band-art"
      :class="{ 'is-in': shown, 'is-fill': layer.fit === 'fill' }"
      :src="layer.src"
      alt=""
      :width="layer.w"
      :height="layer.h"
      loading="lazy"
      decoding="async"
      :style="styleFor(layer, i)"
    />
  </template>
</template>

<style scoped>
/*
 * Held in the start state by `visibility` rather than a paused animation: the
 * animation only exists once `.is-in` lands, so nothing has to be un-paused and
 * the element still fetches its image while hidden.
 */
.band-art {
  position: absolute;
  max-width: none; /* several layers are authored wider than the frame */
  visibility: hidden;
  opacity: var(--a, 1);
  will-change: transform, opacity;
  object-fit: cover;
  pointer-events: none;
}

.band-art.is-fill,
.band-art__img.is-fill {
  object-fit: fill;
}

.band-art--box {
  display: flex;
  align-items: center;
  justify-content: center;
}

.band-art__sprite {
  position: relative;
  flex: none;
}

.band-art__img {
  position: absolute;
  inset: 0;
  display: block;
  width: 100%;
  height: 100%;
  max-width: none;
  object-fit: cover;
}

.band-art__img.is-crop {
  inset: auto;
}

.band-art.is-in {
  visibility: visible;
  animation: layer-in var(--dur, 2700ms) cubic-bezier(0.16, 1, 0.28, 1) backwards;
}

@keyframes layer-in {
  from {
    opacity: 0;
    transform: translate3d(calc(var(--tx) * var(--px)), calc(var(--ty) * var(--px)), 0)
      rotate(var(--rot)) scale(var(--scale));
  }
  to {
    opacity: var(--a, 1);
    transform: none;
  }
}

/*
 * Motion this large is exactly what a vestibular disorder cannot tolerate, so the
 * reduced-motion path is not a shortened version of it — it is no movement at all.
 */
@media (prefers-reduced-motion: reduce) {
  .band-art,
  .band-art.is-in {
    visibility: visible;
    animation: none;
    will-change: auto;
  }
}
</style>
