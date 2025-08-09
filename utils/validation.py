import re

def validate_email(email):
    """
    Validate email address format
    Returns True if valid, False otherwise
    """
    if not email:
        return True  # Email is optional
    
    email = email.strip()
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Check if email matches pattern
    if not re.match(email_pattern, email):
        return False
    
    # Additional checks
    if len(email) > 320:  # Maximum email length
        return False
    
    if '..' in email:  # No consecutive dots
        return False
    
    if email.startswith('.') or email.endswith('.'):  # No dots at start/end
        return False
    
    return True

def validate_phone(phone):
    """
    Validate phone number format
    Accepts Turkish phone numbers in various formats
    Returns True if valid, False otherwise
    """
    if not phone:
        return False  # Phone is required
    
    phone = phone.strip()
    
    # Remove common separators and spaces
    clean_phone = re.sub(r'[\s\-\(\)\+\.]', '', phone)
    
    # Turkish phone number patterns
    patterns = [
        r'^90[0-9]{10}$',        # +905551234567 -> 905551234567
        r'^0[0-9]{10}$',         # 05551234567
        r'^5[0-9]{9}$',          # 5551234567
        r'^[0-9]{10}$',          # 5551234567 (10 digits)
    ]
    
    # Check if phone matches any valid Turkish pattern
    for pattern in patterns:
        if re.match(pattern, clean_phone):
            return True
    
    # Also accept international formats (basic validation)
    if len(clean_phone) >= 10 and len(clean_phone) <= 15 and clean_phone.isdigit():
        return True
    
    return False

def get_validation_error_message(field, lang='tr'):
    """
    Get validation error message in specified language
    """
    messages = {
        'tr': {
            'invalid_email': 'Geçersiz e-posta adresi formatı',
            'invalid_phone': 'Geçersiz telefon numarası formatı. Lütfen Türk telefon numarası formatında giriniz (örn: 0555 123 45 67)',
            'required_phone': 'Telefon numarası gereklidir',
            'required_name': 'İsim gereklidir'
        },
        'en': {
            'invalid_email': 'Invalid email address format',
            'invalid_phone': 'Invalid phone number format. Please enter a valid Turkish phone number (e.g., 0555 123 45 67)',
            'required_phone': 'Phone number is required',
            'required_name': 'Name is required'
        },
        'ar': {
            'invalid_email': 'تنسيق عنوان البريد الإلكتروني غير صحيح',
            'invalid_phone': 'تنسيق رقم الهاتف غير صحيح. يرجى إدخال رقم هاتف تركي صحيح',
            'required_phone': 'رقم الهاتف مطلوب',
            'required_name': 'الاسم مطلوب'
        }
    }
    
    return messages.get(lang, messages['tr']).get(field, 'Validation error')
