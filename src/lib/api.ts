const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const DEFAULT_SLUG = import.meta.env.VITE_DEFAULT_SLUG || 'tema-pink-royal-dream'

export const DESIGN_MODE =
  import.meta.env.VITE_DESIGN_MODE === '1' || import.meta.env.VITE_DESIGN_MODE === 'true'

/*
 * The theme's own folder on the VPS (/TemaPinkroyaldream) is part of every URL, so it
 * is never the slug — and neither is its kebab form (/tema-pinkroyaldream), which the
 * base treats the same way. Read from Vite's BASE_URL rather than hardcoding the name,
 * so renaming the deploy folder needs no code change here.
 */
const kebab = (s: string) => s.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()
const THEME_SEGMENTS = import.meta.env.BASE_URL.split('/')
  .filter(Boolean)
  .flatMap((s) => [s.toLowerCase(), kebab(s)])

export function resolveSlug(): string {
  const searchParams = new URLSearchParams(window.location.search)
  const querySlug = searchParams.get('slug')
  if (querySlug) return querySlug

  const segments = window.location.pathname
    .split('/')
    .filter(Boolean)
    .filter((s) => !THEME_SEGMENTS.includes(s.toLowerCase()))
  if (segments.length === 0) return DEFAULT_SLUG

  return segments[segments.length - 1]
}

async function request(path: string, options: RequestInit = {}): Promise<any> {
  let res: Response
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      ...options,
    })
  } catch (networkError: any) {
    throw new Error(`Network error: ${networkError.message}`)
  }

  let payload: any = null
  try {
    payload = await res.json()
  } catch {
    // Non-JSON response
  }

  if (!res.ok || (payload && payload.success === false)) {
    const message = (payload && payload.message) || `Request failed (${res.status})`
    throw new Error(message)
  }

  return payload
}

export async function getHome(slug: string, to = ''): Promise<any> {
  const query = to ? `?to=${encodeURIComponent(to)}` : ''
  const payload = await request(`/v1/service/menu/getHome/${encodeURIComponent(slug)}${query}`)
  return payload?.data ?? null
}

export async function submitRsvp(slug: string, body: any): Promise<any> {
  if (DESIGN_MODE) {
    throw new Error('Design mode: undangan ini belum terhubung ke server.')
  }
  return request(`/v1/service/menu/hadir2/${encodeURIComponent(slug)}`, {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export async function submitUcapan(slug: string, body: any): Promise<any> {
  if (DESIGN_MODE) {
    throw new Error('Design mode: undangan ini belum terhubung ke server.')
  }
  return request(`/v1/service/menu/ucapan/${encodeURIComponent(slug)}`, {
    method: 'POST',
    body: JSON.stringify(body),
  })
}
