"""
Test if admin routes can access the database
"""
from database import SessionLocal, Institute, Student, Certificate

def test_admin_db_access():
    db = SessionLocal()
    try:
        print("\n=== TESTING ADMIN DATABASE ACCESS ===")
        
        # Test direct query
        institutes = db.query(Institute).all()
        students = db.query(Student).all()
        certificates = db.query(Certificate).all()
        
        print(f"Institutes found: {len(institutes)}")
        print(f"Students found: {len(students)}")
        print(f"Certificates found: {len(certificates)}")
        
        print("\n=== TEST COMPLETE ===\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_admin_db_access()
