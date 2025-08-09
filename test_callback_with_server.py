import requests
import json
import threading
import time
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_server():
    """Start the Flask server in a separate thread"""
    try:
        from app import app
        app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Server error: {e}")

def test_callback():
    """Test callback functionality"""
    # Wait for server to start
    time.sleep(2)
    
    url = "http://127.0.0.1:5001/callback-request"
    
    # Test with valid data
    data = {
        'callback_name': 'Test User',
        'callback_phone': '05551234567',
        'language': 'tr'
    }
    
    try:
        print("Testing callback request with valid data...")
        print(f"URL: {url}")
        print(f"Data: {data}")
        
        response = requests.post(url, data=data, timeout=10)
        
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                json_response = response.json()
                print(f"JSON Response: {json.dumps(json_response, indent=2)}")
            except:
                print("Failed to parse JSON response")
                
    except Exception as e:
        print(f"Error: {e}")
    
    # Test with invalid data
    print("\n" + "="*50)
    print("Testing with invalid phone number...")
    
    invalid_data = {
        'callback_name': 'Test User',
        'callback_phone': '123',  # Invalid phone
        'language': 'tr'
    }
    
    try:
        response = requests.post(url, data=invalid_data, timeout=10)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                json_response = response.json()
                print(f"JSON Response: {json.dumps(json_response, indent=2)}")
            except:
                print("Failed to parse JSON response")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Run tests
    test_callback()
    
    print("\nTest completed!")
