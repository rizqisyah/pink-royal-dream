import { computed } from 'vue'
import { useWedding } from './useWedding'
import { parentLine } from '../lib/format'

/*
 * Frame 263 draws two identical name blocks — first slot at y 3606, second at 5190.
 * Which person fills each slot follows `order_groom_first`, so both bands read the same
 * fields through here and only their coordinates differ.
 */
const DESIGN = {
  groom: {
    nickname: 'Mario',
    fullName: 'Mario Widjaja Tjandra Putra',
    parents: 'Anak Pertama dari Bapak Harjanto Tjandra\n& Ibu Farida Syarief Khan',
    instagram: 'Syifahadju',
  },
  bride: {
    nickname: 'Amanda',
    fullName: 'Amanda Putri Syaharani',
    parents: 'Anak Kedua dari Bapak Kapten Tek Syahroni\n& Ibu Maya Agni',
    instagram: 'Syifahadju',
  },
}

/** "@name", "instagram.com/name" or a full URL, down to the bare handle. */
function handleOf(raw?: string | null): string {
  const v = (raw || '').trim()
  if (!v) return ''
  const m = v.match(/instagram\.com\/([^/?#\s]+)/i)
  return (m ? m[1] : v).replace(/^@/, '')
}

export function usePerson(slot: 0 | 1) {
  const { groom, bride, isGroomFirst, wedding, parsedOverride } = useWedding()

  const isGroom = computed(() => (slot === 0) === isGroomFirst.value)
  const person = computed(() => (isGroom.value ? groom.value : bride.value))
  const design = computed(() => (isGroom.value ? DESIGN.groom : DESIGN.bride))
  // Live data never borrows the design's people: a blank field stays blank.
  const live = computed(() => !!wedding.value)

  const fullName = computed(() => person.value?.name?.trim() || (live.value ? '' : design.value.fullName))

  const nickname = computed(() => {
    if (person.value?.nickname?.trim()) return person.value.nickname.trim()
    if (person.value?.name?.trim()) return person.value.name.trim().split(' ')[0]
    return live.value ? '' : design.value.nickname
  })

  const parents = computed(() => parentLine(person.value) || (live.value ? '' : design.value.parents))

  const instagram = computed(() => {
    const p = person.value
    const raw = p?.instagram || p?.ig || p?.instagram_url || p?.social_media
    return handleOf(raw) || (live.value ? '' : design.value.instagram)
  })

  const photo = computed(() => {
    const images = parsedOverride.value?.images || {}
    const custom = isGroom.value
      ? person.value?.photo_url || images.foto_mempelai_pria || images.foto_pria || images.groom
      : person.value?.photo_url || images.foto_mempelai_wanita || images.foto_wanita || images.bride
    return (custom as string) || ''
  })

  return { isGroom, fullName, nickname, parents, instagram, photo }
}
