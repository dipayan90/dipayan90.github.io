"""MkDocs hook for the static "Ask about Dipayan" Q&A (KAJ-19).

The corpus lives in qa/entries.json at the repo root, deliberately outside docs/ so it
is never published as a page. This hook is the only place that turns the corpus into
published artefacts:

  * site/qa.json  -> fetched by the client-side search widget
  * docs/ask.md   -> the no-JavaScript <details> fallback is injected at the marker

Both come from the same source of truth, so they can never drift apart.
"""

import html
import json
from pathlib import Path

FALLBACK_MARKER = "<!-- QA_FALLBACK -->"
ENTRIES_PATH = Path("qa") / "entries.json"

# Whitelisted source pages -> (nav label, url relative to the /ask/ page).
SOURCES = {
    "docs/index.md": ("Home", ".."),
    "docs/summary.md": ("About Me", "../summary/"),
    "docs/experience.md": ("Experience", "../experience/"),
    "docs/opensource.md": ("Projects", "../opensource/"),
    "docs/skills.md": ("Skills & Expertise", "../skills/"),
    "docs/miscellaneous.md": ("Personal", "../miscellaneous/"),
}


def _entries(config):
    path = Path(config.config_file_path).resolve().parent / ENTRIES_PATH
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)["entries"]


def _published(entry):
    """Corpus entry plus the display metadata the widget needs."""
    label, url = SOURCES[entry["source"]]
    published = dict(entry)
    published["sourceLabel"] = label
    published["sourceUrl"] = url
    return published


def _fallback_html(entries):
    parts = ['<section id="qa-fallback" class="qa-fallback">']
    parts.append('<p class="qa-fallback-note">Every answer below comes from a page of this site.</p>')
    for entry in entries:
        label, url = SOURCES[entry["source"]]
        parts.append('<details class="qa-item">')
        parts.append("<summary>%s</summary>" % html.escape(entry["q"]))
        parts.append('<p class="qa-a">%s</p>' % html.escape(entry["a"]))
        parts.append('<p class="qa-source">Source: <a href="%s">%s</a></p>' % (url, html.escape(label)))
        parts.append("</details>")
    parts.append("</section>")
    return "\n".join(parts)


def on_page_markdown(markdown, page=None, config=None, files=None, **kwargs):
    if page is None or config is None or page.file.src_uri != "ask.md":
        return markdown
    if FALLBACK_MARKER not in markdown:
        raise RuntimeError("docs/ask.md is missing the %s marker" % FALLBACK_MARKER)
    return markdown.replace(FALLBACK_MARKER, _fallback_html(_entries(config)))


def on_post_build(config=None, **kwargs):
    if config is None:
        return
    entries = _entries(config)
    target = Path(config.site_dir) / "qa.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump({"version": 1, "entries": [_published(e) for e in entries]}, handle,
                  indent=2, ensure_ascii=False)
        handle.write("\n")
