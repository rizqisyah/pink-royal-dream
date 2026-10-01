<script setup lang="ts">
/*
 * The screen before the cover, after the TemaPsrt theme's loader: the cover's own wax
 * seal floating over a typed "Wait a second..." with a blinking caret.
 *
 * It stays at least `duration` ms, as that loader does — and, unlike it, also until the
 * cover's sprites are decoded (`ready`), so a slow connection never lifts it onto a
 * half-loaded envelope. Whichever comes later ends it.
 */
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { assets } from '../../lib/bandAssets'

const props = withDefaults(defineProps<{ ready: boolean; duration?: number }>(), {
  duration: 3800,
})
const emit = defineEmits<{ finish: [] }>()

const seal = assets['opening/parts/wax-seal.webp']

const CAPTION = 'Wait a second...'
const TYPE_MS = 190

const typed = ref('')
let typer: number | null = null
let timer: number | null = null
const elapsed = ref(false)

/*
 * One character every 190ms; once the line is complete it holds for one tick, then
 * clears and starts over — the loop the reference runs for as long as it is shown.
 */
function startTyping() {
  let i = 0
  let full = false
  typer = window.setInterval(() => {
    if (full) {
      typed.value = ''
      i = 0
      full = false
    } else if (i < CAPTION.length) {
      typed.value = CAPTION.slice(0, ++i)
    } else {
      full = true
    }
  }, TYPE_MS)
}

let done = false
function finishIfDone() {
  if (done || !elapsed.value || !props.ready) return
  done = true
  emit('finish')
}

watch(() => props.ready, finishIfDone)

onMounted(() => {
  startTyping()
  timer = window.setTimeout(() => {
    elapsed.value = true
    finishIfDone()
  }, props.duration)
})

onBeforeUnmount(() => {
  if (typer) window.clearInterval(typer)
  if (timer) window.clearTimeout(timer)
})
</script>

<template>
  <div class="preloader" role="status" aria-live="polite">
    <div class="preloader__content">
      <div class="preloader__logo">
        <img class="preloader__seal" :src="seal" alt="" loading="eager" />
      </div>
      <p class="preloader__caption">
        <span class="sr-only">Memuat undangan…</span>
        <span aria-hidden="true">{{ typed }}</span><span class="preloader__cursor" aria-hidden="true">|</span>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Above everything, the desktop column included. Same ground as the cover it lifts onto. */
.preloader {
  position: fixed;
  inset: 0;
  z-index: 9999999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 100vh;
  height: 100dvh;
  padding: 24px;
  background: var(--cover-bg);
  user-select: none;
}

.preloader__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.preloader__logo {
  display: flex;
  align-items: center;
  justify-content: center;
  animation: gentle-float 2.6s ease-in-out infinite;
}

.preloader__seal {
  display: block;
  width: 70px;
  max-width: 100%;
  height: auto;
  object-fit: contain;
  filter: drop-shadow(0 4px 14px rgba(0, 0, 0, 0.09));
}

.preloader__caption {
  min-height: 20px;
  margin: 0;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.5px;
  line-height: 1.4;
  text-align: center;
  color: var(--maroon-text);
}

.preloader__cursor {
  display: inline-block;
  margin-left: 2px;
  font-weight: 300;
  animation: blink 0.9s infinite;
}

@keyframes gentle-float {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-5px) scale(1.02);
  }
}

@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

@media (max-width: 600px) {
  .preloader__seal {
    width: 60px;
  }

  .preloader__caption {
    font-size: 12px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .preloader__logo,
  .preloader__cursor {
    animation: none;
  }
}
</style>
