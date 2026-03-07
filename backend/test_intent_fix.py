#!/usr/bin/env python3
"""
Quick test for intent detection fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_query_service import AIQueryService

def test_intent_detection():
    """Test intent detection with various query formats"""
    
    service = AIQueryService()
    
    test_queries = [
        ("total number of institutes", "count_institutes"),
        ("how many institutes", "count_institutes"), 
        ("total institutes", "count_institutes"),
        ("number of institutes", "count_institutes"),
        ("count of institutes", "count_institutes"),
        ("how many students", "count_students"),
        ("total number of students", "count_students"),
        ("total certificates", "count_certificates"),
        ("number of certificates", "count_certificates"),
        ("how many verifiers", "count_verifiers"),
        ("total verifications", "count_verifications"),
        ("show student INST00001-00001", "student_details"),
        ("which institute issued most", "top_institute"),
        ("list verifiers", "list_verifiers"),
        ("random question", "general")
    ]
    
    print("Testing Intent Detection Fix")
    print("=" * 40)
    
    for query, expected_intent in test_queries:
        detected_intent = service.detect_intent(query)
        status = "PASS" if detected_intent == expected_intent else "FAIL"
        print(f"{status} '{query}' -> {detected_intent} (expected: {expected_intent})")
    
    print("\n" + "=" * 40)
    print("Intent detection test complete!")

if __name__ == "__main__":
    test_intent_detection()