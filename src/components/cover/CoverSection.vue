<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useWedding } from '../../composables/useWedding'
import {
  BACKDROP_BOX,
  COVER_BACKDROP,
  COVER_H,
  COVER_LAYERS,
  COVER_W,
  type CoverLayer,
} from '../../lib/coverLayers'

// `ready` gates the reveal on the layers being decoded — see App.vue.
const props = defineProps<{ guestName: string; coupleName: string; ready: boolean }>()
defineEmits<{ open: [] }>()

const { wedding } = useWedding()

// The design breaks the names after the ampersand: "Mario &" / "Amanda".
const coupleLines = computed(() => props.coupleName.replace(/\s*&\s*/, ' &\n'))

// The polaroid is the couple's own photo when the API has one.
const polaroid = computed(() => (wedding.value?.image_cover as string) || '')
const srcFor = (l: CoverLayer) => (l.id === '2756:652' && polaroid.value ? polaroid.value : l.src)

/*
 * The frame always shows whole — nothing of the envelope or the names is ever cropped.
 * The illustration behind it is bigger than the frame (867 x 1225 at -134, -17), so on
 * a screen taller or wider than 596:1183 it bleeds out to fill the gap instead of
 * leaving bare paper: scaled about the frame's centre just enough to reach every edge.
 *
 * Past MAX_ZOOM (a landscape tablet, say) filling would blow the flowers up out of all
 * proportion, so the cover becomes a card the size of the frame and clips at its edge,
 * exactly as Figma does.
 */
const MAX_ZOOM = 1.15
const CX = COVER_W / 2 - BACKDROP_BOX.x
const CY = COVER_H / 2 - BACKDROP_BOX.y

const root = ref<HTMLElement | null>(null)
const zoom = ref(1)
const mode = ref<'fill' | 'card'>('fill')

function measure() {
  const el = root.value
  if (!el) return
  const W = el.clientWidth
  const H = el.clientHeight
  if (!W || !H) return
  const s = Math.min(W / COVER_W, H / COVER_H)
  const need = Math.max(
    1,
    W / 2 / (CX * s),
    W / 2 / ((BACKDROP_BOX.w - CX) * s),
    H / 2 / (CY * s),
    H / 2 / ((BACKDROP_BOX.h - CY) * s),
  )
  mode.value = need <= MAX_ZOOM ? 'fill' : 'card'
  zoom.value = mode.value === 'fill' ? need : 1
}

let observer: ResizeObserver | null = null
onMounted(() => {
  measure()
  observer = new ResizeObserver(() => requestAnimationFrame(measure))
  if (root.value) observer.observe(root.value)
})
onBeforeUnmount(() => observer?.disconnect())

const px = (v: number) => `calc(${v} * var(--px))`

const boxStyle = (l: CoverLayer) => ({
  zIndex: String(l.z),
  left: px(l.x),
  top: px(l.y),
  width: px(l.w),
  height: px(l.h),
})

const spriteStyle = (l: CoverLayer) => {
  const t: string[] = []
  if (l.rotate) t.push(`rotate(${l.rotate}deg)`)
  if (l.flipY) t.push('scaleY(-1)')
  return {
    width: px(l.iw ?? l.w),
    height: px(l.ih ?? l.h),
    ...(t.length ? { transform: t.join(' ') } : {}),
    ...(l.filter ? { filter: l.filter } : {}),
  }
}

const backdropStyle = computed(() => ({
  left: px(BACKDROP_BOX.x),
  top: px(BACKDROP_BOX.y),
  width: px(BACKDROP_BOX.w),
  height: px(BACKDROP_BOX.h),
  transformOrigin: `${(CX / BACKDROP_BOX.w) * 100}% ${(CY / BACKDROP_BOX.h) * 100}%`,
  '--zoom': String(zoom.value),
}))
</script>

