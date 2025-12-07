#!/usr/bin/env python3
"""
Fetch RSS/Atom feeds and generate feed-data.json

This script accepts a single URL or comma-separated list of feed URLs
via command line argument or FEED_URLS environment variable.
"""

import sys
import os
import json
import re
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin

try:
    import requests
    import feedparser
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error: Missing required dependency - {e}")
    print("Install dependencies: pip install feedparser requests beautifulsoup4")
    sys.exit(1)


def clean_html(html_content):
    """Extract plain text from HTML content."""
    if not html_content:
        return ""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        # Get text and clean up whitespace
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text
    except Exception as e:
        print(f"Warning: Failed to parse HTML: {e}")
        return html_content


def generate_feed_id(url):
    """Generate a simple ID from feed URL."""
    parsed = urlparse(url)
    # Use domain and path to create ID
    domain = parsed.netloc.replace('www.', '').lower()
    path = parsed.path.strip('/').replace('/', '-')
    
    # Create simple identifier - use exact domain matching or endswith for subdomains
    if domain == 'cisa.gov' or domain.endswith('.cisa.gov'):
        return 'cisa-gov'
    elif domain == 'feeder.co' or domain.endswith('.feeder.co'):
        # Extract the discovery ID if present
        match = re.search(r'/discover/([^/]+)', url)
        if match:
            return f'feeder-co-discover-{match.group(1)[:12]}'
        return 'feeder-co'
    elif domain == 'thecyberwire.com' or domain.endswith('.thecyberwire.com'):
        return 'cyberwire'
    else:
        # Generic ID from domain and path
        base_id = domain.split('.')[0] if '.' in domain else domain
        if path:
            base_id += f'-{path[:20]}'
        return base_id.replace('.', '-')


def get_bozo_error_message(feed):
    """Extract error message from feedparser bozo exception."""
    if not hasattr(feed, 'bozo') or not feed.bozo:
        return None
    exception = getattr(feed, 'bozo_exception', None)
    if exception is None:
        return 'Unknown parsing error'
    return str(exception)


def check_feed_validity(feed, context=''):
    """Check if feed is valid and print appropriate messages.
    
    Args:
        feed (feedparser.FeedParserDict): Parsed feed object from feedparser
        context (str): Optional context string to append to error messages (e.g., ' with .rss')
    
    Returns:
        bool: True if feed has entries, False otherwise
    """
    if feed.entries:
        return True
    
    bozo_msg = get_bozo_error_message(feed)
    if bozo_msg:
        print(f"  ⚠ Feed parsing had errors{context}: {bozo_msg}")
    else:
        print(f"  ⚠ Feed fetched but contains no entries{context}")
    return False


def fetch_feed_with_fallback(url, session):
    """
    Fetch feed with multiple fallback strategies.
    
    1. Try direct fetch with feedparser
    2. Try adding .rss or .xml suffix
    3. Try fetching as HTML and looking for feed links
    """
    print(f"\nFetching feed: {url}")
    
    # Strategy 1: Direct fetch
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        content = response.content
        feed = feedparser.parse(content)
        
        # Check if feed parsed successfully and has entries
        if check_feed_validity(feed):
            print(f"  ✓ Successfully parsed feed directly ({len(feed.entries)} entries)")
            return feed, url
    except Exception as e:
        print(f"  ⚠ Direct fetch failed: {e}")
    
    # Strategy 2: Try .rss and .xml suffixes
    if not url.endswith(('.rss', '.xml', '.atom')):
        for suffix in ['.rss', '.xml']:
            try_url = url.rstrip('/') + suffix
            try:
                print(f"  Trying with {suffix} suffix...")
                response = session.get(try_url, timeout=30)
                response.raise_for_status()
                
                feed = feedparser.parse(response.content)
                if check_feed_validity(feed, f' with {suffix}'):
                    print(f"  ✓ Successfully parsed with {suffix} suffix ({len(feed.entries)} entries)")
                    return feed, try_url
            except Exception as e:
                print(f"  ⚠ Failed with {suffix}: {e}")
    
    # Strategy 3: Fetch as HTML and look for feed links
    try:
        print(f"  Trying to find feed link in HTML...")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for feed links
        feed_links = soup.find_all('link', attrs={'type': ['application/rss+xml', 'application/atom+xml']})
        
        for link in feed_links:
            feed_url = link.get('href')
            if feed_url:
                # Handle relative URLs
                feed_url = urljoin(url, feed_url)
                print(f"  Found feed link: {feed_url}")
                
                try:
                    feed_response = session.get(feed_url, timeout=30)
                    feed_response.raise_for_status()
                    
                    feed = feedparser.parse(feed_response.content)
                    if check_feed_validity(feed, ' for linked feed'):
                        print(f"  ✓ Successfully parsed linked feed ({len(feed.entries)} entries)")
                        return feed, feed_url
                except Exception as e:
                    print(f"  ⚠ Failed to fetch linked feed: {e}")
    except Exception as e:
        print(f"  ⚠ HTML parsing strategy failed: {e}")
    
    print(f"  ✗ All strategies failed for {url}")
    return None, None


