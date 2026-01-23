"""Main FastHTML application."""

from fasthtml.common import *
from monsterui.all import *
from src.database import get_session, Article, Classification
from datetime import datetime

# Create FastHTML app with link to external CSS
app, rt = fast_app(hdrs=(Link(rel="stylesheet", href="/static/styles.css"),))


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
            Div("🌱 GreenAI Digest", cls="nav-brand"),
            # Nav links
            Div(
                A("Daily Digest", href="/", cls="nav-link"),
                A("About", href="/about", cls="nav-link"),
                A("Archive", href="/archive", cls="nav-link"),
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
    return Title("About - GreenAI Digest"), Div(
        NavBar(),
        Div(
            H2("About GreenAI Digest", style="margin: 0 0 0.5rem 0;"),
            P(
                "AI Research Focused on Environmental and Medical Impact",
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
                Li("AI for Planet - Climate modeling, energy efficiency"),
                Li("AI for Medicine - Lesion detection, diagnostic imaging"),
                Li("Green AI - Model efficiency, sustainable computing"),
                style="margin-left: 2rem; line-height: 1.8;",
            ),
            style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;",
        ),
    )


if __name__ == "__main__":
    serve()
