# PostgreSQL Setup Guide

## ℹ️ You're Using It! 

Your production app on Railway is **already using PostgreSQL**. This guide is for local testing only.

---

## 🖥️ Local PostgreSQL Setup (Optional)

### macOS - Using EDB PostgreSQL

1. **Download & Install:**
   - Visit [edb.com/download/postgresql](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
   - Download PostgreSQL installer
   - Run installer, follow prompts

2. **Create Database:**
   - Open pgAdmin (comes with EDB)
   - Create new database: `greenai_db`
   - Note the password you set

3. **Connect Your App:**
   ```bash
   export DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@localhost:5432/greenai_db"
   python main.py
   ```

### macOS - Using Homebrew (Simpler)

```bash
brew install postgresql@15
brew services start postgresql@15
createdb greenai_db
export DATABASE_URL="postgresql://localhost:5432/greenai_db"
```

---

## 🔗 Connection Formats

**Local (no password):**
```
postgresql://localhost:5432/greenai_db
```

**Local (with password):**
```
postgresql://postgres:password@localhost:5432/greenai_db
```

**Railway (auto-provided):**
```
postgresql://user:pass@region.railway.app:5432/dbname
```

---

## ✅ Verify Connection

```bash
python -c "from src.database import get_engine; print('✓ Connected:', get_engine().url)"
```

---

## 📊 Local Testing Workflow

```bash
# Terminal 1: Start PostgreSQL
brew services start postgresql@15

# Terminal 2: Activate venv and set DATABASE_URL
source venv/bin/activate
export DATABASE_URL="postgresql://localhost:5432/greenai_db"

# Initialize database
python scripts/init_db.py

# Fetch test articles
python scripts/fetch_articles.py

# Run app
python main.py
```

Visit: `http://localhost:5001`

---

## 🚀 No Need for Local PostgreSQL

**For development, SQLite works great:**
```bash
# Just unset the variable
unset DATABASE_URL

# Use SQLite automatically
python main.py
```

**Production:** Railway handles PostgreSQL automatically ✨


