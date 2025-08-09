import os
import logging
from flask import Flask
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix

# Try to load environment variables from .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without it
    pass

# Configure logging
logging.basicConfig(level=logging.DEBUG)

mail = Mail()

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "luxury-real-estate-secret-key")

# Session configuration - Fix for partitioned cookie issue
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Monkey patch to fix partitioned cookie parameter issue
from werkzeug.wrappers import Response
original_set_cookie = Response.set_cookie

def patched_set_cookie(self, *args, **kwargs):
    # Remove the partitioned parameter if it exists
    kwargs.pop('partitioned', None)
    return original_set_cookie(self, *args, **kwargs)

Response.set_cookie = patched_set_cookie

# Only add ProxyFix for production environments (Heroku, Railway, etc.)
if os.environ.get("DYNO") or os.environ.get("RAILWAY_ENVIRONMENT"):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Mail configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# initialize extensions
mail.init_app(app)

# Import routes (no database models needed)
import routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
