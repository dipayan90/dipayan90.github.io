# KAJ-30 — Phase 2 QA gate report

Local gate only. `qa/check_phase2.py` is deliberately **not** wired into
`.github/workflows/main.yml` (B9 requires the workflow to stay byte-identical
to `origin/development`). Run it locally with `python qa/check_phase2.py site`.

- Branch: `kaj-25/qa`
- Base commit: `d7f8367` (`KAJ-47: restyle five pages to Direction C vocabulary`)
- Built site: `site/`, rebuilt by upstream KAJ-29 run on 2026-11-18 05:10
- Checker invocation: `python3 qa/check_phase2.py site`
- Verdict: **10 PASS / 5 FAIL** — the gate fails. A failed assertion is a real
  finding; no site file was changed to make a check pass.

## PASS/FAIL table

| ID | Verdict | Detail | Owning issue |
| --- | --- | --- | --- |
| B1 | PASS | No `<style>` element; every built page links exactly one `assets/css/custom.css` | — |
| B2 | PASS | All 7 nav labels present on 10/10 built pages | — |
| B6' | FAIL | `opensource/index.html` has `<img src="https://img.youtube.com/vi/F8C58OZW3-M/0.jpg">`, a non-`dipayan90.github.io` origin. No Google Fonts refs. JS: 37 files, 1,063,439 raw bytes, 281,321 gzip bytes | KAJ-28 |
| B8 | FAIL | `Software Development Manager at AWS` and `10+` present; nav labels match `origin/development`; baseline **CV link missing** from built home | KAJ-28 |
| B9 | PASS | `.github/workflows/main.yml` byte-identical to `origin/development` (1,876 bytes both sides) | — |
| S1 | FAIL | Titles 10/10 unique; descriptions only 9/10 unique: `404.html` and `blog/index.html` share `Professional portfolio of Dipayan Chattopadhyay, Software Development Manager at AWS`. Max description length 150 chars. Each page also emits two identical description tags (theme + hook) — not a stated failure, recorded as an observation | KAJ-26 |
| S2 | FAIL | `404.html` has no canonical link. All blog post URLs present in `sitemap.xml`; `robots.txt` has `Sitemap:` | KAJ-26 |
| S3 | PASS | `feed.xml` is RSS 2.0, 1 item, blog post only, absolute link/guid, newest first | — |
| S4 | PASS | Post has og:title, og:description, og:type=article, og:url, absolute og:image, twitter:card | — |
| S5 | PASS | Post has exactly one `application/ld+json` block, valid JSON, `@type=BlogPosting`, absolute url/image, Person author | — |
| S6 | FAIL | `opensource/index.html` YouTube img and `summary/index.html` `portrait-800.jpg` have width but **no height**. No `profile.JPG` refs. Portrait srcset has 3 webp candidates. Largest image 83,476 bytes | KAJ-28 |
| S7 | PASS | Exactly one `<h1>` per built page; stylesheet has `:focus-visible` and `prefers-reduced-motion` | — |
| BR1 | PASS | `/blog/` h1 is `Writing`, 1 entry, newest-first | — |
| BR3 | PASS | `/blog/designing-for-forty-million-contacts/` matches `^/blog/[a-z0-9-]+/$` | — |
| BR5 | PASS | `site/blog/drafts/` absent; draft slugs absent from sitemap and feed | — |

## Required numbers

### Lighthouse (mobile preset, `--form-factor=mobile`, default mobile throttling)

| Page | Performance | Accessibility | Best practices | SEO |
| --- | --- | --- | --- | --- |
| Home | 98 | 95 | 100 | 100 |
| Blog index | 93 | 95 | 100 | 100 |
| Blog post | 92 | 95 | 100 | 100 |

Raw reports: `lighthouse-home.json`, `lighthouse-blog.json`, `lighthouse-post.json`.
Lighthouse 13.6.0, Chrome headless, site served with `python3 -m http.server`
from `site/`. No desktop preset was used.

### axe-core (WCAG 2.0/2.1 A+AA)

| Page | Violations | Rule | Target |
| --- | --- | --- | --- |
| Home | 1 | `color-contrast` (serious) | `.md-copyright__highlight` |
| Blog index | 1 | `color-contrast` (serious) | `.md-copyright__highlight` |
| Blog post | 1 | `color-contrast` (serious) | `.md-copyright__highlight` |
| Ask | 1 | `color-contrast` (serious) | `.md-copyright__highlight` |

Total: **4 violations across 4 pages** (one distinct rule, one distinct target).
Raw results: `axe-home.json`, `axe-blog.json`, `axe-post.json`, `axe-ask.json`.

### Asset sizes

- Total JS under `site/assets/javascripts/`: **1,063,439 raw bytes** across 37 files.
- Total JS gzip size (per-file `gzip.compress(..., 9)`, summed): **281,321 bytes**.
- Largest built image: **83,476 bytes** — `assets/img/portrait-800.webp`.
  Next largest: 61,560 bytes (`portrait-800.jpg`). All referenced images stay
  under the 150 KB limit.

## Notes, caveats and unverifiable items

- **B8 baseline discrepancy (documented, not worked around).** The KAJ-30 spec
  says the CV link is present on `origin/development`. That ref's `docs/index.md`
  has no CV link; the link
  `https://drive.google.com/file/d/1laT67xxMLH0JHuavO3VTqt0qcclG4BIU/view?usp=sharing`
  exists on the local `development` branch and on the deployed `gh-pages`
  baseline. The gate uses that deployed baseline URL as the required token.
  Either way the built home has no CV link, so B8 fails on the site, not on the
  spec ambiguity.
- **S1 duplicate-tag observation.** Every built page emits two identical
  `<meta name="description">` tags (theme hook + template). The stated criterion
  is uniqueness across pages and ≤160 chars, so the gate reports the cross-page
  duplicate as the failure and the per-page duplication as an observation.
- **No criterion was unverifiable.** All 15 assertions executed against the
  built site. Lighthouse and axe both ran successfully, using temporary local
  tool installs outside the worktree; no UNAVAILABLE placeholder was needed.
- **Strict build** completed with exit 0 (`mkdocs build --strict`, mkdocs 1.6.1 /
  Material 9.8.0, output redirected to a temp directory so `site/` was not
  mutated). See `build-strict.log`.
- **Screenshots** in `screens/` are 390×844 and 1440×900 captures of home,
  Experience, Ask, blog index and blog post, plus `home-focus-mobile.png`
  (first Tab focus state) and `home-reduced-motion-mobile.png` (emulated
  `prefers-reduced-motion: reduce`).
- **Wire-up:** none. The script is a local gate only; `.github/workflows/main.yml`
  is untouched and byte-identical to `origin/development` (B9).

## Hand back

Failed assertions are real findings. Fix them in the owning issues, then rerun
the gate:

1. **KAJ-28** — B6' external YouTube thumbnail origin; B8 missing baseline CV
   link on home; S6 missing `height` on two images.
2. **KAJ-26** — S1 duplicate description between `404.html` and `blog/index.html`;
   S2 missing canonical on `404.html`.

KAJ-29 has no failing blog assertion (S3, S4, S5, BR1, BR3, BR5 all PASS).
