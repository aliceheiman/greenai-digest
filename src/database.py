"""Database models and setup."""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from src.config import settings

Base = declarative_base()


class Article(Base):
    """Article model for storing news articles and research papers."""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    published_date = Column(DateTime)
    fetched_date = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)
    summary = Column(Text)
    authors = Column(String)

    # Relationship
    classifications = relationship(
        "Classification", back_populates="article", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:50]}...')>"


class Classification(Base):
    """Classification model for LLM-based article categorization."""

    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    category = Column(String, nullable=False)
    confidence = Column(Float)
    relevancy_score = Column(Float)
    tags = Column(String)  # Comma-separated tags
    classified_date = Column(DateTime, default=datetime.utcnow)

    # Relationship
    article = relationship("Article", back_populates="classifications")

    def __repr__(self):
        return f"<Classification(article_id={self.article_id}, category='{self.category}', relevancy={self.relevancy_score})>"


class Category(Base):
    """Category model for defining article categories."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    parent_category = Column(String)

    def __repr__(self):
        return f"<Category(name='{self.name}')>"


class UserPreference(Base):
    """User preference model for personalized relevancy scoring."""

    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String, nullable=False)
    weight = Column(Float, default=1.0)
    keywords = Column(String)

    def __repr__(self):
        return f"<UserPreference(topic='{self.topic}', weight={self.weight})>"


# Database setup
def get_engine():
    """Create and return database engine with appropriate settings for SQLite or PostgreSQL."""
    db_url = settings.database_url

    # SQLite-specific configuration
    if db_url.startswith("sqlite"):
        return create_engine(
            db_url, connect_args={"check_same_thread": False}, pool_pre_ping=True
        )

    # PostgreSQL-specific configuration
    else:
        return create_engine(
            db_url,
            pool_size=10,  # Connection pool size
            max_overflow=20,  # Max connections beyond pool_size
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,  # Recycle connections after 1 hour
            echo=False,  # Set to True for SQL query logging
        )


def get_session():
    """Create and return database session."""
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def init_db():
    """Initialize database tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def seed_categories():
    """Seed initial categories."""
    session = get_session()

    categories = [
        Category(
            name="AI for Planet",
            description="Environmental applications of AI including climate modeling and energy efficiency",
        ),
        Category(
            name="AI for Medicine",
            description="Healthcare applications including lesion detection and diagnostic imaging",
        ),
        Category(
            name="Green AI",
            description="Sustainable AI development and model efficiency",
        ),
        Category(
            name="AI Ethics & Policy",
            description="Governance, fairness, and privacy in AI",
        ),
        Category(
            name="General AI Research",
            description="General AI research and developments",
        ),
    ]

    for cat in categories:
        existing = session.query(Category).filter_by(name=cat.name).first()
        if not existing:
            session.add(cat)

    session.commit()
    session.close()
    print("Categories seeded successfully!")
