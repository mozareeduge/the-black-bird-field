---
id: plan-portfolio
title: Portfolio (The Black Bird Field) — decision plan
kind: work-plan
status: active
version: 1
scope: "[[the-black-bird-field]]"
depends_on: []
date_decided: 2026-08-30
decided_by: Mohammad Zare
---

# Portfolio — decision plan

Diagnosis session: 2026-08-30, atelier protocol, two linked purposes
(differentiation critique grounded in `mozare-wiki`; readiness audit for a
sixth work across design/technical/copy). Full diagnosis given in
conversation; this file carries only the decisions that followed it.

---

```yaml
decision: PF-01
title: Rewrite Practice-page copy for academic register and structural extensibility
status: decided
priority: P1
origin: unmade-decision
finding: >
  content/site.json's practice.modules[1].text and modules[2].text are
  hand-written prose that individually enumerate work names inside one
  flowing sentence per module ("Movement leaves a route in The Black Bird.
  Nearness governs visibility in Winter Road. UNHAPPY Scenario lets
  procedural notices keep their calm... Grave-Machine holds the poem beside
  its trace, while TAROKE REMIXER exposes the act of composition."). Unlike
  every count/list elsewhere on the site, this is not template-generated:
  a sixth work either goes unmentioned (the claim silently becomes
  incomplete) or the sentence needs manual extension — the one place in
  visitor-facing copy where docs/ADDING_A_WORK.md's "an addition, not
  another portfolio rebuild" promise does not hold. Separately: the
  Practice/About copy's plain register never surfaces the actual
  theoretical lineage behind the interface choices (object-oriented
  ontology / withdrawal, minor literature, genetic criticism — see
  mozare-wiki 03-objects/concepts/object-oriented-ontology.md,
  withdrawal.md; 06-relations/scenography-to-interface-architecture.md,
  minor-literature-to-object-oriented-ontology.md). Asked whether the
  plain register was an intentional accessibility choice: confirmed not
  intentional. Decision: the copy should read as academically credible and
  theoretically grounded while remaining legible to a non-scholar reader
  encountering the site cold.
evidence:
  repo: mozareeduge/the-black-bird-field
  commit: 9aded6b8f158f502142399778fb84620c0279afd
  locus: "content/site.json:practice.modules[1].text, [2].text (rendered at /practice/, confirmed in both desktop and mobile screenshots)"
  observed: 2026-08-30
  method: both
decision_text: >
  Rewrite content/site.json's practice.mast, practice.intro, and all three
  practice.modules[].text fields as one coherent pass — not patch two
  modules in isolation, since the three read as one paragraph sequence.
  Each module keeps its structural function (a claim about research,
  generation, interface) but is grounded with the actual theoretical term
  it enacts, introduced through use before being named (per the supplied
  writing-guidelines skill's concept-discipline rule: material first,
  concept named because the material required it, never a chain of
  keywords). The per-work sentence in modules[1] and [2] is restructured
  from an exhaustive enumeration into a bounded example pattern (one or two
  named works as illustration, explicitly marked as example rather than
  inventory) so a sixth work needs no edit here to keep the claim true.
  About's paragraphs are read for consistency of register but are not
  themselves rewritten under this decision — they were not flagged as
  academically thin, and rewriting them is out of this finding's scope.
implementation:
  - "Build and load the writing-guidelines skill (converted from the supplied 'Writing Guidelines for Mohammad Zare' document) before drafting."
  - "Draft replacement text for content/site.json: practice.mast, practice.intro[0..1], practice.modules[0].text, modules[1].text, modules[2].text."
  - "Verify each new module sentence names at most one or two works as bounded example, not as an implicit closed set — grep the new text for co-occurring work names to confirm no 3+ enumeration remains."
  - "python3 src/build.py --check; python3 -m pytest tests/static -q"
  - "Screenshot /practice/ (desktop+mobile) and visually confirm register and layout are unaffected (this is a copy-only change, no template edit)."
acceptance:
  - "No practice.* field enumerates 3+ work names in one sentence."
  - "Each newly introduced theoretical term (withdrawal, object-oriented ontology, minor literature, genetic criticism, or equivalent) appears with a plain-language grounding clause in the same sentence or the one before it, not as an unglossed proper noun."
  - "tests/static pass unchanged; build succeeds with the existing 5-work manifest set."
  - "A reader unfamiliar with the wiki's vocabulary can follow the Practice page without external context (self-check against writing-guidelines skill's audience-discipline rule)."
risk: >
  Over-correcting toward density is the likely failure mode given the
  instruction to be "academically credible and rich" — the writing-
  guidelines skill's own style-calibration section (density only where the
  material demands it) is the guardrail; if a drafted sentence needs a
  gloss for the gloss, it has failed the audience-discipline check and
  must be rewritten, not footnoted.
```

