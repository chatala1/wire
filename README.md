# Wire - Multi-Feed Cybersecurity Aggregator

A dark-themed GitHub Pages site that displays cybersecurity advisories and threat intelligence from multiple RSS/Atom feeds in a clean, responsive grid layout.

## Features

- **Dark Theme**: Clean black background with contrasting white text
- **Multiple Feeds**: Aggregates content from multiple sources, each displayed in its own section
- **Responsive Grid Layout**: 3-column grid on desktop, adapts to 2 columns on tablets and 1 column on mobile
- **Auto-Updates**: Feeds are automatically fetched and updated twice daily (6 AM and 6 PM UTC)
- **Navigation Bar**: Simple navigation with title on the left and section links on the right
- **RSS Integration**: Displays the 9 most recent items from https://feeder.co/discover/18fedcbe1e/cisa-gov (CISA cybersecurity advisories via Feeder)

## Setup

1. Enable GitHub Pages in repository settings:
   - Go to Settings > Pages
   - Set Source to "Deploy from a branch"
   - Select branch: `main` or `master`
   - Select folder: `/ (root)`

2. The GitHub Action will automatically run:
   - Twice daily at 6 AM and 6 PM UTC
   - Can be manually triggered from the Actions tab
   - Fetches feed data using scripts/fetch_feed.py and generates feed-data.json

## Technology Stack

- **Pure HTML/CSS/JavaScript**: No build process required
- **Python Script**: `scripts/fetch_feed.py` for feed fetching and parsing
- **GitHub Actions**: Automated feed updates
- **GitHub Pages**: Static site hosting

## Local Development

1. Open `index.html` in a web browser to view the site
2. To test feed fetching locally:
   ```bash
   # Create a virtual environment (optional)
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install feedparser requests beautifulsoup4
   
   # Run the script
   python3 scripts/fetch_feed.py "https://www.cisa.gov/cybersecurity-advisories/all.xml,https://feeder.co/discover/18fedcbe1e/cisa-gov"
   
   # Or use environment variable
   FEED_URLS="https://example.com/feed1.xml,https://example.com/feed2.rss" python3 scripts/fetch_feed.py
   ```
3. Inspect the generated `feed-data.json` file to verify the output