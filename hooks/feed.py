"""Write site/feed.xml (RSS 2.0) from the blog posts.

Only pages under docs/blog/posts/ with a `date` in front matter are collected.
Drafts are already removed by `draft_docs`, so they never reach on_page_context.
"""

import html
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path

POST_PREFIX = "blog/posts/"
FALLBACK_SITE_URL = "https://dipayan90.github.io"
FEED_NAME = "feed.xml"

_posts = []


def on_pre_build(config=None, **kwargs):
    _posts.clear()


def _as_datetime(value):
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, date):
        return datetime.combine(value, time.min, tzinfo=timezone.utc)
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.strip())
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


def on_page_context(context, page=None, config=None, **kwargs):
    if page is None or not page.file.src_uri.startswith(POST_PREFIX):
        return context
    published = _as_datetime(page.meta.get("date"))
    if published is None:
        return context
    site = (config.site_url or FALLBACK_SITE_URL).rstrip("/")
    _posts.append({
        "title": page.meta.get("title") or page.title or config.site_name,
        "date": published,
        "description": page.meta.get("description") or "",
        "url": page.canonical_url or site + "/" + page.url.lstrip("/"),
    })
    return context


def _item(post):
    return (
        "<item>"
        "<title>%s</title>"
        "<link>%s</link>"
        '<guid isPermaLink="true">%s</guid>'
        "<pubDate>%s</pubDate>"
        "<description>%s</description>"
        "</item>"
    ) % (
        html.escape(post["title"]),
        html.escape(post["url"]),
        html.escape(post["url"]),
        format_datetime(post["date"]),
        html.escape(post["description"]),
    )


def on_post_build(config=None, **kwargs):
    if config is None:
        return
    site = (config.site_url or FALLBACK_SITE_URL).rstrip("/")
    feed_url = site + "/" + FEED_NAME
    items = "".join(
        _item(post) for post in sorted(_posts, key=lambda post: post["date"], reverse=True)
    )
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<rss version="2.0">\n'
        "<channel>\n"
        "<title>%s</title>\n"
        "<link>%s</link>\n"
        "<description>%s</description>\n"
        "<language>en</language>\n"
        "<lastBuildDate>%s</lastBuildDate>\n"
        "%s\n"
        "</channel>\n"
        "</rss>\n"
    ) % (
        html.escape(config.site_name),
        html.escape(feed_url),
        html.escape(config.site_description or config.site_name),
        format_datetime(datetime.now(timezone.utc)),
        items,
    )
    target = Path(config.site_dir) / FEED_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(xml, encoding="utf-8")
