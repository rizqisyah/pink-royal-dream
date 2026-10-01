<script setup lang="ts">
// Figma Frame 263 band "acara", y 6920–9960. Coords are band-local design px.
//
// Two events, each printed inside its own arch: 2750:524 at y 7406 and 2757:678 at
// 8943. The second is the first moved down 1537 with nothing else changed.
//
// Each card is one column that FLOWS, not seven rows pinned at Figma's y: a long event
// name, venue or address wraps and pushes everything under it down instead of printing
// over it. The gaps between rows are Figma's own, so the design's copy lands exactly
// where the render has it.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { useLineFit } from '../../composables/useLineFit'
import { formatEventDateId, formatEventTime } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/acara'

const { el, shown } = useReveal(0.15)
const { acara, gallery, wedding } = useWedding()

// One fitter per card: a heading is capped at two lines and shrinks past that.
const fitTitles = [useLineFit(2), useLineFit(2)]

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
 * "Resepsi | Family Only": the part after the first "|" is the small italic line under
 * the script heading — the design's "Family Only". It wins over `description`, since it
 * is what the admin typed into the event name on purpose.
 */
function splitTitle(raw: string): { title: string; note: string } {
  const at = raw.indexOf('|')
  if (at < 0) return { title: raw.trim(), note: '' }
  return { title: raw.slice(0, at).trim(), note: raw.slice(at + 1).trim() }
}

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
    const { title, note } = splitTitle(String(a.title || a.name || ''))
    return {
      title,
      note: note || a.description || a.note || '',
      date: when ? `${when.weekday},\n${when.date}` : '',
      time: withZone(formatEventTime(a.event_time)),
      venue: a.location_name || '',
      address: a.address || '',
      maps: a.maps_url || '',
    }
  })
})

/*
 * One event: the second arch and everything that belongs to it go, and the band closes
 * up by exactly the 1537 the second card sits below the first — the next band then
 * starts where the second arch would have.
 *
 *   2750:525 arch · 2750:526 ellipse · 2750:527 swans · 2750:528 "It's The Day!"
 *   2755:611/612/617/618 the pastel sprays that frame the second arch
 */
const SECOND_CARD = [
  '2750:525', '2750:526', '2750:527', '2750:528',
  '2755:611', '2755:612', '2755:617', '2755:618',
  // The first card's side sprays (2750:539/540) hang 600px below where a single card
  // ends — straight over the RSVP heading and form — so they go with the second card.
  '2750:539', '2750:540',
]
const CARD_STEP = 1537

const single = computed(() => cards.value.length === 1)
const skipLayers = computed(() => (single.value ? SECOND_CARD : []))
const sectionHeight = computed(() => (single.value ? BAND_HEIGHT - CARD_STEP : BAND_HEIGHT))

/*
 * In the design the last sprays hang ~290px into the gallery band, where the "Gallery"
 * heading and photo paint over them. When the gallery is not next (a wedding without
 * photos, or the cut-down single-card band), those sprays would land on whatever band
 * is — so the band is clipped at its own bottom edge instead.
 */
const galleryHidden = computed(() => !!wedding.value && !(gallery.value as any[]).some((g) => g?.image_url))
const clipBottom = computed(() => single.value || galleryHidden.value)
</script>

<template>
  <section
    :ref="el"
    class="band acara"
    :class="{ 'is-in': shown, 'is-clipped': clipBottom }"
    aria-labelledby="acara-0"
  >
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />

    <div
      v-for="(card, i) in cards"
      :key="i"
      class="acara__card"
      :style="{ '--t': SLOT_TOPS[i], zIndex: 88 + i }"
    >
      <!-- 2745:207 — Pinyon Script 98.456/109.275, #ed8cae. -->
      <h2 :id="`acara-${i}`" :ref="fitTitles[i]" class="acara__title">{{ card.title }}</h2>
      <!-- 2745:206 — Ibarra Real Nova Italic 23.327/34.991, #ac5b5b. Also the part of a
           "Resepsi | Family Only" name after the bar. -->
      <p v-if="card.note" class="acara__note">{{ card.note }}</p>
      <!-- 2745:258 -->
      <p v-if="card.date" class="acara__date">{{ card.date }}</p>
      <!-- 2745:259 — Bold 23.327/31.026. -->
      <p v-if="card.time" class="acara__time">{{ card.time }}</p>
      <!-- 2745:251 — SemiBold, #710000. -->
      <p v-if="card.venue" class="acara__venue">{{ card.venue }}</p>
      <!-- 2745:253 — Regular 18.662/27.993, #710000. -->
      <p v-if="card.address" class="acara__address">{{ card.address }}</p>
      <!-- 2745:257 — Bold, underlined. With no maps_url there is no dead link. -->
      <a
        v-if="card.maps"
        class="acara__maps"
        :href="card.maps"
        target="_blank"
        rel="noopener noreferrer"
        >View Maps</a
      >
    </div>
  </section>
