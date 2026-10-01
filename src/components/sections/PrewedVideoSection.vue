<script setup lang="ts">
// Figma Frame 263 band "video", y 10850–11280. Coords are band-local design px.
//
// The design draws a still (Rectangle 27) captioned "video prewed". This theme drops the
// still: with a configured `video_prewed` the player itself sits in the still's rounded
// box from the start, and without one there is nothing to show, so the band is not
// rendered at all.
import { computed } from 'vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT } from '../../lib/bands/video'

const { el, shown } = useReveal(0.15)
const { videoPrewed } = useWedding()

const videoSrc = computed(() => ((videoPrewed.value as string) || '').trim())
const hasVideo = computed(() => !!videoSrc.value)

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

// The background music and the film would play over each other.
function pauseMusic() {
  document.querySelector('audio')?.pause()
}

function onVolumeChange(e: Event) {
  const v = e.target as HTMLVideoElement
  if (!v.muted && v.volume > 0) pauseMusic()
}
</script>

<template>
  <section
    v-if="hasVideo"
    :ref="el"
    class="band video-band"
    :class="{ 'is-in': shown }"
    aria-label="Video prewedding"
  >
    <!-- The still's own box (2745:284): 8, 23, 584 x 329, radius 23 — now the player. -->
    <div class="video-band__player">
      <iframe
        v-if="youtubeId"
        :src="`https://www.youtube.com/embed/${youtubeId}?rel=0&playsinline=1`"
        title="Video prewedding"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        loading="lazy"
      />
      <iframe
        v-else-if="vimeoId"
        :src="`https://player.vimeo.com/video/${vimeoId}`"
        title="Video prewedding"
        frameborder="0"
        allow="autoplay; fullscreen; picture-in-picture"
        allowfullscreen
        loading="lazy"
      />
      <video
        v-else
        :src="videoSrc"
        controls
        playsinline
        preload="metadata"
        @play="pauseMusic"
        @volumechange="onVolumeChange"
      />
    </div>
  </section>
</template>

<style scoped>
.video-band {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.video-band__player {
  --delay: 200ms;
  z-index: 45;
  left: calc(8 * var(--px));
  top: calc(23 * var(--px));
  width: calc(584 * var(--px));
  height: calc(329 * var(--px));
  border-radius: calc(23 * var(--px));
  overflow: hidden;
  background: #18120e;
}

/* `contain`: a portrait phone clip letterboxes inside the frame instead of being cropped. */
.video-band__player iframe,
.video-band__player video {
  display: block;
  width: 100%;
  height: 100%;
  border: 0;
  object-fit: contain;
}
</style>
