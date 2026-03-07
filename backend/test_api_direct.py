"""
Direct API test - Check what admin endpoints actually return
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Login as admin
print("Logging in as admin...")
response = requests.post(
    f"{BASE_URL}/auth/admin/login",
    json={"username": "admin", "password": "admin123"}
)

if response.status_code != 200:
    print(f"Login failed: {response.status_code}")
    print(response.text)
    exit(1)

token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

print(f"Token: {token[:20]}...\n")

# Test admin endpoints
endpoints = [
    "/admin/students",
    "/admin/certificates",
    "/admin/analytics"
]

for endpoint in endpoints:
    print(f"\n{'='*60}")
    print(f"Testing: {endpoint}")
    print('='*60)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

print(f"\n{'='*60}")
print("Test complete")
print('='*60)
