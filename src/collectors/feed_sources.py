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
    ("https://blogs.microsoft.com/ai/feed/", "Microsoft AI Blog", False),
    (
        "https://aws.amazon.com/blogs/machine-learning/feed/",
        "AWS Machine Learning Blog",
        False,
    ),
    ("https://deepmind.google/blog/rss.xml", "Google DeepMind", False),
    # ========== Sustainability-focused sources ==========
    (
        "https://blog.google/company-news/outreach-and-initiatives/sustainability/rss/",
        "Google Sustainability",
        False,
    ),
    # ========== High-quality peer-reviewed journals (filtered) ==========
    # Nature family
    ("https://www.nature.com/nm.rss", "Nature Medicine", False),
    ("https://www.nature.com/natsustain.rss", "Nature Sustainability", False),
    ("https://www.nature.com/nclimate.rss", "Nature Climate Change", False),
    ("https://www.nature.com/natmachintell.rss", "Nature Machine Intelligence", False),
    ("https://www.nature.com/nenergy.rss", "Nature Energy", False),
    # Science/AAAS
    ("https://www.science.org/rss/news_current.xml", "Science Magazine", False),
    # Medical Journals
    # (
    #     "https://www.thelancet.com/collection/rss/001611",
    #     "The Lancet Digital Health Oncology",
    #     False,
    # ),
    # (
    #     "https://www.thelancet.com/collection/rss/001639",
    #     "The Lancet Digital Health Radiology & Medical Imaging",
    #     False,
    # ),
    # (
    #     "https://www.thelancet.com/collection/rss/001536",
    #     "The Lancet Digital Health Cardiology & Vascular Medicine",
    #     False,
    # ),
    # (
    #     "https://www.thelancet.com/collection/rss/001585",
    #     "The Lancet Digital Health Neurology",
    #     False,
    # ),
    # Climate & Environment
    # ========== UN & International Organizations (filtered) ==========
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
    # ========== Research institutions & universities (filtered) ==========
    ("https://news.mit.edu/rss/topic/artificial-intelligence2", "MIT News - AI", False),
    # ========== Tech news & industry (filtered) ==========
    ("https://www.apple.com/newsroom/rss-feed.rss", "Apple Newsroom", False),
    ("https://www.wired.com/feed/tag/ai/latest/rss", "WIRED AI", False),
    # ("https://spectrum.ieee.org/feeds/feed.rss", "IEEE Spectrum", False),
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
