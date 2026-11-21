# KAJ-30 — Phase 2 QA gate report

Local gate only. `qa/check_phase2.py` is deliberately **not** wired into
`.github/workflows/main.yml` (B9 requires the workflow to stay byte-identical
to `origin/development`). Run it locally with `python qa/check_phase2.py site`.

- Branch: `kaj-25/qa`
- Base commit: `db5080f`
- Built site: `site/`, rebuilt by this run on 2026-11-19
- Checker invocation: `python3 qa/check_phase2.py site`
- Verdict: **17 PASS / 0 FAIL** — all assertions pass, including B3 on the
  refreshed axe evidence.

## PASS/FAIL table

| ID | Verdict | Detail | Owning issue |
| --- | --- | --- | --- |
| B1 | PASS | No `<style>` element; every built page links exactly one `assets/css/custom.css` | — |
| B2 | PASS | All 7 nav labels present on 10/10 built pages | — |
| B3 | PASS | axe records 0 violations on home, blog, post and ask after the `db5080f` contrast fix | KAJ-28 |
| B4 | PASS | Lighthouse mobile: home 0.98/0.95, blog 0.93/0.95, post 0.92/0.95 (performance/accessibility); all at or above thresholds | — |
| B6' | PASS | No external image origins; no Google Fonts refs. JS: 37 files, 1,057,471 raw bytes, 279,262 gzip bytes | — |
| B8 | PASS | `Software Development Manager at AWS` and `10+` present; nav labels match `origin/development`; baseline CV link present on built home | — |
| B9 | PASS | `.github/workflows/main.yml` byte-identical to `origin/development` (1,876 bytes both sides) | — |
| S1 | PASS | Titles 10/10 unique; descriptions 10/10 unique; max description length 150 chars; exactly one description tag per page | — |
| S2 | PASS | Exactly one canonical link per built page, including `404.html`; blog posts present in `sitemap.xml`; `robots.txt` has `Sitemap:` | — |
| S3 | PASS | `feed.xml` is RSS 2.0, 1 item, blog post only, absolute link/guid, newest first | — |
| S4 | PASS | Post has og:title, og:description, og:type=article, og:url, absolute og:image, twitter:card | — |
| S5 | PASS | Post has exactly one `application/ld+json` block, valid JSON, `@type=BlogPosting`, absolute url/image, Person author | — |
| S6 | PASS | No image lacks width/height. No `profile.JPG` refs. Portrait srcset has 3 webp candidates. Largest image 83,476 bytes | — |
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
from `site/`. No desktop preset was used. These reports were not re-run by this
backend fix; B4 reads them as committed evidence.

### axe-core (WCAG 2.0/2.1 A+AA)

Re-run on 2026-11-21 against the rebuilt site with axe-core 4.10.3, the same
`wcag2a`, `wcag2aa`, `wcag21a` and `wcag21aa` tags, a 390×844 viewport and a
local `http.server` on port 8765. All four audited pages report zero violations.

| Page | Violations |
| --- | --- |
| Home | 0 |
| Blog index | 0 |
| Blog post | 0 |
| Ask | 0 |

Total: **0 violations across 4 pages**. Raw results: `axe-home.json`,
`axe-blog.json`, `axe-post.json`, `axe-ask.json`. The
`.md-copyright__highlight` contrast rule comes from branch commit `db5080f` /
KAJ-55 and is outside this backend patch; KAJ-55 deliberately left the evidence
bundle untouched.

### Asset sizes

- Total JS under `site/assets/javascripts/`: **1,057,471 raw bytes** across 37 files.
- Total JS gzip size (per-file `gzip.compress(..., 9)`, summed): **279,262 bytes**.
- Largest built image: **83,476 bytes** — `assets/img/portrait-800.webp`.
  Next largest: 61,560 bytes (`portrait-800.jpg`). All referenced images stay
  under the 150 KB limit.

## Notes, caveats and unverifiable items

- **B3 is evidence-bound.** A zero-violation axe run is required to pass it.
  The new assertion was checked both ways: zeroing the four committed axe
  reports makes B3 PASS (17 PASS / 0 FAIL); lowering home Lighthouse
  performance to 0.80 makes B4 FAIL (15 PASS / 2 FAIL); both edits were then
  restored. The four axe reports have now been refreshed with a live
  zero-violation run, so the recorded verdict is 17 PASS / 0 FAIL.
- **S1/S2 fix.** `overrides/partials/meta.html` no longer emits a second
  description; the theme remains the single source. It emits the canonical
  only where the theme omits one (the `404.html` page, which has no `page`
  object), and `docs/blog/index.md` now has its own description.
- **Parallel frontend fixes.** B6', B8 and S6 pass because branch commit
  `db5080f` already carries the YouTube-thumbnail removal, CV-link addition,
  image `height` attributes and footer contrast rule. Those files are outside
  this backend patch; the gate output describes the whole branch as built.
- **Theme version.** This rebuild used mkdocs 1.6.1 / Material 9.6.21, the
  version available here; the earlier baseline evidence was produced with
  Material 9.8.0. That changes bundle hashes and JS byte totals, but not the
  meta-tag structure checked by S1/S2.
- **Screenshots** in `screens/` are the earlier 390×844 and 1440×900 captures
  of home, Experience, Ask, blog index and blog post, plus focus and reduced
  motion captures. They were not re-captured by this backend run.
- **Wire-up:** none. The script is a local gate only; `.github/workflows/main.yml`
  is untouched and byte-identical to `origin/development` (B9).

## Hand back

The axe evidence has been refreshed after the parallel contrast fix, so B3
passes and the gate exits 0. S1 and S2 are closed by this patch, and B3/B4 are
now hard assertions rather than prose observations.

KAJ-29 has no failing blog assertion (S3, S4, S5, BR1, BR3, BR5 all PASS).
