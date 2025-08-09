import json
import os

def get_translations(language='tr'):
    """Get translations for specified language"""
    try:
        file_path = os.path.join('lang', f'{language}.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Fallback to Turkish if language file not found
        try:
            with open('lang/tr.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

def get_supported_languages():
    """Get list of supported languages"""
    return ['tr', 'en', 'ar']
