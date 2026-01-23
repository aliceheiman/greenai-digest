"""RSS feed collector for fetching articles from RSS feeds."""

import feedparser
from datetime import datetime
from typing import List, Dict, Optional
import logging
import re
from html.parser import HTMLParser
from html import unescape

logger = logging.getLogger(__name__)


class HTMLStripper(HTMLParser):
    """Strip HTML tags from text."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return "".join(self.text).strip()


def strip_html(html_content: str) -> str:
    """
    Remove HTML tags and decode HTML entities from content.

    Args:
        html_content: HTML string to clean

    Returns:
        Plain text with HTML tags removed
    """
    if not html_content:
        return ""

    # Remove img tags and their attributes
    html_content = re.sub(r"<img[^>]*>", "", html_content, flags=re.IGNORECASE)

    # Strip remaining HTML tags
    stripper = HTMLStripper()
    try:
        stripper.feed(html_content)
        text = stripper.get_data()
    except Exception:
        # Fallback: simple regex-based removal
        text = re.sub(r"<[^>]+>", "", html_content)

    # Decode HTML entities (e.g., &amp; -> &)
    text = unescape(text)

    # Clean up extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


class RSSCollector:
    """Collects articles from RSS feeds."""

    def __init__(self):
        """Initialize the RSS collector."""
        self.feeds = []

    def add_feed(self, url: str, source_name: str) -> None:
        """
        Add an RSS feed to collect from.

        Args:
            url: The RSS feed URL
            source_name: Display name for this source (e.g., "Nature AI", "arXiv ML")
        """
        self.feeds.append({"url": url, "source_name": source_name})
        logger.info(f"Added RSS feed: {source_name} ({url})")

    def fetch_articles(self, max_per_feed: int = 10) -> List[Dict]:
        """
        Fetch articles from all configured RSS feeds.

        Args:
            max_per_feed: Maximum number of articles to fetch per feed

        Returns:
            List of article dictionaries with keys:
                - title: Article title
                - url: Article URL
                - source: Source name
                - published_date: Publication datetime
                - content: Article description/summary
                - authors: Comma-separated author names
        """
        all_articles = []

        for feed_config in self.feeds:
            try:
                articles = self._fetch_feed(
                    feed_config["url"], feed_config["source_name"], max_per_feed
                )
                all_articles.extend(articles)
                logger.info(
                    f"Fetched {len(articles)} articles from {feed_config['source_name']}"
                )
            except Exception as e:
                logger.error(
                    f"Error fetching feed {feed_config['source_name']}: {str(e)}"
                )
                continue

        return all_articles

    def _fetch_feed(
        self, feed_url: str, source_name: str, max_articles: int
    ) -> List[Dict]:
        """
        Fetch and parse a single RSS feed.

        Args:
            feed_url: RSS feed URL
            source_name: Name of the source
            max_articles: Maximum number of articles to fetch

        Returns:
            List of parsed articles
        """
        # Parse the feed with a realistic User-Agent to avoid 403 errors
        feed = feedparser.parse(
            feed_url,
            agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        )

        # Check for errors
        if hasattr(feed, "bozo") and feed.bozo:
            logger.warning(
                f"Feed {source_name} has parsing issues: {feed.get('bozo_exception', 'Unknown error')}"
            )

        articles = []

        # Process entries
        for entry in feed.entries[:max_articles]:
            try:
                article = self._parse_entry(entry, source_name)
                if article:
                    articles.append(article)
            except Exception as e:
                logger.error(f"Error parsing entry: {str(e)}")
                continue

        return articles

    def _parse_entry(self, entry, source_name: str) -> Optional[Dict]:
        """
        Parse a single feed entry into an article dictionary.

        Args:
            entry: feedparser entry object
            source_name: Name of the source

        Returns:
            Article dictionary or None if parsing fails
        """
        # Extract title (required)
        title = entry.get("title", "").strip()
        if not title:
            return None

        # Extract URL (required)
        url = entry.get("link", "").strip()
        if not url:
            return None

        # Extract publication date
        published_date = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                published_date = datetime(*entry.published_parsed[:6])
            except Exception:
                pass

        # If no published date, try updated date
        if (
            not published_date
            and hasattr(entry, "updated_parsed")
            and entry.updated_parsed
        ):
            try:
                published_date = datetime(*entry.updated_parsed[:6])
            except Exception:
                pass

        # Extract content/summary
        content = ""
        if hasattr(entry, "summary"):
            content = entry.summary
        elif hasattr(entry, "description"):
            content = entry.description
        elif hasattr(entry, "content") and len(entry.content) > 0:
            content = entry.content[0].get("value", "")

        # Clean HTML from content
        content = strip_html(content)
        authors = ""
        if hasattr(entry, "authors"):
            authors = ", ".join([author.get("name", "") for author in entry.authors])
        elif hasattr(entry, "author"):
            authors = entry.author

        return {
            "title": title,
            "url": url,
            "source": source_name,
            "published_date": published_date,
            "content": content,
            "authors": authors or "Unknown",
        }


# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Example: Create collector and add a feed
    collector = RSSCollector()
    collector.add_feed(
        "http://export.arxiv.org/rss/cs.AI", "arXiv - Artificial Intelligence"
    )

    # Fetch articles
    articles = collector.fetch_articles(max_per_feed=5)

    # Display results
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
        print(f"Published: {article['published_date']}")
        print(f"Authors: {article['authors']}")
        print(f"Content preview: {article['content'][:100]}...")
