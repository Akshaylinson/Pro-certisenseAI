#!/usr/bin/env python3
"""
Test script for AI report API endpoints
"""

import requests
import json

def test_api_endpoints():
    """Test the report API endpoints"""
    base_url = "http://localhost:8000/admin/reports"
    
    # Mock admin token (you'll need to replace with actual token)
    headers = {
        "Authorization": "Bearer mock_admin_token",
        "Content-Type": "application/json"
    }
    
    endpoints = [
        ("institute", "Institute Report"),
        ("certificates", "Certificate Report"), 
        ("verifications", "Verification Report"),
        ("system", "System Report")
    ]
    
    print("Testing AI Report API Endpoints")
    print("=" * 40)
    
    for endpoint, name in endpoints:
        try:
            print(f"Testing {name}...")
            url = f"{base_url}/{endpoint}"
            print(f"URL: {url}")
            
            # Note: This will fail without proper authentication
            # But shows the endpoint structure
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"  Success! Generated report with:")
                print(f"  - Metrics: {len(data.get('metrics', {}))}")
                print(f"  - AI Summary: {data.get('ai_summary', '')[:50]}...")
                print(f"  - Chart URL: {data.get('chart_url', '')}")
            else:
                print(f"  Status: {response.status_code}")
                print(f"  Response: {response.text[:100]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"  Connection failed - FastAPI server not running")
        except Exception as e:
            print(f"  Error: {str(e)}")
        
        print()

def show_api_documentation():
    """Show API documentation"""
    print("AI-Powered Report API Documentation")
    print("=" * 40)
    print()
    print("Base URL: http://localhost:8000/admin/reports")
    print()
    print("Endpoints:")
    print("  GET /admin/reports/institute")
    print("  GET /admin/reports/certificates") 
    print("  GET /admin/reports/verifications")
    print("  GET /admin/reports/system")
    print()
    print("Headers Required:")
    print("  Authorization: Bearer <admin_token>")
    print()
    print("Response Format:")
    print("  {")
    print("    'metrics': { ... },")
    print("    'ai_summary': 'AI generated analysis...',")
    print("    'chart_url': '/uploads/reports/chart_123.png',")
    print("    'generated_at': '2024-01-01T12:00:00'")
    print("  }")
    print()

if __name__ == "__main__":
    show_api_documentation()
    print()
    test_api_endpoints()