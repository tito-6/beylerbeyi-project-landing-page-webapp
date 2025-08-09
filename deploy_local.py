#!/usr/bin/env python3
"""
Local Deployment Script
Prepares the project for production deployment
"""

import os
import sys
import subprocess
import shutil

def create_production_files():
    """Create production-ready configuration files"""
    
    # Create production requirements file
    prod_requirements = """Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Mail==0.9.1
Werkzeug==3.0.1
email-validator==2.1.0
gunicorn==21.2.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9"""
    
    with open('requirements.txt', 'w') as f:
        f.write(prod_requirements)
    
    # Create production startup script
    startup_script = """#!/bin/bash
# Production startup script

# Set production environment
export FLASK_ENV=production

# Start with gunicorn
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 main:app
"""
    
    with open('start.sh', 'w') as f:
        f.write(startup_script)
    
    os.chmod('start.sh', 0o755)
    
    # Create Procfile for Heroku deployment
    with open('Procfile', 'w') as f:
        f.write('web: gunicorn main:app\n')
    
    # Create Docker support
    dockerfile = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile)
    
    print("✅ Production deployment files created:")
    print("   - requirements.txt")
    print("   - start.sh")
    print("   - Procfile (Heroku)")
    print("   - Dockerfile")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log

# Runtime
.replit
replit.nix
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore file created")

def main():
    print("🚀 Preparing project for local deployment...")
    
    create_production_files()
    create_gitignore()
    
    print("\n📋 Next steps for local deployment:")
    print("1. Set up your environment variables in .env file")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run locally: python run_local.py")
    print("4. For production: gunicorn main:app")
    
    print("\n🌐 Deployment platforms supported:")
    print("- Heroku: Use Procfile")
    print("- Docker: Use Dockerfile") 
    print("- VPS: Use start.sh script")
    print("- Local: Use run_local.py")

if __name__ == "__main__":
    main()