<script setup lang="ts">
// Figma Frame 263 band "gift", y 11280–12090. Coords are band-local design px.
//
// Each card is the same shape: a white 359-wide plate (Rectangle 20) over a #e4b7b2 tab
// (Rectangle 21) whose visible strip carries the copy button. All flat colour, so the
// cards are drawn here and the copy icon is a real button, not a picture of one.
import { computed, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/gift'
import { assets } from '../../lib/bandAssets'

const { el, shown } = useReveal(0.15)
const { gift } = useWedding()

const copyIcon = assets['gift/parts/copy-icon.webp']

type Card =
  | { kind: 'bank'; bank: string; number: string; holder: string; copy: string }
  | { kind: 'kado'; address: string; phone: string; holder: string; copy: string }

// The design's own mock data: two accounts and a postal address.
const DESIGN: Card[] = [
  { kind: 'bank', bank: 'Mandiri', number: '1760001522505', holder: 'A/n Harry Widjaja', copy: '1760001522505' },
  { kind: 'bank', bank: 'BCA', number: '6044573649', holder: 'A/n Amanda Putri Syaharani', copy: '6044573649' },
  {
    kind: 'kado',
    address: 'Melmerby, Penrith CA10, nomor VII A 1HB, Jakarta Pusat, Jakarta, Indonesia',
    phone: '1234567890',
    holder: 'A/n Budiyanto Ahmad',
    copy: 'Melmerby, Penrith CA10, nomor VII A 1HB, Jakarta Pusat, Jakarta, Indonesia',
  },
]

/* A `kado` row is a postal address, not an account — the API has no separate field. */
const isKado = (bank?: string) => /kado|alamat|address/i.test(bank || '')

const cards = computed<Card[]>(() => {
  const live = (gift.value as any[])
    .map((g): Card | null => {
      const number = String(g.account_number || '').trim()
      const name = String(g.account_name || '').trim()
      if (!number && !name) return null
      return isKado(g.bank_name)
        ? { kind: 'kado', address: number, phone: String(g.phone || '').trim(), holder: name ? `A/n ${name}` : '', copy: number }
        : { kind: 'bank', bank: String(g.bank_name || '').trim(), number, holder: name ? `A/n ${name}` : '', copy: number }
    })
    .filter((c): c is Card => !!c)
  // Three slots, like the design; a fourth account would run into the RSVP band.
  return live.length ? live.slice(0, 3) : DESIGN
})

/* Cards stack from y 243, 24 apart: Figma's own 11523 / 11650 / 11777. */
const FIRST = 243
const GAP = 24
const HEIGHT = { bank: 103, kado: 254.656 }

const placed = computed(() => {
  let top = FIRST
  return cards.value.map((card, i) => {
    const at = { card, top, height: HEIGHT[card.kind], z: 39 + i }
    top += HEIGHT[card.kind] + GAP
    return at
  })
})

// Grows only if three tall address cards would not fit the design's band.
const sectionHeight = computed(() => {
  const last = placed.value[placed.value.length - 1]
  return Math.max(BAND_HEIGHT, last ? last.top + last.height + 58 : BAND_HEIGHT)
})

const copied = ref(-1)
async function copy(i: number, text: string) {
  if (!text) return
  try {
    await navigator.clipboard.writeText(text)
    copied.value = i
    window.setTimeout(() => (copied.value = -1), 1600)
  } catch {
    // Clipboard is permission-gated and absent over plain http; the number is on
    // screen either way, so a failure is silent rather than an error the guest
    // cannot act on.
  }
}
</script>

<template>
  <section :ref="el" class="band gift" :class="{ 'is-in': shown }" aria-labelledby="gift-heading">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2745:216 — Pinyon Script 98.27/91.474, #dda2a3. -->
    <h2 id="gift-heading" class="gift__heading">Wedding Gift</h2>

    <div
      v-for="(p, i) in placed"
      :key="i"
      class="gift__card"
      :style="{ '--top': p.top, '--h': p.height, '--delay': `${200 + i * 120}ms`, zIndex: p.z }"
    >
      <div class="gift__tab"></div>
      <div class="gift__plate"></div>

      <template v-if="p.card.kind === 'bank'">
        <!-- 2745:220 — Rosarivo 18. -->
        <p class="gift__bank">{{ p.card.bank }}</p>
        <!-- 2745:221 — Ropa Sans 24. -->
        <p class="gift__number">{{ p.card.number }}</p>
        <!-- 2745:222 — Rosarivo 15. -->
        <p class="gift__holder">{{ p.card.holder }}</p>
      </template>
      <template v-else>
        <!-- 2745:234 — Rosarivo 24. -->
        <p class="gift__label">Alamat</p>
        <!-- 2745:235 — Ibarra Real Nova 18.662/27.993, #710000. -->
        <p class="gift__address">{{ p.card.address }}</p>
        <!-- 2751:556 — Ropa Sans 24. -->
        <p v-if="p.card.phone" class="gift__phone">{{ p.card.phone }}</p>
        <!-- 2745:236 — Rosarivo 15. -->
        <p class="gift__holder gift__holder--kado">{{ p.card.holder }}</p>
      </template>

      <button
        type="button"
        class="gift__copy"
        :aria-label="copied === i ? 'Tersalin' : `Salin ${p.card.copy}`"
        @click="copy(i, p.card.copy)"
      >
        <img class="gift__copyicon" :class="{ 'is-copied': copied === i }" :src="copyIcon" alt="" />
        <span v-if="copied === i" class="gift__done" aria-hidden="true">Tersalin</span>
      </button>
    </div>
  </section>
</template>

<style scoped>
.gift {
  height: calc(v-bind(sectionHeight) * var(--px));
}

.gift__heading {
  --delay: 60ms;
  z-index: 38;
  left: calc(41 * var(--px));
  top: calc(49 * var(--px));
  width: calc(500 * var(--px));
  font-family: var(--font-script);
  font-size: calc(98.27 * var(--px));
  font-weight: 400;
  line-height: calc(91.474 * var(--px));
  white-space: nowrap;
  color: var(--title);
}

/* Child coordinates are relative to the frame's left edge and the card's top. */
.gift__card {
  left: 0;
  top: calc(var(--top) * var(--px));
  width: calc(596 * var(--px));
  height: calc(var(--h) * var(--px));
  text-align: left;
}

.gift__card > * {
  position: absolute;
  margin: 0;
}

.gift__tab,
.gift__plate {
  top: 0;
  height: 100%;
  border-radius: 1px;
}

.gift__tab {
  left: calc(364 * var(--px));
  width: calc(177 * var(--px));
  background: var(--gift-tab);
}

.gift__plate {
  left: calc(54 * var(--px));
  width: calc(359 * var(--px));
  background: #fff;
}

.gift__bank,
.gift__number,
.gift__holder,
.gift__label,
.gift__phone {
  line-height: normal;
  color: var(--gift-ink);
}

.gift__bank {
  left: calc(89 * var(--px));
  top: calc(33 * var(--px));
  width: calc(100 * var(--px));
  font-family: var(--font-bank);
  font-size: calc(18 * var(--px));
}

.gift__number,
.gift__phone {
  font-family: var(--font-figures);
  font-size: calc(24 * var(--px));
}

.gift__number {
  left: calc(194 * var(--px));
  top: calc(22 * var(--px));
  width: calc(215 * var(--px));
}

.gift__holder {
  left: calc(194 * var(--px));
  top: calc(52 * var(--px));
  width: calc(215 * var(--px));
  font-family: var(--font-bank);
  font-size: calc(15 * var(--px));
}

.gift__label {
  left: calc(89 * var(--px));
  top: calc(30 * var(--px));
  font-family: var(--font-bank);
  font-size: calc(24 * var(--px));
}

.gift__address {
  left: calc(90 * var(--px));
  top: calc(70 * var(--px));
  width: calc(313 * var(--px));
  font-family: var(--font-detail);
  font-size: calc(18.662 * var(--px));
  line-height: calc(27.993 * var(--px));
  color: var(--wine);
}

.gift__phone {
  left: calc(90 * var(--px));
  top: calc(136 * var(--px));
}

.gift__holder--kado {
  left: calc(90 * var(--px));
  top: calc(166 * var(--px));
  width: calc(313 * var(--px));
}

/* The visible strip of the tab, 413–541: the whole strip is the hit area. */
.gift__copy {
  left: calc(413 * var(--px));
  top: 0;
  width: calc(128 * var(--px));
  height: 100%;
  padding: 0;
  border: 0;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gift__copyicon {
  display: block;
  width: calc(35 * var(--px));
  height: calc(35 * var(--px));
  object-fit: cover;
  transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1), opacity 200ms ease;
}

.gift__copy:hover .gift__copyicon,
.gift__copy:focus-visible .gift__copyicon {
  transform: translateY(calc(-2 * var(--px)));
}

.gift__copyicon.is-copied {
  transform: scale(0.82);
  opacity: 0.55;
}

.gift__done {
  position: absolute;
  left: 0;
  right: 0;
  top: calc(50% + 22 * var(--px));
  font-family: var(--font-bank);
  font-size: calc(14 * var(--px));
  text-align: center;
  color: #fff;
}
</style>
