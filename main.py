"""Main FastHTML application."""

from fasthtml.common import *
from monsterui.all import *
from src.database import get_session, Article, Classification
from src.collectors.feed_sources import get_all_feeds
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

# Create FastHTML app with link to external CSS
app, rt = fast_app(hdrs=(Link(rel="stylesheet", href="/static/styles.css"),))

# Initialize scheduler (optional - can be disabled by setting DISABLE_SCHEDULER=true)
if os.getenv("DISABLE_SCHEDULER", "false").lower() != "true":
    try:
        from src.scheduler import create_scheduler
        from scripts.fetch_articles_modular import fetch_and_store_articles

        # Create and start scheduler
        scheduler = create_scheduler(
            fetch_function=fetch_and_store_articles,
            hour=int(os.getenv("FETCH_HOUR", "2")),
            minute=int(os.getenv("FETCH_MINUTE", "0")),
        )
        logger.info("✓ Article fetching scheduler enabled")
    except Exception as e:
        logger.warning(
            f"⚠ Scheduler initialization failed: {e}. Continuing without scheduled fetching."
        )
else:
    logger.info("ℹ Article fetching scheduler disabled (DISABLE_SCHEDULER=true)")


def get_category_class(category):
    """Return custom CSS class for different categories."""
    styles = {
        "AI for Medicine": "category-medicine",
        "Green AI": "category-green-ai",
        "AI for Planet": "category-planet",
    }
    return styles.get(category, "category-default")


def NavBar():
    return Div(
        Div(
            # Brand
            Div(A("🌱 GreenAI Digest", href="/"), cls="nav-brand"),
            # Nav links
            Div(
                A("About", href="/about", cls="nav-link"),
                # A("Archive", href="/archive", cls="nav-link"),
                style="display: flex; gap: 0.5rem; align-items: center;",
            ),
            style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; padding: 1.5rem 2rem;",
        ),
        style="background: white; border-bottom: 1px solid #e5e5e5; margin-bottom: 2rem;",
    )


def ArticleCard(article, classification=None):
    """Component to display an article card with custom styling."""
    # Format published date
    date_str = (
        article.published_date.strftime("%b %d, %Y")
        if article.published_date
        else "No date"
    )

    # Get relevancy score and category
    relevancy = classification.relevancy_score if classification else 0
    category = classification.category if classification else "Uncategorized"
    tags = (
        classification.tags.split(",") if classification and classification.tags else []
    )

    return Div(
        # Header row with title and category badge
        Div(
            Div(
                H4(article.title, style="margin: 0 0 0.5rem 0;"),
                P(
                    f"{article.source} • {date_str}",
                    style="margin: 0; font-size: 0.9rem; color: var(--text-light);",
                ),
                style="flex: 1;",
            ),
            Span(category, cls=get_category_class(category)),
            style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;",
        ),
        # Summary text
        P(
            article.summary
            or (
                article.content[:200] + "..."
                if article.content
                else "No summary available"
            ),
            style="color: var(--text-medium); line-height: 1.6; margin-bottom: 1rem;",
        ),
        # Tags row
        (
            Div(
                *[Span(tag.strip(), cls="tag-badge") for tag in tags[:5]],
                style="margin-bottom: 1rem; display: flex; flex-wrap: wrap; gap: 0.5rem;",
            )
            if tags
            else None
        ),
        # Footer with relevancy and button
        Div(
            # (
            #     Span(f"Relevancy: {int(relevancy)}/100", cls="relevancy-badge")
            #     if classification
            #     else None
            # ),
            A("Read Article →", href=article.url, target="_blank", cls="btn-primary"),
            style="display: flex; justify-content: space-between; align-items: center;",
        ),
        cls="article-card",
    )