executed: 2026-08-30 · 3305ed6980c454bbfa79690451ec8db8d5dd2936

amended: 2026-08-30 · first execution reduced each module from an
  exhaustive roll call to one or two named works ("Grave-Machine tests...
  TAROKE REMIXER goes further...") — this satisfied the literal acceptance
  bullet (no 3+ enumeration) but not the actual finding: a module that
  names one or two specific works is still not count-agnostic, still reads
  as an arbitrary subset once a reader notices the site has more works
  than get named, and still leaves an implicit, undocumented human
  decision at the next work's launch ("does the new work's name get added
  here too?"). Flagged directly: "you did not solve the problems, you
  just made more text, but they are still about specific works." Correct
  fix: remove every work proper noun from practice.modules[].text
  entirely — the module's concrete instance is already carried by its
  image + caption fields (unchanged, unflagged), so the running text is
  free to state the mechanism in general terms that need no edit, ever,
  regardless of work count. Acceptance bullet 1 is superseded by: "no
  practice.modules[].text field names a specific work by proper noun,
  under any count." Re-executed and re-validated (build + tests + fresh
  screenshot) in the same session.

PF-01 in prose: the Practice page currently says less than the site knows
about itself, and says it in a way that cannot survive a sixth work without
a manual rewrite. Both problems have the same fix — write the three
modules from the actual theoretical apparatus behind the site (which the
wiki already documents, and which the site's own apparatus vocabulary
already gestures at through "edition," "citation," "current public build")
rather than from a generic explainer register, and write the illustrative
work-mentions as bounded examples rather than a closed roll call.

---

```yaml
decision: PF-02
title: Correct stale/inaccurate counts and one misspelling in README and docs
status: decided
priority: P2
origin: mistake
finding: >
  Four present-day accuracy errors, independent of future-work readiness:
  (1) README.md:5,47 spell the fifth work "TAROKE RIMIXER"; the canonical
  title (content/works/taroke-remixer.json:title) is "TAROKE REMIXER".
  (2) README.md:65 and docs/DEPLOYMENT.md:64 both say "Eight legacy
  redirect stubs"; src/build.py's LEGACY dict has 9 entries (confirmed by
  AST-parsing the literal). (3) docs/TECHNICAL_ARCHITECTURE.md:36 states
  "five `/works/<slug>/` pages" as a literal count in a document whose own
  subject is count-agnostic extensibility — self-undermining phrasing that
  will read as wrong the moment work six ships. (4) docs/MOTION_MEDIA.md:48
  and :50 reference `validation/check_motion_media.py` and
  `scripts/normalize_taroke_capture_identity.py`; neither exists in this
  repo snapshot (confirmed: no validation/ directory; scripts/ contains
  only add_work.py, build_motion_media.py, update_protected_artifacts.py).
evidence:
  repo: mozareeduge/the-black-bird-field
  commit: 9aded6b8f158f502142399778fb84620c0279afd
  locus: "README.md:3,5,47,65; docs/DEPLOYMENT.md:64; docs/TECHNICAL_ARCHITECTURE.md:36; docs/MOTION_MEDIA.md:48,50"
  observed: 2026-08-30
  method: source-read
decision_text: >
  Fix all four in place. "TAROKE RIMIXER" → "TAROKE REMIXER" (both
  occurrences). "Eight legacy redirect stubs" → "Nine legacy redirect
  stubs" (both occurrences). TECHNICAL_ARCHITECTURE.md's "five
  `/works/<slug>/` pages" → "one `/works/<slug>/` page per work" (removes
  the literal count without losing the information; consistent with the
  same document's own "Work-count scaling" section). MOTION_MEDIA.md's two
  dangling tool references are removed rather than fabricated as working
  scripts; the Reproduction section keeps only
  `python scripts/build_motion_media.py`, which exists and is real.
implementation:
  - "Edit README.md: lines 5, 47 (spelling); line 65 (count)."
  - "Edit docs/DEPLOYMENT.md: line 64 (count)."
  - "Edit docs/TECHNICAL_ARCHITECTURE.md: line 36 (delexicalize the count)."
  - "Edit docs/MOTION_MEDIA.md: remove the two dangling-script lines (48, 50) from the Reproduction section."
  - "grep -rn 'RIMIXER' . (excluding archive/, .git/) to confirm zero remaining occurrences."
acceptance:
  - "grep -rn 'RIMIXER' outside archive/ and .git/ returns nothing."
  - "grep -rn 'Eight legacy' returns nothing; the stub count in prose matches len(LEGACY) in src/build.py."
  - "No doc references a script or module absent from the actual scripts/ or validation/ tree."
```

executed: 2026-08-30 · 3305ed6980c454bbfa79690451ec8db8d5dd2936
