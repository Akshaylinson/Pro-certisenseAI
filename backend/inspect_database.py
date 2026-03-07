"""
Database inspection script - Check what data exists
"""
from database import SessionLocal, Institute, Student, Certificate, Verifier, Verification

def inspect_database():
    db = SessionLocal()
    try:
        print("\n" + "="*60)
        print("DATABASE INSPECTION")
        print("="*60)
        
        # Check Institutes
        institutes = db.query(Institute).all()
        print(f"\nINSTITUTES: {len(institutes)}")
        for inst in institutes:
            print(f"  - {inst.institute_id}: {inst.name} (UUID: {inst.id})")
        
        # Check Students
        students = db.query(Student).all()
        print(f"\nSTUDENTS: {len(students)}")
        for student in students:
            print(f"  - {student.student_id}: {student.name}")
            print(f"    UUID: {student.id}")
            print(f"    Institute UUID: {student.institute_id}")
        
        # Check Certificates
        certificates = db.query(Certificate).all()
        print(f"\nCERTIFICATES: {len(certificates)}")
        for cert in certificates:
            print(f"  - {cert.id}: {cert.name}")
            print(f"    Student UUID: {cert.student_id}")
            print(f"    Institute UUID: {cert.institute_id}")
            print(f"    Status: {cert.status}")
        
        # Check Verifiers
        verifiers = db.query(Verifier).all()
        print(f"\nVERIFIERS: {len(verifiers)}")
        for verifier in verifiers:
            print(f"  - {verifier.username}: {verifier.email}")
        
        # Check Verifications
        verifications = db.query(Verification).all()
        print(f"\nVERIFICATIONS: {len(verifications)}")
        for verif in verifications:
            print(f"  - {verif.id}: Result={verif.result}")
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total Institutes: {len(institutes)}")
        print(f"Total Students: {len(students)}")
        print(f"Total Certificates: {len(certificates)}")
        print(f"Total Verifiers: {len(verifiers)}")
        print(f"Total Verifications: {len(verifications)}")
        print("="*60 + "\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    inspect_database()
