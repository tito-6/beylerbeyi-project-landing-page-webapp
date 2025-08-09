from app import db
from datetime import datetime

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    language = db.Column(db.String(5), default='tr')
    unit_interest = db.Column(db.String(50), nullable=True)
    budget_range = db.Column(db.String(50), nullable=True)
    timeline = db.Column(db.String(50), nullable=True)
    best_call_time = db.Column(db.String(50), nullable=True)
    whatsapp_optin = db.Column(db.Boolean, default=False)
    marketing_consent = db.Column(db.Boolean, default=False)
    kvkk_consent = db.Column(db.Boolean, nullable=False)
    utm_source = db.Column(db.String(100), nullable=True)
    utm_medium = db.Column(db.String(100), nullable=True)
    utm_campaign = db.Column(db.String(100), nullable=True)
    utm_content = db.Column(db.String(100), nullable=True)
    utm_term = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Lead {self.name} - {self.phone}>'
