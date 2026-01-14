"""Configuration for RSS feed sources."""

# RSS feed sources for AI research
# Format: (url, display_name, always_include)
# - always_include=True: Skip relevance filtering (for AI-focused sources)
# - always_include=False: Apply keyword filtering

RSS_FEEDS = [
    # ========== AI-focused sources (filtered) ==========
    # Must still match one of the 4 categories (Medicine, Planet, Green AI, Ethics)
    ("https://openai.com/news/rss.xml", "OpenAI News", False),
    (
        "https://blog.google/innovation-and-ai/technology/ai/rss/",
        "Google AI Blog",
        False,
    ),
    ("https://nvidianews.nvidia.com/rss.xml", "NVIDIA News", False),
    # ("https://ai.stanford.edu/blog/feed.xml", "Stanford AI Lab", False),
    # ========== Sustainability-focused sources (always include) ==========
    # Auto-include all articles from sustainability feeds
    (
        "https://blog.google/company-news/outreach-and-initiatives/sustainability/rss/",
        "Google Sustainability",
        True,
    ),
    # Note: Apple Environment doesn't have RSS, only HTML page
    # ========== High-quality peer-reviewed journals (filtered) ==========
    # Nature family
    ("https://www.nature.com/nm.rss", "Nature Medicine", False),
    ("https://www.nature.com/natsustain.rss", "Nature Sustainability", False),
    ("https://www.nature.com/nclimate.rss", "Nature Climate Change", False),
    # Science/AAAS
    ("https://www.science.org/rss/news_current.xml", "Science Magazine", False),
    # ========== UN News (filtered) ==========
    (
        "https://news.un.org/feed/subscribe/en/news/topic/health/feed/rss.xml",
        "UN Health News",
        False,
    ),
    (
        "https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml",
        "UN Climate Change",
        False,
    ),
    (
        "https://news.un.org/feed/subscribe/en/news/topic/sdgs/feed/rss.xml",
        "UN SDGs",
        False,
    ),
    # ========== General tech news (filtered) ==========
    ("https://www.apple.com/newsroom/rss-feed.rss", "Apple Newsroom", False),
    # ========== arXiv feeds (experimental/preprints - for later use) ==========
    # ("http://export.arxiv.org/rss/q-bio.QM", "arXiv - Quantitative Methods in Biology", False),
    # ("http://export.arxiv.org/rss/cs.AI", "arXiv - Artificial Intelligence", False),
    # ("http://export.arxiv.org/rss/physics.ao-ph", "arXiv - Atmospheric & Oceanic Physics", False),
]


def get_all_feeds():
    """
    Get all configured RSS feeds.

    Returns:
        List of tuples: (url, source_name, always_include)
        - url: RSS feed URL
        - source_name: Display name for the source
        - always_include: If True, skip relevance filtering
    """
    return RSS_FEEDS
