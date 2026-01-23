"""Initialize database and seed with sample data."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import init_db, seed_categories, get_session, Article, Classification
from datetime import datetime, timedelta
import random


def seed_sample_articles():
    """Add sample articles for testing."""
    session = get_session()

    # Sample articles data
    sample_articles = [
        {
            "title": "Deep Learning for Skin Lesion Detection Achieves 95% Accuracy",
            "url": "https://example.com/lesion-detection-dl",
            "source": "Nature Medicine",
            "content": "Researchers developed a deep learning model that can detect skin lesions with 95% accuracy, potentially revolutionizing dermatology diagnostics.",
            "summary": "New deep learning model achieves 95% accuracy in skin lesion detection.",
            "category": "AI for Medicine",
            "relevancy": 95,
            "tags": "lesion detection,medical imaging,deep learning",
        },
        {
            "title": "AI Model Reduces Data Center Energy Consumption by 40%",
            "url": "https://example.com/datacenter-energy",
            "source": "DeepMind Blog",
            "content": "DeepMind's AI system optimizes cooling in data centers, reducing energy consumption by 40% and significantly lowering carbon footprint.",
            "summary": "DeepMind AI reduces data center energy use by 40% through intelligent cooling optimization.",
            "category": "Green AI",
            "relevancy": 85,
            "tags": "energy efficiency,data centers,carbon footprint",
        },
        {
            "title": "Climate Prediction Models Enhanced with Transformer Architecture",
            "url": "https://example.com/climate-transformers",
            "source": "arXiv",
            "content": "New research applies transformer neural networks to climate modeling, improving prediction accuracy for extreme weather events.",
            "summary": "Transformers improve climate prediction accuracy for extreme weather events.",
            "category": "AI for Planet",
            "relevancy": 82,
            "tags": "climate modeling,transformers,weather prediction",
        },
        {
            "title": "Automated Medical Image Analysis Speeds Up Cancer Diagnosis",
            "url": "https://example.com/cancer-diagnosis-ai",
            "source": "NVIDIA Blog",
            "content": "AI-powered medical imaging tools are helping radiologists detect cancer earlier and more accurately.",
            "summary": "AI medical imaging accelerates cancer detection and improves accuracy.",
            "category": "AI for Medicine",
            "relevancy": 88,
            "tags": "medical imaging,cancer detection,radiology",
        },
        {
            "title": "New Guidelines for Ethical AI Development Released",
            "url": "https://example.com/ai-ethics-guidelines",
            "source": "UN AI Advisory",
            "content": "International consortium releases comprehensive guidelines for ethical AI development and deployment.",
            "summary": "UN releases new ethical AI development guidelines.",
            "category": "AI Ethics & Policy",
            "relevancy": 65,
            "tags": "ethics,policy,governance",
        },
        {
            "title": "Efficient Attention Mechanisms Reduce Model Size by 70%",
            "url": "https://example.com/efficient-attention",
            "source": "OpenAI Research",
            "content": "Researchers develop more efficient attention mechanisms that maintain performance while dramatically reducing model size.",
            "summary": "New attention mechanisms cut model size by 70% without performance loss.",
            "category": "Green AI",
            "relevancy": 78,
            "tags": "model efficiency,attention,optimization",
        },
        {
            "title": "AI Detects Melanoma from Smartphone Photos",
            "url": "https://example.com/melanoma-smartphone",
            "source": "Stanford Medicine",
            "content": "Mobile app uses AI to detect melanoma from smartphone photos with dermatologist-level accuracy.",
            "summary": "Smartphone AI app detects melanoma with expert-level accuracy.",
            "category": "AI for Medicine",
            "relevancy": 92,
            "tags": "melanoma,lesion detection,mobile health",
        },
        {
            "title": "Machine Learning Optimizes Solar Panel Placement",
            "url": "https://example.com/solar-ml",
            "source": "Nature Energy",
            "content": "ML algorithms optimize solar panel placement and angle, increasing energy generation by 25%.",
            "summary": "ML optimization boosts solar panel efficiency by 25%.",
            "category": "AI for Planet",
            "relevancy": 75,
            "tags": "solar energy,optimization,renewable energy",
        },
    ]

    # Create articles and classifications
    for idx, article_data in enumerate(sample_articles):
        # Check if article already exists
        existing = session.query(Article).filter_by(url=article_data["url"]).first()
        if existing:
            continue

        # Create article
        article = Article(
            title=article_data["title"],
            url=article_data["url"],
            source=article_data["source"],
            published_date=datetime.now() - timedelta(days=random.randint(0, 7)),
            content=article_data["content"],
            summary=article_data["summary"],
            authors="Research Team",
        )
        session.add(article)
        session.flush()  # Get article.id

        # Create classification
        classification = Classification(
            article_id=article.id,
            category=article_data["category"],
            confidence=random.uniform(0.85, 0.98),
            relevancy_score=article_data["relevancy"],
            tags=article_data["tags"],
        )
        session.add(classification)

    session.commit()
    session.close()
    print(f"Added {len(sample_articles)} sample articles!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Initialize database and seed data")
    parser.add_argument(
        "--with-samples",
        action="store_true",
        help="Add sample articles for testing (default: schema and categories only)",
    )

    args = parser.parse_args()

    print("Initializing database...")
    init_db()

    print("Seeding categories...")
    seed_categories()

    if args.with_samples:
        print("Adding sample articles...")
        seed_sample_articles()
    else:
        print("Skipping sample articles (use --with-samples to include)")

    print("\n✓ Database setup complete!")
    if args.with_samples:
        print("Database initialized with sample data.")
    else:
        print("Database initialized with schema and categories only.")
    print("Run 'python main.py' to start the application.")
