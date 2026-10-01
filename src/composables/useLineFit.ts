import { onUnmounted, type ComponentPublicInstance } from 'vue'

/**
 * Shrinks an element's text until it sets in at most `maxLines` lines.
 *
 * useFitText's sibling for script headings. That one compares scrollHeight to the box,
 * which a script face defeats: its glyphs run taller than a tight line box, so the
 * heading always reads as overflowing and shrinks to the minimum. This counts the lines
 * the text actually broke into instead.
 *
 * Same contract as useFitText — it drives a `--fit` multiplier the CSS applies:
 *
 *   const fit = useLineFit(2)
 *   <h2 :ref="fit">
 *   font-size: calc(98 * var(--px) * var(--fit, 1));
 */
const MIN_SCALE = 0.5
const STEP = 0.03

function lineCount(node: HTMLElement): number {
  const range = document.createRange()
  range.selectNodeContents(node)
  const tops = new Set<number>()
  for (const r of range.getClientRects()) {
    if (r.width > 0 && r.height > 0) tops.add(Math.round(r.top))
  }
  return tops.size
}

export function useLineFit(
  maxLines: number,
): (node: Element | ComponentPublicInstance | null) => void {
  let observer: ResizeObserver | null = null
  let visibility: IntersectionObserver | null = null

  function fit(node: HTMLElement): void {
    // No box yet — behind the cover. The observers below refit once it is rendered.
    if (!node.clientWidth) return
    let scale = 1
    node.style.setProperty('--fit', '1')
    while (lineCount(node) > maxLines && scale > MIN_SCALE) {
      scale -= STEP
      node.style.setProperty('--fit', String(scale))
    }
  }

  function disconnect(): void {
    observer?.disconnect()
    observer = null
    visibility?.disconnect()
    visibility = null
  }

  onUnmounted(disconnect)

  return (node) => {
    disconnect()
    if (!(node instanceof HTMLElement)) return

    // Width changes re-break the lines; never refit inside the callback that fired it.
    observer = new ResizeObserver(() => requestAnimationFrame(() => fit(node)))
    observer.observe(node)

    // The sheet sits behind the cover under `v-show`, so there is no box until it opens.
    visibility = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) requestAnimationFrame(() => fit(node))
    })
    visibility.observe(node)

    fit(node)
    // Measured against the fallback face, the first fit is wrong; redo it once the real
    // face has arrived.
    document.fonts?.ready.then(() => fit(node))
  }
}
