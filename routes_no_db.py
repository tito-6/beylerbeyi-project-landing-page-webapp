from flask import render_template, request, flash, redirect, url_for, jsonify, session
from app import app
from utils.mail import send_whatsapp_notification_simple
from utils.i18n import get_translations, get_supported_languages
from utils.validation import validate_email, validate_phone, get_validation_error_message
import logging
import os
from datetime import datetime

@app.route('/')
@app.route('/<lang>')
def index(lang='tr'):
    if lang not in get_supported_languages():
        lang = 'tr'
    
    session['language'] = lang
    translations = get_translations(lang)
    
    # Check if we need to show success message and then clear it
    show_success = session.get('lead_submitted', False)
    if show_success:
        session.pop('lead_submitted', None)  # Clear the flag after showing once
    
    return render_template('index.html', 
                         translations=translations, 
                         current_lang=lang,
                         supported_languages=get_supported_languages(),
                         show_success_message=show_success)

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        language = request.form.get('language', 'tr')
        unit_interest = request.form.get('unit_interest', '')
        budget_range = request.form.get('budget_range', '')
        timeline = request.form.get('timeline', '')
        best_call_time = request.form.get('best_call_time', '')
        whatsapp_optin = request.form.get('whatsapp_optin') == 'on'
        marketing_consent = request.form.get('marketing_consent') == 'on'
        kvkk_consent = request.form.get('kvkk_consent') == 'on'
        
        # UTM parameters
        utm_source = request.form.get('utm_source', '')
        utm_medium = request.form.get('utm_medium', '')
        utm_campaign = request.form.get('utm_campaign', '')
        utm_content = request.form.get('utm_content', '')
        utm_term = request.form.get('utm_term', '')
        
        # Validation
        if not name or not phone:
            flash(get_validation_error_message('required_name', language) if not name else get_validation_error_message('required_phone', language), 'error')
            return redirect(url_for('index', lang=language))
        
        # Validate phone number format
        if not validate_phone(phone):
            flash(get_validation_error_message('invalid_phone', language), 'error')
            return redirect(url_for('index', lang=language))
        
        # Validate email format (if provided)
        if email and not validate_email(email):
            flash(get_validation_error_message('invalid_email', language), 'error')
            return redirect(url_for('index', lang=language))
        
        if not kvkk_consent:
            flash('KVKK consent is required', 'error')
            return redirect(url_for('index', lang=language))
        
        # Create lead data object (no database save)
        lead_data = {
            'name': name,
            'phone': phone,
            'email': email or 'Belirtilmedi',
            'language': language,
            'unit_interest': unit_interest or 'Belirtilmedi',
            'budget_range': budget_range or 'Belirtilmedi',
            'timeline': timeline or 'Belirtilmedi',
            'best_call_time': best_call_time or 'Belirtilmedi',
            'whatsapp_optin': 'Evet' if whatsapp_optin else 'Hayir',
            'marketing_consent': 'Evet' if marketing_consent else 'Hayir',
            'kvkk_consent': 'Evet' if kvkk_consent else 'Hayir',
            'utm_source': utm_source or 'Direkt',
            'utm_medium': utm_medium or 'Yok',
            'utm_campaign': utm_campaign or 'Yok',
            'utm_content': utm_content or 'Yok',
            'utm_term': utm_term or 'Yok',
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Send WhatsApp notification
        try:
            send_whatsapp_notification_simple(lead_data)
        except Exception as e:
            logging.error(f"WhatsApp notification error: {e}")
        
        flash('Thank you! We will contact you soon.', 'success')
        session['lead_submitted'] = True
        session['lead_name'] = name
        session['lead_whatsapp'] = whatsapp_optin
        
        return redirect(url_for('success', lang=language))
        
    except Exception as e:
        logging.error(f"Lead submission error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index', lang=language))

@app.route('/success')
@app.route('/success/<lang>')
def success(lang='tr'):
    if lang not in get_supported_languages():
        lang = 'tr'
    
    translations = get_translations(lang)
    
    return render_template('success.html', 
                         translations=translations, 
                         current_lang=lang,
                         supported_languages=get_supported_languages())

@app.route('/callback-request', methods=['POST'])
def callback_request():
    try:
        name = request.form.get('callback_name', '').strip()
        phone = request.form.get('callback_phone', '').strip()
        language = request.form.get('language', 'tr')
        
        if not name or not phone:
            return jsonify({'success': False, 'message': get_validation_error_message('required_name' if not name else 'required_phone', language)})
        
        # Validate phone number format
        if not validate_phone(phone):
            return jsonify({'success': False, 'message': get_validation_error_message('invalid_phone', language)})
        
        # Create callback lead data
        lead_data = {
            'name': name,
            'phone': phone,
            'email': 'Belirtilmedi',
            'language': language,
            'unit_interest': 'callback_request',
            'budget_range': 'Belirtilmedi',
            'timeline': 'Belirtilmedi',
            'best_call_time': 'Belirtilmedi',
            'whatsapp_optin': 'Hayir',
            'marketing_consent': 'Hayir',
            'kvkk_consent': 'Evet',  # Implied for callback
            'utm_source': 'Direkt',
            'utm_medium': 'Yok',
            'utm_campaign': 'Yok',
            'utm_content': 'Yok',
            'utm_term': 'Yok',
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Send WhatsApp notification
        try:
            send_whatsapp_notification_simple(lead_data)
        except Exception as e:
            logging.error(f"Callback notification error: {e}")
        
        return jsonify({'success': True, 'message': 'Callback requested successfully'})
        
    except Exception as e:
        logging.error(f"Callback request error: {e}")
        return jsonify({'success': False, 'message': 'Error occurred'})

@app.route('/kvkk')
@app.route('/kvkk/<lang>')
def kvkk(lang='tr'):
    if lang not in get_supported_languages():
        lang = 'tr'
    
    session['language'] = lang
    translations = get_translations(lang)
    
    return render_template('kvkk.html',
                         translations=translations,
                         current_lang=lang,
                         supported_languages=get_supported_languages())

# Health check endpoint for deployment
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Admin test endpoint for WhatsApp
@app.route('/admin/test-whatsapp')
def test_whatsapp():
    try:
        test_data = {
            'name': 'Test User',
            'phone': '05551234567',
            'email': 'test@example.com',
            'language': 'tr',
            'unit_interest': 'Test',
            'budget_range': 'Test',
            'timeline': 'Test',
            'best_call_time': 'Test',
            'whatsapp_optin': 'Evet',
            'marketing_consent': 'Evet',
            'kvkk_consent': 'Evet',
            'utm_source': 'Test',
            'utm_medium': 'Test',
            'utm_campaign': 'Test',
            'utm_content': 'Test',
            'utm_term': 'Test',
            'ip_address': '127.0.0.1',
            'user_agent': 'Test Agent',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        send_whatsapp_notification_simple(test_data)
        
        return jsonify({
            'status': 'success',
            'message': 'Test WhatsApp message sent',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Test WhatsApp error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
