import requests
import json

# Test callback request functionality
url = "http://127.0.0.1:5000/callback-request"

# Test data
data = {
    'callback_name': 'Test User',
    'callback_phone': '05551234567',
    'language': 'tr'
}

try:
    print("Testing callback request...")
    print(f"URL: {url}")
    print(f"Data: {data}")
    
    response = requests.post(url, data=data)
    
    print(f"\nResponse Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Content: {response.text}")
    
    if response.headers.get('content-type', '').startswith('application/json'):
        try:
            json_response = response.json()
            print(f"JSON Response: {json.dumps(json_response, indent=2)}")
        except:
            print("Failed to parse JSON response")
            
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
except Exception as e:
    print(f"Error: {e}")

# Also test with invalid data
print("\n" + "="*50)
print("Testing with invalid phone number...")

invalid_data = {
    'callback_name': 'Test User',
    'callback_phone': '123',  # Invalid phone
    'language': 'tr'
}

try:
    response = requests.post(url, data=invalid_data)
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
