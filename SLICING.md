# Slicing notes — Mario & Amanda (envelope theme)

Built on the **tema-envelop base** (`F:\Undangan\qinvi\envelope-qinvi`, served at
`/TemaEnvelop/`) and its variant `envelope-red`: same app shell, `useWedding()` data
layer, API calls, `BandArt` + `lib/bands/*.ts` layer tables, `useReveal` entrances,
`BottomNav` music and `VideoSection`. What differs is listed here.

Figma file `10VuhE58VrDL7mY7QUvMRl` ("Desain Wesbite 25ribuaja"):

| Frame | Node | Size | What it is | Code |
|-------|------|------|------------|------|
| Frame 264 | `2745:354` | 596 × 1183 | Opening cover — pink envelope, "Click to open" | `components/cover/CoverSection.vue`, `lib/coverLayers.ts`, `assets/opening/` |
| Frame 263 | `2745:44` | 596 × 16075 | The scrolling invitation | `components/invite/InviteBody.vue`, `lib/bands/*.ts`, every other `assets/*` |

**The frame is 596 wide, not the base's 375.** One design px is `calc(100cqw / 596)`
(`--px`), on the cover frame and on the sheet. `BandArt`'s entrance distances are the
base's, scaled by `596 / 375` so they move the same distance on screen.

## Running it

The theme is **TemaPinkRoyalDream**: built under `/TemaPinkRoyalDream/`, deployed by
`.github/workflows/deploy.yml` to `/var/www/qinvi/themes/TemaPinkRoyalDream/`, with
`tema-pink-royal-dream` as the default slug — the same pattern as `TemaEnvelopRed` /
`tema-envelop-red`.

| Env | Effect |
|-----|--------|
| `VITE_DESIGN_MODE=1` | Show Frame 263's own content (Mario & Amanda) and never call the API. `.env` sets this for local work. |
| `VITE_DEFAULT_SLUG` | The wedding a URL with no slug renders. Unset falls back to `tema-pink-royal-dream`. |
| `VITE_BASE_PATH` | Overrides the `/TemaPinkRoyalDream/` base. `api.ts` reads the base so neither the folder nor its kebab form (`tema-pink-royal-dream` in the path) is ever taken for a slug. |
| `VITE_API_BASE_URL` / `VITE_API_PROXY_TARGET` | As in the base. |

## Bands

Frame 263 is flat — no section frames. Bands are cut by y in `scripts/gen_bands.py`;
each layer goes to the band its **top** falls in. `z` is the layer's index in Figma's
child order and stays global, so a layer that hangs into the next band still stacks
correctly against it (all bands share the sheet's stacking context). Text nodes carry
their own Figma `z` in their band's CSS instead of the base's blanket `z-index: 900`,
because in this design art paints over text in places (florals over "And", the pastel
sprays over the name blocks).

| Band | y | Height | Live content |
|------|---|--------|--------------|
| hero | 0 | 1110 | title, hero photo (`customHeroPhoto`) |
| quote | 1110 | 1510 | QS Ar-Rum ref + verse (`quoteVerse`, `quoteText`, fitted) |
| groom | 2620 | 1530 | "Bride & Groom", first person: nickname, name block, portrait |
| bride | 4150 | 1540 | "And", second person |
| savedate | 5690 | 1230 | "Save the Date", live countdown |
| acara | 6920 | 3040 | two event cards (`acara`, all-or-nothing, max 2) |
| gallery | 9960 | 890 | main photo, 4 thumbs, nav, `<dialog>` preview, autoplay |
| video | 10850 | 430 | prewed still → player when `video_prewed` is set; dropped live without one |
| gift | 11280 | 810 | account / address cards (`rekening`), copy buttons |
| rsvp | 12090 | 690 | form → `hadir2`, `has_rsvp` + localStorage receipt |
| wish | 12780 | 1400 | form → `ucapan`, 3-card scrolling window + Show more |
| closing | 14180 | 1895 | thank-you copy, couple, hashtag, mirror photo, credit |

The sheet measures exactly **16075** — the frame's own height. That only lands if every
band height is right; check it after any change.

Edit layer geometry in `scripts/gen_bands.py` and run `python scripts/gen_bands.py`.
The `lib/bands/*.ts` files are generated — do not hand-edit them.

## Assets: shared sprites, not per-node exports

The base exports every node pre-rotated. This design reuses a few illustrations dozens
of times (`floral-regency` 12×, `floral-pastel` 14× at six stacked fills, `cloud` 10×),
so each source image ships **once** as webp and `BandLayer` carries the node's transform
instead: `rotate`, `flipX/flipY`, `iw/ih` (unrotated size inside the AABB box), `crop`,
`radius`, `fit: 'fill'`, `stack`, `maskBox`, `filter`. 50 files, 3.3 MB (the raw Figma
fills were 39.6 MB).

- `stack: n` repeats a semi-transparent fill n times — Figma stacked the same image fill
  to deepen it (the pastel sprays × 6, two clouds × 4).
- `fit: 'fill'` reproduces Figma's stretched image fills (`arch-wedding`, `podium`,
  `event-arch`): drawn with `object-fit: cover` they look wrong.
