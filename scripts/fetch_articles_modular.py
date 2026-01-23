"""Fetch articles from configured RSS feeds and store in database.

This module can be run:
1. Standalone: python scripts/fetch_articles.py
2. Via APScheduler: scheduler calls this function
3. Via GitHub Actions: workflow calls this script
4. Via Railway: manual or scheduled execution
"""

import sys
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import get_session, Article, Classification
from src.collectors.rss_collector import RSSCollector
from src.collectors.feed_sources import get_all_feeds
from src.collectors.relevance_filter import calculate_relevance

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_and_store_articles(max_per_feed=20):
    """
    Fetch articles from RSS feeds and store in database.

    This is the core function that can be called from:
    - APScheduler (background job)
    - GitHub Actions (scheduled workflow)
    - Railway CLI (manual execution)
    - Command line (direct script execution)

    Args:
        max_per_feed: Maximum articles per feed to fetch
    """
    logger.info("🔄 Starting article fetch...")

    try:
        # Initialize collector
        collector = RSSCollector()
        feeds = get_all_feeds()
        always_include_sources = set()

        # Add feeds and track always-include sources
        for feed_data in feeds:
            url, source_name = feed_data[0], feed_data[1]
            always_include = feed_data[2] if len(feed_data) > 2 else False
            collector.add_feed(url, source_name)
            if always_include:
                always_include_sources.add(source_name)

        logger.info(f"Configured {len(feeds)} RSS feeds")

        # Fetch articles
        articles = collector.fetch_articles(max_per_feed=max_per_feed)
        logger.info(f"Fetched {len(articles)} articles")

        # Store in database
        session = get_session()
        new_count = 0
        duplicate_count = 0
        filtered_count = 0

        for article_data in articles:
            # Check if already exists
            existing = session.query(Article).filter_by(url=article_data["url"]).first()
            if existing:
                duplicate_count += 1
                continue

            # Check if source should bypass filtering
            source_always_included = article_data["source"] in always_include_sources

            # Classify article
            classification_data = calculate_relevance(
                article_data["title"], article_data["content"]
            )

            # Skip if not classified and not auto-included
            if not classification_data and not source_always_included:
                filtered_count += 1
                continue

            # Create article
            article = Article(
                title=article_data["title"],
                url=article_data["url"],
                source=article_data["source"],
                published_date=article_data.get("published_date"),
                content=article_data.get("content"),
                summary=article_data.get("summary"),
                authors=article_data.get("authors"),
            )
            session.add(article)
            session.flush()

            # Create classification if available
            if classification_data:
                classification = Classification(
                    article_id=article.id,
                    category=classification_data["category"],
                    confidence=classification_data.get("confidence", 0),
                    relevancy_score=classification_data.get("relevancy_score", 0),
                    tags=", ".join(classification_data.get("tags", [])),
                )
                session.add(classification)

            new_count += 1

        session.commit()
        session.close()

        logger.info(
            f"✓ Fetch complete: {new_count} new, {duplicate_count} duplicates, {filtered_count} filtered"
        )
        return {
            "new": new_count,
            "duplicate": duplicate_count,
            "filtered": filtered_count,
        }

    except Exception as e:
        logger.error(f"✗ Error fetching articles: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch articles from RSS feeds")
    parser.add_argument(
        "--max-per-feed",
        type=int,
        default=20,
        help="Maximum articles to fetch per feed (default: 20)",
    )

    args = parser.parse_args()

    try:
        result = fetch_and_store_articles(max_per_feed=args.max_per_feed)
        print(f"\nFetch Summary:")
        print(f"  New articles: {result['new']}")
        print(f"  Duplicates: {result['duplicate']}")
        print(f"  Filtered: {result['filtered']}")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
