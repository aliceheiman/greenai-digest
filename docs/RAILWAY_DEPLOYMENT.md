# Railway Deployment Guide

## 🚀 Current Setup

Your GreenAI Digest is **already deployed on Railway**!

**Live URL:** Check your Railway project's Networking tab  
**Database:** PostgreSQL (auto-provisioned)  
**Deployment:** Auto-deploys on GitHub push

---

## 🔄 Deployment Workflow

**Make changes locally:**
```bash
git add .
git commit -m "Your changes"
git push origin main
git push deploy main:main # to deployment account
```

**Railway automatically:**
1. Detects the push
2. Builds the app (installs dependencies)
3. Initializes database (if needed)
4. Deploys with zero downtime

**View logs:**
- Go to Railway dashboard → `greenai-digest` service → Deployments → Logs

---

## 🛠️ Common Tasks

### Fetch Latest Articles
Option 1 - Automatic (scheduled):
```bash
# Coming soon: GitHub Actions cron job
```

Option 2 - Manual (using Railway CLI):
```bash
brew install railway
railway login
railway link
railway run python scripts/fetch_articles.py
```

### Check Database Status
1. Go to Railway project
2. Click `postgres` service
3. Click "Data" to browse tables

### View Live Logs
```bash
railway logs
```

---

## 📊 Environment Variables

**Automatically set by Railway:**
- `DATABASE_URL` → PostgreSQL connection string
- `PORT` → 8080 (handled in main.py)

**Optional (add in Railway Settings → Variables):**
```
DEBUG=False
LOG_LEVEL=INFO
SECRET_KEY=<secure-key>
```

---

## 🆘 Troubleshooting

| Error | Solution |
|-------|----------|
| "Tables don't exist" | Already fixed - `init_db.py` runs on startup |
| App won't start | Check logs: Railway → Deployments → Logs |
| PostgreSQL not connecting | Verify `DATABASE_URL` exists in Environment Variables |
| Deployment stuck | Manual redeploy: Railway → Settings → Redeploy |

---

## 📈 Scaling

**Current tier:** Hobby ($5/month credit)  
**Upgrade path:**
1. Railway → Settings → Billing
2. Upgrade to Pro for more resources
3. Add background job service for scheduled tasks (next step)

---

## 🔮 Next Steps

1. **Automate article fetching** (GitHub Actions or Railway cron)
2. **Add monitoring** (error alerts, uptime checks)
3. **Custom domain** (Railway → Settings → Networking → Custom Domain)
4. **Performance optimization** (caching, indexes)


