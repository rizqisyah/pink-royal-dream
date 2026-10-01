<script setup lang="ts">
// Figma Frame 263 band "bride", y 4150–5690. Coords are band-local design px.
// Opens with the embossed "And" between the two portraits, then the second slot.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import NameBlock from '../invite/NameBlock.vue'
import { useReveal } from '../../composables/useReveal'
import { usePerson } from '../../composables/usePerson'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/bride'

const { el, shown } = useReveal(0.15)
const { fullName, nickname, parents, instagram, photo } = usePerson(1)

// 2750:451 — the portrait inside the floral arch.
const PORTRAIT = '2750:451'

const layers = computed(() =>
  photo.value
    ? LAYERS.map((l) =>
        l.id === PORTRAIT ? { ...l, src: photo.value, crop: undefined, objectPosition: 'center top' } : l,
      )
    : LAYERS,
)
</script>

<template>
  <section :ref="el" class="band bride" :class="{ 'is-in': shown }" aria-labelledby="bride-name">
    <BandArt :layers="layers" :shown="shown" />

    <!-- 2745:196 — Bickham Script Pro 269.754/193.886, #f9f0e9, embossed by two shadows. -->
    <p class="bride__and" aria-hidden="true">And</p>

    <!-- 2750:471 — Pinyon Script 111.503/80.143, #dda2a3. -->
    <p id="bride-name" class="bride__nickname">{{ nickname }}</p>

    <NameBlock :x="29" :y="1123" :z="34" :full-name="fullName" :parents="parents" :instagram="instagram" />
  </section>
</template>

<style scoped>
.bride {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * z 37: the pastel florals (65+) and the flying swan paint over its tail.
 * Figma's box is (-141, 41); Bickham's ink lands 20.5 high and 3 left of the render in
 * that box (a 194px line box around 270px type), so the box is moved, not the size.
 */
.bride__and {
  --delay: 60ms;
  z-index: 37;
  left: calc(-138 * var(--px));
  top: calc(61.5 * var(--px));
  width: calc(805.435 * var(--px));
  font-family: var(--font-and);
  font-size: calc(269.754 * var(--px));
  line-height: calc(193.886 * var(--px));
  color: var(--bg-body);
  text-shadow:
    calc(2.12 * var(--px)) calc(2.12 * var(--px)) 0 #dca5ac,
    calc(-2.12 * var(--px)) calc(-4.239 * var(--px)) calc(10.598 * var(--px)) rgba(255, 255, 255, 0.96);
}

.bride__nickname {
  --delay: 200ms;
  z-index: 64;
  left: calc(84 * var(--px));
  top: calc(1040 * var(--px));
  width: calc(389 * var(--px));
  height: calc(99 * var(--px));
  font-family: var(--font-script);
  font-size: calc(111.503 * var(--px));
  line-height: calc(80.143 * var(--px));
  color: var(--title);
}
</style>
