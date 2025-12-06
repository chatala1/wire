#!/usr/bin/env python3
"""
Fetch an RSS/Atom feed and write feed-data.json in the repository root.
Usage:
  python3 scripts/fetch_feed.py "https://feeder.co/..."
If no arg is provided, the script reads FEED_URL from the environment.
"""
import sys
import os
import json
import datetime
import feedparser
import requests
import html
from bs4 import BeautifulSoup

MAX_ITEMS = 9

def text_from_html(html_text):
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return html.unescape(text)

def fetch_raw(url):
    headers = {"User-Agent": "wire-feed-fetcher/1.0 (+https://github.com/chatala1/wire)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.content

def parse_feed(url):
    feed = feedparser.parse(url)
    if getattr(feed, 'bozo', False):
        try:
            content = fetch_raw(url)
            feed = feedparser.parse(content)
        except Exception:
            for alt in (url + '.rss', url + '.xml'):
                try:
                    feed = feedparser.parse(alt)
                    if not getattr(feed, 'bozo', False):
                        return feed
                except Exception:
                    continue
    return feed

def main():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        url = sys.argv[1].strip()
    else:
        url = os.environ.get("FEED_URL")
    if not url:
        print("Feed URL not provided. Set FEED_URL env or pass as argument.", file=sys.stderr)
        sys.exit(2)

    print(f"Fetching feed: {url}")
    try:
        feed = parse_feed(url)
    except Exception as e:
        print(f"Failed to fetch feed: {e}", file=sys.stderr)
        sys.exit(3)

    if not feed or not getattr(feed, 'entries', None):
        print("No feed entries found.", file=sys.stderr)
        sys.exit(4)

    feed_title = feed.feed.get("title", url)
    items = []
    for entry in feed.entries[:MAX_ITEMS]:
        link = entry.get("link") or entry.get("id") or ""
        title = entry.get("title", "No title")
        content_html = entry.get("summary") or (entry.get("content", [{}])[0].get("value", "") if entry.get("content") else "")
        content_text = text_from_html(content_html)
        published = entry.get("published") or entry.get("updated") or ""
        items.append({
            "title": title,
            "link": link,
            "published": published,
            "summary": content_text
        })

    out = {
        "source": feed_title,
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        "items": items
    }

    with open("feed-data.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    print(f"Wrote feed-data.json with {len(items)} items (source: {feed_title})")

if __name__ == "__main__":
    main()
