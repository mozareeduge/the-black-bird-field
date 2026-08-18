# Motion and static-fallback contract — v08.1

Motion exists to exhibit temporal behavior that a still cannot carry. It is evidence of the work's duration, not ambient portfolio animation.

## Surface boundary

Allowed moving surfaces:

- selected Home work preview;
- project-page hero.

Still-only surfaces:

- Home feature sequence;
- Works thumbnails;
- project Selected Views;
- Practice figures;
- About and Contact.

## Delivery contract

- H.264 MP4, no audio, muted, loop, `playsinline`.
- Desktop + mobile files per motion-enabled work.
- Current loop target: approximately 10 seconds.
- Maximum file budget encoded in source validator: 1.5 MB per file.
- Poster is visible before video and remains the semantic fallback.
- Home loads only the selected work's video source.
- Reduced Motion / Save Data / no-JS / media failure never removes access or meaning.

## Per-work temporal grammar

| Work | Temporal verb | Authored fallback |
|---|---|---|
| The Black Bird | focus travel → afterglow | `view-midpoint` |
| Winter Road | approach → condense → recede | `view-midpoint` |
| UNHAPPY Scenario | fail → reconnect → report → return | `view-reconnecting` |
| Grave-Machine | tick → accrue → retain trace | `view-midpoint` |
| TAROKE REMIXER | edit → propagate → inspect evidence | `view-midpoint` |

The current package loops are constructed from authentic v07/v08 captured work states with restrained cross-dissolve and minute optical drift. When a corrected live runtime can be captured directly, authentic runtime capture outranks reconstructed interpolation.

## Reproduction

`python scripts/build_motion_media.py`

Technical validation:

`python validation/check_motion_media.py`

The capture/spelling-normalization utility for inherited TAROKE desktop evidence is `scripts/normalize_taroke_capture_identity.py`; it is idempotent and changes only the title glyph cell required by the owner-locked identity correction.
