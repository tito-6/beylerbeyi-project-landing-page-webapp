from flask_mail import Message
from app import mail
import os
import requests
import json

WHATSAPP_NUMBER = "+905525242866"

def send_whatsapp_notification(lead):
    """Send WhatsApp notification for new lead"""
    try:
        # Format the message with simple formatting to avoid encoding issues
        message = f"""YENI MUSTERI BASVURUSU - Beylerbeyi Residences

Isim: {lead.name}
Telefon: {lead.phone}
Email: {lead.email or 'Belirtilmedi'}
Dil: {lead.language}
Ilgilendigi Unite: {lead.unit_interest or 'Belirtilmedi'}
Butce: {lead.budget_range or 'Belirtilmedi'}
Zaman Cizelgesi: {lead.timeline or 'Belirtilmedi'}
En Iyi Arama Saati: {lead.best_call_time or 'Belirtilmedi'}
WhatsApp Izni: {'Evet' if lead.whatsapp_optin else 'Hayir'}
Pazarlama Izni: {'Evet' if lead.marketing_consent else 'Hayir'}

UTM Bilgileri:
- Kaynak: {lead.utm_source or 'Direkt'}
- Medium: {lead.utm_medium or 'Yok'}
- Kampanya: {lead.utm_campaign or 'Yok'}

Tarih: {lead.created_at}
IP: {lead.ip_address}

Lutfen musteriyle en kisa surede iletisime gecin!"""

        print(f"\n🚨 NEW LEAD SUBMISSION for {WHATSAPP_NUMBER}")
        print(f"Lead: {lead.name} - {lead.phone}")
        
        # Try sending methods in order of preference
        success = False
        
        # Method 1: CallMeBot API (Free and recommended)
        if not success:
            success = send_via_callmebot(message)
        
        # Method 2: WhatsApp Business API (if configured)
        if not success and os.environ.get('WHATSAPP_API_TOKEN'):
            success = send_via_whatsapp_business_api(message)
        
        # Method 3: WhatsApp Web URL (Always works as fallback)
        if not success:
            success = create_whatsapp_web_url(message)
        
        return success
        
    except Exception as e:
        print(f"❌ Error sending WhatsApp notification: {e}")
        # Always try the fallback URL method
        try:
            return create_whatsapp_web_url(f"Error in automated sending. Lead: {lead.name} - {lead.phone}")
        except:
            return False

def send_via_whatsapp_business_api(message):
    """Send via WhatsApp Business API"""
    try:
        token = os.environ.get('WHATSAPP_API_TOKEN')
        phone_number_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
        
        if not token or not phone_number_id:
            return False
        
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": WHATSAPP_NUMBER.replace("+", ""),
            "text": {"body": message}
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        return response.status_code == 200
        
    except Exception as e:
        print(f"WhatsApp Business API error: {e}")
        return False

def send_via_callmebot(message):
    """Send via CallMeBot API (free service)"""
    try:
        # CallMeBot API requires phone number registration and API key
        api_key = os.environ.get('CALLMEBOT_API_KEY')
        if not api_key:
            # If no API key is set, show instructions
            print("\n" + "="*60)
            print("📱 CALLMEBOT SETUP REQUIRED")
            print("="*60)
            print("To enable automatic WhatsApp sending to +905525242866:")
            print("")
            print("1. Add +34 684 73 40 44 to your phone contacts")
            print("2. Send: 'I allow callmebot to send me messages'")
            print("3. Wait for API key from CallMeBot")
            print("4. Add CALLMEBOT_API_KEY=your_key to .env file")
            print("")
            print("For now, using WhatsApp Web URL fallback...")
            print("="*60)
            return False
            
        # CallMeBot API endpoint
        url = "https://api.callmebot.com/whatsapp.php"
        
        # Don't manually encode - let requests handle it properly
        params = {
            'phone': WHATSAPP_NUMBER.replace("+", ""),  # Remove + from phone number
            'text': message,  # Send raw message, requests will handle encoding
            'apikey': api_key
        }
        
        print(f"📤 Sending WhatsApp via CallMeBot to {WHATSAPP_NUMBER}...")
        print(f"🔑 Using API Key: {api_key}")
        print(f"� Message Preview: {message[:100]}...")
        
        response = requests.get(url, params=params, timeout=15)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📝 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ WhatsApp message sent successfully via CallMeBot!")
            return True
        else:
            print(f"❌ CallMeBot API error: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ CallMeBot API error: {e}")
        return False

def create_whatsapp_web_url(message):
    """Create WhatsApp Web URL for manual sending"""
    try:
        # This creates a WhatsApp Web URL that can be opened manually
        # The server admin can use this as a fallback
        import urllib.parse
        
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER.replace('+', '')}?text={encoded_message}"
        
        # Log the URL for manual use
        print(f"\n=== WHATSAPP NOTIFICATION ===")
        print(f"Manual WhatsApp URL: {whatsapp_url}")
        print("=== END WHATSAPP NOTIFICATION ===\n")
        
        return True
        
    except Exception as e:
        print(f"WhatsApp Web URL error: {e}")
        return False

