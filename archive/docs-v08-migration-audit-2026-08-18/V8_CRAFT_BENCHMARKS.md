# v08.1 craft benchmark note

This note records why the four owner-identified problems were solved as system rules rather than local CSS patches. External references are benchmarks, not aesthetic authority.

## Apparatus sizing

USWDS distinguishes a 10px `micro` system token from its normal theme scale and exposes 12/13/14px steps above it. The Black Bird Field intentionally retains a smaller-than-conventional apparatus voice, but v07's 8–9px text sat below even that micro benchmark. v08.1 uses 11px only for constrained peripheral notation and 12px for semantic apparatus.

Source: https://designsystem.digital.gov/design-tokens/typesetting/font-size/

## Contact anatomy

GOV.UK's Summary List formalizes a row as **key + value + optional action**. The contact page is not visually copied from GOV.UK, but the semantic decomposition is useful: the label is a key, the address/name is the value, and the arrow is an action/direction cue. v08.1 therefore stops treating the arrow as a far-edge decoration.

Source: https://design-system.service.gov.uk/components/summary-list/

## Reflow / enlargement

WCAG 2.2 guidance requires text to remain usable when enlarged to 200% and non-exempt content to reflow at a width equivalent to 320 CSS px. v08.1 therefore raises microtext without fixing component heights and tests the new Contact/About arrangements at narrow widths instead of solving readability by clipping or hiding content.

Sources:
- https://www.w3.org/WAI/WCAG22/Understanding/resize-text
- https://www.w3.org/WAI/WCAG22/Understanding/reflow

## Contrast

WCAG AA requires 4.5:1 for ordinary-size text. v07's general muted/signal colors are intentionally subtle, but using them unchanged at 8–12px weakened the apparatus. v08.1 adds darker *micro-only* light-field variants so the palette and larger-text behavior stay intact.

Source: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

## Pointer targets

WCAG 2.2 introduces a 24×24 CSS-px minimum target/spacing criterion. Contact keeps each full-width row clickable; action buttons already retain a 48px minimum height. The visual arrow can stay small because it is not the target boundary.

Source: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
