<script setup lang="ts">
// Figma Frame 263 band "video", y 10850–11280. Coords are band-local design px.
//
// The design draws a still (Rectangle 27) captioned "video prewed". With a configured
// `video_prewed` the still becomes the play button and the player takes its place in
// the same rounded box; live data without one drops the band rather than show a still
// that promises a video nobody can play.
import { computed, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/video'

const { el, shown } = useReveal(0.15)
const { videoPrewed, wedding } = useWedding()

const videoSrc = computed(() => ((videoPrewed.value as string) || '').trim())
const hasVideo = computed(() => !!videoSrc.value)
const showBand = computed(() => hasVideo.value || !wedding.value)

const youtubeId = computed(() => {
  const m = videoSrc.value.match(
    /(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=|shorts\/))([^&?/\s]{11})/,
  )
  return m ? m[1] : null
})

const vimeoId = computed(() => {
  const m = videoSrc.value.match(/vimeo\.com\/(?:video\/)?(\d+)/)
  return m ? m[1] : null
})

const playing = ref(false)

function play() {
  if (!hasVideo.value) return
  // The background music and the film would play over each other.
  document.querySelector('audio')?.pause()
  playing.value = true
}
</script>

<template>
  <section
    v-if="showBand"
    :ref="el"
    class="band video-band"
    :class="{ 'is-in': shown }"
    aria-labelledby="prewed-heading"
  >
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2745:285 — Miss Fajardose 91/101, #000000. -->
    <p v-if="!playing" id="prewed-heading" class="video-band__label">video prewed</p>

    <button
      v-if="hasVideo && !playing"
      type="button"
      class="video-band__play"
      aria-labelledby="prewed-heading"
      @click="play"
    />

    <div v-if="playing" class="video-band__player">
      <iframe
        v-if="youtubeId"
        :src="`https://www.youtube.com/embed/${youtubeId}?rel=0&playsinline=1&autoplay=1`"
        title="Video prewedding"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      />
      <iframe
        v-else-if="vimeoId"
        :src="`https://player.vimeo.com/video/${vimeoId}?autoplay=1`"
        title="Video prewedding"
        frameborder="0"
        allow="autoplay; fullscreen; picture-in-picture"
        allowfullscreen
      />
      <video v-else :src="videoSrc" controls autoplay playsinline preload="metadata" />
    </div>
  </section>
</template>

<style scoped>
.video-band {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* z 44: over the still (43). */
.video-band__label {
  --delay: 300ms;
  z-index: 44;
  left: calc(66 * var(--px));
  top: calc(98 * var(--px));
  width: calc(469 * var(--px));
  height: calc(114 * var(--px));
  font-family: var(--font-video);
  font-size: calc(91 * var(--px));
  line-height: calc(101 * var(--px));
  color: #000;
  pointer-events: none;
}

/* The still's own box (2745:284): 8, 23, 584 x 329, radius 23. */
.video-band__play,
.video-band__player {
  z-index: 45;
  left: calc(8 * var(--px));
  top: calc(23 * var(--px));
  width: calc(584 * var(--px));
  height: calc(329 * var(--px));
  border-radius: calc(23 * var(--px));
  overflow: hidden;
}

.video-band__play {
  border: 0;
  background: transparent;
  cursor: pointer;
  transition: background 0.24s ease;
}

.video-band__play:hover,
.video-band__play:focus-visible {
  background: rgba(255, 255, 255, 0.12);
}

.video-band__player {
  background: #18120e;
}

.video-band__player iframe,
.video-band__player video {
  display: block;
  width: 100%;
  height: 100%;
  border: 0;
  object-fit: cover;
}
</style>