def extract_feed_info(feed, original_url):
    """Extract feed metadata and items."""
    # Get feed title/source
    if hasattr(feed, 'feed'):
        feed_title = feed.feed.get('title', '')
        if not feed_title:
            # Try to extract from URL
            parsed = urlparse(original_url)
            domain = parsed.netloc.lower()
            # Use exact domain matching or endswith for subdomains
            if domain == 'cisa.gov' or domain.endswith('.cisa.gov'):
                feed_title = 'CISA Cybersecurity Advisories'
            elif domain == 'feeder.co' or domain.endswith('.feeder.co'):
                feed_title = 'Feeder Discovery Feed'
            elif domain == 'thecyberwire.com' or domain.endswith('.thecyberwire.com'):
                feed_title = 'The CyberWire'
            else:
                feed_title = parsed.netloc.replace('www.', '').split('.')[0].upper()
    else:
        feed_title = 'Unknown Feed'
    
    items = []
    for entry in feed.entries[:9]:  # Limit to 9 items
        try:
            # Extract title
            title = entry.get('title', 'Untitled')
            
            # Extract link
            link = entry.get('link', '')
            if not link:
                print(f"  Warning: Entry '{title}' has no link, skipping")
                continue
            
            # Extract published date
            published = ''
            for date_field in ['published', 'updated', 'created']:
                if date_field in entry:
                    published = entry[date_field]
                    break
            
            # Extract and clean summary/description
            summary = ''
            for content_field in ['summary', 'description', 'content']:
                if content_field in entry:
                    if content_field == 'content' and isinstance(entry[content_field], list):
                        summary = entry[content_field][0].get('value', '')
                    else:
                        summary = entry[content_field]
                    break
            
            # Clean HTML from summary
            summary = clean_html(summary)
            
            items.append({
                'title': title,
                'link': link,
                'published': published,
                'summary': summary[:500] if summary else ''  # Limit summary length
            })
            
        except Exception as e:
            print(f"  Warning: Error processing entry: {e}")
            continue
    
    return {
        'source': feed_title,
        'items': items
    }


def main():
    """Main function to fetch feeds and generate JSON."""
    # Get feed URLs from command line or environment
    feed_urls_str = None
    
    if len(sys.argv) > 1:
        feed_urls_str = sys.argv[1]
    elif 'FEED_URLS' in os.environ:
        feed_urls_str = os.environ['FEED_URLS']
    
    if not feed_urls_str:
        print("Error: No feed URLs provided")
        print("Usage: python fetch_feed.py <url1,url2,...>")
        print("   or: FEED_URLS=<url1,url2,...> python fetch_feed.py")
        sys.exit(1)
    
    # Parse comma-separated URLs
    feed_urls = [url.strip() for url in feed_urls_str.split(',') if url.strip()]
    
    if not feed_urls:
        print("Error: No valid feed URLs found")
        sys.exit(1)
    
    print(f"Processing {len(feed_urls)} feed(s)...")
    
    # Create session for requests
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (compatible; FeedFetcher/1.0)'
    })
    
    feeds_data = []
    
    for url in feed_urls:
        feed, final_url = fetch_feed_with_fallback(url, session)
        
        if feed and feed.entries:
            feed_info = extract_feed_info(feed, url)
            feed_id = generate_feed_id(url)
            
            feeds_data.append({
                'id': feed_id,
                'source': feed_info['source'],
                'url': final_url or url,
                'items': feed_info['items']
            })
            print(f"  ✓ Extracted {len(feed_info['items'])} items from {feed_info['source']}")
        else:
            print(f"  ✗ Failed to fetch or parse feed: {url}")
    
    if not feeds_data:
        print("\nError: No feeds were successfully fetched")
        sys.exit(1)
    
    # Calculate total items
    total_items = sum(len(feed['items']) for feed in feeds_data)
    
    # Create output JSON
    output = {
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'feeds': feeds_data
    }
    
    # Write to feed-data.json in repository root
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'feed-data.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Successfully generated feed-data.json")
    print(f"  Total feeds: {len(feeds_data)}")
    print(f"  Total items: {total_items}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
