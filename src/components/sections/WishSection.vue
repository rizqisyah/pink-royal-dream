<script setup lang="ts">
// Figma Frame 263 band "wish", y 12780–14180. Coords are band-local design px.
//
// Everything below the heading is live: two inputs, a Send button, and the list. The
// design shows three wishes and a "Show more" pill; the list keeps that window — a
// fixed-height panel that scrolls — so a long list never moves the bands below it.
import { computed, ref, watch } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { formatWishTime } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/wish'

const { el, shown } = useReveal(0.15)
const { wishes, sendWish, guest, guestName, wedding } = useWedding()

type Wish = { guest_name?: string; message?: string; created_at?: string | null; time?: string }

const DESIGN_MESSAGE =
  'Wishing you a lifetime filled with endless love, gentle laughter, and countless beautiful moments together. Happy Wedding!'
const DESIGN: Wish[] = Array.from({ length: 3 }, () => ({
  guest_name: 'Satrio & Istri',
  time: '09 June 2025, 09:00',
  message: DESIGN_MESSAGE,
}))

const list = computed<Wish[]>(() => {
  const live = ((wishes.value || []) as Wish[]).filter((w) => w?.guest_name || w?.message)
  // The design's cards only stand in for an unconfigured render, never beside real wishes.
  if (live.length || wedding.value) return live
  return DESIGN
})

const PAGE = 3
const visible = ref(PAGE)
const shownList = computed(() => list.value.slice(0, visible.value))
const hasMore = computed(() => visible.value < list.value.length)

const name = ref('')
watch(
  [guest, guestName],
  () => {
    if (!name.value) {
      const resolved =
        guest.value?.guest_name ||
        guest.value?.name ||
        (guestName.value !== 'Nama Tamu' ? guestName.value : '')
      if (resolved) name.value = resolved
    }
  },
  { immediate: true },
)
const message = ref('')
const sending = ref(false)
const error = ref('')
const showPopup = ref(false)

async function send() {
  error.value = ''
  if (!name.value.trim()) {
    error.value = 'Nama wajib diisi.'
    return
  }
  if (!message.value.trim()) {
    error.value = 'Ucapannya masih kosong.'
    return
  }
  sending.value = true
  try {
    await sendWish({ guest_name: name.value.trim(), message: message.value.trim() })
    message.value = ''
    visible.value = Math.max(visible.value, PAGE)
    showPopup.value = true
  } catch (err: any) {
    error.value = err?.message || 'Gagal mengirim ucapan. Coba lagi.'
  } finally {
    sending.value = false
  }
}

const timeOf = (w: Wish) => w.time || formatWishTime(w.created_at)
</script>

<template>
  <section :ref="el" class="band wish" :class="{ 'is-in': shown }" aria-labelledby="wish-heading">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2745:303 — Pinyon Script 93.746/100.567, #dda2a3. -->
    <h2 id="wish-heading" class="wish__heading">Wedding Wishes</h2>

    <!-- 2745:310 / 2745:304 / 2745:306 — the two fields and their Send pill. -->
    <form class="wish__form" novalidate @submit.prevent="send">
      <label class="sr-only" for="wish-name">Nama</label>
      <input id="wish-name" v-model="name" class="wish__name" type="text" placeholder="Name" />

      <label class="sr-only" for="wish-message">Ucapan</label>
      <textarea id="wish-message" v-model="message" class="wish__message" placeholder="Give your wish"></textarea>

      <button class="wish__btn wish__send" type="submit" :disabled="sending">
        {{ sending ? 'Mengirim…' : 'Send' }}
      </button>

      <p v-if="error" class="wish__error" role="alert">{{ error }}</p>
    </form>

    <!-- 2745:315… — name, time, message, three to a window, 191.3 apart. -->
    <ul class="wish__list">
      <li v-for="(w, i) in shownList" :key="i" class="wish__card">
        <p class="wish__who">{{ w.guest_name || 'Tamu' }}</p>
        <p v-if="timeOf(w)" class="wish__time">{{ timeOf(w) }}</p>
        <p class="wish__text">{{ w.message }}</p>
      </li>
    </ul>

    <!-- 2745:308 -->
    <button
      type="button"
      class="wish__btn wish__more"
      :aria-disabled="!hasMore"
      @click="hasMore && (visible += PAGE)"
    >
      Show more
    </button>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showPopup" class="success-popup">
          <div class="success-popup__box">
            <svg viewBox="0 0 24 24" class="success-popup__icon">
              <path d="M20 6L9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <p class="success-popup__title">Terima Kasih!</p>
            <p class="success-popup__text">Ucapan dan doa Anda telah berhasil dikirim.</p>
            <button class="success-popup__close" type="button" @click="showPopup = false">Tutup</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<style scoped>
