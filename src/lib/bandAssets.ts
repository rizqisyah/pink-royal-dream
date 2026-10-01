/*
 * Every sliced sprite, keyed by its `<section>/parts/<name>.<ext>` path so the band
 * tables can name assets as plain strings instead of dozens of import lines.
 * SVGs are included: the blurred ellipses, ornaments and mask shapes ship as vectors.
 */
const modules = import.meta.glob('../assets/**/parts/*.{webp,svg}', {
  eager: true,
  import: 'default',
}) as Record<string, string>

export const assets = Object.fromEntries(
  Object.entries(modules).map(([path, url]) => [path.replace('../assets/', ''), url]),
) as Record<string, string>
