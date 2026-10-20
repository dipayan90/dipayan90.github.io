#!/usr/bin/env python3
"""Check internal links in a built MkDocs site. Stdlib only, no network.

Usage: check_links.py [site_dir]     (default: site)
       check_links.py --selftest

Verifies every href/src in *.html that is not external (http/https/mailto/...)
resolves to a file inside the site, and that any #fragment exists as an id/name
in the target document. External links are skipped (offline by design).
"""
import json
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from posixpath import dirname, join, normpath
from urllib.parse import unquote, urlsplit

ATTR_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
EXTERNAL_SCHEMES = ("http", "https", "mailto", "tel", "data", "javascript", "ftp")


class _IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("id", "name") and value:
                self.ids.add(value)


def _collect_ids(path):
    collector = _IdCollector()
    try:
        collector.feed(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        pass  # unreadable target is reported as missing by existence check
    return collector.ids


def check_site(root):
    """Return list of (source_page, link, reason) for broken internal links."""
    root = Path(root)
    broken = []
    id_cache = {}
    html_files = sorted(root.rglob("*.html"))

    for page in html_files:
        rel_page = page.relative_to(root).as_posix()
        text = page.read_text(encoding="utf-8", errors="replace")
        for raw in ATTR_RE.findall(text):
            url = raw.strip()
            if not url:
                continue
            parts = urlsplit(url)
            if parts.scheme and parts.scheme.lower() not in ("", "file"):
                continue  # external or special scheme
            if not parts.scheme and url.startswith("//"):
                continue  # protocol-relative external
            if not parts.path:
                target_rel = rel_page  # same-page fragment
            else:
                path = unquote(parts.path)
                if path.startswith("/"):
                    target_rel = normpath(path.lstrip("/"))
                else:
                    target_rel = normpath(join(dirname(rel_page), path))
                if target_rel == "." or target_rel == "":
                    target_rel = rel_page
                if parts.path.endswith("/"):
                    target_rel = join(target_rel, "index.html")
            target = root / target_rel
            if target.is_dir():
                target = target / "index.html"
                target_rel = target.relative_to(root).as_posix()
            if not target.is_file():
                broken.append((rel_page, url, "missing target %s" % target_rel))
                continue
            fragment = unquote(parts.fragment)
            if fragment and target.suffix == ".html":
                if target_rel not in id_cache:
                    id_cache[target_rel] = _collect_ids(target)
                if fragment not in id_cache[target_rel]:
                    broken.append((rel_page, url, "missing fragment #%s" % fragment))
    return broken


def selftest():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "sub").mkdir()
        (root / "index.html").write_text(
            '<a href="sub/page.html">ok</a>'
            '<a href="/sub/page.html">ok-root</a>'
            '<a href="missing.html">bad</a>'
            '<a href="sub/page.html#nope">bad-frag</a>'
            '<a href="https://example.com/x">ext</a>'
            '<a href="mailto:a@b.c">ext</a>'
            '<a href="sub/page.html#anchor">ok-frag</a>'
        )
        (root / "sub" / "page.html").write_text(
            '<h1 id="anchor">x</h1><img src="../img.png">'
        )
        (root / "img.png").write_bytes(b"\x89PNG")
        broken = check_site(root)
        reasons = {(s, u) for s, u, _ in broken}
        assert ("index.html", "missing.html") in reasons, broken
        assert ("index.html", "sub/page.html#nope") in reasons, broken
        assert len(broken) == 2, broken
    # no broken links -> empty
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "index.html").write_text('<a href="a.html">x</a>')
        (root / "a.html").write_text("<p>a</p>")
        assert check_site(root) == []
    print("selftest ok: catches broken target + bad fragment, passes clean site")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    root = Path(argv[1]) if len(argv) > 1 else Path("site")
    if not root.is_dir():
        print("check_links: site directory not found: %s" % root)
        return 2
    broken = check_site(root)
    for src, url, reason in broken:
        print("BROKEN %s: %s (%s)" % (src, url, reason))
    if broken:
        print("check_links: %d broken internal link(s)" % len(broken))
        return 1
    print("check_links: all internal links ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
