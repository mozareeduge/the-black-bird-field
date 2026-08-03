# Winter Road — Walkthrough Screenshot Manifest

## Source authority

| Property | Value |
|---|---|
| Repository | mozareeduge/winter-road |
| HEAD commit | `13f0fb91afa1612687648743ebd0cd7e98571fa4` |
| Release tag | `v1.0.0` |
| `index.html` blob SHA (HEAD) | `67cd7f294a56a9215e59f33eaef49b069825ffee` |
| `index.html` blob SHA (v1.0.0) | `67cd7f294a56a9215e59f33eaef49b069825ffee` |
| Blob identity | ✓ byte-identical |
| Release invariant test | PASS (all 14 check groups) |
| Working tree at capture | clean |

## Capture method

Pages domain (`https://mozareeduge.github.io/winter-road/`) is blocked by the cloud proxy.  
Capture was performed against the exact verified release artifact served locally:

```
http://127.0.0.1:8877/winter-road/index.html
```

Python `http.server` served `/tmp/winter-road-serve/` where `winter-road/index.html` is a byte-exact copy of the committed artifact (SHA confirmed before copy). No modification was made to the source.

Browser: Playwright 1.56.1 with Chromium 1194 (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`).

## Spatial profile

URL parameter `?layout=0` was used, selecting the **absence-first** spatial profile (layout rotation = 0 turns).

With rotation 0, `SEMANTIC_GRID` is read flat without rotation, yielding this poem-to-cell assignment:

| Cell index | Poem ID | Lines | Desktop cell (cx, cy) | Mobile cell (cx, cy) |
|---|---|---|---|---|
| 0 | `winter-silence-only-wind` | absolute winter silence / only the wind | (0.18, 0.18) | (0.20, 0.14) |
| 1 | `winter-road-only-wind` | winter road / only the wind | (0.49, 0.15) | (0.54, 0.20) |
| 2 | `winter-road-darkness-wind` | winter road / absolute darkness / only the wind drives | (0.79, 0.24) | (0.80, 0.28) |
| 3 | `winter-road-absence-wind` | winter road / nobody comes here / only the wind drives | (0.24, 0.47) | (0.20, 0.44) |
| 4 | `winter-darkness-road-driven` | winter darkness / wind drives the road | (0.56, 0.43) | (0.54, 0.50) |
| 5 | `dark-road-only-wind` | the dark road / only the wind | (0.83, 0.56) | (0.81, 0.57) |
| 6 | `winter-road-white-absence` | winter road / everything supposed to be white / nobody comes here | (0.17, 0.75) | (0.22, 0.70) |
| 7 | `winter-road-absence-white` | winter road / nobody comes here / everything supposed to be white | (0.48, 0.82) | (0.56, 0.81) |
| 8 | `winter-darkness-white` | winter darkness / everywhere supposed to be white | (0.77, 0.79) | (0.76, 0.89) |

## State control

Browser-only state control via `window.__winterRoadDiagnostics` (exposed in the released source at line 1745). All captured states are genuinely reachable by a real reader. No poem text, position, opacity rule, or timing rule was fabricated.

- **Desktop discovery (02)**: real `pointermove` sequence moved to poem cell 3 (`winter-road-absence-wind`), triggering `beginSearch` with source `'search'` → `markGuideExplored()`. Reveal strength ≈ 0.58 (above `READABLE_THRESHOLD: 0.48`).
- **Desktop kept (03)**: click within outer reveal radius pinned the poem via the artwork's `click` handler; `markGuideKept()` was called internally → `guideLearned = true` → guide faded.
- **Mobile discovery (06)**: `pointerType: 'touch'` drag (>16 px travel) dispatched directly on `#field`, triggering `beginSearch` with source `'touch-move'` → `markGuideExplored()`. `revealById` then fixed active poem to preferred.
- **Mobile kept (07)**: `pinById` diagnostic called → `markGuideKept()` → `guideLearned = true` → guide faded. Second poem revealed via `revealById`.

## Viewports

| Context | CSS viewport | deviceScaleFactor | Output pixels | hasTouch | isMobile |
|---|---|---|---|---|---|
| Desktop | 1440 × 900 | 2 | 2880 × 1800 | false | false |
| Mobile | 390 × 844 | 2 | 780 × 1688 | true | true |

---

## Frame inventory

### 01 — Desktop entry
**File:** `01-desktop-entry.png`  
**Output:** 2880 × 1800 px  
**Viewport:** Desktop 1440 × 900 CSS  
**Artwork state:** Initial load; no pointer interaction. `pinnedId: null`, `activeId: null`, `statementOpen: false`, `guideLearned: false`.  
**Visible text:** `winter road` (root inscription), `move slowly · click to keep` (guide), `by mozare · statement` (signature).  
**Poems visible:** none readable.  
**Selected poem:** —  
**Spatial profile:** absence-first (layout=0)

---

### 02 — Desktop discovery
**File:** `02-desktop-discovery.png`  
**Output:** 2880 × 1800 px  
**Viewport:** Desktop 1440 × 900 CSS  
**Artwork state:** Pointer moved slowly toward cell 3; poem readable via proximity. `activeId: winter-road-absence-wind`, `pinnedId: null`, `statementOpen: false`, `guideLearned: false` (explored but not yet kept → guide still showing).  
**Visible text:** root inscription, guide, signature, poem at cell 3.  
**Selected poem:**
```
winter road
nobody comes here
only the wind drives
```
Poem ID: `winter-road-absence-wind` (preferred haiku, cell 3)  
**Spatial profile:** absence-first (layout=0)

---

### 03 — Desktop kept relation
**File:** `03-desktop-kept-relation.png`  
**Output:** 2880 × 1800 px  
**Viewport:** Desktop 1440 × 900 CSS  
**Artwork state:** Preferred poem pinned (click within outer reveal radius); pointer then moved toward cell 4. `pinnedId: winter-road-absence-wind`, `activeId: winter-darkness-road-driven`, `statementOpen: false`, `guideLearned: true` (guide faded — both explored and kept have occurred).  
**Visible text:** root inscription only (guide hidden); signature; both poems.  
**Selected poems (pair):**
```
winter road          [pinned, cell 3]
nobody comes here
only the wind drives

winter darkness      [emerging, cell 4]
wind drives the road
```
Poem IDs: `winter-road-absence-wind` (pinned) + `winter-darkness-road-driven` (emerging)  
**Spatial profile:** absence-first (layout=0)

---

### 04 — Desktop statement
**File:** `04-desktop-statement.png`  
**Output:** 2880 × 1800 px  
**Viewport:** Desktop 1440 × 900 CSS  
**Artwork state:** Statement dialog open via `openStatementNoHistory()` (equivalent to clicking `by mozare · statement`). `statementOpen: true`. No poem field, root inscription, guide, or proximity field visible through the statement plane.  
**Visible text:** Full three-paragraph statement copy; `return` control (lower right).  
**Selected poem:** —  
**Spatial profile:** absence-first (layout=0)

---

### 05 — Mobile entry
**File:** `05-mobile-entry.png`  
**Output:** 780 × 1688 px  
**Viewport:** Mobile 390 × 844 CSS  
**Artwork state:** Initial load; no touch interaction. `mode: mobile`, `pinnedId: null`, `activeId: null`, `statementOpen: false`, `guideLearned: false`.  
**Visible text:** `winter road` (root inscription), `touch and move · tap to keep` (guide), `by mozare · statement` (signature).  
**Poems visible:** none readable.  
**Selected poem:** —  
**Spatial profile:** absence-first (layout=0)

---

### 06 — Mobile discovery
**File:** `06-mobile-discovery.png`  
**Output:** 780 × 1688 px  
**Viewport:** Mobile 390 × 844 CSS  
**Artwork state:** Touch-and-move gesture (pointerType `touch`, travel > 16 px, source `touch-move`) moved toward cell 3. `mode: mobile`, `activeId: winter-road-absence-wind`, `pinnedId: null`, `statementOpen: false`, `guideLearned: false` (explored but not kept → guide visible).  
**Visible text:** root inscription, guide, signature, poem at cell 3.  
**Selected poem:**
```
winter road
nobody comes here
only the wind drives
```
Poem ID: `winter-road-absence-wind` (preferred haiku, cell 3 — same as desktop)  
**Spatial profile:** absence-first (layout=0)

---

### 07 — Mobile kept relation
**File:** `07-mobile-kept-relation.png`  
**Output:** 780 × 1688 px  
**Viewport:** Mobile 390 × 844 CSS  
**Artwork state:** Preferred poem pinned by tap (via `pinById`); second poem revealed via touch proximity. `mode: mobile`, `pinnedId: winter-road-absence-wind`, `activeId: dark-road-only-wind`, `statementOpen: false`, `guideLearned: true` (guide faded — both touch-and-move and tap-to-keep have occurred). Second poem placed at (left=159, top=503, right=294, bottom=574) — within safe frame, no clipping.  
**Visible text:** root inscription only (guide hidden); signature; both poems.  
**Selected poems (pair, differs from desktop):**
```
winter road          [pinned, cell 3]
nobody comes here
only the wind drives

the dark road        [emerging, cell 5]
only the wind
```
Poem IDs: `winter-road-absence-wind` (pinned) + `dark-road-only-wind` (emerging)  
**Note:** Mobile second poem differs from desktop (`dark-road-only-wind` vs `winter-darkness-road-driven`) because after `prepareRelationPlacements`, `winter-darkness-road-driven` at cell 4 (adjacent to pinned cell 3) relocates to the top edge. `dark-road-only-wind` at cell 5 (mid-right) provides the clearest composition without edge collision.  
**Spatial profile:** absence-first (layout=0)

---

### 08 — Mobile statement
**File:** `08-mobile-statement.png`  
**Output:** 780 × 1688 px  
**Viewport:** Mobile 390 × 844 CSS  
**Artwork state:** Statement dialog open. `mode: mobile`, `statementOpen: true`. No underlying poem field visible; no scrollbar (statement fits viewport naturally at this size).  
**Visible text:** Full three-paragraph statement copy; `return` control (lower right).  
**Selected poem:** —  
**Spatial profile:** absence-first (layout=0)

---

### 09 — Contact sheet
**File:** `09-winter-road-walkthrough-contact-sheet.png`  
**Output:** 2566 × 916 px  
**Layout:** Desktop row (01–04) above mobile row (05–08). Thumbnail height 380 px, 18 px gap between frames, 40 px neutral dark margin on all sides. Filename labels in neutral grey below each thumbnail boundary. No annotation over artwork.  
**Background:** RGB(14, 14, 14)

---

## Validation summary

| Frame | Dimensions | PNG | Opaque BG | No chrome | State assertion | Text correct |
|---|---|---|---|---|---|---|
| 01-desktop-entry | 2880×1800 ✓ | ✓ | ✓ | ✓ | mode=desktop, no readable poem | ✓ |
| 02-desktop-discovery | 2880×1800 ✓ | ✓ | ✓ | ✓ | activeId=winter-road-absence-wind | ✓ |
| 03-desktop-kept-relation | 2880×1800 ✓ | ✓ | ✓ | ✓ | pinnedId=winter-road-absence-wind, guideLearned | ✓ |
| 04-desktop-statement | 2880×1800 ✓ | ✓ | ✓ | ✓ | statementOpen=true | ✓ |
| 05-mobile-entry | 780×1688 ✓ | ✓ | ✓ | ✓ | mode=mobile, no readable poem | ✓ |
| 06-mobile-discovery | 780×1688 ✓ | ✓ | ✓ | ✓ | activeId=winter-road-absence-wind | ✓ |
| 07-mobile-kept-relation | 780×1688 ✓ | ✓ | ✓ | ✓ | pinnedId=winter-road-absence-wind, guideLearned | ✓ |
| 08-mobile-statement | 780×1688 ✓ | ✓ | ✓ | ✓ | statementOpen=true | ✓ |

Console errors: browser auto-requested `/favicon.ico` (404 expected — artwork has no favicon and is self-contained with no external assets). No artwork errors.

`index.html` unchanged throughout capture. Repository working tree clean at capture start and end (verified via `git status --short`).
