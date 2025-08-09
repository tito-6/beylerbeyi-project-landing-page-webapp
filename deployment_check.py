#!/usr/bin/env python3
"""
Comprehensive Deployment Readiness Check
Tests all critical functionality before production deployment
"""

import os
import sys
import requests
import time
import threading
import json
from datetime import datetime

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing imports...")
    try:
        from app import app, db
        from models import Lead
        from utils.mail import send_lead_notification, send_whatsapp_notification
        from utils.i18n import get_translations
        from utils.validation import validate_email, validate_phone
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("🗄️ Testing database...")
    try:
        from app import app, db
        from models import Lead
        
        with app.app_context():
            # Create tables
            db.create_all()
            
            # Test creating a lead
            test_lead = Lead(
                name="Test User",
                phone="05551234567",
                email="test@example.com",
                language="tr",
                kvkk_consent=True,
                ip_address="127.0.0.1",
                user_agent="Test Agent"
            )
            
            db.session.add(test_lead)
            db.session.commit()
            
            # Test querying
            leads = Lead.query.all()
            print(f"✅ Database working - {len(leads)} leads found")
            
            # Clean up test lead
            db.session.delete(test_lead)
            db.session.commit()
            
            return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_validation():
    """Test form validation"""
    print("✅ Testing validation...")
    try:
        from utils.validation import validate_email, validate_phone, get_validation_error_message
        
        # Test email validation
        assert validate_email("test@example.com") == True
        assert validate_email("invalid-email") == False
        assert validate_email("") == True  # Optional field
        
        # Test phone validation
        assert validate_phone("05551234567") == True
        assert validate_phone("123") == False
        assert validate_phone("") == False  # Required field
        
        # Test error messages
        msg = get_validation_error_message('invalid_email', 'tr')
        assert 'Geçersiz' in msg
        
        print("✅ Validation tests passed")
        return True
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def test_translations():
    """Test multi-language support"""
    print("🌐 Testing translations...")
    try:
        from utils.i18n import get_translations, get_supported_languages
        
        languages = get_supported_languages()
        assert 'tr' in languages
        assert 'en' in languages
        assert 'ar' in languages
        
        for lang in languages:
            translations = get_translations(lang)
            assert 'meta' in translations
            assert 'hero' in translations
            
        print(f"✅ Translations working for {len(languages)} languages")
        return True
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return False

def start_test_server():
    """Start Flask server for testing"""
    try:
        from app import app
        app.run(host='127.0.0.1', port=5002, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Server error: {e}")

def test_web_endpoints():
    """Test web endpoints"""
    print("🌐 Testing web endpoints...")
    
    # Start server in background
    server_thread = threading.Thread(target=start_test_server, daemon=True)
    server_thread.start()
    time.sleep(3)  # Wait for server to start
    
    base_url = "http://127.0.0.1:5002"
    
    try:
        # Test main page
        response = requests.get(base_url, timeout=10)
        assert response.status_code == 200
        assert 'Beylerbeyi' in response.text
        
        # Test language switching
        response = requests.get(f"{base_url}/en", timeout=10)
        assert response.status_code == 200
        
        # Test KVKK page
        response = requests.get(f"{base_url}/kvkk/tr", timeout=10)
        assert response.status_code == 200
        
        # Test callback request
        callback_data = {
            'callback_name': 'Test User',
            'callback_phone': '05551234567',
            'language': 'tr'
        }
        response = requests.post(f"{base_url}/callback-request", data=callback_data, timeout=10)
        assert response.status_code == 200
        json_resp = response.json()
        assert json_resp['success'] == True
        
        print("✅ Web endpoints working")
        return True
    except Exception as e:
        print(f"❌ Web endpoint error: {e}")
        return False

def check_environment():
    """Check environment configuration"""
    print("⚙️ Checking environment configuration...")
    
    issues = []
    warnings = []
    
    # Check critical environment variables
    critical_vars = ['SESSION_SECRET', 'DATABASE_URL']
    for var in critical_vars:
        if not os.environ.get(var):
            issues.append(f"Missing critical environment variable: {var}")
    
    # Check optional but recommended variables
    optional_vars = {
        'MAIL_USERNAME': 'Email notifications will not work',
        'MAIL_PASSWORD': 'Email notifications will not work',
        'GTM_ID': 'Google Analytics will not track',
        'GA4_ID': 'Google Analytics will not track'
    }
    
    for var, warning in optional_vars.items():
        if not os.environ.get(var):
            warnings.append(f"{var} not set - {warning}")
    
    # Check WhatsApp configuration
    if os.environ.get('CALLMEBOT_API_KEY') == '9250107':
        print("✅ WhatsApp CallMeBot API configured")
    
    if issues:
        print("❌ Critical configuration issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    if warnings:
        print("⚠️ Configuration warnings:")
        for warning in warnings:
            print(f"   - {warning}")
    
    print("✅ Environment configuration OK")
    return True

def check_static_files():
    """Check static files are present"""
    print("📁 Checking static files...")
    
    required_files = [
        'static/css/style.css',
        'static/css/validation.css',
        'static/js/main.js',
        'templates/base.html',
        'templates/index.html',
        'templates/kvkk.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing static files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required static files present")
    return True

def create_deployment_files():
    """Create missing deployment files"""
    print("📦 Creating deployment files...")
    
    # Create Procfile for Heroku
    procfile_content = "web: gunicorn main:app\n"
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    
    # Create production main.py
    main_content = """from app import app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
"""
    with open('main.py', 'w') as f:
        f.write(main_content)
    
    # Update requirements.txt to include requests
    requirements = """Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-Mail==0.10.0
Werkzeug==3.1.3
email-validator==2.2.0
gunicorn==23.0.0
python-dotenv==1.0.1
psycopg2-binary==2.9.10
SQLAlchemy==2.0.42
requests==2.31.0"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    # Create Dockerfile
    dockerfile_content = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    
    # Create .dockerignore
    dockerignore_content = """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
venv
.venv
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
.env
.env.*
!.env.example
"""
    
    with open('.dockerignore', 'w') as f:
        f.write(dockerignore_content)
    
    print("✅ Deployment files created:")
    print("   - Procfile (Heroku)")
    print("   - main.py (Production entry point)")
    print("   - requirements.txt (Updated)")
    print("   - Dockerfile (Docker deployment)")
    print("   - .dockerignore")

def run_deployment_check():
    """Run complete deployment readiness check"""
    print("🚀 DEPLOYMENT READINESS CHECK")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    results = []
    
    # Run all tests
    results.append(("Imports", test_imports()))
    results.append(("Database", test_database()))
    results.append(("Validation", test_validation()))
    results.append(("Translations", test_translations()))
    results.append(("Static Files", check_static_files()))
    results.append(("Environment", check_environment()))
    results.append(("Web Endpoints", test_web_endpoints()))
    
    # Create deployment files
    create_deployment_files()
    
    # Print summary
    print("\n" + "=" * 50)
    print("📋 DEPLOYMENT READINESS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:15} {status}")
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 READY FOR DEPLOYMENT!")
        print("\n📋 Deployment Options:")
        print("1. Heroku: git push heroku main")
        print("2. Docker: docker build -t estate-vue .")
        print("3. Local: python main.py")
        print("\n⚠️ Remember to:")
        print("- Set production environment variables")
        print("- Configure email SMTP settings")
        print("- Set up SSL certificates")
        print("- Configure domain DNS")
    else:
        print("❌ NOT READY FOR DEPLOYMENT")
        print("Please fix the failing tests before deploying.")
    
    return passed == total

if __name__ == "__main__":
    run_deployment_check()
