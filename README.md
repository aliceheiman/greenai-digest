# GreenAI Digest

A news aggregation and curation system focused on AI research with environmental and medical impact.

## Features

- **Daily Digest**: Curated list of top AI articles by relevancy
- **Categories**:
  - AI for Planet (climate modeling, energy efficiency)
  - AI for Medicine (lesion detection, diagnostic imaging)
  - Green AI (model efficiency, sustainable computing)

## Quick Start

### 1. Setup Python Environment

Make sure you have Python 3.10+ installed:

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

Run the initialization script to create the database and add sample data:

```bash
python scripts/init_db.py
```

This will:
- Create the SQLite database in `data/greenai.db`
- Set up all necessary tables
- Seed initial categories
- Add sample articles for testing

### 4. Run the Application

Start the FastHTML server:

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