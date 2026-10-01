<script setup lang="ts">
// Figma Frame 263 band "savedate", y 5690–6920. Coords are band-local design px.
// The countdown is live: Figma prints four zeroes, this counts down to the first event.
import { computed, onUnmounted, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { parseEventStart, remainingUntil } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/savedate'

const { el, shown } = useReveal(0.15)
const { acara, wedding } = useWedding()

const now = ref(Date.now())
const timer = window.setInterval(() => (now.value = Date.now()), 1000)
onUnmounted(() => window.clearInterval(timer))

/*
 * The design's own event: "Minggu, 25 Oktober 2026, 19.00 - 21.00 WIB". Used only when
 * no event is configured; a deployment with real `acara` counts to that instead.
 */
const DESIGN_DAY = new Date(2026, 9, 25, 19, 0)

const target = computed(() => {
  if (wedding.value?.countdown_date) {
    const at = new Date(wedding.value.countdown_date)
    if (!Number.isNaN(at.getTime())) return at
  }
  for (const a of acara.value as any[]) {
    const at = parseEventStart(a?.event_date, a?.event_time)
    if (at) return at
  }
  return DESIGN_DAY
})

const left = computed(() => remainingUntil(target.value, now.value))

/*
 * 2745:170 / 181 / 176 / 186 — four 8px-padded cells, not on a grid: Figma placed each
 * by hand, so each keeps its own origin. Digit and label are positioned separately
 * rather than stacked, so the digit's line box never moves the label.
 */
const cells = computed(() => [
  { key: 'days', label: 'Days', value: left.value.days, x: 160, y: 591, w: 143.817 },
  { key: 'hours', label: 'Hours', value: left.value.hours, x: 294.05, y: 591, w: 143.583 },
  { key: 'minutes', label: 'Minutes', value: left.value.minutes, x: 155, y: 704.25, w: 143.817 },
  { key: 'seconds', label: 'Seconds', value: left.value.seconds, x: 288.76, y: 704.25, w: 143.583 },
])

// Figma authors this break; the box sets `white-space: pre-line`.
const TITLE = 'Save the\nDate'
</script>

<template>
  <section :ref="el" class="band savedate" :class="{ 'is-in': shown }" aria-labelledby="save-the-date">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2745:166 — Pinyon Script 113.156/81.331, #dda2a3. -->
    <h2 id="save-the-date" class="savedate__title">{{ TITLE }}</h2>

    <!-- 2745:172… — Ibarra Real Nova Italic 64 for the figures, Regular 25 for the labels, #c18182. -->
    <template v-for="(c, i) in cells" :key="c.key">
      <p
        class="savedate__n"
        :style="{ '--x': c.x, '--y': c.y, '--w': c.w, '--delay': `${200 + i * 90}ms` }"
      >
        {{ c.value }}
      </p>
      <p
        class="savedate__l"
        :style="{ '--x': c.x, '--y': c.y, '--w': c.w, '--delay': `${260 + i * 90}ms` }"
      >
        {{ c.label }}
      </p>
    </template>
  </section>
</template>

<style scoped>
.savedate {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* z 111: the last thing Figma paints in this band, over the border plate. */
.savedate__title {
  --delay: 60ms;
  z-index: 111;
  left: calc(74 * var(--px));
  top: calc(114 * var(--px));
  width: calc(449 * var(--px));
  height: calc(163 * var(--px));
  font-family: var(--font-script);
  font-size: calc(113.156 * var(--px));
  font-weight: 400;
  line-height: calc(81.331 * var(--px));
  white-space: pre-line;
  color: var(--title);
}

/* z 36: on the white ellipse (35), under the pastel florals (71–74). */
.savedate__n,
.savedate__l {
  z-index: 36;
  left: calc((var(--x) + 8) * var(--px));
  width: calc((var(--w) - 16) * var(--px));
  font-family: var(--font-detail);
  line-height: normal;
  white-space: nowrap;
  color: var(--gold);
}

.savedate__n {
  top: calc((var(--y) + 8) * var(--px));
  height: calc(71 * var(--px));
  font-size: calc(64 * var(--px));
  font-style: italic;
  /* The seconds tick every second; a proportional face would shuffle the row sideways. */
  font-variant-numeric: tabular-nums;
}

.savedate__l {
  top: calc((var(--y) + 87) * var(--px));
  font-size: calc(25 * var(--px));
}
</style>
