#!/usr/bin/env python3
"""
Database Migration Helper Script
Migrates data from SQLite to PostgreSQL
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, Article, Classification, Category, UserPreference
import os


def migrate_sqlite_to_postgres(sqlite_url: str, postgres_url: str):
    """
    Migrate data from SQLite database to PostgreSQL database.

    Args:
        sqlite_url: SQLite database URL (e.g., sqlite:///data/greenai.db)
        postgres_url: PostgreSQL database URL (e.g., postgresql://user:pass@host:5432/dbname)
    """
    print(f"🔄 Starting migration from SQLite to PostgreSQL...")

    # Create engines
    sqlite_engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    postgres_engine = create_engine(postgres_url)

    # Create sessions
    SqliteSession = sessionmaker(bind=sqlite_engine)
    PostgresSession = sessionmaker(bind=postgres_engine)

    sqlite_session = SqliteSession()
    postgres_session = PostgresSession()

    try:
        # Create all tables in PostgreSQL
        print("📦 Creating PostgreSQL tables...")
        Base.metadata.create_all(bind=postgres_engine)

        # Migrate Categories
        print("📋 Migrating categories...")
        categories = sqlite_session.query(Category).all()
        for cat in categories:
            new_cat = Category(
                name=cat.name,
                description=cat.description,
                parent_category=cat.parent_category,
            )
            postgres_session.merge(new_cat)
        postgres_session.commit()
        print(f"  ✓ Migrated {len(categories)} categories")

        # Migrate Articles
        print("📰 Migrating articles...")
        articles = sqlite_session.query(Article).all()
        article_id_map = {}  # Map old IDs to new IDs

        for article in articles:
            new_article = Article(
                title=article.title,
                url=article.url,
                source=article.source,
                published_date=article.published_date,
                fetched_date=article.fetched_date,
                content=article.content,
                summary=article.summary,
                authors=article.authors,
            )
            postgres_session.add(new_article)
            postgres_session.flush()  # Get the new ID
            article_id_map[article.id] = new_article.id

        postgres_session.commit()
        print(f"  ✓ Migrated {len(articles)} articles")

        # Migrate Classifications
        print("🏷️  Migrating classifications...")
        classifications = sqlite_session.query(Classification).all()
        for cls in classifications:
            new_cls = Classification(
                article_id=article_id_map.get(cls.article_id, cls.article_id),
                category=cls.category,
                confidence=cls.confidence,
                relevancy_score=cls.relevancy_score,
                tags=cls.tags,
                classified_date=cls.classified_date,
            )
            postgres_session.add(new_cls)

        postgres_session.commit()
        print(f"  ✓ Migrated {len(classifications)} classifications")

        # Migrate User Preferences
        print("⚙️  Migrating user preferences...")
        preferences = sqlite_session.query(UserPreference).all()
        for pref in preferences:
            new_pref = UserPreference(
                topic=pref.topic, weight=pref.weight, keywords=pref.keywords
            )
            postgres_session.add(new_pref)

        postgres_session.commit()
        print(f"  ✓ Migrated {len(preferences)} user preferences")

        print("✅ Migration completed successfully!")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        postgres_session.rollback()
        raise

    finally:
        sqlite_session.close()
        postgres_session.close()


def main():
    """Main migration entry point."""
    print("=" * 60)
    print("GreenAI Digest - Database Migration Tool")
    print("SQLite → PostgreSQL")
    print("=" * 60)
    print()

    # Get SQLite database path
    sqlite_url = input(
        "Enter SQLite database URL [sqlite:///data/greenai.db]: "
    ).strip()
    if not sqlite_url:
        sqlite_url = "sqlite:///data/greenai.db"

    # Get PostgreSQL connection string
    print("\nPostgreSQL URL format: postgresql://username:password@host:5432/database")
    postgres_url = input("Enter PostgreSQL database URL: ").strip()

    if not postgres_url:
        print("❌ PostgreSQL URL is required!")
        sys.exit(1)

    # Confirm migration
    print("\n⚠️  This will copy all data from SQLite to PostgreSQL")
    print(f"   Source: {sqlite_url}")
    print(
        f"   Target: {postgres_url.split('@')[1] if '@' in postgres_url else postgres_url}"
    )
    confirm = input("\nProceed with migration? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("❌ Migration cancelled")
        sys.exit(0)

    # Run migration
    print()
    migrate_sqlite_to_postgres(sqlite_url, postgres_url)
    print()
    print("🎉 You can now set DATABASE_URL in your .env file to use PostgreSQL!")


if __name__ == "__main__":
    main()
