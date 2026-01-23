# Article Fetching Architecture

## Overview

The article fetching system is **modular** and can be triggered via multiple methods:

1. **APScheduler** (current) - Built-in background scheduler
2. **GitHub Actions** - Scheduled workflow (recommended for production)
3. **Railway CLI** - Manual execution
4. **Command line** - Direct script execution

## Core Module

**Location:** `scripts/fetch_articles_modular.py`

**Function:** `fetch_and_store_articles(max_per_feed=20)`

This is the **single source of truth** for fetching logic. It:
- Connects to RSS feeds
- Filters by relevance
- Stores in database
- Returns stats

Can be called from any scheduler.

## Scheduler Module

**Location:** `src/scheduler.py`

**Function:** `create_scheduler(fetch_function, hour, minute)`

This module abstracts away APScheduler. To switch schedulers:
1. Replace `src/scheduler.py` with new implementation
2. main.py doesn't need to change

## Current Setup: APScheduler

**How it works:**
```python
# In main.py
from src.scheduler import create_scheduler
from scripts.fetch_articles_modular import fetch_and_store_articles

scheduler = create_scheduler(
    fetch_function=fetch_and_store_articles,
    hour=2,  # 2 AM UTC
    minute=0
)
```

**Configuration via environment variables:**
```bash
FETCH_HOUR=2          # Hour to run (0-23, UTC)
FETCH_MINUTE=0        # Minute to run (0-59)
DISABLE_SCHEDULER=true  # Disable scheduler entirely
```

## Switching to GitHub Actions

To switch to GitHub Actions:

1. **Disable APScheduler in production:**
   ```bash
   export DISABLE_SCHEDULER=true
   ```

2. **Create GitHub Actions workflow** (`.github/workflows/fetch-articles.yml`):
   ```yaml
   name: Fetch Articles Nightly
   on:
     schedule:
       - cron: '0 2 * * *'  # 2 AM UTC daily
   
   jobs:
     fetch:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - run: pip install -r requirements.txt
         - run: python scripts/fetch_articles_modular.py
   ```

3. **For Railway database access:**
   - Add `DATABASE_URL` as GitHub secret
   - Workflow uses it to connect to Railway PostgreSQL

## Usage Examples

### Local testing
```bash
python scripts/fetch_articles_modular.py
```

### With custom max articles
```bash
python scripts/fetch_articles_modular.py --max-per-feed 50
```

### From Python code
```python
from scripts.fetch_articles_modular import fetch_and_store_articles

result = fetch_and_store_articles(max_per_feed=20)
print(f"New: {result['new']}, Duplicates: {result['duplicate']}, Filtered: {result['filtered']}")
```

### Via Railway CLI
```bash
railway run python scripts/fetch_articles_modular.py
```

## Design Principles

✅ **Separation of concerns:**
- Fetching logic in `fetch_articles_modular.py`
- Scheduling abstraction in `src/scheduler.py`
- Main app in `main.py`

✅ **Easy to swap schedulers:**
- Replace `src/scheduler.py`
- main.py remains unchanged

✅ **Works standalone:**
- Can run as script
- Can be called from any scheduler
- Can be triggered by webhooks

✅ **Configurable:**
- Fetch time via environment variables
- Max articles per feed as parameter
- Disable scheduler if needed

## Migration Path

**Current:** APScheduler + APScheduler  
**Future:** APScheduler disabled + GitHub Actions workflow

No code changes needed - just environment variables!

