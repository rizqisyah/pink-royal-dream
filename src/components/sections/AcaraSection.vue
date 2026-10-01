<script setup lang="ts">
// Figma Frame 263 band "acara", y 6920–9960. Coords are band-local design px.
//
// Two events, each printed inside its own arch: 2750:524 at y 7406 and 2757:678 at
// 8943. The second is the first moved down 1537 with nothing else changed, so each row
// is placed once against a per-card top.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { formatEventDateId, formatEventTime } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/acara'

const { el, shown } = useReveal(0.15)
const { acara } = useWedding()

type Card = {
  title: string
  note: string
  date: string
  time: string
  venue: string
  address: string
  maps: string
}

const SLOT_TOPS = [486, 2023]

// The design prints the same reception twice; an unconfigured render keeps both.
const DESIGN_CARD: Card = {
  title: 'Resepsi',
  note: 'Family Only',
  date: 'Minggu,\n25 Oktober 2026',
  time: '19.00 - 21.00 WIB',
  venue: 'Intercontinental Jakarta\nPondok Indah',
  address: 'Jl. Metro Pondok Indah Kav. IV TA PD. Pinang, Kebayoran Lama, Jakarta Selatan',
  maps: 'https://www.google.com/maps/search/?api=1&query=Intercontinental+Jakarta+Pondok+Indah',
}

/** The design's times carry their zone; the API's usually do not. */
const withZone = (t: string) => (t && !/\b(WIB|WITA|WIT)\b/i.test(t) ? `${t} WIB` : t)

/*
 * All or nothing, never a mix: topping a one-event list up from the design would print
 * the design's venue as if it were this couple's, and a guest would drive there. Capped
 * at two — the band has two arches.
 */
const cards = computed<Card[]>(() => {
  const live = (acara.value as any[]).filter((a) => a?.title || a?.name || a?.event_date)
  if (!live.length) return [DESIGN_CARD, DESIGN_CARD]
  return live.slice(0, 2).map((a) => {
    const when = formatEventDateId(a.event_date)
    return {
      title: a.title || a.name || '',
      note: a.description || a.note || '',
      date: when ? `${when.weekday},\n${when.date}` : '',
      time: withZone(formatEventTime(a.event_time)),
      venue: a.location_name || '',
      address: a.address || '',
      maps: a.maps_url || '',
    }
  })
})
</script>

<template>
  <section :ref="el" class="band acara" :class="{ 'is-in': shown }" aria-labelledby="acara-0">
    <BandArt :layers="LAYERS" :shown="shown" />

    <template v-for="(card, i) in cards" :key="i">
      <!-- 2745:207 — Pinyon Script 98.456/109.275, #ed8cae. -->
      <h2 :id="`acara-${i}`" class="acara__title" :style="{ '--t': SLOT_TOPS[i], zIndex: 88 + i }">
        {{ card.title }}
      </h2>
      <!-- 2745:206 — Ibarra Real Nova Italic 23.327/34.991, #ac5b5b. -->
      <p v-if="card.note" class="acara__note" :style="{ '--t': SLOT_TOPS[i], zIndex: 88 + i }">
        {{ card.note }}
      </p>
      <!-- 2745:258 -->
      <p class="acara__date" :style="{ '--t': SLOT_TOPS[i], zIndex: 88 + i }">{{ card.date }}</p>
      <!-- 2745:259 — Bold 23.327/31.026. -->
      <p class="acara__time" :style="{ '--t': SLOT_TOPS[i], zIndex: 88 + i }">{{ card.time }}</p>
      <!-- 2745:251 — SemiBold, #710000. -->
      <p class="acara__venue" :style="{ '--t': SLOT_TOPS[i], zIndex: 88 + i }">{{ card.venue }}</p>
      <!-- 2745:253 — Regular 18.662/27.993, #710000. -->
      <p class="acara__address" :style="{ '--t': SLOT_TOPS[i], zIndex: 88 + i }">{{ card.address }}</p>
      <!-- 2745:257 — Bold, underlined. With no maps_url it is plain text, not a dead link. -->
      <a
        v-if="card.maps"
        class="acara__maps"
        :style="{ '--t': SLOT_TOPS[i], zIndex: 88 + i }"
        :href="card.maps"
        target="_blank"
        rel="noopener noreferrer"
        >View Maps</a
      >
    </template>
  </section>
</template>

<style scoped>
.acara {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.acara__title,
.acara__note,
.acara__date,
.acara__time,
.acara__venue,
.acara__address,
.acara__maps {
  font-family: var(--font-detail);
  font-size: calc(23.327 * var(--px));
  line-height: calc(34.991 * var(--px));
  color: var(--rosewood);
}

/* Each single-line row is a 300-wide box on the design's own centre. */
.acara__title {
  --delay: 60ms;
  left: calc(139.5 * var(--px));
  top: calc(var(--t) * var(--px));
  width: calc(300 * var(--px));
  font-family: var(--font-script);
  font-size: calc(98.456 * var(--px));
  font-weight: 400;
  line-height: calc(109.275 * var(--px));
  white-space: nowrap;
  color: var(--hot-pink);
}

.acara__note {
  --delay: 140ms;
  left: calc(148.98 * var(--px));
  top: calc((var(--t) + 110.31) * var(--px));
  width: calc(300 * var(--px));
  font-style: italic;
}

.acara__date {
  --delay: 200ms;
  left: calc(149.15 * var(--px));
  top: calc((var(--t) + 164.12) * var(--px));
  width: calc(300 * var(--px));
  white-space: pre-line;
}

.acara__time {
  --delay: 260ms;
  left: calc(149.4 * var(--px));
  top: calc((var(--t) + 238.77) * var(--px));
  width: calc(300 * var(--px));
  font-weight: 700;
  line-height: calc(31.026 * var(--px));
}

.acara__venue {
  --delay: 320ms;
  left: calc(148 * var(--px));
  top: calc((var(--t) + 317) * var(--px));
  width: calc(300 * var(--px));
  font-weight: 600;
  white-space: pre-line;
  color: var(--wine);
}

.acara__address {
  --delay: 380ms;
  left: calc(161 * var(--px));
  top: calc((var(--t) + 387) * var(--px));
  width: calc(264 * var(--px));
  font-size: calc(18.662 * var(--px));
  line-height: calc(27.993 * var(--px));
  color: var(--wine);
}

.acara__maps {
  --delay: 440ms;
  left: calc(199.06 * var(--px));
  top: calc((var(--t) + 485.5) * var(--px));
  width: calc(200 * var(--px));
  font-weight: 700;
  text-decoration: underline;
}

.acara__maps:hover,
.acara__maps:focus-visible {
  color: var(--wine);
}
</style>
