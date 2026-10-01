<script setup lang="ts">
// Figma Frame 263 band "rsvp", y 12090–12780. Coords are band-local design px.
//
// The four fields are Figma frames — white, #67764d outline, the label typed inside as
// a placeholder. They ship as real controls, not as art: a raster of a form cannot be
// filled in.
import { computed, ref, watch } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { submitRsvp } from '../../lib/api'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/rsvp'

const { el, shown } = useReveal(0.15)
const { slug, guestCode, guest, guestName } = useWedding()

const name = ref('')
const phone = ref('')
const attendance = ref('')
const guestCount = ref('')
const sending = ref(false)
const error = ref('')
const done = ref(false)
const showPopup = ref(false)

/*
 * A guest can already have replied two ways: a receipt this browser kept, or
 * `guest.has_rsvp` from the API — the only signal when they replied from another
 * device. `guest` arrives after this band mounts, so it is watched, not read once.
 */
const receiptKey = computed(() => `rsvp_${slug.value}_${guestCode.value || 'general'}`)
try {
  if (localStorage.getItem(receiptKey.value)) done.value = true
} catch {
  // Storage blocked (private mode): the API's has_rsvp still covers a repeat visit.
}

watch(
  [guest, guestName],
  ([g, gName]) => {
    if (g?.has_rsvp) done.value = true
    if (g?.phone && !phone.value) phone.value = String(g.phone)
    const known = g?.guest_name ?? g?.name ?? (gName !== 'Nama Tamu' ? gName : '')
    if (known && !name.value) name.value = String(known)
  },
  { immediate: true },
)

