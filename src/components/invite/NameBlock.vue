<script setup lang="ts">
/*
 * 2745:121 / 2750:457 — the name block under each portrait: full name, parents and the
 * Instagram pill. The two copies are the same 500 x 252 container placed at different
 * spots, so the band passes the container's origin and everything inside is relative.
 *
 * Renders three root nodes on purpose: each must be a direct child of `.band` so the
 * shared band rules position it and run its entrance.
 */
import { computed } from 'vue'
import { useFitText } from '../../composables/useFitText'

const props = defineProps<{
  x: number
  y: number
  /** Figma child order of the container — the pastel florals paint over it. */
  z: number
  fullName: string
  parents: string
  instagram: string
}>()

const fitName = useFitText()

const origin = computed(() => ({
  '--bx': String(props.x),
  '--by': String(props.y),
  zIndex: String(props.z),
}))
</script>

<template>
  <!-- 2745:122 — Wonderia 48/101, #dda2a3. -->
  <p :ref="fitName" class="name__full" :style="origin">{{ fullName }}</p>
  <!-- 2745:124 — Cormorant Infant 24/28.4, #62401c. -->
  <p v-if="parents" class="name__parents" :style="origin">{{ parents }}</p>
  <!-- 2745:126 — the pill: #dda2a3, Font Awesome Brands + Cormorant Infant 20/30. -->
  <div v-if="instagram" class="name__social" :style="origin">
    <a
      class="name__pill"
      :href="`https://instagram.com/${instagram}`"
      target="_blank"
      rel="noopener noreferrer"
    >
      <i class="fa-brands fa-instagram" aria-hidden="true"></i>
      <span>@{{ instagram }}</span>
    </a>
  </div>
</template>

<style scoped>
/*
 * Wonderia draws its own capitals for the lowercase, so no `small-caps` is asked for —
 * synthesising it would replace those glyphs. Fixed height so a long name shrinks
 * rather than wraps.
 */
.name__full {
  --delay: 120ms;
  left: calc((var(--bx) - 9) * var(--px));
  top: calc((var(--by) + 5) * var(--px));
  width: calc(543 * var(--px));
  height: calc(101 * var(--px));
  font-family: var(--font-caps);
  font-size: calc(48 * var(--px) * var(--fit, 1));
  line-height: calc(101 * var(--px) * var(--fit, 1));
  color: var(--title);
}

.name__parents {
  --delay: 240ms;
  left: calc((var(--bx) + 24) * var(--px));
  top: calc((var(--by) + 90) * var(--px));
  width: calc(452 * var(--px));
  font-family: var(--font-parent);
  font-size: calc(24 * var(--px));
  line-height: calc(28.4 * var(--px));
  white-space: pre-line;
  color: var(--parent-ink);
}

.name__social {
  --delay: 360ms;
  display: flex;
  justify-content: center;
  left: calc((var(--bx) + 24) * var(--px));
  top: calc((var(--by) + 190) * var(--px));
  width: calc(452 * var(--px));
  height: calc(46 * var(--px));
}

.name__pill {
  display: flex;
  align-items: center;
  gap: calc(8 * var(--px));
  padding: calc(8 * var(--px)) calc(12 * var(--px));
  border-radius: 999px;
  background: var(--title);
  color: var(--pill-ink);
  text-decoration: none;
  font-family: var(--font-parent);
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  white-space: nowrap;
  transition: filter 0.2s ease;
}

.name__pill:hover,
.name__pill:focus-visible {
  filter: brightness(0.95);
}

.name__pill .fa-brands {
  font-size: calc(20 * var(--px));
  line-height: calc(20 * var(--px));
}
</style>