.wish {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.wish__heading,
.wish__form,
.wish__list,
.wish__more {
  z-index: 46;
}

/* Wider than the 549 the words take, centred on the design's 305.9: a nowrap line that
   overflows its box only spills rightward, off centre. */
.wish__heading {
  --delay: 60ms;
  left: calc(-44.1 * var(--px));
  top: calc(28.96 * var(--px));
  width: calc(700 * var(--px));
  font-family: var(--font-script);
  font-size: calc(93.746 * var(--px));
  font-weight: 400;
  line-height: calc(100.567 * var(--px));
  white-space: nowrap;
  color: var(--title);
}

/* The form spans the band so its children keep frame coordinates. */
.wish__form {
  --delay: 180ms;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.wish__form > * {
  position: absolute;
  pointer-events: auto;
}

.wish__name,
.wish__message {
  left: calc(33.6 * var(--px));
  width: calc(545.304 * var(--px));
  border: max(1px, calc(0.88 * var(--px))) solid var(--field-line);
  background: #fff;
  font-family: var(--font-field);
  font-size: calc(21.988 * var(--px));
  color: var(--ink);
  outline: none;
}

.wish__name::placeholder,
.wish__message::placeholder {
  color: rgba(117, 117, 117, 0.5);
}

.wish__name:focus,
.wish__message:focus {
  border-color: var(--title);
  box-shadow: 0 0 0 calc(2 * var(--px)) rgba(221, 162, 163, 0.35);
}

.wish__name {
  top: calc(157.59 * var(--px));
  height: calc(61.567 * var(--px));
  padding: 0 calc(13.19 * var(--px)) calc(2 * var(--px));
  border-radius: calc(8.795 * var(--px));
}

.wish__message {
  top: calc(234.55 * var(--px));
  height: calc(98.946 * var(--px));
  padding: calc(13.193 * var(--px));
  border-radius: calc(12.093 * var(--px));
  line-height: calc(32.982 * var(--px));
  resize: none;
}

.wish__btn {
  width: calc(468.346 * var(--px));
  height: calc(59.368 * var(--px));
  border: 0;
  border-radius: calc(108.841 * var(--px));
  background: var(--button);
  font-family: var(--font-field);
  font-size: calc(21.988 * var(--px));
  line-height: calc(32.982 * var(--px));
  color: var(--ink);
  cursor: pointer;
  transition: filter 0.2s ease;
}

.wish__btn:hover:not(:disabled):not([aria-disabled='true']) {
  filter: brightness(0.96);
}

.wish__btn:disabled,
.wish__btn[aria-disabled='true'] {
  cursor: default;
}

.wish__send {
  left: calc(70.98 * var(--px));
  top: calc(348.89 * var(--px));
}

.wish__error {
  left: calc(70.98 * var(--px));
  top: calc(410 * var(--px));
  width: calc(468.346 * var(--px));
  font-family: var(--font-field);
  font-size: calc(18 * var(--px));
  text-align: center;
  color: var(--gift-ink);
}

.wish__more {
  --delay: 360ms;
  left: calc(69.88 * var(--px));
  top: calc(1004.13 * var(--px));
}

/* The three-card window of the design; longer lists scroll inside it. */
.wish__list {
  --delay: 280ms;
  left: calc(70.98 * var(--px));
  top: calc(437.94 * var(--px));
  width: calc(470 * var(--px));
  height: calc(552 * var(--px));
  overflow-y: auto;
  scrollbar-width: thin;
  list-style: none;
  text-align: left;
  color: var(--ink);
}

.wish__card {
  margin-bottom: calc(29.6 * var(--px));
}

.wish__who {
  font-family: var(--font-card);
  font-weight: 800;
  font-size: calc(21.988 * var(--px));
  line-height: calc(32.982 * var(--px));
}

.wish__time {
  font-family: var(--font-field);
  font-size: calc(19.789 * var(--px));
  line-height: calc(29.684 * var(--px));
}

.wish__text {
  font-family: var(--font-field);
  font-size: calc(21.988 * var(--px));
  line-height: calc(32.982 * var(--px));
  overflow-wrap: break-word;
}
</style>