async function send() {
  error.value = ''
  if (!name.value.trim()) {
    error.value = 'Nama masih kosong.'
    return
  }
  if (!attendance.value) {
    error.value = 'Pilih kehadiran dulu.'
    return
  }
  sending.value = true
  try {
    await submitRsvp(slug.value, {
      guest_name: name.value.trim(),
      phone: phone.value.trim(),
      attendance_status: attendance.value,
      guest_count: attendance.value === 'hadir' ? parseInt(guestCount.value) || 1 : 0,
    })
    done.value = true
    showPopup.value = true
    try {
      localStorage.setItem(receiptKey.value, new Date().toISOString())
    } catch {
      // See above.
    }
  } catch (err: any) {
    error.value = err?.message || 'Gagal mengirim. Coba lagi.'
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <section :ref="el" class="band rsvp" :class="{ 'is-in': shown }" aria-labelledby="rsvp-heading">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2745:287 — Pinyon Script 108.038/100.567, #dda2a3. -->
    <h2 id="rsvp-heading" class="rsvp__heading">Reservation</h2>
    <!-- 2745:289 — EB Garamond 21.988/29.684, #3f3b3a. -->
    <p class="rsvp__copy">Mohon konfirmasi kehadiran Anda melalui formulir reservasi di bawah:</p>

    <form class="rsvp__form" novalidate @submit.prevent="send">
      <div class="rsvp__fields">
        <label class="sr-only" for="rsvp-name">Nama</label>
        <input
          id="rsvp-name"
          v-model="name"
          class="rsvp__field"
          type="text"
          autocomplete="name"
          placeholder="Nama"
        />

        <label class="sr-only" for="rsvp-phone">No Hp</label>
        <input
          id="rsvp-phone"
          v-model="phone"
          class="rsvp__field"
          type="tel"
          inputmode="tel"
          autocomplete="tel"
          placeholder="No Hp"
        />

        <label class="sr-only" for="rsvp-going">Kehadiran</label>
        <select
          id="rsvp-going"
          v-model="attendance"
          class="rsvp__field"
          :class="{ 'is-empty': !attendance }"
        >
          <option value="" disabled>Will you be joining us?</option>
          <option value="hadir">Ya, saya akan hadir</option>
          <option value="tidak">Maaf, tidak bisa hadir</option>
        </select>

        <label class="sr-only" for="rsvp-count">Jumlah tamu</label>
        <select
          id="rsvp-count"
          v-model="guestCount"
          class="rsvp__field"
          :class="{ 'is-empty': !guestCount }"
          :disabled="attendance === 'tidak'"
        >
          <option value="" disabled>Number of Guests:</option>
          <option v-for="n in 5" :key="n" :value="String(n)">{{ n }} Orang</option>
        </select>
      </div>

      <!-- 2745:300 — #efc7cb pill, Bellefair 21.988/32.982, #603e24. -->
      <!-- Solid like the design until sent; `send()` explains what is missing instead. -->
      <button class="rsvp__send" type="submit" :disabled="sending">
        {{ done ? 'Terkirim' : sending ? 'Mengirim…' : 'Send' }}
      </button>

      <p v-if="error" class="rsvp__error" role="alert">{{ error }}</p>
    </form>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showPopup" class="success-popup">
          <div class="success-popup__box">
            <svg viewBox="0 0 24 24" class="success-popup__icon">
              <path d="M20 6L9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <p class="success-popup__title">Terima Kasih!</p>
            <p class="success-popup__text">Konfirmasi kehadiran Anda telah berhasil dikirim.</p>
            <button class="success-popup__close" type="button" @click="showPopup = false">Tutup</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<style scoped>
.rsvp {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.rsvp__heading,
.rsvp__copy,
.rsvp__form {
  z-index: 45;
}

.rsvp__heading {
  --delay: 60ms;
  left: calc(52.08 * var(--px));
  top: calc(33 * var(--px));
  width: calc(500 * var(--px));
  font-family: var(--font-script);
  font-size: calc(108.038 * var(--px));
  font-weight: 400;
  line-height: calc(100.567 * var(--px));
  white-space: nowrap;
  color: var(--title);
}

.rsvp__copy {
  --delay: 160ms;
  left: calc(145.74 * var(--px));
  top: calc(155.03 * var(--px));
  width: calc(325.423 * var(--px));
  font-family: var(--font-body);
  font-size: calc(21.988 * var(--px));
  line-height: calc(29.684 * var(--px));
  color: var(--ink-dark);
}

/* The form spans the band so its children keep frame coordinates. */
.rsvp__form {
  --delay: 260ms;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.rsvp__form > * {
  position: absolute;
  pointer-events: auto;
}

.rsvp__fields {
  left: calc(27 * var(--px));
  top: calc(231.99 * var(--px));
  width: calc(550.801 * var(--px));
  display: flex;
  flex-direction: column;
  gap: calc(7.696 * var(--px));
}

.rsvp__field {
  width: 100%;
  height: calc(59.368 * var(--px));
  padding: 0 calc(13.193 * var(--px)) calc(6 * var(--px));
  border: max(1px, calc(0.88 * var(--px))) solid var(--field-line);
  border-radius: calc(12.093 * var(--px));
  background: #fff;
  font-family: var(--font-field);
  font-size: calc(21.988 * var(--px));
  color: var(--ink-dark);
  outline: none;
}

/*
 * The native <select> keeps its dropdown indicator: the design's flat plate has none,
 * but hiding it would leave the control with no affordance at all.
 */
.rsvp__field::placeholder,
.rsvp__field.is-empty {
  color: rgba(30, 60, 114, 0.5);
}

.rsvp__field option {
  color: var(--ink-dark);
}

.rsvp__field:focus {
  border-color: var(--title);
  box-shadow: 0 0 0 calc(2 * var(--px)) rgba(221, 162, 163, 0.35);
}

.rsvp__field:disabled {
  opacity: 0.55;
}

.rsvp__send {
  left: calc(70.98 * var(--px));
  top: calc(514.54 * var(--px));
  width: calc(468.346 * var(--px));
  height: calc(59.368 * var(--px));
  border: 0;
  border-radius: calc(108.841 * var(--px));
  background: var(--button);
  font-family: var(--font-field);
  font-size: calc(21.988 * var(--px));
  line-height: calc(32.982 * var(--px));
  color: var(--button-ink);
  cursor: pointer;
  transition: filter 0.2s ease;
}

.rsvp__send:hover:not(:disabled) {
  filter: brightness(0.96);
}

.rsvp__send:disabled {
  cursor: default;
  opacity: 0.7;
}

.rsvp__error {
  left: calc(70.98 * var(--px));
  top: calc(584 * var(--px));
  width: calc(468.346 * var(--px));
  font-family: var(--font-field);
  font-size: calc(20 * var(--px));
  text-align: center;
  color: var(--gift-ink);
}
</style>
