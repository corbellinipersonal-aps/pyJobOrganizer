# Environment Configuration Guide

## 🎯 Overview

This project now has **proper separation** between development and production environments. Each environment has its own configuration, database, and API endpoints.

---

## 📁 Environment Files

### Backend Files

```
backend/
├── .env.development          # Development config (local)
├── .env.production.example   # Production template (Render)
├── .env                       # Active config (gitignored)
└── app/core/config.py        # Environment-aware configuration
```

### Frontend Files

```
OrganizPY-Reflex/
├── .env.development          # Development config (local)
├── .env.production.example   # Production template (Render)
└── .env.example              # General template
```

---

## 🔧 Development Environment

### Backend (FastAPI)

**Configuration:** `.env.development`
```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/job_organizer
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:8001
LOG_LEVEL=DEBUG
```

**Features:**
- ✅ Local PostgreSQL database
- ✅ Debug mode enabled
- ✅ Verbose logging (DEBUG level)
- ✅ CORS allows all local development servers
- ✅ Hot reload enabled

**Run Development Backend:**
```bash
cd /root/ORGANIZER-Python/Organiz_Py-00/backend
cp .env.development .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Reflex)

**Configuration:** `.env.development`
```env
ENVIRONMENT=development
DEBUG=true
API_BASE_URL=http://localhost:8000/api
PORT=3000
LOG_LEVEL=DEBUG
```

**Features:**
- ✅ Points to local backend
- ✅ Debug mode enabled
- ✅ Verbose logging
- ✅ Hot reload enabled

**Run Development Frontend:**
```bash
cd /root/ORGANIZER-Python/PY-Reflex-ORGANIZ/OrganizPY-Reflex
./start.sh
```

---

## 🚀 Production Environment

### Backend (FastAPI on Render)

**Configuration:** Set in Render Dashboard
```env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=<provided-by-render>
CORS_ORIGINS=https://job-organizer-reflex.onrender.com
LOG_LEVEL=INFO
```

**Features:**
- ✅ Render PostgreSQL database
- ✅ Debug mode disabled
- ✅ INFO level logging (less verbose)
- ✅ CORS restricted to deployed frontend only
- ✅ Production-optimized

**Deployment:**
- Render automatically sets `DATABASE_URL`
- Other variables set in Render environment UI
- Auto-deploys on git push

### Frontend (Reflex on Render)

**Configuration:** Set in `render.yaml`
```yaml
envVars:
  - key: ENVIRONMENT
    value: production
  - key: DEBUG
    value: false
  - key: API_BASE_URL
    value: https://job-organizer-api.onrender.com/api
  - key: LOG_LEVEL
    value: INFO
```

**Features:**
- ✅ Points to deployed backend
- ✅ Debug mode disabled
- ✅ INFO level logging
- ✅ Production-optimized

---

## 🔐 Environment-Specific Behavior

### Backend (`app/core/config.py`)

```python
# Environment detection
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

def is_production() -> bool:
    return ENVIRONMENT == "production"

def is_development() -> bool:
    return ENVIRONMENT == "development"

# Database - Different per environment
if is_production():
    DATABASE_URL = os.getenv("DATABASE_URL")  # Required
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL must be set in production")
else:
    DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/job_organizer"

# CORS - Restricted in production
if is_production():
    CORS_ORIGINS = ["https://job-organizer-reflex.onrender.com"]
else:
    CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8001"]

# Logging - Verbose in dev, concise in prod
LOG_LEVEL = "DEBUG" if is_development() else "INFO"
```

### Frontend (`job_organizer/config.py`)

```python
class Config:
    # Environment detection
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # API URL - Different per environment
    API_BASE_URL: str = os.getenv(
        "API_BASE_URL",
        "http://localhost:8000/api"  # Development default
    )
    
    @classmethod
    def is_production(cls) -> bool:
        return cls.ENVIRONMENT == "production"
