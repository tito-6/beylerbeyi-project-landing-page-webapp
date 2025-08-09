# Local Development Setup

This guide will help you run the Beylerbeyi Bosphorus Residences luxury real estate landing page on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for version control)

## Setup Instructions

### 1. Download the Project
Download all project files to your local machine.

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r local_requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.local .env

# Edit .env file with your settings (optional for basic functionality)
```

### 5. Run the Application

#### Option 1: Using the local runner (Recommended)
```bash
python run_local.py
```

#### Option 2: Using Flask directly
```bash
export FLASK_APP=main.py  # On Windows: set FLASK_APP=main.py
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
flask run
```

#### Option 3: Using Gunicorn (Production-like)
```bash
gunicorn --bind 127.0.0.1:5000 --reload main:app
```

### 6. Access the Application
Open your browser and navigate to: `http://localhost:5000`

## Configuration Options

### Database
- **SQLite (Default)**: No setup required, database file created automatically
- **PostgreSQL**: Update DATABASE_URL in .env file

### Email (Optional)
For contact form functionality, configure email settings in .env:
- MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

### Analytics (Optional)
Add your analytics IDs in .env:
- GTM_ID (Google Tag Manager)
- GA4_ID (Google Analytics 4)
- FACEBOOK_PIXEL_ID
- LINKEDIN_INSIGHT_ID

## Project Structure
```
├── app.py              # Flask application configuration
├── main.py             # Application entry point
├── routes.py           # URL routes and view functions
├── models.py           # Database models
├── run_local.py        # Local development server
├── local_requirements.txt  # Python dependencies
├── static/             # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── templates/          # HTML templates
├── lang/               # Language files (TR, EN, AR)
└── utils/              # Utility functions
```

## Features Included
- ✅ Multi-language support (Turkish, English, Arabic)
- ✅ Advanced glassmorphism design with 2025 trends
- ✅ Lead capture and management system
- ✅ Email notifications
- ✅ Mobile-responsive design
- ✅ Analytics integration ready
- ✅ KVKV/GDPR compliance features

## Development Notes
- The application uses Flask with SQLAlchemy ORM
- Frontend uses Bootstrap 5 with custom luxury styling
- Modern JavaScript effects with glassmorphism and animations
- All text content is stored in JSON files for easy translation

## Production Deployment
For production deployment:
1. Set FLASK_ENV=production in .env
2. Use a proper database (PostgreSQL recommended)
3. Configure email settings
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Set up proper security headers and SSL

## Troubleshooting
- **Import errors**: Make sure all dependencies are installed
- **Database errors**: Check DATABASE_URL configuration
- **Port conflicts**: Change port in run_local.py if 5000 is occupied
- **Email issues**: Verify SMTP settings in .env file