#!/usr/bin/env python3
"""
WhatsApp Test Script
Run this to test WhatsApp notification functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.mail import send_whatsapp_notification
from models import Lead
from datetime import datetime

def test_whatsapp():
    """Test WhatsApp notification with sample data"""
    
    # Create a test lead object
    class TestLead:
        def __init__(self):
            self.name = "Test Müşteri"
            self.phone = "+90555123456"
            self.email = "test@example.com"
            self.language = "tr"
            self.unit_interest = "3+1 Daire"
            self.budget_range = "5-7 Milyon TL"
            self.timeline = "6 ay içinde"
            self.best_call_time = "Sabah 09:00-12:00"
            self.whatsapp_optin = True
            self.marketing_consent = True
            self.utm_source = "test"
            self.utm_medium = "manual"
            self.utm_campaign = "whatsapp_test"
            self.created_at = datetime.now()
            self.ip_address = "127.0.0.1"
    
    print("🧪 Testing WhatsApp notification system...")
    print(f"📱 Target WhatsApp number: +905525242866")
    print("-" * 50)
    
    test_lead = TestLead()
    
    try:
        success = send_whatsapp_notification(test_lead)
        
        if success:
            print("✅ WhatsApp notification sent successfully!")
            print("Check the console output above for the WhatsApp Web URL")
        else:
            print("❌ WhatsApp notification failed")
            print("Check the console output for any error messages")
    
    except Exception as e:
        print(f"❌ Error testing WhatsApp: {e}")
    
    print("-" * 50)
    print("💡 To enable automatic WhatsApp API sending:")
    print("1. Set WHATSAPP_API_TOKEN in your .env file")
    print("2. Set WHATSAPP_PHONE_NUMBER_ID in your .env file")
    print("3. Or set CALLMEBOT_API_KEY for free service")
    print("\n🔗 For now, use the WhatsApp Web URL shown above to send manually")

if __name__ == "__main__":
    test_whatsapp()
