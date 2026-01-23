# GreenAI Digest

A news aggregation and AI classification system focused on research with environmental and medical impact.

## 🎯 Features

- **Latest Articles**: Real-time feed from 28+ RSS sources
- **Smart Filtering**: Keyword-based classification into 3 categories
- **Category Filter**: AI for Planet | AI for Medicine | Green AI
- **Pagination**: Browse articles with Previous/Next navigation
- **Relevancy Scoring**: 0-100 score based on keyword matching

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         GreenAI Digest Application          │
├─────────────────────────────────────────────┤
│  FastHTML (Web Framework)                   │
│  + MonsterUI (UI Components)                │
├─────────────────────────────────────────────┤
│  RSS Collectors → Keyword Filter → Database │
├─────────────────────────────────────────────┤
│  Local: SQLite  │  Production: PostgreSQL   │
└─────────────────────────────────────────────┘
```

## 📦 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Web Framework** | FastHTML |
| **UI Components** | MonsterUI |
| **Database** | SQLite (local) / PostgreSQL (production) |
| **ORM** | SQLAlchemy |
| **RSS Parsing** | feedparser |
| **Deployment** | Railway |

## 🚀 Quick Start (Local Development)

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run
```bash
python scripts/init_db.py  # First time only
python main.py             # Then run app
```

Visit: `http://localhost:5001`

## 🌐 Production Deployment

**Deployed on:** Railway  
**Database:** PostgreSQL  
**Auto-deploy:** GitHub push → Railway

### Deploy Changes
```bash
git add .
git commit -m "Your message"
git push  # Auto-deploys to Railway
```

## 📚 Documentation

- **[RAILWAY_DEPLOYMENT.md](docs/RAILWAY_DEPLOYMENT.md)** - Deployment guide
- **[POSTGRESQL_SETUP.md](docs/POSTGRESQL_SETUP.md)** - Database setup (local testing)
- **[design_spec.md](docs/design_spec.md)** - Architecture & design

## 🗂️ Project Structure

```
greenai-digest/
├── main.py                    # FastHTML app + routes
├── src/
│   ├── database.py           # SQLAlchemy models
│   ├── config.py             # Settings
│   ├── collectors/
│   │   ├── rss_collector.py  # RSS fetching
│   │   ├── relevance_filter.py # Classification
│   │   └── feed_sources.py   # 28 RSS feeds
│   └── models/
├── scripts/
│   ├── init_db.py            # Initialize database
│   ├── fetch_articles.py     # Populate articles
│   ├── test_feed_urls.py     # Validate feeds
│   └── migrate_to_postgres.py # SQLite→PostgreSQL
├── static/
│   └── styles.css            # Custom styles
└── data/
    └── greenai.db            # SQLite (local only)
```

## 📊 Data Pipeline

```
RSS Feeds (28 sources)
    ↓
Fetch & Parse (feedparser)
    ↓
HTML Cleanup (strip tags, decode entities)
    ↓
Keyword Matching (relevance_filter.py)
    ↓
Classification (AI for Planet/Medicine/Green AI)
    ↓
Store in Database (SQLite/PostgreSQL)
    ↓
Display in UI (sorted by date, with relevancy score)
```

## 🔄 Database Difference

| Local Development | Production |
|---|---|
| **SQLite** | **PostgreSQL** |
| File-based | Client-server |
| No setup needed | Automatic on Railway |
| `sqlite:///data/greenai.db` | `DATABASE_URL` env var |

## 📋 Categories & Keywords

**3 Active Categories:**
- **AI for Planet** (23 keywords): climate, energy, emissions, sustainability...
- **AI for Medicine** (20 keywords): diagnosis, lesion detection, imaging, treatment...
- **Green AI** (45+ keywords): efficiency, optimization, carbon, model compression...

Articles need 5% minimum keyword match to be included.

```bash
python src/main.py
```

Open your browser to: http://localhost:5001

## Project Structure

```
greenai-digest/
├── src/
│   ├── main.py           # FastHTML app with MonsterUI
│   ├── config.py         # Configuration settings
│   ├── database.py       # SQLAlchemy models
│   ├── collectors/       # Data source collectors (future)
│   ├── services/         # Classification & processing (future)
│   └── routes/           # Additional routes (future)
├── scripts/
│   └── init_db.py        # Database initialization
├── data/                 # SQLite database storage
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Current Status - MVP

This is a **barebones MVP** with:
- ✅ Database schema and models
- ✅ FastHTML app with MonsterUI theme
- ✅ Home page with article cards
- ✅ Sample data for testing
- ✅ Basic navigation

### Not Yet Implemented
- ⏳ Article collectors (arXiv, RSS feeds, etc.)
- ⏳ Classification service
- ⏳ Automated scheduling
- ⏳ Search and filtering

## Tech Stack

- **Backend**: FastHTML (Python web framework)
- **UI**: MonsterUI (styled components for FastHTML)
- **Database**: SQLite (via SQLAlchemy ORM)
- **Styling**: FrankenUI + Tailwind CSS (via MonsterUI)