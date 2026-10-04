<script setup lang="ts">
// Figma Frame 263 band "groom", y 2620–4150. Coords are band-local design px.
// The first portrait slot — the groom in the design, whoever comes first live.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import NameBlock from '../invite/NameBlock.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { usePerson } from '../../composables/usePerson'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/groom'

const { el, shown } = useReveal(0.15)
const { parsedOverride } = useWedding()
const { fullName, nickname, parents, instagram, photo, zoom } = usePerson(0)

// 2748:419 — the portrait inside the floral arch.
const PORTRAIT = '2748:419'

const layers = computed(() =>
  photo.value
    ? LAYERS.map((l) =>
        l.id === PORTRAIT
          ? {
              ...l,
              src: photo.value,
              crop: undefined,
              objectPosition: 'center top',
              // Admin "Zoom & Posisi Foto Mempelai" for whoever this slot shows.
              zoom: zoom.value ?? undefined,
            }
          : l,
      )
    : LAYERS,
)

// Figma authors the break after the ampersand.
const heading = computed(() => parsedOverride.value?.words?.couple_title || 'Bride &\nGroom')
</script>

<template>
  <section :ref="el" class="band groom" :class="{ 'is-in': shown }" aria-labelledby="groom-name">
    <BandArt :layers="layers" :shown="shown" />

    <!-- 2748:398 — Pinyon Script 127.269/91.474, #dda2a3. -->
    <h2 class="groom__heading">{{ heading }}</h2>

    <!-- 2749:420 — Pinyon Script 111.503/80.143, #dda2a3. -->
    <p id="groom-name" class="groom__nickname">{{ nickname }}</p>

    <NameBlock :x="49" :y="1069" :z="31" :full-name="fullName" :parents="parents" :instagram="instagram" />
  </section>
</template>

<style scoped>
.groom {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.groom__heading {
  --delay: 60ms;
  z-index: 20;
  left: calc(-52 * var(--px));
  top: calc(61 * var(--px));
  width: calc(700 * var(--px));
  height: calc(232 * var(--px));
  font-family: var(--font-script);
  font-size: calc(127.269 * var(--px));
  font-weight: 400;
  line-height: calc(91.474 * var(--px));
  white-space: pre-line;
  color: var(--title);
}

/* z 63: above the portrait's clouds, under the pastel florals (65+) beside it. */
.groom__nickname {
  --delay: 200ms;
  z-index: 63;
  left: calc(125 * var(--px));
  top: calc(986 * var(--px));
  width: calc(346 * var(--px));
  height: calc(99 * var(--px));
  font-family: var(--font-script);
  font-size: calc(111.503 * var(--px));
  line-height: calc(80.143 * var(--px));
  color: var(--title);
}
</style>
