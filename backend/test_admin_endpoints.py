"""
Test script to verify admin endpoints are working
Run this after starting the backend server
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Test admin login"""
    print("\n=== Testing Admin Login ===")
    response = requests.post(
        f"{BASE_URL}/auth/admin/login",
        json={"username": "admin", "password": "admin123"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful")
        return data["access_token"]
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_admin_endpoints(token):
    """Test all admin endpoints"""
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        "/admin/analytics",
        "/admin/institutes",
        "/admin/students",
        "/admin/verifiers",
        "/admin/verifications",
        "/admin/certificates",
        "/admin/feedback"
    ]
    
    print("\n=== Testing Admin Endpoints ===")
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: {response.status_code} - {json.dumps(data, indent=2)[:100]}...")
            else:
                print(f"❌ {endpoint}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {str(e)}")

def main():
    print("🔍 Testing CertiSense Admin Backend")
    print("=" * 50)
    
    # Test login
    token = test_admin_login()
    if not token:
        print("\n❌ Cannot proceed without valid token")
        return
    
    # Test endpoints
    test_admin_endpoints(token)
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")

if __name__ == "__main__":
    main()
