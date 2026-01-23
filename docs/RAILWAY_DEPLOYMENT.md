# Railway Deployment Guide

## Quick Deploy to Railway

### 1. Create Railway Account
- Go to [railway.app](https://railway.app)
- Sign up with GitHub

### 2. Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Select your `greenai-digest` repository
4. Railway will auto-detect the Python app

### 3. Add PostgreSQL Database
1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically creates a PostgreSQL instance
4. It will auto-set `DATABASE_URL` environment variable

### 4. Configure Environment Variables
Railway auto-sets `DATABASE_URL`, but you can add more in Settings → Variables:

```
DATABASE_URL=<automatically set by Railway>
SECRET_KEY=<generate a secure key>
DEBUG=False
LOG_LEVEL=INFO
```

### 5. Initialize Database (First Time Only)
After first deployment, run this command in Railway:
```bash
python scripts/init_db.py
```

To run commands in Railway:
- Go to your service → Settings → "Deploy" section
- Or use Railway CLI (see below)

### 6. Populate Articles
Schedule or manually run:
```bash
python scripts/fetch_articles.py
```

---

## Railway CLI (Optional but Recommended)

### Install Railway CLI:
```bash
npm i -g @railway/cli
# or with Homebrew:
brew install railway
```

### Login and link project:
```bash
railway login
railway link
```

### Run commands on Railway:
```bash
# Initialize database
railway run python scripts/init_db.py

# Fetch articles
railway run python scripts/fetch_articles.py

# Check logs
railway logs
```

---

## Deployment Workflow

### Every time you push to GitHub:
1. Commit and push changes:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. Railway automatically:
   - Detects the push
   - Builds the app
   - Deploys with zero downtime
   - Uses PostgreSQL from DATABASE_URL

### View your live site:
- Railway provides a public URL (e.g., `greenai-digest-production.up.railway.app`)
- Find it in: Settings → Domains

---

## Environment Setup Summary

**Local Development:**
- Uses SQLite (`sqlite:///data/greenai.db`)
- No DATABASE_URL environment variable needed
- Run: `python main.py`

**Railway Production:**
- Uses PostgreSQL (auto-configured)
- DATABASE_URL automatically set by Railway
- Auto-deploys on git push

---

## Initial Setup Checklist

- [ ] Push code to GitHub
- [ ] Create Railway account
- [ ] Deploy from GitHub repo
- [ ] Add PostgreSQL database
- [ ] Run `railway run python scripts/init_db.py`
- [ ] Run `railway run python scripts/fetch_articles.py`
- [ ] Visit your live URL!

---

## Monitoring

- **Logs**: `railway logs` or view in Railway dashboard
- **Database**: Use Railway's built-in PostgreSQL viewer
- **Metrics**: Check CPU, memory, requests in Railway dashboard

---

## Cost

- **Free Tier**: $5/month credit (enough for small apps)
- **Usage-based**: Pay only for what you use
- **Includes**: Web service + PostgreSQL database

---

## Troubleshooting

**Build fails:**
- Check `railway logs`
- Verify `requirements.txt` is complete

**Database connection errors:**
- Ensure PostgreSQL database is added
- Check DATABASE_URL is set automatically

**App not starting:**
- Verify PORT environment variable is used (already configured in main.py)
- Check Procfile exists

---

## Next Steps

After deployment, consider:
1. Set up automated nightly article fetching (cron job)
2. Add custom domain
3. Monitor usage and scale as needed
