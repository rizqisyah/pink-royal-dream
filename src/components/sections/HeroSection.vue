<script setup lang="ts">
// Figma Frame 263 band "hero", y 0–1110. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/hero'

const { el, shown } = useReveal(0.15)
const { parsedOverride, customHeroPhoto, fotoMempelaiTransform } = useWedding()

// 2746:364 — the couple illustration on the podium; the API's photo takes its place.
const COUPLE = '2746:364'

const layers = computed(() => {
  const photo = customHeroPhoto.value
  if (!photo) return LAYERS
  const t = fotoMempelaiTransform.value
  return LAYERS.map((l) =>
    l.id === COUPLE ? { ...l, src: photo, objectPosition: `${t.x}% ${t.y}%` } : l,
  )
})

const heading = computed(
  () =>
    parsedOverride.value?.words?.hero_title ||
    parsedOverride.value?.words?.hero_heading ||
    'Wedding Invitation',
)
</script>

<template>
  <section :ref="el" class="band hero" :class="{ 'is-in': shown }" aria-labelledby="hero-heading">
    <BandArt :layers="layers" :shown="shown" />

    <!-- 2747:386 — rgba(249,240,233,.77), layer blur: the haze the title sits in. -->
    <div class="hero__haze" aria-hidden="true"></div>

    <!-- 2745:81 — Pinyon Script 75.636/54.364, #dda2a3. -->
    <h1 id="hero-heading" class="hero__title">{{ heading }}</h1>
  </section>
</template>

<style scoped>
.hero {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.hero__haze {
  z-index: 15;
  left: calc(43 * var(--px));
  top: calc(143 * var(--px));
  width: calc(491 * var(--px));
  height: calc(309 * var(--px));
  background: rgba(249, 240, 233, 0.77);
  filter: blur(calc(61.55 * var(--px)));
}

/* z 19: under the regency florals (z 50/51) that frame it. */
.hero__title {
  --delay: 200ms;
  z-index: 19;
  left: calc(90 * var(--px));
  top: calc(174 * var(--px));
  width: calc(416 * var(--px));
  height: calc(137.879 * var(--px));
  font-family: var(--font-script);
  font-size: calc(75.636 * var(--px));
  font-weight: 400;
  line-height: calc(54.364 * var(--px));
  color: var(--title);
}
</style>