- Rotated layers: x/y/w/h is the **axis-aligned box** from Figma's code export, not the
  node's reported bounds (those are the unrotated size at the transform origin).

## Things that bit, and will bite again

1. **Vite inlines small SVGs as data URIs written with single quotes.** `url('…')` then
   closes early and the mask silently never applies — the groom/bride backdrops lost
   their arched tops and the closing mirror showed a hard rectangle. `BandArt` writes
   `url("…")`. Any new `url()` built from an imported asset must use double quotes.
2. **A nowrap line that overflows its box spills only rightward**, even centred. Give
   single-line script headings a box wider than the words, centred on the design's own
   centre ("Wedding Wishes" was clipped at the right edge).
3. **Reduced motion hides fade bugs** (base note, still true). Verify once with motion
   on: scroll the whole sheet, wait out the longest entrance, assert every band is
   `.is-in` and every direct child is at opacity 1.

## Typography

Google faces are self-hosted via `@fontsource`. Six of the design's faces are
commercial with no webfont; each token in `style/tokens.css` names the real face first,
so adding its `@font-face` to `style.css` swaps it in. All six are installed from the
foundry files in `src/assets/fonts/`:

| Design face | Used for | Status |
|-------------|----------|--------|
| Bickham Script Pro | "And" | **installed** |
| Barley Sign | hashtag | **installed** |
| Norveil Fantasy Demo | "(Qs. Ar-Rum: 21)" | **installed** — DEMO cut, personal use only |
| Wonderia | full names | **installed** — 7NTypes, free for personal use only |
| Cloister Black | footer credit | **installed** — no licence file came with the download |
| Calligraphy Script | closing message | **installed** — Craft Supply Co DEMO cut, personal use only, lacks some Unicode glyphs (falls back per character to Pinyon Script) |

The right Calligraphy Script is Craft Supply Co's (`calligraphy-script.zip`). "zai
Calligraphy Script Handwritten" only shares the name — heavier and upright — and was
rejected against the render, as was every face in the 135-font archive.

Every installed face runs at Figma's own size; only `top`/`left` moved, each measured
off the glyph ink against the render: "And" (+20.5, +3), hashtag (+5), closing message
(−10). `--closing-comp` is 1 — it was the 1.3 size fudge for the Pinyon stand-in.

The Instagram glyph on the name pills is Font Awesome Brands, as in the design.

## Preloader

`components/cover/PreloaderScreen.vue`, after the TemaPsrt theme's loader
(qinvi.id/TemaPsrt): the cover's own wax seal (`opening/parts/wax-seal.webp`, 70px,
60px under 600px) floating over a typed "Wait a second..." (Inter 500 13px, one
character per 190ms, looping) with a blinking caret, on the cover's `--cover-bg`. It
lifts with a 0.8s fade + 1.04 scale.

It stays **3.8s, and also until the cover's sprites are decoded** — whichever is later.
TemaPsrt lifts on the timer alone; on a slow connection that drops the guest onto a
half-loaded envelope. The cover's entrance (`ready`) starts when the loader lifts, not
when the assets land, so it plays where it can be seen.

`?open=1` or `?preview=1` skips loader and cover and lands on the invitation, unlocked
— the same switch TemaPsrt reads, and what an admin preview frame wants.

## Cover

The cover frame is **contained, never cropped** — the base crops the sides on narrow
screens, which here cut off the top-right rose. The illustration (2755:609, 867 × 1225 at
−134, −17) is larger than the frame; `CoverSection` scales it about the frame's centre
just enough to fill the screen. Past 1.15× (landscape) it would blow the flowers up, so
the cover becomes a card the size of the frame instead.

Entrance timings are the base's: names 0.2 s, envelope 0.64 s, seal drop 1.24 s, label
1.46 s then breathing, guest 1.7 s; splash leave 1.3 s, content rises at 0.45 s.

## Band figures

Puppeteer at 596 × dsf 1, reduced motion, design mode; mean per-channel difference
/255 against the Frame 263 render (`get_screenshot` at scale 1):

| Band | Diff | Note |
|------|------|------|
| hero | 2.21 | |
| quote | 2.22 | |
| groom | 2.53 | Wonderia name block |
| bride | 2.64 | "And" in Bickham, ink within 1px of the render |
| savedate | 2.66 | live clock against printed zeroes |
| acara | 3.99 | |
| gallery | 7.28 | the photo is the design's, resampled to 1200 px |
| video | 2.30 | |
| gift | 0.53 | |
| rsvp | 2.00 | |
| wish | 3.40 | |
| closing | 2.16 | every face the design's own |
| cover | 2.30 | |