</template>

<style scoped>
.acara {
  height: calc(v-bind(sectionHeight) * var(--px));
}

/* `clip`, not `hidden`: it creates no scroll container and no stacking context, so the
   band's layers still stack against the bands around it by their global z. */
.acara.is-clipped {
  overflow: clip;
}

/*
 * The card: a 300-wide column centred on x 298, the axis the design's rows share. Rows
 * whose own centre sits a few px off it (the heading 8.5 left, the address 5 left, …)
 * keep that offset with `left`, so the design's copy lands on the render's ink.
 */
.acara__card {
  --delay: 0ms;
  left: calc(148 * var(--px));
  top: calc(var(--t) * var(--px));
  width: calc(300 * var(--px));
  display: flex;
  flex-direction: column;
  align-items: center;
}

.acara__card > * {
  position: relative;
  max-width: 100%;
  margin: 0;
  font-family: var(--font-detail);
  font-size: calc(23.327 * var(--px));
  line-height: calc(34.991 * var(--px));
  color: var(--rosewood);
  overflow-wrap: break-word;
  /* The band's shared entrance only reaches its direct children; carry it one level down
     so the rows still arrive one after another. */
  opacity: 0;
  transform: translateY(calc(24 * var(--px)));
  transition:
    opacity 1200ms cubic-bezier(0.16, 1, 0.3, 1) var(--delay, 0ms),
    transform 1600ms cubic-bezier(0.16, 1, 0.28, 1) var(--delay, 0ms);
}

.acara.is-in .acara__card > * {
  opacity: 1;
  transform: none;
}

/*
 * Wraps when the name is long. Single-line height is Figma's 109.275 — an 80 line box
 * plus padding that puts the glyphs exactly where the 109.275 box did — so a wrapped
 * name stacks at 80 instead of leaving a 109px gulf between its lines.
 *
 * Capped at two lines: at 98px a script name wider than the arch would otherwise break
 * word by word down the whole card. useLineFit counts the lines and shrinks past two;
 * a one-line name is untouched.
 */
.acara__title {
  --delay: 60ms;
  left: calc(-8.5 * var(--px));
  width: 100%;
  padding-block: calc(14.6375 * var(--px));
  font-family: var(--font-script);
  font-size: calc(98.456 * var(--px) * var(--fit, 1));
  font-weight: 400;
  line-height: calc(80 * var(--px) * var(--fit, 1));
  color: var(--hot-pink);
}

/* Gaps below are Figma's: each row's y minus where the row above it ends. */
.acara__note {
  --delay: 140ms;
  left: calc(0.98 * var(--px));
  margin-top: calc(1.035 * var(--px));
  font-style: italic;
}

.acara__date {
  --delay: 200ms;
  left: calc(1.15 * var(--px));
  margin-top: calc(18.82 * var(--px));
  white-space: pre-line;
}

.acara__time {
  --delay: 260ms;
  left: calc(1.4 * var(--px));
  margin-top: calc(4.668 * var(--px));
  font-weight: 700;
  line-height: calc(31.026 * var(--px));
}

.acara__venue {
  --delay: 320ms;
  margin-top: calc(47.204 * var(--px));
  font-weight: 600;
  white-space: pre-line;
  color: var(--wine);
}

.acara__address {
  --delay: 380ms;
  left: calc(-5 * var(--px));
  width: calc(264 * var(--px));
  font-size: calc(18.662 * var(--px));
  line-height: calc(27.993 * var(--px));
  color: var(--wine);
}

.acara__maps {
  --delay: 440ms;
  left: calc(1.06 * var(--px));
  margin-top: calc(14.521 * var(--px));
  font-weight: 700;
  text-decoration: underline;
}

@media (prefers-reduced-motion: reduce) {
  .acara__card > * {
    opacity: 1;
    transform: none;
    transition: none;
  }
}

.acara__maps:hover,
.acara__maps:focus-visible {
  color: var(--wine);
}
</style>
