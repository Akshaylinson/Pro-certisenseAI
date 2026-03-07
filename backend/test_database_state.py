#!/usr/bin/env python3
"""
Test script to verify database seeding and reset functionality
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, Institute, Student, Certificate, Verifier, Verification, Feedback

def test_database_state():
    """Test and display current database state"""
    db = SessionLocal()
    
    try:
        print("Current Database State:")
        print("=" * 30)
        
        # Count records in each table
        institutes = db.query(Institute).count()
        students = db.query(Student).count()
        certificates = db.query(Certificate).count()
        verifiers = db.query(Verifier).count()
        verifications = db.query(Verification).count()
        feedbacks = db.query(Feedback).count()
        
        print(f"Institutes: {institutes}")
        print(f"Students: {students}")
        print(f"Certificates: {certificates}")
        print(f"Verifiers: {verifiers}")
        print(f"Verifications: {verifications}")
        print(f"Feedbacks: {feedbacks}")
        
        # Check certificate files
        cert_dir = "uploads/certificates"
        pdf_count = 0
        if os.path.exists(cert_dir):
            pdf_files = [f for f in os.listdir(cert_dir) if f.endswith('.pdf')]
            pdf_count = len(pdf_files)
        
        print(f"PDF Files: {pdf_count}")
        print("=" * 30)
        
        # Show sample data if available
        if institutes > 0:
            print("\nSample Institute:")
            sample_institute = db.query(Institute).first()
            print(f"  ID: {sample_institute.institute_id}")
            print(f"  Name: {sample_institute.name}")
            print(f"  Email: {sample_institute.email}")
            print(f"  Location: {sample_institute.location}")
        
        if students > 0:
            print("\nSample Student:")
            sample_student = db.query(Student).first()
            print(f"  ID: {sample_student.student_id}")
            print(f"  Name: {sample_student.name}")
            print(f"  Email: {sample_student.email}")
            print(f"  Program: {sample_student.program}")
        
        if certificates > 0:
            print("\nSample Certificate:")
            sample_cert = db.query(Certificate).first()
            print(f"  ID: {sample_cert.id}")
            print(f"  Name: {sample_cert.name}")
            print(f"  Hash: {sample_cert.hash[:20]}...")
            print(f"  Status: {sample_cert.status}")
        
        if verifiers > 0:
            print("\nSample Verifier:")
            sample_verifier = db.query(Verifier).first()
            print(f"  Username: {sample_verifier.username}")
            print(f"  Email: {sample_verifier.email}")
            print(f"  Company: {sample_verifier.company_name}")
            print(f"  Type: {sample_verifier.verifier_type}")
        
        total_records = institutes + students + certificates + verifiers + verifications + feedbacks
        
        if total_records == 0:
            print("\nDatabase is empty - ready for seeding")
        else:
            print(f"\nTotal records: {total_records}")
            print("Use reset_database.py to clean before seeding")
        
    except Exception as e:
        print(f"❌ Error checking database state: {str(e)}")
    finally:
        db.close()

def main():
    print("CertiSense AI v3.0 - Database State Test")
    print("=" * 50)
    test_database_state()
    print("=" * 50)

if __name__ == "__main__":
    main()