def send_lead_notification(lead):
    """Send lead notification to sales team"""
    try:
        sales_email = os.environ.get('SALES_EMAIL', 'info@queenvillaofficial.com')
        
        subject = f"New Lead: {lead.name} - Beylerbeyi Residences"
        
        body = f"""
New lead received for Beylerbeyi Bosphorus Residences:

Name: {lead.name}
Phone: {lead.phone}
Email: {lead.email or 'Not provided'}
Language: {lead.language}
Unit Interest: {lead.unit_interest or 'Not specified'}
Budget Range: {lead.budget_range or 'Not specified'}
Timeline: {lead.timeline or 'Not specified'}
Best Call Time: {lead.best_call_time or 'Not specified'}
WhatsApp Opt-in: {'Yes' if lead.whatsapp_optin else 'No'}
Marketing Consent: {'Yes' if lead.marketing_consent else 'No'}

UTM Data:
Source: {lead.utm_source or 'Direct'}
Medium: {lead.utm_medium or 'None'}
Campaign: {lead.utm_campaign or 'None'}

Submitted: {lead.created_at}
IP: {lead.ip_address}
        """
        
        msg = Message(
            subject=subject,
            recipients=[sales_email],
            body=body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Error sending lead notification: {e}")
        return False

def send_auto_reply(lead):
    """Send auto-reply to lead"""
    try:
        if not lead.email:
            return False
            
        translations = {
            'tr': {
                'subject': 'Beylerbeyi Boğaz Rezidansları - Bilgileriniz Alındı',
                'greeting': f'Sayın {lead.name},',
                'message': 'Beylerbeyi Boğaz Rezidansları ile ilgili gösterdiğiniz ilgi için teşekkür ederiz. Uzmanlarımız en kısa sürede sizinle iletişime geçecektir.',
                'signature': 'Beylerbeyi Boğaz Rezidansları Satış Ekibi'
            },
            'en': {
                'subject': 'Beylerbeyi Bosphorus Residences - Information Received',
                'greeting': f'Dear {lead.name},',
                'message': 'Thank you for your interest in Beylerbeyi Bosphorus Residences. Our specialists will contact you shortly.',
                'signature': 'Beylerbeyi Bosphorus Residences Sales Team'
            },
            'ar': {
                'subject': 'مساكن بوسفور بييلربيي - تم استلام معلوماتك',
                'greeting': f'عزيزي {lead.name}،',
                'message': 'شكراً لك على اهتمامك بمساكن بوسفور بييلربيي. سيتواصل معك فريق الخبراء لدينا قريباً.',
                'signature': 'فريق مبيعات مساكن بوسفور بييلربيي'
            }
        }
        
        lang_data = translations.get(lead.language, translations['en'])
        
        subject = lang_data['subject']
        body = f"""
{lang_data['greeting']}

{lang_data['message']}

{lang_data['signature']}
        """
        
        msg = Message(
            subject=subject,
            recipients=[lead.email],
            body=body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Error sending auto-reply: {e}")
        return False

def send_whatsapp_notification_simple(lead_data):
    """Send WhatsApp notification for new lead without database dependency"""
    try:
        # Format the message with simple formatting to avoid encoding issues
        message = f"""YENI MUSTERI BASVURUSU - Beylerbeyi Residences

Isim: {lead_data['name']}
Telefon: {lead_data['phone']}
Email: {lead_data['email']}
Dil: {lead_data['language']}
Ilgilendigi Unite: {lead_data['unit_interest']}
Butce: {lead_data['budget_range']}
Zaman Cizelgesi: {lead_data['timeline']}
En Iyi Arama Saati: {lead_data['best_call_time']}
WhatsApp Izni: {lead_data['whatsapp_optin']}
Pazarlama Izni: {lead_data['marketing_consent']}

UTM Bilgileri:
- Kaynak: {lead_data['utm_source']}
- Medium: {lead_data['utm_medium']}
- Kampanya: {lead_data['utm_campaign']}

Tarih: {lead_data['timestamp']}
IP: {lead_data['ip_address']}

Lutfen musteriyle en kisa surede iletisime gecin!"""
        
        print(f"🚨 NEW LEAD SUBMISSION for {WHATSAPP_NUMBER}")
        print(f"Lead: {lead_data['name']} - {lead_data['phone']}")
        
        # Use CallMeBot API
        send_via_callmebot(message)
        
        return True
        
    except Exception as e:
        print(f"Error sending WhatsApp notification: {e}")
        return False
