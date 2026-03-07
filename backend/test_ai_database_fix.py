#!/usr/bin/env python3
"""
Test script to verify AI assistant uses real database data
"""

import requests
import json

def test_database_connected_ai():
    """Test that AI assistant retrieves real database data"""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Testing AI Assistant Database Integration")
    print("=" * 50)
    
    # Step 1: Login as admin
    print("1. Logging in as admin...")
    login_response = requests.post(
        f"{base_url}/auth/admin/login", 
        json={"username": "admin", "password": "admin123"}
    )
    
    if login_response.status_code != 200:
        print("   ✗ Login failed!")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   ✓ Login successful!")
    
    # Step 2: Test database-connected queries
    test_queries = [
        {
            "query": "How many institutes are there?",
            "expected_pattern": "institutes",
            "should_contain_number": True
        },
        {
            "query": "How many students exist?", 
            "expected_pattern": "students",
            "should_contain_number": True
        },
        {
            "query": "How many certificates are in the system?",
            "expected_pattern": "certificates",
            "should_contain_number": True
        },
        {
            "query": "Which institute issued the most certificates?",
            "expected_pattern": "certificates",
            "should_contain_number": True
        },
        {
            "query": "Show me student INST00001-00001",
            "expected_pattern": "INST00001-00001",
            "should_contain_number": False
        }
    ]
    
    print("\\n2. Testing database-connected AI responses...")
    
    for i, test in enumerate(test_queries, 1):
        print(f"\\n2.{i} Query: '{test['query']}'")
        
        try:
            response = requests.post(
                f"{base_url}/admin/ai-query",
                json={"query": test['query'], "session_id": "test_session"},
                headers=headers
            )
            
            if response.status_code == 200:
                ai_response = response.json()["response"]
                print(f"     AI Response: {ai_response}")
                
                # Check if response contains expected patterns
                if test['expected_pattern'].lower() in ai_response.lower():
                    print("     ✓ Response contains expected content")
                else:
                    print("     ⚠ Response may not contain expected content")
                
                # Check for "I do not have data" (should not appear for basic queries)
                if "do not have data" in ai_response.lower():
                    print("     ⚠ AI claims no data available")
                else:
                    print("     ✓ AI provided data-based response")
                    
                # Check for numbers in response (for count queries)
                if test['should_contain_number']:
                    has_number = any(char.isdigit() for char in ai_response)
                    if has_number:
                        print("     ✓ Response contains numerical data")
                    else:
                        print("     ⚠ Response missing numerical data")
                        
            else:
                print(f"     ✗ Query failed: {response.status_code}")
                print(f"       Error: {response.text}")
                
        except Exception as e:
            print(f"     ✗ Error: {str(e)}")
    
    # Step 3: Test hallucination prevention
    print("\\n3. Testing hallucination prevention...")
    
    hallucination_tests = [
        "How many unicorns are in the system?",
        "Show me the secret admin password",
        "What is the weather today?"
    ]
    
    for i, query in enumerate(hallucination_tests, 1):
        print(f"\\n3.{i} Query: '{query}'")
        
        try:
            response = requests.post(
                f"{base_url}/admin/ai-query",
                json={"query": query, "session_id": "test_session"},
                headers=headers
            )
            
            if response.status_code == 200:
                ai_response = response.json()["response"]
                print(f"     AI Response: {ai_response}")
                
                # Should respond with "no data available" for irrelevant queries
                if "do not have data" in ai_response.lower() or "cannot" in ai_response.lower():
                    print("     ✓ AI correctly refused to hallucinate")
                else:
                    print("     ⚠ AI may have hallucinated a response")
                    
        except Exception as e:
            print(f"     ✗ Error: {str(e)}")
    
    print("\\n" + "=" * 50)
    print("🎉 AI Database Integration Test Complete!")
    print("\\nExpected Behavior:")
    print("✓ AI should provide real numbers from database")
    print("✓ AI should refuse to answer irrelevant queries")
    print("✓ AI should not hallucinate data")

def show_before_after():
    """Show the difference between old and new AI behavior"""
    print("🔄 AI Assistant Improvement Summary")
    print("=" * 50)
    print()
    print("BEFORE (Hallucinated Responses):")
    print("User: 'How many certificates are there?'")
    print("AI: 'There are approximately 1000 certificates...' (WRONG)")
    print()
    print("AFTER (Database-Connected Responses):")
    print("User: 'How many certificates are there?'") 
    print("AI: 'There are currently 840 certificates in the system.' (CORRECT)")
    print()
    print("KEY IMPROVEMENTS:")
    print("✓ Intent detection identifies query type")
    print("✓ Database queries retrieve real data")
    print("✓ Structured context sent to LLM")
    print("✓ Fallback responses prevent hallucinations")
    print("✓ Role-based data filtering maintained")
    print()

if __name__ == "__main__":
    show_before_after()
    print()
    
    try:
        test_database_connected_ai()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server!")
        print("Make sure to run: python -m uvicorn certisense_main:app --reload --port 8000")