```

---

## 🎯 Key Differences

| Feature | Development | Production |
|---------|-------------|------------|
| **Database** | Local PostgreSQL | Render PostgreSQL |
| **Backend URL** | `http://localhost:8000` | `https://job-organizer-api.onrender.com` |
| **Frontend URL** | `http://localhost:3000` | `https://job-organizer-reflex.onrender.com` |
| **Debug Mode** | Enabled | Disabled |
| **Logging** | DEBUG (verbose) | INFO (concise) |
| **CORS** | Allow all local | Restrict to frontend domain |
| **Hot Reload** | Enabled | Disabled |
| **Error Details** | Full stack traces | Generic messages |

---

## 🔄 Switching Environments

### Local Development

```bash
# Backend
cd backend
cp .env.development .env
uvicorn app.main:app --reload

# Frontend
cd OrganizPY-Reflex
cp .env.development .env
./start.sh
```

### Production (Render)

Environment variables are set in Render dashboard:
1. Go to service settings
2. Click "Environment" tab
3. Add/update variables
4. Redeploy if needed

---

## 🛡️ Security Best Practices

### Never Commit

```gitignore
# Environment files
.env
.env.local
.env.production

# Only commit templates
.env.example
.env.development
.env.production.example
```

### Production Secrets

- Set in Render dashboard UI
- Never hardcode in code
- Use environment variables
- Rotate regularly

### Database URLs

- Development: Local connection string
- Production: Render provides automatically
- Never commit database credentials

---

## ✅ Environment Checklist

### Development Setup

- [ ] Copy `.env.development` to `.env` (backend)
- [ ] Copy `.env.development` to `.env` (frontend)
- [ ] Local PostgreSQL running
- [ ] Database `job_organizer` created
- [ ] Backend starts on port 8000
- [ ] Frontend starts on port 3000
- [ ] API calls work between frontend/backend

### Production Setup

- [ ] Backend deployed to Render
- [ ] Database created on Render
- [ ] `DATABASE_URL` set automatically
- [ ] `ENVIRONMENT=production` set
- [ ] `DEBUG=false` set
- [ ] CORS configured for frontend domain
- [ ] Frontend deployed to Render
- [ ] `API_BASE_URL` points to backend
- [ ] End-to-end test successful

---

## 🧪 Testing Environments

### Test Development

```bash
# Backend
curl http://localhost:8000/api/stats

# Frontend
open http://localhost:3000
```

### Test Production

```bash
# Backend
curl https://job-organizer-api.onrender.com/api/stats

# Frontend
open https://job-organizer-reflex.onrender.com
```

---

## 📊 Environment Variables Reference

### Backend Variables

| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `ENVIRONMENT` | `development` | `production` | Environment name |
| `DEBUG` | `true` | `false` | Debug mode |
| `DATABASE_URL` | Local PostgreSQL | Render PostgreSQL | Database connection |
| `CORS_ORIGINS` | Local servers | Frontend domain | Allowed origins |
| `LOG_LEVEL` | `DEBUG` | `INFO` | Logging verbosity |

### Frontend Variables

| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `ENVIRONMENT` | `development` | `production` | Environment name |
| `DEBUG` | `true` | `false` | Debug mode |
| `API_BASE_URL` | `http://localhost:8000/api` | `https://...onrender.com/api` | Backend API URL |
| `PORT` | `3000` | Set by Render | Frontend port |
| `LOG_LEVEL` | `DEBUG` | `INFO` | Logging verbosity |

---

## 🎓 Benefits of Separation

### 1. **Safety**
- Production database isolated from development
- No risk of corrupting production data during testing
- Different CORS policies prevent unauthorized access

### 2. **Debugging**
- Verbose logging in development
- Full error details in development
- Concise logging in production

### 3. **Performance**
- Debug mode disabled in production
- Optimized for speed in production
- Hot reload only in development

### 4. **Security**
- Secrets managed separately
- CORS restricted in production
- Environment-specific configurations

### 5. **Maintainability**
- Clear separation of concerns
- Easy to switch environments
- Template files for new developers

---

**Created:** November 2, 2025  
**Last Updated:** November 2, 2025  
**Version:** 1.0
