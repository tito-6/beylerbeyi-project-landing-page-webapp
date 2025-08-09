# 🚀 DEPLOYMENT GUIDE - Beylerbeyi Residences

## ✅ PRE-DEPLOYMENT CHECKLIST

All systems have been tested and verified:
- ✅ Database functionality (SQLite/PostgreSQL)
- ✅ Form validation (email/phone number)
- ✅ Multi-language support (TR/EN/AR)
- ✅ WhatsApp notifications (CallMeBot API)
- ✅ KVKK compliance pages
- ✅ Static files and templates
- ✅ Web endpoints and routing
- ✅ Lead capture and storage

## 🎯 DEPLOYMENT OPTIONS

### Option 1: Heroku Deployment (Recommended)

```bash
# 1. Install Heroku CLI
# 2. Login to Heroku
heroku login

# 3. Create new app
heroku create your-app-name

# 4. Set environment variables
heroku config:set SESSION_SECRET="your-super-secret-key-32-chars-minimum"
heroku config:set DATABASE_URL="postgresql://..."  # Heroku provides this
heroku config:set MAIL_USERNAME="info@queenvillaofficial.com"
heroku config:set MAIL_PASSWORD="your-gmail-app-password"
heroku config:set CALLMEBOT_API_KEY="9250107"
heroku config:set FLASK_ENV="production"

# 5. Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# 6. Deploy
git add .
git commit -m "Production deployment"
git push heroku main

# 7. Initialize database
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Option 2: Docker Deployment

```bash
# 1. Build image
docker build -t beylerbeyi-residences .

# 2. Run container
docker run -p 5000:5000 \
  -e SESSION_SECRET="your-secret-key" \
  -e DATABASE_URL="postgresql://..." \
  -e MAIL_USERNAME="info@queenvillaofficial.com" \
  -e MAIL_PASSWORD="your-app-password" \
  -e CALLMEBOT_API_KEY="9250107" \
  beylerbeyi-residences
```

### Option 3: Railway Deployment

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables:set SESSION_SECRET="your-secret-key"
railway variables:set MAIL_USERNAME="info@queenvillaofficial.com"
railway variables:set MAIL_PASSWORD="your-app-password"
railway variables:set CALLMEBOT_API_KEY="9250107"

# 5. Deploy
railway up
```

### Option 4: VPS/Server Deployment

```bash
# 1. Copy files to server
scp -r . user@your-server:/path/to/app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export SESSION_SECRET="your-secret-key"
export DATABASE_URL="postgresql://..."
export MAIL_USERNAME="info@queenvillaofficial.com"
export MAIL_PASSWORD="your-app-password"

# 4. Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 2 main:app
```

## ⚙️ CRITICAL ENVIRONMENT VARIABLES

### Required (Must Set):
```
SESSION_SECRET=minimum-32-character-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
MAIL_USERNAME=info@queenvillaofficial.com
MAIL_PASSWORD=your-gmail-app-password
CALLMEBOT_API_KEY=9250107
```

### Recommended:
```
GTM_ID=GTM-XXXXXXX
GA4_ID=G-XXXXXXXXXX
FACEBOOK_PIXEL_ID=1234567890
```

## 📧 EMAIL SETUP (REQUIRED)

1. **Gmail App Password Setup:**
   - Go to Google Account settings
   - Enable 2-factor authentication
   - Generate App Password for "Mail"
   - Use this as MAIL_PASSWORD

2. **Email Configuration:**
   - MAIL_USERNAME: info@queenvillaofficial.com
   - MAIL_PASSWORD: your-16-character-app-password
   - MAIL_SERVER: smtp.gmail.com
   - MAIL_PORT: 587

## 📱 WHATSAPP NOTIFICATIONS

✅ **Already Configured:**
- CallMeBot API Key: 9250107
- Target Phone: +905525242866
- Working and tested

## 🗄️ DATABASE SETUP

### SQLite (Development Only):
```
DATABASE_URL=sqlite:///beylerbeyi.db
```

### PostgreSQL (Production):
```
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🔒 SECURITY CHECKLIST

- ✅ Strong SESSION_SECRET (32+ characters)
- ✅ Environment variables (no hardcoded secrets)
- ✅ KVKK compliance implemented
- ✅ Form validation (prevents malicious input)
- ✅ Database ORM (prevents SQL injection)
- ✅ HTTPS ready (configure SSL on platform)

## 🌐 DOMAIN SETUP

1. **DNS Configuration:**
   - Point A record to deployment IP
   - Set up CNAME for www subdomain

2. **SSL Certificate:**
   - Heroku: Auto SSL available
   - Other platforms: Use Let's Encrypt

## 📊 ANALYTICS INTEGRATION

Set these environment variables for tracking:
```
GTM_ID=GTM-XXXXXXX        # Google Tag Manager
GA4_ID=G-XXXXXXXXXX      # Google Analytics 4
FACEBOOK_PIXEL_ID=123456  # Facebook Pixel
```

## 🚦 TESTING AFTER DEPLOYMENT

1. **Basic Functionality:**
   - Visit homepage: https://your-domain.com
   - Test language switching: /en, /ar
   - Check KVKK page: /kvkk/tr

2. **Forms Testing:**
   - Submit main contact form
   - Test callback request modal
   - Verify WhatsApp notifications received

3. **Validation Testing:**
   - Try invalid email/phone formats
   - Check error messages display

## 📞 SUPPORT CONTACTS

- **Primary Contact:** Tuba İşler (+90 538 059 10 52)
- **Email:** info@queenvillaofficial.com
- **WhatsApp Notifications:** +905525242866

## 🎉 DEPLOYMENT SUMMARY

**Status:** ✅ READY FOR PRODUCTION
**Lead Capture:** ✅ Working (WhatsApp + Email)
**Validation:** ✅ Working (Client + Server)
**Multi-language:** ✅ Working (TR/EN/AR)
**Legal Compliance:** ✅ KVKK implemented
**Mobile Ready:** ✅ Responsive design
**Analytics Ready:** ✅ GTM/GA4/Pixel integration

The application is fully tested and production-ready! 🚀
