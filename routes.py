from flask import render_template, request, flash, redirect, url_for, jsonify, session
from app import app, db
from models import Lead
from utils.mail import send_lead_notification, send_auto_reply
from utils.i18n import get_translations, get_supported_languages
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
    
    return render_template('index.html', 
                         translations=translations, 
                         current_lang=lang,
                         supported_languages=get_supported_languages())

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
            flash('Name and phone are required', 'error')
            return redirect(url_for('index', lang=language))
        
        if not kvkk_consent:
            flash('KVKK consent is required', 'error')
            return redirect(url_for('index', lang=language))
        
        # Create lead
        lead = Lead(
            name=name,
            phone=phone,
            email=email,
            language=language,
            unit_interest=unit_interest,
            budget_range=budget_range,
            timeline=timeline,
            best_call_time=best_call_time,
            whatsapp_optin=whatsapp_optin,
            marketing_consent=marketing_consent,
            kvkk_consent=kvkk_consent,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            utm_content=utm_content,
            utm_term=utm_term,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        
        db.session.add(lead)
        db.session.commit()
        
        # Send notifications
        try:
            send_lead_notification(lead)
            if email:
                send_auto_reply(lead)
        except Exception as e:
            logging.error(f"Email notification error: {e}")
        
        flash('Thank you! We will contact you soon.', 'success')
        session['lead_submitted'] = True
        session['lead_name'] = name
        session['lead_whatsapp'] = whatsapp_optin
        
        return redirect(url_for('index', lang=language) + '#success')
        
    except Exception as e:
        logging.error(f"Lead submission error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index', lang=language))

@app.route('/callback-request', methods=['POST'])
def callback_request():
    try:
        name = request.form.get('callback_name', '').strip()
        phone = request.form.get('callback_phone', '').strip()
        language = request.form.get('language', 'tr')
        
        if not name or not phone:
            return jsonify({'success': False, 'message': 'Name and phone required'})
        
        # Create quick callback lead
        lead = Lead(
            name=name,
            phone=phone,
            language=language,
            unit_interest='callback_request',
            kvkk_consent=True,  # Implied for callback
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        
        db.session.add(lead)
        db.session.commit()
        
        # Send notification
        try:
            send_lead_notification(lead)
        except Exception as e:
            logging.error(f"Callback notification error: {e}")
        
        return jsonify({'success': True, 'message': 'Callback requested successfully'})
        
    except Exception as e:
        logging.error(f"Callback request error: {e}")
        return jsonify({'success': False, 'message': 'Error occurred'})

@app.context_processor
def inject_globals():
    return {
        'GOOGLE_MAPS_API_KEY': os.environ.get('GOOGLE_MAPS_API_KEY', ''),
        'GA4_ID': os.environ.get('GA4_ID', ''),
        'GTM_ID': os.environ.get('GTM_ID', ''),
        'META_PIXEL_ID': os.environ.get('META_PIXEL_ID', ''),
        'LINKEDIN_ID': os.environ.get('LINKEDIN_ID', '')
    }