<template>
  <!-- Figma Frame 264 (2745:354), 596 x 1183. Coords below are frame-local design px. -->
  <section ref="root" class="cover" :class="`cover--${mode}`">
    <div class="cover__frame" :class="{ 'cover__frame--ready': ready }">
      <!-- 2755:609 — z 1, the illustration the whole cover sits on. -->
      <img class="cover__backdrop" :src="COVER_BACKDROP" alt="" :style="backdropStyle" />

      <div
        v-for="layer in COVER_LAYERS"
        :key="layer.id"
        class="cover__layer"
        :class="`cover__layer--${layer.part}`"
        :style="boxStyle(layer)"
      >
        <img v-if="layer.src" class="cover__sprite" :src="srcFor(layer)" alt="" :style="spriteStyle(layer)" />
        <!-- 2756:651 — the polaroid's white card. -->
        <div v-else class="cover__plate" :style="spriteStyle(layer)" />
      </div>

      <!-- 2745:357 — Pinyon Script 80/69, #dda2a3. -->
      <h1 class="cover__couple">{{ coupleLines }}</h1>

      <!-- 2745:358 — Lisu Bosa Italic 24/62, #b78081. -->
      <div class="cover__guest">
        <p class="cover__dear">kepada Yth.</p>
        <p class="cover__name">{{ guestName }}</p>
      </div>

      <!--
        2745:361 — the words are the label; the envelope above them is the hit area, which
        is what the design actually invites you to tap. So the text is a plain <p> and the
        button is a transparent plate over the envelope and the label, named by the label.
      -->
      <p id="cover-open-label" class="cover__open">Click to open</p>
      <button
        type="button"
        class="cover__hit"
        aria-labelledby="cover-open-label"
        @click="$emit('open')"
      />
    </div>
  </section>
</template>

<style scoped>
.cover {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100dvh;
  overflow: hidden;
  background: var(--cover-bg);
}

/*
 * One design pixel = 1cqw / 5.96, so the whole composition scales as a unit instead of
 * reflowing. Contained, never cropped: the frame is as big as the screen allows in both
 * directions, and the backdrop fills whatever is left around it (see `measure`).
 */
.cover__frame {
  container-type: inline-size;
  position: relative;
  flex: 0 0 auto;
  width: min(100%, calc(100dvh * 596 / 1183));
  aspect-ratio: 596 / 1183;
}

.cover--card .cover__frame {
  overflow: hidden;
  box-shadow: 0 0 60px rgba(183, 128, 129, 0.18);
}

.cover__frame > * {
  --px: calc(100cqw / 596);
  position: absolute;
  margin: 0;
  text-align: center;
  /*
   * Held until the layers are decoded. `animation-play-state` rather than `display`
   * so the images are still in the document and actually fetching while hidden.
   */
  visibility: hidden;
}

/*
 * More specific than any single element's `animation` shorthand below — a shorthand
 * resets play-state to running, which would let the entrance play out unseen.
 */
.cover__frame:not(.cover__frame--ready) > * {
  animation-play-state: paused;
}

.cover__frame--ready > * {
  visibility: visible;
}

.cover__backdrop {
  z-index: 1;
  max-width: none;
  object-fit: cover;
  pointer-events: none;
  user-select: none;
  /* Two transforms, two properties: `scale` fills the screen, the animation drives `transform`. */
  scale: var(--zoom, 1);
  animation: backdrop-in 1600ms cubic-bezier(0.16, 1, 0.3, 1) backwards;
}

.cover__layer {
  display: flex;
  align-items: center;
  justify-content: center;
  /* Florals are authored across the label; they must not swallow the tap meant for the button. */
  pointer-events: none;
}

.cover__sprite,
.cover__plate {
  flex: none;
  max-width: none;
  object-fit: cover;
  user-select: none;
}

.cover__plate {
  background: #fff;
  box-shadow: 0 calc(4 * var(--px)) calc(4 * var(--px)) rgba(0, 0, 0, 0.46);
}

