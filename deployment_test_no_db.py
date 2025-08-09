#!/usr/bin/env python3
"""
Deployment Test Script - No Database Version
Tests all functionality without database dependencies
"""

import requests
import json
import threading
import time
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_server():
    """Start Flask server for testing"""
    try:
        from app import app
        app.run(host='127.0.0.1', port=5002, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Server error: {e}")

def test_endpoints():
    """Test all application endpoints"""
    time.sleep(2)  # Wait for server to start
    
    base_url = "http://127.0.0.1:5002"
    results = []
    
    # Test cases
    tests = [
        {
            'name': 'Home Page (Turkish)',
            'method': 'GET',
            'url': f'{base_url}/',
            'expected_status': 200
        },
        {
            'name': 'Home Page (English)', 
            'method': 'GET',
            'url': f'{base_url}/en',
            'expected_status': 200
        },
        {
            'name': 'KVKK Page',
            'method': 'GET', 
            'url': f'{base_url}/kvkk/tr',
            'expected_status': 200
        },
        {
            'name': 'Health Check',
            'method': 'GET',
            'url': f'{base_url}/health',
            'expected_status': 200
        },
        {
            'name': 'WhatsApp Test (Admin)',
            'method': 'GET',
            'url': f'{base_url}/admin/test-whatsapp',
            'expected_status': 200
        },
        {
            'name': 'Valid Lead Submission',
            'method': 'POST',
            'url': f'{base_url}/submit-lead',
            'data': {
                'name': 'Test User',
                'phone': '05551234567',
                'email': 'test@example.com',
                'language': 'tr',
                'kvkk_consent': 'on'
            },
            'expected_status': 302,  # Redirect after successful submission
            'allow_redirects': False  # Don't follow redirects to test redirect status
        },
        {
            'name': 'Valid Callback Request',
            'method': 'POST',
            'url': f'{base_url}/callback-request',
            'data': {
                'callback_name': 'Callback User',
                'callback_phone': '05559876543',
                'language': 'tr'
            },
            'expected_status': 200
        },
        {
            'name': 'Invalid Callback Request',
            'method': 'POST',
            'url': f'{base_url}/callback-request',
            'data': {
                'callback_name': 'Invalid User',
                'callback_phone': '123',  # Invalid phone
                'language': 'tr'
            },
            'expected_status': 200
        }
    ]
    
    print("🧪 Starting Deployment Tests...")
    print("=" * 60)
    
    for test in tests:
        try:
            print(f"Testing: {test['name']}...")
            
            if test['method'] == 'GET':
                response = requests.get(test['url'], timeout=10)
            else:
                allow_redirects = test.get('allow_redirects', True)
                response = requests.post(test['url'], data=test.get('data', {}), timeout=10, allow_redirects=allow_redirects)
            
            status_ok = response.status_code == test['expected_status']
            
            result = {
                'name': test['name'],
                'status': '✅ PASS' if status_ok else '❌ FAIL',
                'expected': test['expected_status'],
                'actual': response.status_code,
                'details': ''
            }
            
            # Additional checks for specific endpoints
            if test['name'] == 'Health Check' and status_ok:
                try:
                    health_data = response.json()
                    if 'status' in health_data and health_data['status'] == 'healthy':
                        result['details'] = f"✅ Health status: {health_data['status']}"
                    else:
                        result['status'] = '⚠️ WARN'
                        result['details'] = "Health endpoint returned unexpected data"
                except:
                    result['status'] = '⚠️ WARN'
                    result['details'] = "Health endpoint didn't return JSON"
            
            elif test['name'] == 'Valid Callback Request' and status_ok:
                try:
                    callback_data = response.json()
                    if callback_data.get('success'):
                        result['details'] = "✅ Callback request succeeded"
                    else:
                        result['status'] = '❌ FAIL'
                        result['details'] = f"Callback failed: {callback_data.get('message', 'Unknown error')}"
                except:
                    result['status'] = '❌ FAIL'
                    result['details'] = "Callback endpoint didn't return JSON"
            
            elif test['name'] == 'Invalid Callback Request' and status_ok:
                try:
                    callback_data = response.json()
                    if not callback_data.get('success'):
                        result['details'] = "✅ Validation correctly rejected invalid phone"
                    else:
                        result['status'] = '❌ FAIL'
                        result['details'] = "Validation should have rejected invalid phone"
                except:
                    result['status'] = '❌ FAIL'
                    result['details'] = "Invalid callback test didn't return JSON"
            
            elif 'Home Page' in test['name'] and status_ok:
                if 'Beylerbeyi' in response.text:
                    result['details'] = "✅ Page content looks correct"
                else:
                    result['status'] = '⚠️ WARN'
                    result['details'] = "Page content may be missing"
            
            results.append(result)
            
        except requests.exceptions.RequestException as e:
            results.append({
                'name': test['name'],
                'status': '❌ FAIL',
                'expected': test['expected_status'],
                'actual': 'CONNECTION_ERROR',
                'details': f"Connection error: {str(e)}"
            })
        except Exception as e:
            results.append({
                'name': test['name'],
                'status': '❌ FAIL',
                'expected': test['expected_status'],
                'actual': 'ERROR',
                'details': f"Test error: {str(e)}"
            })
    
    # Print results
    print("\n📊 TEST RESULTS:")
    print("=" * 60)
    
    passed = failed = warned = 0
    
    for result in results:
        status_symbol = result['status'][:2]
        print(f"{status_symbol} {result['name']}")
        print(f"   Expected: {result['expected']} | Actual: {result['actual']}")
        if result['details']:
            print(f"   {result['details']}")
        print()
        
        if '✅' in result['status']:
            passed += 1
        elif '❌' in result['status']:
            failed += 1
        else:
            warned += 1
    
    print(f"📈 SUMMARY: {passed} passed, {failed} failed, {warned} warnings")
    
    if failed == 0:
        print("\n🎉 ALL CRITICAL TESTS PASSED - READY FOR DEPLOYMENT!")
        return True
    else:
        print(f"\n⚠️  {failed} TESTS FAILED - FIX ISSUES BEFORE DEPLOYMENT")
        return False

if __name__ == "__main__":
    print("🚀 Estate Vue - Deployment Readiness Test (No Database)")
    print("=" * 60)
    
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Run tests
    success = test_endpoints()
    
    if success:
        print("\n✅ DEPLOYMENT READY!")
        print("Next steps:")
        print("1. Set environment variables in your deployment platform")
        print("2. Deploy to your chosen platform (Heroku, Railway, Vercel, etc.)")
        print("3. Test live URL after deployment")
        exit(0)
    else:
        print("\n❌ NOT READY FOR DEPLOYMENT")
        print("Please fix the failing tests before deploying")
        exit(1)
