#!/usr/bin/env python3
"""
Quick test script to verify AI report endpoints work
"""

import requests
import json

def test_reports_with_auth():
    """Test reports with proper admin authentication"""
    
    # Step 1: Login as admin to get token
    login_url = "http://localhost:8000/auth/admin/login"
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        print("1. Logging in as admin...")
        login_response = requests.post(login_url, json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("   ✓ Login successful!")
            
            # Step 2: Test report endpoints
            headers = {"Authorization": f"Bearer {token}"}
            base_url = "http://localhost:8000/admin/reports"
            
            reports = [
                ("institute", "Institute Report"),
                ("certificates", "Certificate Report"),
                ("verifications", "Verification Report"), 
                ("system", "System Report")
            ]
            
            print("\n2. Testing report endpoints...")
            for endpoint, name in reports:
                url = f"{base_url}/{endpoint}"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✓ {name}: Generated successfully")
                    print(f"     - Metrics: {len(data['metrics'])}")
                    print(f"     - Chart: {data['chart_url']}")
                    print(f"     - AI Summary: {data['ai_summary'][:50]}...")
                else:
                    print(f"   ✗ {name}: Failed ({response.status_code})")
                    
        else:
            print(f"   ✗ Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server!")
        print("Make sure to run: python -m uvicorn certisense_main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_reports_with_auth()