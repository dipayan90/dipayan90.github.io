# Portfolio mockups — Phase 1

Three static directions for the personal portfolio of **Dipayan Chattopadhyay**, Software Development Manager at AWS. This folder is a review surface only. It is not linked from MkDocs and does not change the live site.

## View locally

From the repository root:

```sh
python3 -m http.server 8000
```

Open:

- `http://localhost:8000/mockups/a-ledger/`
- `http://localhost:8000/mockups/b-console/`
- `http://localhost:8000/mockups/c-story/`

The portrait uses the existing `docs/assets/profile.JPG` through `../../docs/assets/profile.JPG`. Serving from the repository root keeps that path valid.

## Directions

### A — Ledger

An editorial ledger rather than a dashboard: full-bleed near-black masthead, a centred reading column, slim sticky navigation, dated records with a left rule, and Projects as a plain index. The portrait appears once, in About.

Why it works: the first screen reads as a considered professional statement, not a résumé template. The reading measure and type scale carry the page; the single deep-green accent marks action and current state.

References:

- [Lee Robinson](https://leerob.com/) — calm single-column reading, typography-led hierarchy, no sidebar.
- [Brittany Chiang](https://brittanychiang.com/) — persistent compact navigation and one restrained accent.

No JavaScript.

### B — Console

An operator console for an engineering audience: fixed left identity rail, one scrolling panel, sticky in-page index, current role open by default, and native `<details>` accordions for roles and project chips. Dark is the default; a small toggle provides a light secondary theme.

Why it works: years, scope, contacts, and the section index stay visible while the evidence scrolls. Dense metadata is organised rather than hidden, and the interaction model stays native.

References:

- [Brittany Chiang](https://brittanychiang.com/) — persistent rail and one accent colour.
- [Saurabh Nemade](https://www.nemade.eu/) — leading with years and staff-level scope.

The only script is a 19-line light/dark toggle. Theme state is stored in `localStorage` under `kaj23-theme`.

### C — Story

A magazine spread: asymmetric hero with the portrait bleeding off the right edge, first-person standfirst, pull-quote from the real summary, chapter numerals `01–05`, alternating text/evidence spreads, and numbered experience entries `01–10`.

Why it works: it is the most distinct of the three at first glance. The portrait and chapter structure create a narrative, while the alternating spreads keep the page scannable rather than decorative.

References:

- [Adham Dannaway](https://www.adhamdannaway.com/) — one memorable first-screen device.
- [Lee Robinson](https://leerob.com/) — editorial reading flow and restrained chrome.

No JavaScript.

## Shared rules

- Plain HTML and one CSS file per direction. No framework, build step, npm dependency, CDN asset, or web font.
- System font stacks only. A uses an editorial serif and humanist sans; B uses a tight geometric sans and mono metadata; C uses a display serif and clean sans.
- Navigation is exactly: **Home, About Me, Experience, Projects, Skills, Personal**. The nav label is `Skills`; the section heading remains `Skills & Expertise`.
- The `Experience` nav item links to `experience.html` in every direction; section links use in-page anchors on the home page.
- Every first screen shows the name, role, `10+ years`, the 20-engineer scope line, and a visible route to Experience at both 1440x900 and 390x844.
- Content comes only from `docs/index.md`, `docs/summary.md`, and `docs/experience.md`. No invented employers, numbers, testimonials, logos, or placeholder copy.
- Every page carries the fixed footer: `Copy provisional: role line per owner brief.`
- A and C have no JavaScript. B has only the theme toggle; all disclosure uses native `<details>/<summary>`.
- Skip link, one `<h1>` per page, landmarks, visible `:focus-visible` rings, keyboard-reachable navigation, meaningful image alt text, and `prefers-reduced-motion` support are included.

## Contrast

All pairs below pass WCAG AA for normal text. Ratios were calculated from the CSS values.

| Direction | Pair | Ratio |
| --- | --- | --- |
| A | Ink `#1A1814` on paper `#FAF7F0` | 16.57:1 |
| A | Muted `#5C564C` on paper | 6.79:1 |
| A | Accent `#1F5A46` on paper | 7.52:1 |
| B dark | Text `#E7EDF3` on `#0A0E12` | 16.42:1 |
| B dark | Muted `#94A3B1` on `#0A0E12` | 7.50:1 |
| B dark | Accent `#5CC8FF` on `#0A0E12` | 10.29:1 |
| B light | Text `#0F1720` on `#F5F7F9` | 16.80:1 |
| B light | Muted `#4A5A68` on `#F5F7F9` | 6.62:1 |
| B light | Accent `#0B5F82` on `#F5F7F9` | 6.58:1 |
| C | Ink `#191411` on paper `#F6EFE2` | 15.98:1 |
| C | Muted `#6B5F50` on paper | 5.44:1 |
| C | Accent `#A43D1C` on paper | 5.63:1 |
| C | Sage `#5D6A52` on paper | 5.03:1 |

## Renders

The issue text mentions 13 renders, but the required state matrix produces **17**. All are present in `renders/`:

| Set | Count |
| --- | --- |
| Three directions × home/experience × 1440x900 and 390x844 | 12 |
| B light home × 1440x900 and 390x844 | 2 |
| Keyboard focus in nav × three directions | 3 |
| **Total** | **17** |

Patterns:

- `<direction>-home-1440x900.png`
- `<direction>-home-390x844.png`
- `<direction>-experience-1440x900.png`
- `<direction>-experience-390x844.png`
- `b-home-1440x900-light.png`
- `b-home-390x844-light.png`
- `<direction>-focus.png`

Screenshots use Chromium at device scale factor 1, viewport sizes exactly as named, and are not full-page captures. Each render was checked against its filename dimensions.

## Verification

- `mkdocs build --clean -d /tmp/kaj23-check` succeeds.
- `grep -ri mockups /tmp/kaj23-check` returns nothing; the documentation build does not include this folder.
- `git diff --stat -- docs mkdocs.yml .github` is empty.
- Automated Chromium checks passed at both viewports for all three home pages: six nav links, name/role/`10+ years`/scope visible, visible Experience route, no horizontal overflow, and no page errors.
- Keyboard focus reached the primary nav in all three directions.
- B's light theme toggle changed `data-theme` to `light` in a fresh context before the light captures.
- All local HTML, CSS, and portrait requests returned 200.

## Files

```text
mockups/
  README.md
  a-ledger/{index.html,experience.html,styles.css}
  b-console/{index.html,experience.html,styles.css}
  c-story/{index.html,experience.html,styles.css}
  renders/*.png
  renders/verification.json
```

## Notes for review

- The final role line is still provisional per the owner brief; that is why the footer repeats it on every page.
- The three directions share copy and information architecture, not layout. A is quiet and editorial, B is dense and operational, C is narrative and image-led.
- System-font rendering will vary slightly between macOS, Windows, and Linux. The supplied renders are from local Chromium on macOS.
- Screenshots were generated and checked for layout behaviour, but final aesthetic sign-off should be done by the owner in a browser.
