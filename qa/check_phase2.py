#!/usr/bin/env python3
"""Local Phase 2 QA gate for KAJ-30 (stdlib only).

Usage: python qa/check_phase2.py site
Prints PASS/FAIL per criterion and exits non-zero if any criterion fails.
This is a local gate only; it is deliberately not wired into CI (B9).
"""

import gzip
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = (ROOT / (sys.argv[1] if len(sys.argv) > 1 else "site")).resolve()
EVIDENCE = ROOT / "qa" / "phase2"
ORIGIN = "https://dipayan90.github.io"
CV_TOKEN = "1laT67xxMLH0JHuavO3VTqt0qcclG4BIU"
NAV_LABELS = [
    "Home", "About Me", "Experience", "Projects",
    "Skills & Expertise", "Personal", "Ask",
]
DRAFT_SLUGS = ("example", "example-draft")
MAX_IMAGE_BYTES = 150 * 1024


class PageParser(HTMLParser):
    """Collects tags, nav text, title, meta tags and scripts from one page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []          # (tag, attrs dict)
        self.nav_labels = []
        self.title = ""
        self.scripts = []       # (attrs dict, text)
        self._nav_depth = None
        self._capture = None
        self._script = None

    def handle_starttag(self, tag, attrs):
        attr_map = dict(attrs)
        self.tags.append((tag, attr_map))
        if tag == "nav" and attr_map.get("aria-label") == "Primary":
            self._nav_depth = 1
        elif tag == "a" and self._nav_depth is not None:
            self._capture = []
        elif tag == "title":
            self._capture = []
        elif tag == "script":
            self._script = [attr_map, []]

    def handle_data(self, data):
        if self._capture is not None:
            self._capture.append(data)
        if self._script is not None:
            self._script[1].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._capture is not None and self._nav_depth is not None:
            self.nav_labels.append("".join(self._capture).strip())
            self._capture = None
        if tag == "title" and self._capture is not None:
            self.title = "".join(self._capture).strip()
            self._capture = None
        if tag == "script" and self._script is not None:
            self.scripts.append((self._script[0], "".join(self._script[1])))
            self._script = None
        if tag == "nav":
            self._nav_depth = None

    def find(self, tag, **attrs):
        return [
            a for t, a in self.tags
            if t == tag and all(a.get(k) == v for k, v in attrs.items())
        ]

    def meta(self, key, attr="name"):
        return [a.get("content", "") for a in self.find("meta", **{attr: key})]


def git_show(ref_path, binary=False):
    result = subprocess.run(
        ["git", "-C", str(ROOT), "show", ref_path],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("git show {} failed".format(ref_path))
    return result.stdout if binary else result.stdout.decode("utf-8", "replace")


def load_pages():
    pages = {}
    for path in sorted(SITE.rglob("*.html")):
        rel = path.relative_to(SITE).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        parsed = PageParser()
        parsed.feed(text)
        parsed.close()
        if rel == "index.html":
            url = "/"
        elif rel.endswith("/index.html"):
            url = "/" + rel[:-len("index.html")]
        else:
            url = "/" + rel
        pages[rel] = {"path": path, "text": text, "p": parsed, "url": url}
    return pages


def absolute_or_none(value):
    value = (value or "").strip()
    if value.startswith("//"):
        value = "https:" + value
    parsed = urlparse(value)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return "{}://{}".format(parsed.scheme, parsed.netloc)
    return None


def check(results, cid, ok, detail):
    results.append((cid, bool(ok), detail))


def main():
    results = []
    if not SITE.is_dir():
        print("FAIL setup site directory not found: {}".format(SITE))
        return 1
    pages = load_pages()
    home = pages["index.html"]
    post_pages = {
        rel: pg for rel, pg in pages.items()
        if rel.startswith("blog/") and rel != "blog/index.html" and rel.endswith("index.html")
    }
    css_path = SITE / "assets/css/custom.css"
    css = css_path.read_text(encoding="utf-8", errors="replace") if css_path.exists() else ""

    # B1: no inline <style>, exactly one custom.css link per page.
    styled = [rel for rel, pg in pages.items() if pg["p"].find("style")]
    bad_css = []
    for rel, pg in pages.items():
        links = [
            a for a in pg["p"].find("link", rel="stylesheet")
            if "assets/css/custom.css" in a.get("href", "")
        ]
        if len(links) != 1:
            bad_css.append("{}:{}".format(rel, len(links)))
    check(results, "B1", not styled and not bad_css,
          "style tags={}, custom.css link counts={}".format(styled or "none", bad_css or "all 1"))

    # B2: primary nav labels on every page.
    nav_bad = []
    for rel, pg in pages.items():
        missing = [label for label in NAV_LABELS if label not in pg["p"].nav_labels]
        if missing:
            nav_bad.append("{} missing {}".format(rel, missing))
    check(results, "B2", not nav_bad,
          "7 labels on {} of {} pages{}".format(
              len(pages) - len(nav_bad), len(pages),
              "; " + "; ".join(nav_bad) if nav_bad else ""))

    # B3: axe-core must report zero violations on home, blog index, post and Ask.
    axe_bad, axe_counts, axe_total = [], [], 0
    for name in ("home", "blog", "post", "ask"):
        try:
            report = json.loads((EVIDENCE / "axe-{}.json".format(name)).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            axe_bad.append("{} unreadable ({})".format(name, exc))
            continue
        violations = report.get("violations", [])
        axe_total += len(violations)
        axe_counts.append("{}:{}".format(name, len(violations)))
        if violations:
            rules = sorted({v.get("id", "unknown") for v in violations})
            axe_bad.append("{}:{} {}".format(name, len(violations), "/".join(rules)))
    check(results, "B3", not axe_bad,
          "violations per page={}, total={}, issues={}".format(
              ", ".join(axe_counts) or "none", axe_total, axe_bad or "none"))

    # B4: Lighthouse mobile performance >= 90 and accessibility >= 95 on every audited page.
    lh_bad, lh_scores = [], []
    for name in ("home", "blog", "post"):
        try:
            report = json.loads((EVIDENCE / "lighthouse-{}.json".format(name)).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            lh_bad.append("{} unreadable ({})".format(name, exc))
            continue
        settings = report.get("configSettings", {})
        form = settings.get("formFactor") or settings.get("emulatedFormFactor")
        categories = report.get("categories", {})
        perf = categories.get("performance", {}).get("score")
        a11y = categories.get("accessibility", {}).get("score")
        lh_scores.append("{}={}/{}".format(name, perf, a11y))
        if form != "mobile":
            lh_bad.append("{} formFactor={}".format(name, form))
        if not isinstance(perf, (int, float)) or perf < 0.90:
            lh_bad.append("{} performance={}".format(name, perf))
        if not isinstance(a11y, (int, float)) or a11y < 0.95:
            lh_bad.append("{} accessibility={}".format(name, a11y))
    check(results, "B4", not lh_bad,
          "mobile perf/a11y scores={}, issues={}".format(
              ", ".join(lh_scores) or "none", lh_bad or "none"))

    # B6': no external origin in link/script/img href/src; no Google font refs; JS byte report.
    external, font_refs = [], []
    for rel, pg in pages.items():
        for tag, attrs in pg["p"].tags:
            if tag not in ("link", "script", "img"):
                continue
            for key in ("href", "src"):
                origin = absolute_or_none(attrs.get(key))
                if origin and origin != ORIGIN:
                    external.append("{} {} {}={}".format(rel, tag, key, attrs[key]))
    for path in sorted(SITE.rglob("*")):
        if path.is_file() and path.suffix.lower() in (".html", ".css", ".js"):
            text = path.read_text(encoding="utf-8", errors="replace")
            if "fonts.googleapis.com" in text or "fonts.gstatic.com" in text:
                font_refs.append(path.relative_to(SITE).as_posix())
    js_files = sorted((SITE / "assets/javascripts").rglob("*.js"))
    raw_js = sum(p.stat().st_size for p in js_files)
    gz_js = sum(len(gzip.compress(p.read_bytes(), 9)) for p in js_files)
    check(results, "B6'", not external and not font_refs,
          "external origins={}, google fonts={}, JS files={}, JS raw bytes={}, JS gzip bytes={}".format(
              external or "none", font_refs or "none", len(js_files), raw_js, gz_js))

    # B8: home copy, baseline CV link, baseline nav labels.
    # Spec names origin/development as the CV-link baseline, but that ref has no
    # CV link; the deployed baseline (local development / gh-pages) does.
    home_text = home["text"]
    missing_literals = [
        s for s in ("Software Development Manager at AWS", "10+") if s not in home_text
    ]
    cv_present = CV_TOKEN in home_text
    try:
        baseline_nav_text = git_show("origin/development:mkdocs.yml")
        baseline_nav = re.findall(r"^\s*-\s+([^:]+):\s+\S+\.md\s*$", baseline_nav_text, re.M)
        nav_match = set(baseline_nav) == set(NAV_LABELS) == set(home["p"].nav_labels)
        baseline_detail = "baseline nav={}".format(baseline_nav)
    except RuntimeError as exc:
        nav_match = False
        baseline_detail = str(exc)
    b8_ok = not missing_literals and cv_present and nav_match
    check(results, "B8", b8_ok,
          "literals missing={}, baseline CV link present={}, {}{}".format(
              missing_literals or "none", cv_present, baseline_detail,
              "" if cv_present else " (expected token {})".format(CV_TOKEN)))

    # B9: workflow unchanged against origin/development.
    try:
        current_wf = (ROOT / ".github/workflows/main.yml").read_bytes()
        baseline_wf = git_show("origin/development:.github/workflows/main.yml", binary=True)
        wf_ok = current_wf == baseline_wf
        wf_detail = "{} bytes current vs {} baseline".format(len(current_wf), len(baseline_wf))
    except (OSError, RuntimeError) as exc:
        wf_ok, wf_detail = False, str(exc)
    check(results, "B9", wf_ok, wf_detail)

    # S1: unique titles and descriptions, descriptions <= 160 chars.
    titles = [pg["p"].title for pg in pages.values()]
    descriptions = []
    dup_tags = []
    for rel, pg in pages.items():
        values = pg["p"].meta("description")
        if len(values) != 1:
            dup_tags.append("{}:{}".format(rel, len(values)))
        descriptions.append(values[0] if values else "")
    s1_ok = (len(set(titles)) == len(titles) and len(set(descriptions)) == len(descriptions)
             and all(len(d) <= 160 for d in descriptions) and not dup_tags)
    by_description = {}
    for rel, pg in pages.items():
        values = pg["p"].meta("description")
        if values:
            by_description.setdefault(values[0], []).append(rel)
    duplicates = {k: v for k, v in by_description.items() if len(v) > 1}
    check(results, "S1", s1_ok,
          "titles={} unique={}, descriptions={} unique={}, max length={}, duplicate descriptions={}, tag counts={}".format(
              len(titles), len(set(titles)), len(descriptions), len(set(descriptions)),
              max(map(len, descriptions)), duplicates or "none", ", ".join(dup_tags)))

    # S2: canonical on every page, posts in sitemap, robots Sitemap directive.
    no_canonical = [
        "{}:{}".format(rel, len(pg["p"].find("link", rel="canonical")))
        for rel, pg in pages.items()
        if len(pg["p"].find("link", rel="canonical")) != 1
    ]
    sitemap_path = SITE / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding="utf-8") if sitemap_path.exists() else ""
    posts_not_in_sitemap = [
        pg["url"] for pg in post_pages.values() if ORIGIN + pg["url"] not in sitemap
    ]
    robots_path = SITE / "robots.txt"
    robots_ok = robots_path.exists() and "Sitemap:" in robots_path.read_text(encoding="utf-8")
    check(results, "S2", not no_canonical and not posts_not_in_sitemap and robots_ok,
          "pages with canonical count != 1={}, posts missing from sitemap={}, robots Sitemap={}".format(
              no_canonical or "none", posts_not_in_sitemap or "none", robots_ok))

    # S3: RSS 2.0 feed, blog posts only, absolute link/guid, newest first.
    feed_path = SITE / "feed.xml"
    try:
        feed = ET.parse(str(feed_path)).getroot()
        items = feed.findall("./channel/item") if feed.tag == "rss" and feed.get("version") == "2.0" else []
        feed_bad = []
        if not items:
            feed_bad.append("no RSS 2.0 items")
        dates = []
        for item in items:
            link = (item.findtext("link") or "").strip()
            guid = (item.findtext("guid") or "").strip()
            if not link.startswith(ORIGIN + "/blog/") or not guid.startswith(ORIGIN + "/blog/"):
                feed_bad.append("non-post or relative link/guid: {}".format(link))
            try:
                dates.append(parsedate_to_datetime(item.findtext("pubDate")))
            except (TypeError, ValueError):
                feed_bad.append("bad pubDate: {}".format(item.findtext("pubDate")))
        if any(dates[i] < dates[i + 1] for i in range(len(dates) - 1)):
            feed_bad.append("items not newest first")
        s3_ok = not feed_bad
        s3_detail = "RSS 2.0 items={}, issues={}".format(len(items), feed_bad or "none")
    except (ET.ParseError, OSError) as exc:
        s3_ok, s3_detail = False, str(exc)
    check(results, "S3", s3_ok, s3_detail)

    # S4: Open Graph / Twitter card metadata on the post.
    post = next(iter(post_pages.values()), None)
    s4_bad = []
    post_meta = {}
    if post is None:
        s4_bad.append("no built blog post")
    else:
        post_meta = {k: v[0] for k, v in (
            (k, post["p"].meta(k, "property")) for k in
            ("og:title", "og:description", "og:type", "og:url", "og:image")
        ) if v}
        for key in ("og:title", "og:description", "og:type", "og:url", "og:image"):
            if not post_meta.get(key):
                s4_bad.append("missing " + key)
        if post_meta.get("og:type") != "article":
            s4_bad.append("og:type != article")
        if not absolute_or_none(post_meta.get("og:image")):
            s4_bad.append("og:image not absolute")
        if not post["p"].meta("twitter:card"):
            s4_bad.append("missing twitter:card")
    check(results, "S4", not s4_bad, "issues={}".format(s4_bad or "none"))

    # S5: exactly one BlogPosting JSON-LD block with absolute url/image and Person author.
    s5_bad = []
    if post is None:
        s5_bad.append("no built blog post")
    else:
        ld_blocks = [text for attrs, text in post["p"].scripts
                     if attrs.get("type") == "application/ld+json"]
        if len(ld_blocks) != 1:
            s5_bad.append("ld+json blocks={}".format(len(ld_blocks)))
        else:
            try:
                data = json.loads(ld_blocks[0])
                if data.get("@type") != "BlogPosting":
                    s5_bad.append("@type != BlogPosting")
                for key in ("url", "image"):
                    if not absolute_or_none(data.get(key)):
                        s5_bad.append("{} not absolute".format(key))
                author = data.get("author")
                if not isinstance(author, dict) or author.get("@type") != "Person":
                    s5_bad.append("author is not a Person")
            except ValueError as exc:
                s5_bad.append("invalid JSON: {}".format(exc))
    check(results, "S5", not s5_bad, "issues={}".format(s5_bad or "none"))

    # S6: image sizes, no profile.JPG, width+height on every img, webp srcset.
    s6_bad = []
    image_report = []
    portrait_candidates = 0
    for rel, pg in pages.items():
        for attrs in pg["p"].find("img"):
            src = attrs.get("src", "")
            if not attrs.get("width") or not attrs.get("height"):
                s6_bad.append("{} img {} missing width/height".format(rel, src))
            if "profile.JPG" in src:
                s6_bad.append("{} references profile.JPG".format(rel))
            if "portrait" in src:
                candidates = [
                    part.strip() for part in attrs.get("srcset", "").split(",")
                    if ".webp" in part
                ]
                portrait_candidates = max(portrait_candidates, len(candidates))
            sources = [src]
            sources += [
                part.strip().split()[0]
                for part in attrs.get("srcset", "").split(",") if part.strip()
            ]
            for source in sources:
                origin = absolute_or_none(source)
                if origin == ORIGIN:
                    local = SITE / urlparse(source).path.lstrip("/")
                elif origin:
                    continue  # external img is reported by B6', cannot stat locally
                else:
                    local = (pg["path"].parent / source).resolve()
                if local.is_file():
                    size = local.stat().st_size
                    image_report.append((size, local.relative_to(SITE).as_posix()))
                    if size > MAX_IMAGE_BYTES:
                        s6_bad.append("{} {} bytes exceeds {}".format(rel, size, MAX_IMAGE_BYTES))
    if portrait_candidates < 2:
        s6_bad.append("portrait srcset has {} webp candidates".format(portrait_candidates))
    largest = max(image_report) if image_report else (0, "none")
    check(results, "S6", not s6_bad,
          "issues={}, largest image={} bytes ({}), portrait webp candidates={}".format(
              s6_bad or "none", largest[0], largest[1], portrait_candidates))

    # S7: one h1 per page, focus-visible and reduced-motion in stylesheet.
    h1_bad = ["{}:{}".format(rel, len(pg["p"].find("h1")))
              for rel, pg in pages.items() if len(pg["p"].find("h1")) != 1]
    css_bad = [name for name, token in ((":focus-visible", ":focus-visible"),
                                        ("prefers-reduced-motion", "prefers-reduced-motion"))
               if token not in css]
    check(results, "S7", not h1_bad and not css_bad,
          "h1 counts={}, stylesheet missing={}".format(h1_bad or "all 1", css_bad or "none"))

    # BR1: blog index h1, at least one entry, newest first.
    blog = pages.get("blog/index.html")
    br1_bad = []
    if blog is None:
        br1_bad.append("no blog index")
    else:
        h1s = blog["p"].find("h1")
        if len(h1s) != 1 or "".join([h1s[0].get("id", "")]).lower() != "writing":
            br1_bad.append("h1 is not Writing")
        entries = blog["p"].find("article")
        if len(entries) < 1:
            br1_bad.append("no entries")
        dates = re.findall(r"<time datetime=\"([^\"]+)\"", blog["text"])
        if any(dates[i] < dates[i + 1] for i in range(len(dates) - 1)):
            br1_bad.append("entries not newest first")
    check(results, "BR1", not br1_bad,
          "issues={}, entries={}".format(br1_bad or "none",
                                         len(blog["p"].find("article")) if blog else 0))

    # BR3: post URLs have no date segment.
    post_urls = sorted(pg["url"] for pg in post_pages.values())
    bad_urls = [url for url in post_urls if not re.fullmatch(r"/blog/[a-z0-9-]+/", url)]
    check(results, "BR3", not bad_urls,
          "post URLs={}, invalid={}".format(post_urls or "none", bad_urls or "none"))

    # BR5: no built drafts and no draft slugs in sitemap/feed.
    drafts_exists = (SITE / "blog/drafts").exists()
    feed_text = feed_path.read_text(encoding="utf-8") if feed_path.exists() else ""
    leaked = [slug for slug in DRAFT_SLUGS
              if re.search(r"\b" + re.escape(slug) + r"\b", sitemap + feed_text)]
    check(results, "BR5", not drafts_exists and not leaked,
          "site/blog/drafts exists={}, leaked slugs={}".format(drafts_exists, leaked or "none"))

    for cid, ok, detail in results:
        print("{} {} {}".format("PASS" if ok else "FAIL", cid, detail))
    passed = sum(1 for _, ok, _ in results if ok)
    print("RESULT: {} PASS, {} FAIL".format(passed, len(results) - passed))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
