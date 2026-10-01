<script setup lang="ts">
// Figma Frame 263 band "closing", y 14180–16075. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { useFitText } from '../../composables/useFitText'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/closing'

const { el, shown } = useReveal(0.15)
const {
  coupleNickname,
  closingMessage,
  parsedOverride,
  wedding,
  customSpousePhoto,
  customHeroPhoto,
  spousePhotoTransform,
} = useWedding()

// 2751:580 — the couple inside the pink mirror; the API's photo takes its place.
const MIRROR = '2751:580'

const layers = computed(() => {
  const photo = customSpousePhoto.value || customHeroPhoto.value
  if (!photo) return LAYERS
  const t = spousePhotoTransform.value
  return LAYERS.map((l) =>
    l.id === MIRROR ? { ...l, src: photo, objectPosition: `${t.x ?? 50}% ${t.y ?? 50}%` } : l,
  )
})

/*
 * "#MARriedtomywoMAN" is this couple's pun (MARio + amANda). Live data shows its own
 * hashtag or none — never the design's.
 */
const hashtag = computed(
  () => parsedOverride.value?.words?.hashtag || (wedding.value ? '' : '#MARriedtomywoMAN'),
)

// The closing message is configurable and the box under it is fixed.
const fitMessage = useFitText()
</script>

<template>
  <section :ref="el" class="band closing" :class="{ 'is-in': shown }" aria-labelledby="thanks">
    <BandArt :layers="layers" :shown="shown" />

    <!-- 2745:345 — Pinyon Script 93.746/100.567, #4e4e4e. -->
    <h2 id="thanks" class="closing__thanks">Thank You</h2>
    <!-- 2745:347 — Calligraphy Script 24/41, #9d9191. -->
    <p :ref="fitMessage" class="closing__message">{{ closingMessage }}</p>
    <!-- 2745:346 — Pinyon Script 76.75/63, #dda2a3. -->
    <p class="closing__couple">{{ coupleNickname }}</p>
    <!-- 2757:673 — Barley Sign 38.455/33.167, #dda2a3. -->
    <p v-if="hashtag" class="closing__hashtag">{{ hashtag }}</p>

    <!-- 2745:324 — the #ffd1d4 bar the credit sits on. -->
    <div class="closing__bar" aria-hidden="true"></div>
    <!-- 2745:325 — Cloister Black Light 26/101, #935021. -->
    <p class="closing__credit">Created by 25ribuaja x Qinvi</p>
  </section>
</template>

<style scoped>
.closing {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.closing__thanks {
  --delay: 60ms;
  z-index: 47;
  left: calc(49 * var(--px));
  top: calc(296 * var(--px));
  width: calc(500 * var(--px));
  font-family: var(--font-script);
  font-size: calc(93.746 * var(--px));
  font-weight: 400;
  line-height: calc(100.567 * var(--px));
  white-space: nowrap;
  color: var(--charcoal);
}

/* Figma's y is 429; Calligraphy Script's ink lands 10 low there, measured against the render. */
.closing__message {
  --delay: 180ms;
  z-index: 49;
  left: calc(75 * var(--px));
  top: calc(419 * var(--px));
  width: calc(447 * var(--px));
  height: calc(164 * var(--px));
  font-family: var(--font-closing);
  font-size: calc(24 * var(--px) * var(--fit, 1) * var(--closing-comp, 1));
  line-height: calc(41 * var(--px) * var(--fit, 1));
  color: var(--grey-text);
}

.closing__couple {
  --delay: 300ms;
  z-index: 48;
  left: calc(-31 * var(--px));
  top: calc(630 * var(--px));
  width: calc(659 * var(--px));
  font-family: var(--font-script);
  font-size: calc(76.75 * var(--px));
  line-height: calc(63 * var(--px));
  color: var(--title);
}

/* Figma's y is 703; Barley Sign's ink lands 5 high there, measured against the render. */
.closing__hashtag {
  --delay: 400ms;
  z-index: 112;
  left: calc(87 * var(--px));
  top: calc(708 * var(--px));
  width: calc(423 * var(--px));
  height: calc(86.042 * var(--px));
  font-family: var(--font-hashtag);
  font-size: calc(38.455 * var(--px));
  line-height: calc(33.167 * var(--px));
  color: var(--title);
}

.closing__bar {
  z-index: 100;
  left: calc(-17 * var(--px));
  top: calc(1822 * var(--px));
  width: calc(630 * var(--px));
  height: calc(73 * var(--px));
  background: var(--footer-bar);
}

.closing__credit {
  --delay: 200ms;
  z-index: 101;
  left: calc(102 * var(--px));
  top: calc(1810 * var(--px));
  width: calc(392 * var(--px));
  height: calc(83 * var(--px));
  font-family: var(--font-credit);
  font-size: calc(26 * var(--px));
  line-height: calc(101 * var(--px));
  white-space: nowrap;
  color: var(--footer-ink);
}
</style>
