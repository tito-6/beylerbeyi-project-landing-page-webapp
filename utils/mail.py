from flask_mail import Message
from app import mail
import os

def send_lead_notification(lead):
    """Send lead notification to sales team"""
    try:
        sales_email = os.environ.get('SALES_EMAIL', 'sales@example.com')
        
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
