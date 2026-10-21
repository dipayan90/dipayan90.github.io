#!/usr/bin/env python3
"""Acceptance checks for the static "Ask about Dipayan" Q&A feature.

Usage: python scripts/check_qa.py [site_dir]

Checks:
  1. qa/entries.json holds 25-40 entries citing only whitelisted source pages.
  2. Every number used in an answer appears verbatim in FACTS.md.
  3. site/qa.json was generated from qa/entries.json.
  4. site/ask/index.html carries both the no-JavaScript fallback and the widget.
  5. The feature adds less than 100 KB to the published site.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ENTRIES_FILE = REPO / "qa" / "entries.json"
FACTS_FILE = REPO / "FACTS.md"
SOURCES = {
    "docs/index.md",
    "docs/summary.md",
    "docs/experience.md",
    "docs/opensource.md",
    "docs/skills.md",
    "docs/miscellaneous.md",
}
MIN_ENTRIES = 25
MAX_ENTRIES = 40
MAX_WEIGHT_BYTES = 100 * 1024
NUMBER = re.compile(r"(?<![A-Za-z])\d[\d,]*(?:\.\d+)?%?\+?")

failures = []


def check(condition, message):
    print(("PASS  " if condition else "FAIL  ") + message)
    if not condition:
        failures.append(message)


def main():
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")

    check(ENTRIES_FILE.is_file(), "qa/entries.json exists")
    check(FACTS_FILE.is_file(), "FACTS.md exists")
    if failures:
        return 1

    entries = json.loads(ENTRIES_FILE.read_text(encoding="utf-8"))["entries"]
    facts = FACTS_FILE.read_text(encoding="utf-8")

    check(MIN_ENTRIES <= len(entries) <= MAX_ENTRIES,
          "corpus holds %d entries (allowed %d-%d)" % (len(entries), MIN_ENTRIES, MAX_ENTRIES))
    check(len({entry["id"] for entry in entries}) == len(entries), "entry ids are unique")
    check(all(entry["source"] in SOURCES for entry in entries),
          "every entry cites a whitelisted source page")
    check({entry["source"] for entry in entries} == SOURCES, "all six source pages are used")
    check(all(entry["q"] and entry["a"] and entry["keywords"] for entry in entries),
          "every entry has a question, an answer and keywords")

    untraceable = ["%s: %s" % (entry["id"], token)
                   for entry in entries for token in NUMBER.findall(entry["a"])
                   if token not in facts]
    check(not untraceable,
          "every number in every answer appears verbatim in FACTS.md"
          + (" -> " + ", ".join(untraceable) if untraceable else ""))

    qa_json = site / "qa.json"
    check(qa_json.is_file(), "site/qa.json was generated")
    if qa_json.is_file():
        published = json.loads(qa_json.read_text(encoding="utf-8"))["entries"]
        published_core = [(e["id"], e["q"], e["a"], e["source"]) for e in published]
        corpus_core = [(e["id"], e["q"], e["a"], e["source"]) for e in entries]
        check(published_core == corpus_core, "site/qa.json matches qa/entries.json")

    ask_page = site / "ask" / "index.html"
    check(ask_page.is_file(), "site/ask/index.html was generated")
    ask_html = ask_page.read_text(encoding="utf-8") if ask_page.is_file() else ""
    check(ask_html.count('class="qa-item"') == len(entries),
          "no-JavaScript fallback lists all %d answers" % len(entries))
    check('id="qa-widget"' in ask_html and "id=\"qa-input\"" in ask_html,
          "search widget markup is present")
    check("assets/javascripts/ask.js" in ask_html, "the widget script is loaded by the page")

    fallback = re.search(r'<section id="qa-fallback".*?</section>', ask_html, re.S)
    weight = len(qa_json.read_bytes() if qa_json.is_file() else b"")
    weight += len((site / "assets" / "javascripts" / "ask.js").read_bytes()) \
        if (site / "assets" / "javascripts" / "ask.js").is_file() else 0
    weight += len(fallback.group(0).encode("utf-8")) if fallback else 0
    check(weight < MAX_WEIGHT_BYTES,
          "feature adds %d bytes, under the %d byte budget" % (weight, MAX_WEIGHT_BYTES))

    node = shutil.which("node")
    if node:
        result = subprocess.run([node, str(REPO / "scripts" / "test_ask.js")],
                                capture_output=True, text=True)
        output = (result.stdout + result.stderr).strip()
        check(result.returncode == 0, "widget behaviour test passes"
              + ("" if result.returncode == 0 else " -> " + output))
    else:
        print("SKIP  widget behaviour test (node is not installed)")

    print("")
    if failures:
        print("%d check(s) failed" % len(failures))
        return 1
    print("All Q&A checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
