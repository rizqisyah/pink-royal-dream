<script setup lang="ts">
// Figma Frame 263 band "gallery", y 9960–10850. Coords are band-local design px.
//
// Nothing here is sliced: the main photo, the four thumbnails and the two pink nav
// circles are live, so a configured gallery shows its own photos in the same slots.
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/gallery'
import { assets } from '../../lib/bandAssets'

const { el, shown } = useReveal(0.15)
const { gallery } = useWedding()

const navCircle = assets['gallery/parts/nav-circle.svg']
const navArrow = assets['gallery/parts/nav-arrow.svg']

/*
 * The design fills all five slots with one photo (_DSC4292). Design mode ships no API
 * gallery, so that photo stands in and the same code path runs either way.
 */
const DESIGN_PHOTO = { src: assets['gallery/parts/gallery-1.webp'], caption: '', design: true }
const DESIGN_PHOTOS = [DESIGN_PHOTO, DESIGN_PHOTO, DESIGN_PHOTO, DESIGN_PHOTO]

const photos = computed(() => {
  const live = (gallery.value as any[])
    .map((g) => ({ src: g.image_url as string, caption: (g.caption as string) || '', design: false }))
    .filter((p) => p.src)
  return live.length ? live : DESIGN_PHOTOS
})

const active = ref(0)
watch(photos, () => (active.value = 0))

const step = (d: number) => {
  const n = photos.value.length
  if (n) active.value = (active.value + d + n) % n
}

// Four thumbnail slots; a longer gallery pages through them four at a time.
const THUMBS = 4
const thumbs = computed(() => {
  const start = Math.floor(active.value / THUMBS) * THUMBS
  return photos.value.slice(start, start + THUMBS).map((p, i) => ({ ...p, index: start + i }))
})

let autoplayTimer: number | null = null
const stopAutoplay = () => {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}
const startAutoplay = () => {
  stopAutoplay()
  if (photos.value.length > 1) autoplayTimer = window.setInterval(() => step(1), 4000)
}

/** Any manual choice restarts the clock, so a guest is never yanked off a photo. */
const go = (d: number) => {
  step(d)
  startAutoplay()
}
const pick = (i: number) => {
  active.value = i
  startAutoplay()
}

onMounted(startAutoplay)
onUnmounted(stopAutoplay)

/*
 * Swipe on the main photo; a tap opens the preview. A touch that moved far enough to
 * count as a swipe still fires `click` afterwards, hence `swiped`.
 */
const SWIPE_PX = 30
let startX = 0
let swiped = false
const onStart = (e: TouchEvent) => {
  startX = e.touches[0].clientX
  stopAutoplay()
}
const onEnd = (e: TouchEvent) => {
  const dx = e.changedTouches[0].clientX - startX
  swiped = Math.abs(dx) >= SWIPE_PX
  if (swiped) step(dx < 0 ? 1 : -1)
  if (!dlg.value?.open) startAutoplay()
}
const onClick = () => {
  if (swiped) {
    swiped = false
    return
  }
  stopAutoplay()
  dlg.value?.showModal()
}

/*
 * Preview is a native <dialog>: it brings its own backdrop, top layer, Esc-to-close and
 * focus trap. Teleported to <body> because a child of `.band` is absolutely positioned
 * and faded by the shared band rules.
 */
const dlg = ref<HTMLDialogElement | null>(null)
</script>

<template>
  <section :ref="el" class="band gallery" :class="{ 'is-in': shown }" aria-labelledby="gallery-heading">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2750:541 — 526.271 x 514.831, radius 22.881. -->
    <button
      type="button"
      class="gallery__main"
      :aria-label="`Foto ${active + 1} dari ${photos.length} — ketuk untuk memperbesar`"
      @click="onClick"
      @touchstart.passive="onStart"
      @touchend.passive="onEnd"
    >
      <Transition name="photo">
        <img
          :key="active"
          :src="photos[active].src"
          :alt="photos[active].caption || 'Foto mempelai'"
          :class="{ 'is-design': photos[active].design }"
          loading="lazy"
          decoding="async"
        />
      </Transition>
    </button>

    <!-- 2750:542 — four 122.329 x 129.28 thumbs, 11.121 apart, radius 27.802. -->
    <div class="gallery__thumbs" role="tablist" aria-label="Foto">
      <button
        v-for="t in thumbs"
        :key="t.index"
        type="button"
        role="tab"
        class="gallery__thumb"
        :class="{ 'is-active': t.index === active }"
        :aria-selected="t.index === active"
        :aria-label="`Foto ${t.index + 1}`"
        @click="pick(t.index)"
      >
        <img :src="t.src" alt="" loading="lazy" decoding="async" />
      </button>
    </div>

    <!-- 2750:547 — Pinyon Script 127.269/91.474, #dda2a3. -->
    <h2 id="gallery-heading" class="gallery__heading">Gallery</h2>

    <!-- 2750:548–551 — #ffb8b0 circles with #fff4bf chevrons. -->
    <button type="button" class="gallery__nav gallery__nav--prev" aria-label="Foto sebelumnya" @click="go(-1)">
      <img class="gallery__circle" :src="navCircle" alt="" />
      <img class="gallery__arrow" :src="navArrow" alt="" />
    </button>
    <button type="button" class="gallery__nav gallery__nav--next" aria-label="Foto berikutnya" @click="go(1)">
      <img class="gallery__circle" :src="navCircle" alt="" />
      <img class="gallery__arrow" :src="navArrow" alt="" />
    </button>
  </section>

  <Teleport to="body">
    <dialog ref="dlg" class="preview" @close="startAutoplay" @click.self="dlg?.close()">
      <img
        class="preview__img"
        :src="photos[active].src"
        :alt="photos[active].caption || 'Foto mempelai'"
        @touchstart.passive="onStart"
        @touchend.passive="onEnd"
      />
      <p v-if="photos[active].caption" class="preview__caption">{{ photos[active].caption }}</p>
      <button
        v-if="photos.length > 1"
        type="button"
        class="preview__nav preview__nav--prev"
        aria-label="Foto sebelumnya"
        @click="step(-1)"
      >
        &lsaquo;
      </button>
      <button
        v-if="photos.length > 1"
        type="button"
        class="preview__nav preview__nav--next"
        aria-label="Foto berikutnya"
        @click="step(1)"
      >
        &rsaquo;
      </button>
      <button type="button" class="preview__close" aria-label="Tutup" @click="dlg?.close()">&times;</button>
    </dialog>
  </Teleport>
