# Beylerbeyi Bosphorus Residences - Local Development

A luxury real estate landing page with cutting-edge 2025 design trends, glassmorphism effects, and comprehensive lead management system.

## 🚀 Quick Start

1. **Download all project files to your local machine**

2. **Install Python dependencies:**
   ```bash
   pip install -r local_requirements.txt
   ```

3. **Configure environment (optional):**
   ```bash
   cp .env.local .env
   # Edit .env with your settings
   ```

4. **Run the application:**
   ```bash
   python run_local.py
   ```

5. **Open browser:** http://localhost:5000

## 📁 Project Files Structure

### Core Application Files
- `app.py` - Flask application configuration
- `main.py` - Application entry point  
- `routes.py` - URL routes and view functions
- `models.py` - Database models
- `run_local.py` - Local development server

### Frontend Files
- `templates/` - HTML templates with Jinja2
- `static/css/` - Luxury styling with glassmorphism
- `static/js/` - Modern JavaScript interactions
- `static/images/` - Image assets (placeholder SVGs)

### Language Support
- `lang/tr.json` - Turkish translations
- `lang/en.json` - English translations  
- `lang/ar.json` - Arabic translations

### Configuration Files
- `local_requirements.txt` - Python dependencies
- `.env.local` - Environment variables template
- `LOCAL_SETUP.md` - Detailed setup instructions
- `README_LOCAL.md` - This file

## ✨ Features Included

### Design & UX
- Ultra-modern glassmorphism design
- 2025 cutting-edge visual effects
- Responsive mobile-first layout
- Custom cursor and magnetic buttons
- Smooth animations and transitions
- Premium luxury aesthetic

### Functionality
- Multi-language support (TR/EN/AR)
- Advanced lead capture system
- Email notifications
- Analytics integration ready
- KVKV/GDPR compliance
- WhatsApp integration
- Callback request system

### Technical
- Flask web framework
- SQLAlchemy ORM
- Email integration (Flask-Mail)
- Modern JavaScript ES6+
- Bootstrap 5 framework
- Font Awesome icons
- Google Fonts integration

## 🛠 Development Commands

```bash
# Development server
python run_local.py

# Production-like server
gunicorn --bind 127.0.0.1:5000 --reload main:app

# Install dependencies
pip install -r local_requirements.txt

# Create deployment files
python deploy_local.py
```

## 🌐 Deployment Options

The project is ready for deployment on:
- **Heroku** (Procfile included)
- **Docker** (Dockerfile ready)
- **VPS/Cloud** (start.sh script)
- **Local server** (run_local.py)

## 📧 Email Configuration

For contact forms to work, configure in `.env`:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 🗄 Database Options

### SQLite (Default - No setup needed)
```
DATABASE_URL=sqlite:///luxury_real_estate.db
```

### PostgreSQL (Production recommended)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

## 📊 Analytics Setup

Add your tracking IDs in `.env`:
```
GTM_ID=GTM-XXXXXXX
GA4_ID=G-XXXXXXXXXX
FACEBOOK_PIXEL_ID=xxxxxxxxxxxxx
```

## 🎨 Customization

### Colors & Branding
Edit `static/css/style.css` CSS variables:
```css
:root {
    --gold-primary: #c9a876;
    --luxury-black: #0a0a0a;
    /* ... other variables */
}
```

### Content & Text
Edit language files in `lang/` directory:
- `tr.json` - Turkish
- `en.json` - English  
- `ar.json` - Arabic

### Images
Replace placeholder SVGs in `static/images/` with actual property photos

## 🚨 Important Notes

- All sensitive data should be in `.env` file (never commit to git)
- Default database is SQLite (file-based, perfect for development)
- Email functionality requires proper SMTP configuration
- Analytics require actual tracking IDs to work
- Production deployment needs proper security settings

## 🆘 Troubleshooting

**Import errors:** Install all dependencies from local_requirements.txt
**Database errors:** Check DATABASE_URL in .env
**Email issues:** Verify SMTP settings
**Port conflicts:** Change port in run_local.py

## 📞 Support

This is a complete, production-ready luxury real estate landing page with modern 2025 design trends. All features are implemented and ready for customization with your actual content and branding.