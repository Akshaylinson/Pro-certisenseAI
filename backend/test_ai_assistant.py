#!/usr/bin/env python3
"""
Test script for AI Assistant Widget functionality
"""

import requests
import json

def test_ai_endpoints():
    """Test AI query endpoints with proper authentication"""
    
    base_url = "http://localhost:8000"
    
    # Test queries for each role
    test_cases = [
        {
            "role": "admin",
            "login_endpoint": "/auth/admin/login",
            "ai_endpoint": "/admin/ai-query",
            "credentials": {"username": "admin", "password": "admin123"},
            "test_queries": [
                "How many certificates are in the system?",
                "Which institute issued the most certificates?",
                "Show me details of student INST00001-00001",
                "List all verifiers"
            ]
        },
        {
            "role": "institute", 
            "login_endpoint": "/auth/institute/login",
            "ai_endpoint": "/institute/ai-query",
            "credentials": {"username": "admin@mitaluva.edu", "password": "institute123"},
            "test_queries": [
                "How many students are in my institute?",
                "How many certificates did we issue today?",
                "Show me student INST00001-00001 details"
            ]
        },
        {
            "role": "verifier",
            "login_endpoint": "/auth/verifier/login", 
            "ai_endpoint": "/verifier/ai-query",
            "credentials": {"username": "verifier_001", "password": "verifier123"},
            "test_queries": [
                "How many verifications have I performed?",
                "Show my verification history",
                "Check certificate CERT-123"
            ]
        }
    ]
    
    print("🤖 Testing AI Assistant Widget Endpoints")
    print("=" * 50)
    
    for test_case in test_cases:
        print(f"\n🔍 Testing {test_case['role'].upper()} AI Assistant")
        print("-" * 30)
        
        try:
            # Step 1: Login
            print(f"1. Logging in as {test_case['role']}...")
            login_response = requests.post(
                f"{base_url}{test_case['login_endpoint']}", 
                json=test_case['credentials']
            )
            
            if login_response.status_code == 200:
                token = login_response.json()["access_token"]
                print("   ✓ Login successful!")
                
                # Step 2: Test AI queries
                headers = {"Authorization": f"Bearer {token}"}
                
                for i, query in enumerate(test_case['test_queries'], 1):
                    print(f"\n2.{i} Testing query: '{query}'")
                    
                    ai_response = requests.post(
                        f"{base_url}{test_case['ai_endpoint']}",
                        json={"query": query, "session_id": f"test_session_{test_case['role']}"},
                        headers=headers
                    )
                    
                    if ai_response.status_code == 200:
                        response_data = ai_response.json()
                        print(f"     ✓ AI Response: {response_data['response'][:100]}...")
                    else:
                        print(f"     ✗ AI Query failed: {ai_response.status_code}")
                        print(f"       Error: {ai_response.text}")
                        
            else:
                print(f"   ✗ Login failed: {login_response.status_code}")
                print(f"     Error: {login_response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ✗ Cannot connect to backend server!")
            print("     Make sure to run: python -m uvicorn certisense_main:app --reload --port 8000")
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 AI Assistant Widget Testing Complete!")

def show_usage_instructions():
    """Show how to use the AI assistant widgets"""
    print("🚀 AI Assistant Widget Usage Instructions")
    print("=" * 50)
    print()
    print("1. Start the backend server:")
    print("   cd backend")
    print("   python -m uvicorn certisense_main:app --reload --port 8000")
    print()
    print("2. Start the frontend:")
    print("   cd frontend/web")
    print("   npm run dev")
    print()
    print("3. Access dashboards:")
    print("   • Admin: http://localhost:5173 (admin/admin123)")
    print("   • Institute: Register or use existing institute")
    print("   • Verifier: Register or use existing verifier")
    print()
    print("4. Look for the floating AI assistant button:")
    print("   • Bottom-right corner of each dashboard")
    print("   • Blue circular button with AI icon")
    print("   • Click to open chat dialog")
    print()
    print("5. Example questions to ask:")
    print()
    print("   Admin AI Assistant:")
    print("   • 'How many certificates are issued?'")
    print("   • 'Which institute has the most students?'")
    print("   • 'Show me student INST00001-00001 details'")
    print("   • 'List all verifiers in the system'")
    print()
    print("   Institute AI Assistant:")
    print("   • 'How many students are in my institute?'")
    print("   • 'How many certificates did we issue today?'")
    print("   • 'Show me details of student INST00001-00001'")
    print()
    print("   Verifier AI Assistant:")
    print("   • 'How many verifications have I performed?'")
    print("   • 'Show my recent verification history'")
    print("   • 'Check status of certificate CERT-123'")
    print()
    print("6. Features:")
    print("   • Real-time AI responses")
    print("   • Role-based data access")
    print("   • Chat history within session")
    print("   • Loading indicators")
    print("   • Clear chat functionality")
    print()

if __name__ == "__main__":
    show_usage_instructions()
    print()
    test_ai_endpoints()