@rt("/")
def index(category: str = None, offset: int = 0):
    """Home page - Daily digest of articles."""
    session = get_session()

    per_page = 10

    # Get all articles with their classifications, ordered by latest first
    query = session.query(Article).join(Classification)

    # Apply category filter if specified
    if category and category != "All":
        query = query.filter(Classification.category == category)

    # Get articles with offset and check if there are more
    articles = (
        query.order_by(Article.published_date.desc())
        .offset(offset)
        .limit(per_page)
        .all()
    )

    # Check if there are more articles
    total_count = query.count()
    has_more = (offset + per_page) < total_count

    # If no articles, show empty state
    if not articles:
        content = Section(
            Center(
                DivVStacked(
                    UkIcon("inbox", height=64, width=64),
                    H3("No Articles Yet"),
                    Subtitle(
                        "Articles will appear here once they're collected and classified."
                    ),
                    Button("Learn More", cls=ButtonT.primary, href="/about"),
                    cls="space-y-4",
                ),
                cls="h-96",
            ),
            cls=SectionT.muted,
        )
    else:
        # Display article cards
        article_cards = []
        for article in articles:
            classification = (
                article.classifications[0] if article.classifications else None
            )
            article_cards.append(ArticleCard(article, classification))

        # Category filter buttons
        all_categories = ["All", "AI for Medicine", "AI for Planet", "Green AI"]
        current_category = category or "All"

        filter_buttons = Div(
            *[
                A(
                    cat,
                    href=f"/?category={cat}" if cat != "All" else "/",
                    cls=get_category_class(cat) if cat != "All" else "category-default",
                    style=f"padding: 0.5rem 1rem; text-decoration: none; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 500; {'opacity: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.1);' if cat == current_category else 'opacity: 0.6;'}",
                )
                for cat in all_categories
            ],
            style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem;",
        )

        content = Div(
            # Header section
            Div(
                H2("Daily Digest", style="margin: 0 0 0.5rem 0;"),
                P(
                    f"Latest {len(articles)} articles • {datetime.now().strftime('%B %d, %Y')}",
                    style="color: var(--text-light); font-size: 1rem; margin: 0;",
                ),
                style="margin-bottom: 1.5rem;",
            ),
            # Category filter
            filter_buttons,
            # Article cards
            Div(*article_cards),
            # Pagination buttons
            (
                Div(
                    # Previous button
                    (
                        A(
                            "← Previous Page",
                            href=(
                                f"/?category={category}&offset={max(0, offset - per_page)}"
                                if category
                                else f"/?offset={max(0, offset - per_page)}"
                            ),
                            cls="btn-primary",
                            style="padding: 0.75rem 1.5rem; text-decoration: none; display: inline-block; text-align: center;",
                        )
                        if offset > 0
                        else None
                    ),
                    # Next button
                    (
                        A(
                            "Next Page →",
                            href=(
                                f"/?category={category}&offset={offset + per_page}"
                                if category
                                else f"/?offset={offset + per_page}"
                            ),
                            cls="btn-primary",
                            style="padding: 0.75rem 1.5rem; text-decoration: none; display: inline-block; text-align: center;",
                        )
                        if has_more
                        else None
                    ),
                    style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;",
                )
                if (offset > 0 or has_more)
                else None
            ),
        )

    session.close()

    # Custom Navigation bar

    return Title("GreenAI Digest - Daily News"), Div(
        NavBar(),
        Div(content, style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;"),
    )


@rt("/archive")
def archive():
    """Archive page - Search and filter all articles."""
    return Title("Archive"), Div(
        NavBar(),
        Div(
            H2("Archive", style="margin: 0 0 0.5rem 0;"),
            P(
                "Search and filter all articles",
                style="color: var(--text-light); margin-bottom: 2rem;",
            ),
            P("Coming soon!", style="color: var(--text-medium);"),
            style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;",
        ),
    )


@rt("/about")
def about():
    """About page."""
    # Get all feed sources
    feeds = get_all_feeds()

    # Create table rows for each feed
    feed_rows = []
    for url, name, always_include in feeds:
        feed_rows.append(
            Tr(
                Td(name, style="padding: 0.75rem; border-bottom: 1px solid #e5e5e5;"),
                Td(
                    A(
                        url,
                        href=url,
                        target="_blank",
                        style="color: var(--green-primary); text-decoration: none;",
                    ),
                    style="padding: 0.75rem; border-bottom: 1px solid #e5e5e5; word-break: break-all;",
                ),
                Td(
                    "Always Include" if always_include else "Filtered",
                    style=f"padding: 0.75rem; border-bottom: 1px solid #e5e5e5; color: {'var(--green-primary)' if always_include else 'var(--text-medium)'};",
                ),
            )
        )

    return Title("About - GreenAI Digest"), Div(
        NavBar(),
        Div(
            H2("About GreenAI Digest", style="margin: 0 0 0.5rem 0;"),
            P(
                "AI Research Focused on Human and Planetary Health",
                style="color: var(--text-light); margin-bottom: 2rem;",
            ),
            P(
                "GreenAI Digest is a news aggregation and curation system focused on AI research with environmental and medical impact.",
                style="margin-bottom: 1rem; line-height: 1.6;",
            ),
            P(
                "We automatically collect, classify, and score articles based on their relevance to:",
                style="margin-bottom: 0.5rem; line-height: 1.6;",
            ),
            Ul(
                Li("AI for Medicine - Lesion detection, diagnostic imaging"),
                Li("AI for Planet - Climate modeling, biodiversity monitoring"),
                Li("Green AI - Model efficiency, sustainable computing"),
                style="margin-left: 2rem; line-height: 1.8; margin-bottom: 3rem;",
            ),
            # Data Sources section
            H3("Data Sources", style="margin: 2rem 0 1rem 0;"),
            P(
                "We collect articles from the following high-quality sources:",
                style="color: var(--text-medium); margin-bottom: 1rem;",
            ),
            Div(
                Table(
                    Thead(
                        Tr(
                            Th(
                                "Source",
                                style="padding: 0.75rem; border-bottom: 2px solid var(--green-primary); text-align: left; font-weight: 600;",
                            ),
                            Th(
                                "RSS Feed URL",
                                style="padding: 0.75rem; border-bottom: 2px solid var(--green-primary); text-align: left; font-weight: 600;",
                            ),
                            Th(
                                "Type",
                                style="padding: 0.75rem; border-bottom: 2px solid var(--green-primary); text-align: left; font-weight: 600;",
                            ),
                        )
                    ),
                    Tbody(*feed_rows),
                    style="width: 100%; border-collapse: collapse; background: white; border-radius: 0.5rem; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);",
                ),
                style="overflow-x: auto; margin-bottom: 2rem;",
            ),
            P(
                '"Always Include" sources have all articles included without filtering. "Filtered" sources are checked for relevance to our focus areas.',
                style="color: var(--text-light); font-size: 0.875rem; font-style: italic;",
            ),
            # Methods section
            H3("Methods", style="margin: 3rem 0 1rem 0;"),
            P(
                "Our article collection and classification pipeline consists of four main stages:",
                style="color: var(--text-medium); margin-bottom: 1.5rem;",
            ),
            # Stage 1
            Div(
                H4(
                    "1. RSS Feed Collection",
                    style="color: var(--green-primary); margin: 0 0 0.5rem 0;",
                ),
                P(
                    "Articles are collected from RSS feeds using the feedparser library. Each feed entry is parsed to extract:",
                    style="margin-bottom: 0.5rem;",
                ),
                Ul(
                    Li("Title and URL (required fields)"),
                    Li("Publication date (from published_parsed or updated_parsed)"),
                    Li(
                        "Content/summary (from summary, description, or content fields)"
                    ),
                    Li("Author information"),
                    style="margin-left: 2rem; line-height: 1.6; margin-bottom: 1rem;",
                ),
                P(
                    "HTML tags and entities are stripped from content using a custom HTMLStripper parser to ensure clean text for analysis.",
                    style="margin-bottom: 1.5rem;",
                ),
                style="margin-bottom: 2rem; padding: 1.5rem; background: var(--bg-cream); border-left: 4px solid var(--green-primary);",
            ),
            # Stage 2
            Div(
                H4(
                    "2. AI Relevance Check",
                    style="color: var(--green-primary); margin: 0 0 0.5rem 0;",
                ),
                P(
                    "Articles must first pass a global AI relevance check. The system searches for AI-related keywords such as:",
                    style="margin-bottom: 0.5rem;",
                ),
                P(
                    '"artificial intelligence", "machine learning", "deep learning", "neural network", "computer vision", "AI-powered", and more.',
                    style="font-style: italic; color: var(--text-medium); margin: 0 0 1rem 2rem;",
                ),
                P(
                    "Articles without any AI-related keywords are filtered out.",
                    style="margin-bottom: 1.5rem;",
                ),
                style="margin-bottom: 2rem; padding: 1.5rem; background: var(--bg-cream); border-left: 4px solid var(--green-primary);",
            ),
            # Stage 3
            Div(
                H4(
                    "3. Category Classification",
                    style="color: var(--green-primary); margin: 0 0 0.5rem 0;",
                ),
                P(
                    "Relevant articles are then classified into one of three categories using keyword matching:",
                    style="margin-bottom: 0.5rem;",
                ),
                Ul(
                    Li(
                        Strong("AI for Medicine:"),
                        " Keywords including medical, health, clinical, diagnosis, patient, hospital, imaging, healthcare",
                    ),
                    Li(
                        Strong("AI for Planet:"),
                        " Keywords including climate, environment, sustainability, conservation, biodiversity, ocean, weather, pollution",
                    ),
                    Li(
                        Strong("Green AI:"),
                        " Keywords including energy efficient, model compression, sustainable computing, carbon footprint, edge AI, renewable energy, smart grid",
                    ),
                    style="margin-left: 2rem; line-height: 1.8; margin-bottom: 1rem;",
                ),
                P(
                    "The system counts keyword matches for each category and assigns the article to the category with the highest match percentage.",
                    style="margin-bottom: 1.5rem;",
                ),
                style="margin-bottom: 2rem; padding: 1.5rem; background: var(--bg-cream); border-left: 4px solid var(--green-primary);",
            ),
            # Stage 4
            Div(
                H4(
                    "4. Relevancy Scoring",
                    style="color: var(--green-primary); margin: 0 0 0.5rem 0;",
                ),
                P(
                    "Each classified article receives a relevancy score (0-100) calculated as:",
                    style="margin-bottom: 0.5rem;",
                ),
                P(
                    "Relevancy Score = (Number of Matching Keywords / Total Category Keywords) × 100 × 2",
                    style="font-family: monospace; background: white; padding: 1rem; border-radius: 0.25rem; margin: 1rem 0; border: 1px solid #e5e5e5;",
                ),
                P(
                    "Articles must achieve at least 5% keyword match (minimum threshold) to be included in the digest. This attempts to ensure that only highly relevant articles are displayed.",
                    style="margin-bottom: 0.5rem;",
                ),
                P(
                    "A confidence score (0-1) is also calculated for internal quality assessment, normalized as (match_percentage / 20).",
                    style="margin-bottom: 1.5rem;",
                ),
                style="margin-bottom: 2rem; padding: 1.5rem; background: var(--bg-cream); border-left: 4px solid var(--green-primary);",
            ),
            style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;",
        ),
    )


if __name__ == "__main__":
    import os

    # Get port from environment variable (Railway sets this) or use 5001 for local
    port = int(os.getenv("PORT", 5001))
    # Disable autoreload in production to avoid multiple scheduler instances
    serve(host="0.0.0.0", port=port, reload=False)
