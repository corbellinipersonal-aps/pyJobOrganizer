# Backend Deployment Guide - Job Organizer FastAPI

## 🚀 Deploy FastAPI Backend to Render

This guide will help you deploy the Job Organizer FastAPI backend to Render.

---

## ✅ Pre-Deployment Checklist

- ✅ **Backend code ready** at `/root/ORGANIZER-Python/Organiz_Py-00/backend/`
- ✅ **requirements-render.txt** created (clean dependencies)
- ✅ **render.yaml** created (Render configuration)
- ⏳ **Push to GitHub** (same or separate repository)
- ⏳ **Deploy to Render**

---

## 📦 Step 1: Push Backend to GitHub

### Option A: Add to Existing Repository (Recommended)

```bash
cd /root/ORGANIZER-Python/Organiz_Py-00

# Initialize git if not already done
git init
git config user.name "Cascade AI Assistant"
git config user.email "cascade@windsurf.ai"

# Add backend files
git add backend/
git commit -m "Add FastAPI backend for deployment

Features:
- FastAPI REST API with async support
- PostgreSQL database integration
- Job CRUD operations
- Statistics endpoint
- CORS configuration
- Error handling

Deployment:
- Render-ready configuration
- Clean dependencies in requirements-render.txt
- Database auto-initialization"

# Push to GitHub (use existing pyJobOrganizer repo or create new one)
git remote add origin git@github.com:corbellinipersonal-aps/pyJobOrganizer.git
git push origin main
```

### Option B: Create Separate Backend Repository

```bash
cd /root/ORGANIZER-Python/Organiz_Py-00/backend

git init
git config user.name "Cascade AI Assistant"
git config user.email "cascade@windsurf.ai"

git add .
git commit -m "Initial commit: Job Organizer FastAPI Backend"

# Create new repo: pyJobOrganizer-Backend
git remote add origin git@github.com:corbellinipersonal-aps/pyJobOrganizer-Backend.git
git push -u origin main
```

---

## 🔧 Step 2: Deploy to Render

### Using Blueprint (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +"** → **"Blueprint"**
3. **Connect GitHub repository**
4. **Select repository**: `pyJobOrganizer` (or `pyJobOrganizer-Backend`)
5. **Render detects** `backend/render.yaml`
6. **Review configuration**:
   - Database: `job-organizer-db` (PostgreSQL Free)
   - API Service: `job-organizer-api` (Web Service Free)
7. **Click "Apply"**

### Manual Deployment (Alternative)

#### Create PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `job-organizer-db`
   - **Database**: `job_organizer`
   - **User**: `job_organizer_user`
   - **Region**: Oregon
   - **Plan**: Free
3. Click **"Create Database"**
4. **Copy Internal Database URL** (starts with `postgresql://`)

#### Create Web Service

1. Click **"New +"** → **"Web Service"**
2. **Connect GitHub repository**
3. **Configure**:
   - **Name**: `job-organizer-api`
   - **Region**: Oregon
   - **Branch**: `main`
   - **Root Directory**: `backend` (if in monorepo)
   - **Runtime**: Python 3
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements-render.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

4. **Environment Variables**:
   - `DATABASE_URL`: Paste the Internal Database URL from step 1
   - `PYTHON_VERSION`: `3.11.0`
   - `ENVIRONMENT`: `production`
   - `DEBUG`: `false`

5. **Advanced Settings**:
   - **Health Check Path**: `/api/stats`
   - **Auto-Deploy**: Yes

6. Click **"Create Web Service"**

---

## 🔍 Step 3: Verify Deployment

### Check Build Logs

Monitor the build process:
```
==> Installing dependencies from requirements-render.txt
Successfully installed fastapi uvicorn sqlalchemy...
==> Starting service
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

### Test API Endpoints

Once deployed, test your API:

**Get Statistics**:
```bash
curl https://job-organizer-api.onrender.com/api/stats
```

Expected response:
```json
{
  "total_jobs": 0,
  "status_counts": {},
  "priority_counts": {}
}
```

**Get Jobs**:
```bash
curl https://job-organizer-api.onrender.com/api/jobs
```

**Health Check**:
```bash
curl https://job-organizer-api.onrender.com/api/stats
```

---

## 📊 Step 4: Migrate Database Data

Your Render database is empty. To migrate data:

### Option 1: Use pg_dump/pg_restore

```bash
# Export from local database
pg_dump -U postgres -d job_organizer -F c -f job_organizer.backup

