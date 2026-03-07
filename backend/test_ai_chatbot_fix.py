#!/usr/bin/env python3

"""
Test script to verify the AI chatbot database connection fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_query_service import AIQueryService
from database import get_db

def test_admin_queries():
    """Test admin queries with database connection"""
    print("=== Testing Admin AI Queries ===")
    
    ai_service = AIQueryService()
    db = next(get_db())
    
    test_queries = [
        "How many institutes are there?",
        "Total number of students?",
        "Show me certificate statistics",
        "What can you help me with?",
        "Give me system overview"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = ai_service.process_admin_query(query, db)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    db.close()

def test_intent_detection():
    """Test intent detection improvements"""
    print("\n=== Testing Intent Detection ===")
    
    ai_service = AIQueryService()
    
    test_cases = [
        ("How many institutes?", "count_institutes"),
        ("Total students", "count_students"),
        ("Show me certificates", "count_certificates"),
        ("List verifiers", "list_verifiers"),
        ("Help me", "help"),
        ("System statistics", "general_stats"),
        ("Today's activity", "today_activity"),
        ("Student INST00001-00001 details", "student_details")
    ]
    
    for query, expected in test_cases:
        detected = ai_service.detect_intent(query)
        status = "PASS" if detected == expected else "FAIL"
        print(f"{status} '{query}' -> {detected} (expected: {expected})")

if __name__ == "__main__":
    print("Testing AI Chatbot Database Connection Fix")
    print("=" * 50)
    
    test_intent_detection()
    test_admin_queries()
    
    print("\n" + "=" * 50)
    print("Test completed!")