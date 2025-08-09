#!/usr/bin/env python3
"""
Local Development Server
Run this file to start the application locally
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import app

if __name__ == '__main__':
    # Set default environment variables if not set
    if not os.environ.get('SESSION_SECRET'):
        os.environ['SESSION_SECRET'] = 'dev-secret-key-change-in-production'
    
    if not os.environ.get('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite:///luxury_real_estate.db'
    
    # Run the application
    app.run(
        host='127.0.0.1',  # localhost for local development
        port=5000,
        debug=True
    )