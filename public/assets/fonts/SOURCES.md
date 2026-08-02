# Font sources

Self-hosted WOFF2 subset files per `references/DESIGN_UIUX_TECH_SPEC.md`
Section 5.3. Latin subset only for the three Latin families; Arabic-script
subset (covers Persian) for Estedad. All licensed SIL Open Font License
1.1 (OFL-1.1) — free to embed and self-host.

Extracted from the pinned npm `@fontsource/*` packages (version 5.3.0
throughout), which repackage the original upstream font releases as
static per-weight WOFF2 files without altering the font data.

| File | Family | Weight/style | Source package | Upstream |
|---|---|---|---|---|
| `source-serif-4-400.woff2` | Source Serif 4 | 400 regular | `@fontsource/source-serif-4@5.3.0` | https://github.com/adobe-fonts/source-serif |
| `source-serif-4-500.woff2` | Source Serif 4 | 500 regular | `@fontsource/source-serif-4@5.3.0` | https://github.com/adobe-fonts/source-serif |
| `source-serif-4-500-italic.woff2` | Source Serif 4 | 500 italic | `@fontsource/source-serif-4@5.3.0` | https://github.com/adobe-fonts/source-serif |
| `ibm-plex-sans-400.woff2` | IBM Plex Sans | 400 regular | `@fontsource/ibm-plex-sans@5.3.0` | https://github.com/IBM/plex |
| `ibm-plex-sans-600.woff2` | IBM Plex Sans | 600 semibold | `@fontsource/ibm-plex-sans@5.3.0` | https://github.com/IBM/plex |
| `ibm-plex-mono-400.woff2` | IBM Plex Mono | 400 regular | `@fontsource/ibm-plex-mono@5.3.0` | https://github.com/IBM/plex |
| `ibm-plex-mono-500.woff2` | IBM Plex Mono | 500 medium | `@fontsource/ibm-plex-mono@5.3.0` | https://github.com/IBM/plex |
| `estedad-400.woff2` | Estedad | 400 regular (Arabic-script subset) | `@fontsource/estedad@5.3.0` | https://github.com/aminabedi68/Estedad |

## SHA-256

```
67b28fd96f71a9a08c0f44d5313471065a1fb652bd84fe255c6f5933dc1050db  estedad-400.woff2
08949f728dc52d528e69b1667d15c89a5686a4ee9a296ff90983985f99c380f7  ibm-plex-mono-400.woff2
01d285447409c8a588692162439a038b8cbd7871309ee20267b0d2d91c6e8e22  ibm-plex-mono-500.woff2
3b646991d30055a93a4ecc499713d4347953a74a947ecab435ab72070cbdab0e  ibm-plex-sans-400.woff2
8960851d691c054ed38e259bdcf1a6190d157b4203ed5bb32c632a863fb8ec2f  ibm-plex-sans-600.woff2
02194deb92d3975dd30e11a3824a1f1db32b48c93654e60560cb81ce8e7b5f95  source-serif-4-400.woff2
df3dca6c4e58f28f1f3d81b0640afb100dad7bef4d6a0ecd719c0a94da082fa3  source-serif-4-500-italic.woff2
d3e119de0b756d9fa6d368de570f7168bb74eedf3289aaeae22dd97b900918d1  source-serif-4-500.woff2
```

Total compressed transfer: ~176 KB, within the 300 KB budget in Section
10.4 of the design specification.