/*
 * The scene assembles the way the base theme's envelope does: names first, then the
 * whole envelope rises as one piece, the seal drops onto it, and the call to action
 * arrives last and keeps breathing. `backwards`, not `forwards`: the end state is the
 * element's normal state, so hover transitions get their transform back afterwards.
 */
@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(calc(26 * var(--px)));
  }
}

@keyframes seal-drop {
  from {
    opacity: 0;
    transform: scale(0.7);
  }
}

@keyframes breathe {
  50% {
    opacity: 0.45;
  }
}

@keyframes backdrop-in {
  from {
    opacity: 0;
    transform: scale(1.04);
  }
}

.cover__couple,
.cover__layer--envelope,
.cover__guest,
.cover__open {
  animation: rise 1400ms cubic-bezier(0.16, 1, 0.3, 1) var(--delay, 0ms) backwards;
}

.cover__couple {
  --delay: 200ms;
}

.cover__layer--envelope {
  --delay: 640ms;
}

.cover__layer--seal {
  animation: seal-drop 1100ms cubic-bezier(0.34, 1.5, 0.5, 1) 1240ms backwards;
}

.cover__open {
  --delay: 1460ms;
  animation:
    rise 1400ms cubic-bezier(0.16, 1, 0.3, 1) var(--delay) backwards,
    breathe 3s ease-in-out 3s infinite;
}

.cover__guest {
  --delay: 1700ms;
}

/* 2745:357 */
.cover__couple {
  z-index: 4;
  left: calc(104 * var(--px));
  top: calc(134 * var(--px));
  width: calc(392 * var(--px));
  height: calc(179 * var(--px));
  font-family: var(--font-script);
  font-size: calc(80 * var(--px));
  font-weight: 400;
  line-height: calc(69 * var(--px));
  white-space: pre-line;
  color: var(--title);
}

/* 2745:358 — a 373 x 104 box holding two 62-high lines, 31 apart. */
.cover__guest {
  z-index: 5;
  left: calc(112 * var(--px));
  top: calc(845 * var(--px));
  width: calc(373 * var(--px));
  height: calc(104 * var(--px));
}

.cover__dear,
.cover__name,
.cover__open {
  font-family: var(--font-cover);
  font-style: italic;
  font-size: calc(24 * var(--px));
  line-height: calc(62 * var(--px));
  color: var(--maroon-text);
}

.cover__dear,
.cover__name {
  position: absolute;
  left: 0;
  right: 0;
  overflow-wrap: break-word;
}

.cover__dear {
  top: 0;
}

.cover__name {
  top: calc(31 * var(--px));
}

/* 2745:361 */
.cover__open {
  z-index: 6;
  left: calc(-14 * var(--px));
  top: calc(755 * var(--px));
  width: calc(373 * var(--px));
  pointer-events: none;
}

/* The envelope and its label: 22..575 x 271..817. */
.cover__hit {
  z-index: 16;
  left: calc(22 * var(--px));
  top: calc(271 * var(--px));
  width: calc(553 * var(--px));
  height: calc(546 * var(--px));
  border: 0;
  background: none;
  cursor: pointer;
  /* No entrance of its own — it is invisible, and animating it would gate the tap. */
  animation: none;
}

.cover__layer--seal .cover__sprite {
  transition: transform 300ms cubic-bezier(0.16, 1, 0.3, 1);
}

.cover__frame:has(.cover__hit:hover) .cover__layer--seal .cover__sprite,
.cover__frame:has(.cover__hit:focus-visible) .cover__layer--seal .cover__sprite {
  transform: scale(1.06);
}

.cover__hit:focus-visible {
  outline: calc(2 * var(--px)) solid var(--maroon-text);
  outline-offset: calc(4 * var(--px));
  border-radius: calc(12 * var(--px));
}

@media (prefers-reduced-motion: reduce) {
  .cover__frame > *,
  .cover__open {
    animation: none;
  }
}
</style>
