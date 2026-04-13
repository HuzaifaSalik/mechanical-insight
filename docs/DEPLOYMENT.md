# Deployment Guide - Mechanical Insight

## Production Environment
- **Platform:** Render (https://render.com)
- **URL:** https://mechanical-insight.onrender.com
- **Database:** PostgreSQL (Render managed)
- **Python:** 3.11.7

## Deployment Steps

### 1. Prerequisites
- Render account linked to GitHub
- Repository: HuzaifaSalik/mechanical-insight
- PostgreSQL database created on Render

### 2. Environment Variables
| Variable | Description |
|----------|-------------|
| FLASK_ENV | production |
| FLASK_APP | run.py |
| SECRET_KEY | Auto-generated |
| DATABASE_URL | From Render PostgreSQL |
| MAIL_SERVER | smtp.gmail.com |
| MAIL_PORT | 587 |
| MAIL_USERNAME | Your Gmail address |
| MAIL_PASSWORD | Gmail App Password |

### 3. Auto-Deploy
- Connected to `main` branch
- Every push to `main` triggers auto-deploy
- Build script: `build.sh`
- Start command: `gunicorn run:app`

### 4. Database Setup
- PostgreSQL provisioned automatically via render.yaml
- Migrations run during build via `init_database.py`
- Admin user created via `create_admin_user.py`

### 5. Monitoring
- Health checks configured at /
- Render dashboard for logs and metrics
- Email alerts for deploy failures

## Rollback
To rollback to a previous version:
1. Go to Render Dashboard → mechanical-insight
2. Click "Manual Deploy" → select previous commit
3. Or revert commit on GitHub and push

## SSL
- SSL certificate auto-provisioned by Render
- All HTTP traffic redirected to HTTPS
