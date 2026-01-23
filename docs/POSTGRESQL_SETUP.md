# PostgreSQL Setup Guide

## Option 1: Local PostgreSQL (for testing)

### Install PostgreSQL:

**macOS (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Create database:**
```bash
createdb greenai_db
```

**Set environment variable:**
```bash
export DATABASE_URL="postgresql://localhost:5432/greenai_db"
```

Or add to `.env`:
```
DATABASE_URL=postgresql://localhost:5432/greenai_db
```

---

## Option 2: Cloud PostgreSQL (for production)

### Railway (Recommended - Easy & Free Tier)

1. Go to [railway.app](https://railway.app)
2. Create new project → Add PostgreSQL
3. Copy the `DATABASE_URL` from connection string
4. Add to your `.env` or Railway environment variables

### Render

1. Go to [render.com](https://render.com)
2. Create new PostgreSQL database
3. Copy the external connection string
4. Add to your `.env`

### Supabase (Free PostgreSQL)

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get connection string from Settings → Database
4. Use "Connection Pooling" URL for better performance

---

## Migration Steps

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Set up PostgreSQL database URL:
Create a `.env` file:
```
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

### 3. Initialize PostgreSQL tables:
```bash
python scripts/init_db.py
```

### 4. (Optional) Migrate existing SQLite data:
```bash
python scripts/migrate_to_postgres.py
```

### 5. Verify connection:
```bash
python -c "from src.database import get_engine; print('✓ Connected:', get_engine().url)"
```

---

## Testing Both Databases

**SQLite (local dev):**
```bash
unset DATABASE_URL  # Use default SQLite
python main.py
```

**PostgreSQL (production):**
```bash
export DATABASE_URL="postgresql://..."
python main.py
```

---

## Connection String Format

```
postgresql://[username]:[password]@[host]:[port]/[database]
```

**Examples:**
- Local: `postgresql://localhost:5432/greenai_db`
- Railway: `postgresql://postgres:PASSWORD@containers.railway.app:5432/railway`
- Render: `postgresql://user:pass@region.render.com:5432/dbname`

---

## Performance Tips

1. **Indexes (Already Optimized):**
   - Add indexes for frequently queried columns in future migrations

2. **Connection Pooling:**
   - Already configured in `database.py` (pool_size=10, max_overflow=20)

3. **Query Optimization:**
   - Use `limit()` for pagination (already implemented)
   - Add database-level caching for homepage

---

## Troubleshooting

**Error: "psycopg2 not installed"**
```bash
pip install psycopg2-binary
```

**Error: "database does not exist"**
```bash
createdb greenai_db
```

**Error: "password authentication failed"**
- Check your DATABASE_URL credentials
- Verify PostgreSQL is running: `pg_isready`

**Connection refused:**
- Ensure PostgreSQL is running
- Check firewall settings for cloud databases
