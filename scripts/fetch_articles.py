"""Fetch articles from RSS feeds and store them in the database."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.collectors.rss_collector import RSSCollector
from src.collectors.feed_sources import get_all_feeds
from src.collectors.relevance_filter import calculate_relevance
from src.database import get_session, Article, Classification
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fetch_and_store_articles(max_per_feed: int = 20):
    """
    Fetch articles from all RSS feeds and store them in the database.

    Args:
        max_per_feed: Maximum number of articles to fetch per feed
    """
    logger.info("Starting article collection...")

    # Initialize collector
    collector = RSSCollector()

    # Add all configured feeds and track which sources should always be included
    feeds = get_all_feeds()
    always_include_sources = set()

    for feed_data in feeds:
        url, source_name = feed_data[0], feed_data[1]
        always_include = feed_data[2] if len(feed_data) > 2 else False

        collector.add_feed(url, source_name)
        if always_include:
            always_include_sources.add(source_name)

    logger.info(f"Configured {len(feeds)} RSS feed(s)")
    logger.info(f"  - Always include (no filtering): {len(always_include_sources)}")
    logger.info(f"  - Filtered sources: {len(feeds) - len(always_include_sources)}")

    # Fetch articles
    articles = collector.fetch_articles(max_per_feed=max_per_feed)
    logger.info(f"Fetched {len(articles)} total articles")

    if not articles:
        logger.warning("No articles fetched. Exiting.")
        return

    # Store in database
    session = get_session()
    new_count = 0
    duplicate_count = 0
    filtered_count = 0

    for article_data in articles:
        # Check if article already exists (by URL)
        existing = session.query(Article).filter_by(url=article_data["url"]).first()

        if existing:
            duplicate_count += 1
            logger.debug(f"Skipping duplicate: {article_data['title']}")
            continue

        # Check if this source should always be included (skip filtering)
        source_always_included = article_data["source"] in always_include_sources

        if source_always_included:
            # Auto-classify based on content for always-included sources
            classification_data = calculate_relevance(
                article_data["title"],
                article_data["content"]
            )
            # If no strong classification match, skip the article
            # (don't force everything into Green AI)
            if not classification_data:
                filtered_count += 1
                logger.debug(f"Skipped (always-include source but no category match): {article_data['title']}")
                continue
        else:
            # Check relevance using keyword filter for other sources
            classification_data = calculate_relevance(
                article_data["title"],
                article_data["content"]
            )

            if not classification_data:
                filtered_count += 1
                logger.debug(f"Filtered out (not relevant): {article_data['title']}")
                continue

        # Create new article
        article = Article(
            title=article_data["title"],
            url=article_data["url"],
            source=article_data["source"],
            published_date=article_data["published_date"],
            content=article_data["content"],
            authors=article_data["authors"]
        )

        session.add(article)
        session.flush()  # Get article.id

        # Create classification
        classification = Classification(
            article_id=article.id,
            category=classification_data["category"],
            confidence=classification_data["confidence"],
            relevancy_score=classification_data["relevancy_score"],
            tags=""  # Can add tag extraction later
        )

        session.add(classification)
        new_count += 1
        logger.info(
            f"Added: {article.title} [{classification_data['category']}] "
            f"(relevancy: {int(classification_data['relevancy_score'])})"
        )

    # Commit changes
    session.commit()
    session.close()

    logger.info(f"\n✓ Collection complete!")
    logger.info(f"  - New articles added: {new_count}")
    logger.info(f"  - Filtered out (not relevant): {filtered_count}")
    logger.info(f"  - Duplicates skipped: {duplicate_count}")
    logger.info(f"  - Total fetched: {len(articles)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch articles from RSS feeds")
    parser.add_argument(
        "--max-per-feed",
        type=int,
        default=20,
        help="Maximum articles to fetch per feed (default: 20)"
    )

    args = parser.parse_args()

    fetch_and_store_articles(max_per_feed=args.max_per_feed)
