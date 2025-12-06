# Wire - CISA Cybersecurity Advisories Feed

A dark-themed GitHub Pages site that displays the 9 most recent CISA cybersecurity advisories in a 3-wide grid layout.

## Features

- **Dark Theme**: Clean black background with contrasting white text
- **Responsive Grid Layout**: 3-column grid on desktop, adapts to 2 columns on tablets and 1 column on mobile
- **Auto-Updates**: RSS feed is automatically fetched and updated twice daily (6 AM and 6 PM UTC)
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
- **GitHub Actions**: Official integration for automated feed updates
- **GitHub Pages**: Official static site hosting

## Local Development

Simply open `index.html` in a web browser. Note that the feed data will only be available after the GitHub Action has run at least once.