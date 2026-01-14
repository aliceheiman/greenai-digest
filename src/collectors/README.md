# RSS Feed Collectors

This module handles fetching articles from RSS feeds.

## Quick Start

### 1. Install feedparser

```bash
pip install feedparser
```

### 2. Add RSS Feeds

Edit [feed_sources.py](feed_sources.py) to add new RSS feeds:

```python
RSS_FEEDS = [
    ("http://export.arxiv.org/rss/cs.AI", "arXiv - AI"),
    ("https://your-feed-url.com/rss", "Your Source Name"),
    # Add more here...
]
```

### 3. Fetch Articles

Run the fetch script:

```bash
# Fetch up to 20 articles per feed (default)
python scripts/fetch_articles.py

# Fetch up to 50 articles per feed
python scripts/fetch_articles.py --max-per-feed 50
```

## Architecture

### RSSCollector Class

The main collector class that handles RSS feed parsing:

```python
from src.collectors.rss_collector import RSSCollector

# Create collector
collector = RSSCollector()

# Add feeds
collector.add_feed(
    url="http://export.arxiv.org/rss/cs.AI",
    source_name="arXiv - AI"
)

# Fetch articles
articles = collector.fetch_articles(max_per_feed=10)
```

### Article Format

Each fetched article is a dictionary with:

```python
{
    "title": str,              # Article title
    "url": str,                # Article URL (unique)
    "source": str,             # Source name (e.g., "arXiv - AI")
    "published_date": datetime,# Publication date (or None)
    "content": str,            # Article summary/description
    "authors": str             # Comma-separated author names
}
```

## Adding New RSS Feeds

### Example Sources

Here are some example RSS feeds you can add:

**arXiv (AI/ML research)**:
- Artificial Intelligence: `http://export.arxiv.org/rss/cs.AI`
- Machine Learning: `http://export.arxiv.org/rss/cs.LG`
- Computer Vision: `http://export.arxiv.org/rss/cs.CV`
- Robotics: `http://export.arxiv.org/rss/cs.RO`

**To add a new feed**:

1. Open `src/collectors/feed_sources.py`
2. Add a new tuple to `RSS_FEEDS`:
   ```python
   ("feed_url_here", "Display Name Here"),
   ```
3. Run `python scripts/fetch_articles.py`

## Features

- **Duplicate detection**: Won't re-add articles already in the database
- **Error handling**: Continues fetching even if one feed fails
- **Logging**: Detailed logs of what's being fetched
- **Extensible**: Easy to add new feeds via configuration

## Library Used

This module uses **[feedparser](https://pypi.org/project/feedparser/)** - the industry-standard Python library for parsing RSS feeds. It supports:
- RSS 0.9x, RSS 1.0, RSS 2.0
- Atom 0.3, Atom 1.0
- CDF (Channel Definition Format)

## Next Steps

After fetching articles, you'll want to:
1. Classify them into categories (future feature)
2. Score their relevancy (future feature)
3. Display them on the main page

The fetched articles will appear in your database without classifications initially.
