# The Black Bird Field — Product + Design Authority

**Authority revision:** v8.1 · 2026-08-15  
**Status:** PRODUCT_DESIGN_AUTHORITY_CLOSED  
**Work mode:** EXISTING_PROJECT_CHANGE · DESIGN_RECOMPOSITION · ARTISTIC_SOFTWARE · PUBLIC_PRODUCT · RELEASE_HARDENING

This authority preserves v07 as the accepted portfolio baseline and governs only the v08.1 craft refinements approved from the owner's 2026-08-15 screenshot review. It does not reopen page architecture, copy, work order, motion scope, routes, or the visual premise.

## Current truth / protected horizon

The public portfolio is a light paper-like vitrine around five autonomous browser-native works. Dark work surfaces remain visibly distinct from the vitrine. The portfolio owns framing, sequence, context, metadata, navigation, and threshold media; it does not visually homogenize the works.

The following are protected:

- Home, Works, five work pages, Practice, About, Contact, shared header/menu/footer and legacy routes.
- Five-work order: The Black Bird → Winter Road → UNHAPPY Scenario → Grave-Machine → TAROKE REMIXER.
- Existing visitor copy except where a visible state has materially changed (`Selected still` → `Work preview`).
- `TAROKE REMIXER` / `taroke-remixer` canonical identity.
- Light ground/paper vs dark threshold ontology, 12-column wide composition, thin rules, serif reading/display voice, mono apparatus voice.
- Authored motion only on Home preview and project hero, with still-first fallback behavior.
- No Persian portfolio-language layer.
- Protected Grave-Machine runtime and CV bytes during repository migration.
- Future works remain one manifest + responsive media; motion is optional.

## Authority map

- **OWNER_LOCKED:** v07 acceptance; the four corrections below; canonical REMIXER identity only; no Persian layer.
- **ACCEPTED_TARGET:** current v08.1 source, this authority, `docs/DESIGN_SYSTEM.md`.
- **CURRENT_PRODUCT_TRUTH:** generated `dist/` and the underlying manifests/renderers/CSS/JS.
- **EVIDENCE:** owner screenshots; rendered before/after captures; validation output.
- **EXTERNAL BENCHMARK (not aesthetic authority):** USWDS type scale; GOV.UK summary-list anatomy; WCAG Resize Text, Reflow, Contrast and Target Size guidance.
- **HISTORICAL:** v3.2/v4/v07 implementation details that conflict with later owner decisions.

## Closed decisions

### DEC-201 — Apparatus text becomes a coherent optical tier

**Question:** The portfolio's mono notation is aesthetically correct but many instances at 8–9px become visually incidental rather than readable apparatus.

**Decision:** Keep the mono, uppercase/tracked language and its subordinate status; replace scattered 8–10px values with a two-step system:

- `--micro: 12px` — semantic apparatus: work numbers, section identifiers, form/version, metadata labels, reading-condition steps, view numbers, contact keys, footer navigation.
- `--micro-tight: 11px` — compact captions, preview captions, wordmark subline and similarly constrained peripheral notation.

Navigation and action-label text previously at 10px becomes 11px. No visible site text remains at 8px, 9px, or 10px.

On the light field, microtype gets dedicated darker tonal tokens rather than globally changing the palette:

- `--micro-muted: #514b43`
- `--micro-signal: #684216`

On dark surfaces, `--micro-muted-dark: #b9afa2`; existing bone/sand apparatus colors remain when they already exceed the needed contrast.

**Reason:** small apparatus should remain a distinct voice, not disappear. USWDS exposes 10px as a special `micro` system token while its regular theme scale starts higher; v08.1 deliberately sits between decorative micro and ordinary body text rather than converting apparatus into body copy. The stronger light-field colors preserve the existing hue relationship while restoring legibility.

**Supersedes:** scattered v07/v4 8/9/10px micro sizes.

### DEC-202 — Contact is a key / value / action specimen, not a display-title stack

Each contact row is one large link target with three semantic parts:

1. **key** — 12px mono apparatus, fixed 112px column on wide layouts;
2. **value** — serif 21–27px, normal weight, sized as prominent contact information but below page/display title scale;
3. **direction/action mark** — 16px, immediately following the value, not pinned to the far page edge.

A remaining flexible column absorbs unused width, so arrow proximity belongs to the value rather than the container. On mobile, the key becomes its own first line; value + arrow remain adjacent below. Whole-row borders continue to supply rhythm and large pointer/touch targets.

### DEC-203 — Home About becomes a terminal editorial strip

Remove the giant `Mozare` display word from Home. It duplicated identity already stated in the adjacent sentence and created a false competing headline near the end of the page.

The strip now uses three roles across the same 12-column system:

- columns 1–2: `03 / ABOUT` apparatus;
- columns 3–8: the existing identity paragraph, promoted slightly in measure but not rewritten;
- columns 10–12: the established About action, aligned to the same baseline region.

No replacement headline is invented. The recovered space becomes compositional breathing room and clearer relation between label, statement and exit action.

### DEC-204 — Works index begins with work 01, not a redundant double rule

The page mast already terminates the introductory region with a rule. Remove `border-top` from the first `.work-row`; retain row-ending rules. The sequence now begins with content rather than two near-adjacent separators.

## Scenario / case acceptance

### SCN-201 — Apparatus across the portfolio

**Given** any canonical page at wide, compact, tablet, mobile or 320px width,  
**when** apparatus text appears,  
**then** semantic apparatus is 12px and tight peripheral apparatus is 11px; no authored 8/9/10px text remains; the information stays subordinate to serif/body content; no label clips or escapes its component.

Representative surfaces: Home work number/index/ledger/About/Practice labels; Works numbers + form/version; all work project-form/prelude/view/edition/captions; Practice section identifiers/figcaptions; About facts; Contact keys; footer and mobile-menu apparatus.

### SCN-202 — Contact row

**Given** Contact at desktop,  
**then** the value is visually dominant but not headline-sized, the arrow sits directly after it, all three rows share one grid, and the whole row is the target.  
**At mobile**, key reflows above value/action without horizontal overflow.

### SCN-203 — Home About

**Given** Home near its terminal About region,  
**then** there is no decorative identity headline; label, existing paragraph and action occupy distinct but balanced grid territories and remain legible at mobile.

### SCN-204 — Works opening rhythm

**Given** `/works/`,  
**then** only the page-mast boundary precedes the work list; work 01 does not add another top rule.

### SCN-205 — Preservation

All routes, canonical copy, actions, motion manifests, motion fallbacks, work order, protected artifact contract, and future-work addition model remain unchanged except the explicitly authorized visual refinements above.

## QA handoff

- DEC/SCN 201–204 are **AUTH** oracles.
- Contrast, resize/reflow, target-size checks are **STANDARD** where applicable.
- Whether the refined proportion is artistically preferable is an **OWNER/HEURISTIC** visual gate, not an objective software defect.
- Strongest proof: rendered geometry + computed style + 320px reflow + source assertions + before/after owner review.