# Import to Render database
# Get External Database URL from Render dashboard
pg_restore -d <RENDER_DATABASE_URL> job_organizer.backup
```

### Option 2: Use seed script

Create a seed script to populate initial data or use your existing `seed.py`.

### Option 3: Manual entry

Use the API to create jobs manually through POST requests.

---

## 🔗 Step 5: Update Reflex App

Now that your backend is deployed, update the Reflex app:

1. **Get Backend URL**: `https://job-organizer-api.onrender.com`

2. **Update Reflex render.yaml**:
```yaml
envVars:
  - key: API_BASE_URL
    value: https://job-organizer-api.onrender.com/api
```

3. **Commit and push**:
```bash
cd /root/ORGANIZER-Python/PY-Reflex-ORGANIZ/OrganizPY-Reflex
git add render.yaml
git commit -m "Update API URL to deployed backend"
git push origin main
```

4. **Render auto-deploys** the Reflex app with new backend URL

---

## 🐛 Troubleshooting

### Database Connection Errors

**Problem**: `asyncpg.exceptions.InvalidCatalogNameError`

**Solution**: Database not created. Check:
- Database name matches in Render dashboard
- `DATABASE_URL` environment variable is correct
- Database service is running

### CORS Errors

**Problem**: Frontend can't access API

**Solution**: Update CORS in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://job-organizer-reflex.onrender.com",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Import Errors

**Problem**: `ModuleNotFoundError`

**Solution**: 
- Check `requirements-render.txt` includes all dependencies
- Verify build command runs from correct directory
- Check Python version matches (3.11.0)

### Database Tables Not Created

**Problem**: Tables don't exist

**Solution**: The `init_db()` function should create tables automatically. Check:
- `startup_event` is running
- Database URL is correct
- Models are properly imported

---

## 🔐 Security Configuration

### Environment Variables

Never commit these to GitHub:
- `DATABASE_URL`
- API keys
- Secrets

Use Render's environment variable UI.

### CORS

Update allowed origins for production:
```python
allow_origins=[
    "https://job-organizer-reflex.onrender.com",
    "https://your-custom-domain.com",
]
```

### Database

- Use strong passwords
- Enable SSL connections
- Regular backups (Render Free tier: manual backups)

---

## 📈 Monitoring

### View Logs

1. Go to service in Render dashboard
2. Click **"Logs"** tab
3. Monitor real-time logs
4. Filter by log level

### Health Checks

Render monitors `/api/stats` endpoint:
- Checks every 30 seconds
- Restarts service if unhealthy
- View status in dashboard

### Metrics

Free tier includes:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 💰 Costs

### Free Tier

**Database**:
- 1 GB storage
- 97 connection limit
- Expires after 90 days (manual renewal)

**Web Service**:
- 512 MB RAM
- Spins down after 15 min inactivity
- 750 hours/month free

### Paid Plans

**Starter ($7/month)**:
- Always-on service
- 1 GB RAM
- Better performance

**Database ($7/month)**:
- 10 GB storage
- No expiration
- Daily backups

---

## ✅ Post-Deployment Checklist

- [ ] Backend deployed to Render
- [ ] Database created and connected
- [ ] API endpoints responding
- [ ] `/api/stats` returns data
- [ ] `/api/jobs` returns jobs (or empty array)
- [ ] Health checks passing
- [ ] Logs show no errors
- [ ] CORS configured for Reflex domain
- [ ] Backend URL copied
- [ ] Reflex app updated with backend URL
- [ ] Reflex app redeployed
- [ ] End-to-end test successful

---

## 🎯 Your Backend URL

After deployment, your backend will be available at:

```
https://job-organizer-api.onrender.com
```

API endpoints:
- `GET /api/stats` - Job statistics
- `GET /api/jobs` - List all jobs
- `GET /api/jobs/{id}` - Get specific job
- `POST /api/jobs` - Create job
- `PATCH /api/jobs/{id}` - Update job
- `DELETE /api/jobs/{id}` - Delete job

---

**Created**: November 2, 2025  
**Deployment Platform**: Render.com  
**Backend Framework**: FastAPI + PostgreSQL
