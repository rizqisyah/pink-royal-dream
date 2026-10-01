<script setup lang="ts">
// The invitation sheet: Figma Frame 263, 596 x 16075.
// One component per band of the body frame, in Figma order; each band positions its own
// children relative to its own top, so inserting a band never renumbers the others.
// Band map and asset inventory: ../../../SLICING.md
import HeroSection from '../sections/HeroSection.vue'
import QuoteSection from '../sections/QuoteSection.vue'
import GroomSection from '../sections/GroomSection.vue'
import BrideSection from '../sections/BrideSection.vue'
import SaveDateSection from '../sections/SaveDateSection.vue'
import AcaraSection from '../sections/AcaraSection.vue'
import GallerySection from '../sections/GallerySection.vue'
import PrewedVideoSection from '../sections/PrewedVideoSection.vue'
import GiftSection from '../sections/GiftSection.vue'
import RsvpSection from '../sections/RsvpSection.vue'
import WishSection from '../sections/WishSection.vue'
import ClosingSection from '../sections/ClosingSection.vue'
</script>

<template>
  <div class="sheet">
    <HeroSection />
    <QuoteSection />
    <GroomSection />
    <BrideSection />
    <SaveDateSection />
    <AcaraSection />
    <GallerySection />
    <PrewedVideoSection />
    <GiftSection />
    <RsvpSection />
    <WishSection />
    <ClosingSection />
  </div>
</template>

<style scoped>
/*
 * One design pixel = 1cqw / 5.96, the same unit CoverSection uses. Declared once here
 * so every band inherits it and can place children in raw Figma coordinates.
 */
.sheet {
  container-type: inline-size;
  position: relative;
  /*
   * Full-bleed: the sheet fills its column edge to edge. The cap lives on
   * `.desktop-right-column` instead.
   */
  width: 100%;
  overflow: hidden;
  /* 2745:44 — Frame 263's flat #f9f0e9 fill, so a background rather than an asset. */
  background: var(--bg-body);
}

.sheet > * {
  --px: calc(100cqw / 596);
}
</style>
