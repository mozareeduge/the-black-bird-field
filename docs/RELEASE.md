# v08.1 release gate

A release is eligible only when the real migrated target satisfies all of the following:

- protected Grave runtime and CV match `content/protected_artifacts.json` before and after migration;
- strict `python src/build.py --check` passes;
- static and browser suites pass;
- `python validation/validate_v8_craft.py` passes;
- no authored 8/9/10px text rule has re-entered the design system;
- Contact, Home About, Works opening boundary and representative microtype are visually reviewed at desktop + mobile;
- 320px reflow has no document overflow;
- motion remains limited to Home preview + project hero; exact fallbacks survive Reduced Motion / Save Data;
- canonical visitor copy and routes are unchanged outside authorized v08.1 deltas;
- `git diff` contains no review presenter/evidence under visitor-facing source/output.

Push, tag push, PR, merge and Pages deployment are separate external actions requiring explicit authorization.