</template>

<style scoped>
.gallery {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.gallery__main {
  --delay: 200ms;
  z-index: 90;
  left: calc(36 * var(--px));
  top: calc(190 * var(--px));
  width: calc(526.271 * var(--px));
  height: calc(514.831 * var(--px));
  padding: 0;
  border: 0;
  border-radius: calc(22.881 * var(--px));
  overflow: hidden;
  background: #e8dcd6;
  cursor: zoom-in;
}

.gallery__main img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* The design's crop of _DSC4292: full width, 40.32% cut off the top of a 153% image. */
.gallery__main img.is-design {
  object-position: 50% 75.6%;
}

.photo-enter-active,
.photo-leave-active {
  transition: opacity 0.6s ease;
}
.photo-enter-from,
.photo-leave-to {
  opacity: 0;
}

.gallery__thumbs {
  --delay: 320ms;
  z-index: 91;
  display: flex;
  gap: calc(11.121 * var(--px));
  left: calc(38.29 * var(--px));
  top: calc(735.72 * var(--px));
  width: calc(522.68 * var(--px));
}

.gallery__thumb {
  flex: none;
  width: calc(122.329 * var(--px));
  height: calc(129.28 * var(--px));
  padding: 0;
  border: 1px solid transparent;
  border-radius: calc(27.802 * var(--px));
  overflow: hidden;
  background: #e8dcd6;
  cursor: pointer;
  transition: border-color 0.24s ease, transform 0.24s ease;
}

/* The design outlines the first thumb in white — the active one. */
.gallery__thumb.is-active {
  border-color: #fff;
}

.gallery__thumb:hover {
  transform: translateY(calc(-2 * var(--px)));
}

.gallery__thumb img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery__heading {
  --delay: 60ms;
  z-index: 92;
  left: calc(-31 * var(--px));
  top: calc(42 * var(--px));
  width: calc(658.963 * var(--px));
  font-family: var(--font-script);
  font-size: calc(127.269 * var(--px));
  font-weight: 400;
  line-height: calc(91.474 * var(--px));
  color: var(--title);
}

.gallery__nav {
  --delay: 420ms;
  z-index: 93;
  top: calc(428 * var(--px));
  width: calc(63 * var(--px));
  height: calc(60 * var(--px));
  padding: 0;
  border: 0;
  background: none;
  cursor: pointer;
}

.gallery__nav--prev {
  left: calc(6 * var(--px));
}

.gallery__nav--next {
  left: calc(529 * var(--px));
}

.gallery__circle {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

/* Vector 17's own box, including its stroke bleed (18.769 x 29.262). */
.gallery__arrow {
  position: absolute;
  top: calc(14.869 * var(--px));
  width: calc(18.769 * var(--px));
  height: calc(29.262 * var(--px));
}

.gallery__nav--prev .gallery__arrow {
  left: calc(19.717 * var(--px));
}

/* Vector 18 is Vector 17 mirrored. */
.gallery__nav--next .gallery__arrow {
  left: calc(24.514 * var(--px));
  transform: scaleX(-1);
}

.gallery__nav:focus-visible,
.gallery__main:focus-visible,
.gallery__thumb:focus-visible {
  outline: calc(2 * var(--px)) solid var(--title);
  outline-offset: calc(3 * var(--px));
}

/*
 * Plain units, not `--px`: that variable is a container-query length declared on the
 * sheet element, and this dialog is teleported to <body>, outside it.
 */
.preview {
  width: 100vw;
  max-width: 100vw;
  height: 100dvh;
  max-height: 100dvh;
  padding: 1.5rem;
  border: 0;
  background: transparent;
}

.preview[open] {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.preview::backdrop {
  background: rgb(60 30 32 / 0.92);
}

.preview__img {
  max-width: 100%;
  max-height: 78dvh;
  object-fit: contain;
  border-radius: 8px;
}

.preview__caption {
  max-width: 100%;
  font-family: var(--font-field);
  font-size: 0.95rem;
  text-align: center;
  color: #f7ecec;
}

.preview__nav {
  position: absolute;
  top: 50%;
  translate: 0 -50%;
  width: 2.75rem;
  height: 2.75rem;
  padding: 0 0 0.2rem;
  border: 0;
  border-radius: 50%;
  background: #ffb8b0;
  color: #fff4bf;
  font-size: 1.75rem;
  line-height: 1;
  cursor: pointer;
}

.preview__nav--prev {
  left: 0.75rem;
}

.preview__nav--next {
  right: 0.75rem;
}

.preview__close {
  position: absolute;
  top: 0.75rem;
  right: 1rem;
  width: 2.25rem;
  height: 2.25rem;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: rgb(255 255 255 / 0.18);
  color: #fff;
  font-size: 1.375rem;
  line-height: 1;
  cursor: pointer;
}
</style>
