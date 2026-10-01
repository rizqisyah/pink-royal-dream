<script setup lang="ts">
// Figma Frame 263 band "quote", y 1110–2620. Coords are band-local design px.
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { useFitText } from '../../composables/useFitText'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/quote'

const { el, shown } = useReveal(0.15)
const { quoteText, quoteVerse } = useWedding()

// The verse comes from the API and can be any length; the card it sits on cannot grow.
const fitVerse = useFitText()
</script>

<template>
  <section :ref="el" class="band quote" :class="{ 'is-in': shown }" aria-labelledby="quote-ref">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2745:93 — Norveil Fantasy Demo 37.181/48.335, #c04935. -->
    <h2 id="quote-ref" class="quote__ref">{{ quoteVerse }}</h2>
    <!-- 2745:94 — Montaga 29.745/48.335, justified, #c04935. -->
    <p :ref="fitVerse" class="quote__text">{{ quoteText }}</p>
  </section>
</template>

<style scoped>
.quote {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* z 58: above the quote frame (57) that holds them. */
.quote__ref,
.quote__text {
  z-index: 58;
  color: var(--quote-red);
}

.quote__ref {
  --delay: 200ms;
  left: calc(47.57 * var(--px));
  top: calc(447 * var(--px));
  width: calc(500 * var(--px));
  font-family: var(--font-verse-ref);
  font-size: calc(37.181 * var(--px));
  font-weight: 400;
  line-height: calc(48.335 * var(--px));
  white-space: nowrap;
}

/*
 * The design's verse sets in 436px. The box allows a little more before the card's
 * scalloped foot, and useFitText shrinks a longer configured verse to stay inside it.
 */
.quote__text {
  --delay: 360ms;
  left: calc(110 * var(--px));
  top: calc(541.81 * var(--px));
  width: calc(375.525 * var(--px));
  height: calc(500 * var(--px));
  font-family: var(--font-verse);
  font-size: calc(29.745 * var(--px) * var(--fit, 1));
  line-height: calc(48.335 * var(--px) * var(--fit, 1));
  text-align: justify;
}
</style>
