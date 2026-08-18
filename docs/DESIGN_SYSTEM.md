# The Black Bird Field — enduring design system

**Revision:** v8.1 · 2026-08-15

The system is a curatorial grammar, not a component library pasted over the works. Its job is to hold different works in one field while keeping their visual, temporal and procedural differences active.

## 1. Ontology of surfaces

### FIELD — warm ground

The site-wide ground (`#c7bfb2`) behaves as an archival/exhibition field: quiet, dry, non-luxury, neither white gallery neutrality nor dark-artwork imitation.

### PAPER — reading/document surface

`#ddd6ca` and `#d2cabd` support documentary/contextual reading, metadata and footer material. Paper surfaces belong to the portfolio apparatus.

### THRESHOLD — dark work-facing surface

`#080908` introduces work encounters, feature sequences and project heroes. Dark is not a generic "dark mode"; it marks proximity to the autonomous works.

### SIGNAL — relational notation

Warm brown/orange marks numbering, section addresses and procedural notation. In v08.1 small light-field notation uses the darker optical variant `--micro-signal` so it remains readable without becoming loud.

## 2. Typography as roles

### Serif — reading / identity / display

System stack: `Iowan Old Style → Palatino Linotype → Book Antiqua → Palatino → Georgia → serif`.

It carries work titles, major statements, contextual prose and contact values. Display size indicates curatorial hierarchy, never apparatus.

### Sans — direct explanatory voice

Helvetica Neue / Arial system stack. It carries body explanation and operational language where the portfolio should sound neutral rather than literary.

### Mono — apparatus / address / evidence

System mono stack. It carries things that locate, qualify or index rather than narrate: work numbers, section numbers, versions, captions, states, keys, navigation apparatus.

v08.1 has exactly two small optical tiers:

- `micro = 12px`: semantically consequential apparatus;
- `micro-tight = 11px`: peripheral captions/subline where space is genuinely constrained.

Do not introduce a third smaller tier. Do not solve density by shrinking apparatus below 11px.

Tracking remains approximately `.1em` and uppercase where already authored. This spacing is part of the archival/indexical voice; it is also why the optical floor must be higher than v07's 8–9px values.

## 3. Hierarchy rule

Every major surface distinguishes:

1. **dominant encounter/content** — work image/video, title or primary reading;
2. **supporting statement** — explanatory prose;
3. **apparatus** — number, form, version, caption, state;
4. **action** — bounded, explicit, not mistaken for prose.

Apparatus may be small; it must not become incidental. Actions may be visually restrained; their target area must remain generous.

## 4. Grid and spacing

Wide surfaces use a 12-column grid inside `max-width:1640px` with responsive side padding. Columns define relations rather than equal card slots. Empty columns are legitimate when they produce measure or separation; accidental holes left by removed content are not.

Major vertical intervals typically use 52–96px depending on whether a section is a threshold, reading block, or terminal strip. Rules articulate boundaries; they should never double merely because adjacent components both drew their own beginning/end.

### Terminal About strip

`03 / ABOUT` → existing identity statement → action. No redundant display heading.

### Contact rows

Key (apparatus) → value (serif) → directional mark, followed by flexible remainder. The action mark belongs optically to the value, not to the far edge of the page.

## 5. Lines

Rules are structural evidence: page boundary, row boundary, selected-view plate, metadata cell. A line is not decoration. If an adjacent component already states the boundary, do not duplicate it.

This is why `/works/` no longer adds a first-row top rule below the page-mast rule.

## 6. Motion

Motion is evidence that a work is temporal, not ambient portfolio decoration.

Authorized moving surfaces:

- Home active work preview;
- project hero.

Still surfaces:

- Home feature sequence;
- Works index thumbnails;
- selected views;
- Practice figures.

Each loop is made from authentic captured states, with minute optical drift/cross-dissolve only. It returns to its first state so the loop seam does not become the event. Reduced Motion, Save Data, no-JS and unavailable media preserve the authored still fallback.

Current fallback authority:

- The Black Bird — `view-midpoint`;
- Winter Road — `view-midpoint`;
- UNHAPPY Scenario — `view-reconnecting`;
- Grave-Machine — `view-midpoint`;
- TAROKE REMIXER — `view-midpoint`.

## 7. Responsive transformation

Desktop preserves the 12-column field. Tablet/compact modes reduce simultaneous lateral relationships but do not remove product-defining content. Mobile becomes a vertical sequence.

At ≤760px:

- Home/feature/project media use mobile proportions;
- work index and project contexts stack;
- Contact key occupies a full first line, while value + arrow remain adjacent;
- Home About stacks label → statement → full-width action;
- no capability is removed solely to make the layout fit.

At 320px all non-exempt content must remain within one-dimensional reading flow without document-level horizontal scrolling.

## 8. Accessibility / interaction invariants

- One H1 per canonical page.
- Visible `:focus-visible` outline.
- Mobile menu: focus enters Close, Escape closes, focus returns to Menu.
- Whole Contact row is the link target.
- Action components retain 48px minimum height.
- Reduced Motion removes temporal enhancement, not information.
- Small light-field apparatus uses dedicated higher-contrast tonal variants rather than depending on size alone.

## 9. Adding future works

A future work inherits the vitrine grammar, not the visual identity of another work. It receives:

- one manifest;
- authentic responsive stills;
- optional motion capability if temporality is materially lost in a still;
- generated Home/Works/project/sitemap/count integration.

Do not shrink typography, add another microtier, duplicate shared geometry, or redesign existing works to accommodate a new record.
