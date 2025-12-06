# GitHub Pages Setup Guide

This guide will help you enable GitHub Pages for the Wire project and configure the multi-feed updater.

## Step 1: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/chatala1/wire`
2. Click on **Settings** (in the top menu)
3. In the left sidebar, click on **Pages**
4. Under **Build and deployment**:
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `main` (or `master` if that's your default branch)
   - **Folder**: Select `/ (root)`
5. Click **Save**

## Step 2: Wait for Deployment

GitHub Pages will automatically build and deploy your site. This usually takes 1-2 minutes.

You can monitor the deployment:
1. Go to the **Actions** tab in your repository
2. You'll see a workflow called "pages build and deployment"
3. Once it shows a green checkmark, your site is live!

## Step 3: Access Your Site

Your site will be available at:
```
https://chatala1.github.io/wire/
```

## Step 4: Trigger the Feed Update

The feed updates automatically twice daily (6 AM and 6 PM UTC), but you can trigger it manually for the first time:

1. Go to the **Actions** tab
2. Click on "Update RSS Feed" in the left sidebar
3. Click the **Run workflow** dropdown button
4. Click the green **Run workflow** button

This will fetch the latest CISA cybersecurity advisories from https://feeder.co/discover/18fedcbe1e/cisa-gov and populate the `feed-data.json` file.

## Automatic Updates

Once set up, the site will automatically:
- Update the RSS feed twice daily at 6 AM and 6 PM UTC using `scripts/fetch_feed.py`
- Fetch feed data from https://feeder.co/discover/18fedcbe1e/cisa-gov
- Commit the new feed-data.json to the repository
- Display the 9 most recent CISA cybersecurity advisories

## Troubleshooting

### Site Not Loading
- Verify that GitHub Pages is enabled in Settings > Pages
- Check that the branch and folder are correctly selected
- Wait a few minutes for the initial deployment

### Feed Not Updating
- Check the Actions tab for any failed workflows
- Review workflow logs to identify which feed(s) failed to fetch
- Verify that feed URLs are accessible and valid RSS/Atom feeds
- Manually trigger the "Update RSS Feed" workflow
- Verify that the workflow has write permissions (see below)

### Feed URL Issues
If a feed fails to parse:
- Verify the URL is a direct RSS/Atom feed, not an HTML page
- Check if the feed requires authentication or special headers
- For Feeder discovery pages, try to find the raw RSS export URL
- Test the URL locally using the fetch_feed.py script

### Workflow Permission Issues
If the workflow fails with permission errors:
1. Go to Settings > Actions > General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click Save

### Script Errors
If the Python script fails:
- Check that all dependencies are installed (feedparser, requests, beautifulsoup4)
- Verify Python version is 3.6+ (GitHub Actions uses 3.x by default)
- Review the workflow logs for specific error messages
- Test locally to debug issues

## Custom Domain (Optional)

To use a custom domain:
1. Go to Settings > Pages
2. Enter your custom domain in the "Custom domain" field
3. Follow GitHub's instructions to configure DNS records
