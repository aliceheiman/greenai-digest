"""Add a custom article to the database."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import get_session, Article, Classification
from datetime import datetime


def add_custom_article():
    session = get_session()

    # Create your article
    article = Article(
        title="Unlocking AI’s transformative potential to protect and restore nature",
        url="https://blog.google/company-news/outreach-and-initiatives/sustainability/google-world-resources-institute-new-paper/",
        source="Google Sustainability",
        published_date=datetime.now(),
        content="This is a test article about something awesome!",
        summary="Read Google & WRI’s paper on AI-powered solutions for nature",
        authors="Kate Brandt, Ani Dasgupta",
    )

    session.add(article)
    session.flush()  # This gets us the article.id

    # Add a classification
    classification = Classification(
        article_id=article.id,
        category="AI for Medicine",  # Pick one of your categories
        confidence=0.95,
        relevancy_score=100,  # Make it super relevant!
        tags="tutorial,fun,learning",
    )

    session.add(classification)
    session.commit()
    session.close()

    print("✅ Added your custom article!")


if __name__ == "__main__":
    add_custom_article()
