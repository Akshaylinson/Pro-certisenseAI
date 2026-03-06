"""
Database Consistency Check Script
CertiSense AI v3.0 - Phase 3 Verification
"""

from sqlalchemy import inspect, MetaData
from database import engine, Base, Institute, Student, Certificate, Verifier, Verification, Feedback, AuditLog
from sqlalchemy.orm import Session
from database import SessionLocal

def check_primary_keys():
    """Verify all tables have primary keys"""
    inspector = inspect(engine)
    results = {}
    
    for table_name in inspector.get_table_names():
        pk = inspector.get_pk_constraint(table_name)
        results[table_name] = {
            "has_primary_key": len(pk['constrained_columns']) > 0,
            "primary_key_columns": pk['constrained_columns']
        }
    
    return results

def check_foreign_keys():
    """Verify all foreign key relationships"""
    inspector = inspect(engine)
    results = {}
    
    for table_name in inspector.get_table_names():
        fks = inspector.get_foreign_keys(table_name)
        results[table_name] = {
            "foreign_key_count": len(fks),
            "foreign_keys": [
                {
                    "constrained_columns": fk['constrained_columns'],
                    "referred_table": fk['referred_table'],
                    "referred_columns": fk['referred_columns']
                }
                for fk in fks
            ]
        }
    
    return results

def check_orphan_records():
    """Check for orphan records (records with invalid foreign keys)"""
    db = SessionLocal()
    orphans = {}
    
    try:
        # Check students without institutes
        students = db.query(Student).all()
        orphan_students = []
        for student in students:
            institute = db.query(Institute).filter(Institute.id == student.institute_id).first()
            if not institute:
                orphan_students.append(student.id)
        orphans['students_without_institute'] = orphan_students
        
        # Check certificates without students
        certificates = db.query(Certificate).all()
        orphan_certs_student = []
        for cert in certificates:
            student = db.query(Student).filter(Student.id == cert.student_id).first()
            if not student:
                orphan_certs_student.append(cert.id)
        orphans['certificates_without_student'] = orphan_certs_student
        
        # Check certificates without institutes
        orphan_certs_institute = []
        for cert in certificates:
            institute = db.query(Institute).filter(Institute.id == cert.institute_id).first()
            if not institute:
                orphan_certs_institute.append(cert.id)
        orphans['certificates_without_institute'] = orphan_certs_institute
        
        # Check verifications without certificates
        verifications = db.query(Verification).all()
        orphan_verifs_cert = []
        for verif in verifications:
            if verif.certificate_id:
                cert = db.query(Certificate).filter(Certificate.id == verif.certificate_id).first()
                if not cert:
                    orphan_verifs_cert.append(verif.id)
        orphans['verifications_without_certificate'] = orphan_verifs_cert
        
        # Check verifications without verifiers
        orphan_verifs_verifier = []
        for verif in verifications:
            verifier = db.query(Verifier).filter(Verifier.id == verif.verifier_id).first()
            if not verifier:
                orphan_verifs_verifier.append(verif.id)
        orphans['verifications_without_verifier'] = orphan_verifs_verifier
        
        # Check feedbacks without verifiers
        feedbacks = db.query(Feedback).all()
        orphan_feedbacks = []
        for feedback in feedbacks:
            verifier = db.query(Verifier).filter(Verifier.id == feedback.verifier_id).first()
            if not verifier:
                orphan_feedbacks.append(feedback.id)
        orphans['feedbacks_without_verifier'] = orphan_feedbacks
        
    finally:
        db.close()
    
    return orphans

def check_duplicate_entities():
    """Check for duplicate records"""
    db = SessionLocal()
    duplicates = {}
    
    try:
        # Check duplicate institute IDs
        institutes = db.query(Institute.institute_id).all()
        institute_ids = [i[0] for i in institutes]
        dup_institutes = [x for x in institute_ids if institute_ids.count(x) > 1]
        duplicates['duplicate_institute_ids'] = list(set(dup_institutes))
        
        # Check duplicate student IDs
        students = db.query(Student.student_id).all()
        student_ids = [s[0] for s in students]
        dup_students = [x for x in student_ids if student_ids.count(x) > 1]
        duplicates['duplicate_student_ids'] = list(set(dup_students))
        
        # Check duplicate certificate hashes
        certificates = db.query(Certificate.hash).all()
        cert_hashes = [c[0] for c in certificates]
        dup_certs = [x for x in cert_hashes if cert_hashes.count(x) > 1]
        duplicates['duplicate_certificate_hashes'] = list(set(dup_certs))
        
        # Check duplicate verifier usernames
        verifiers = db.query(Verifier.username).all()
        verifier_usernames = [v[0] for v in verifiers]
        dup_verifiers = [x for x in verifier_usernames if verifier_usernames.count(x) > 1]
        duplicates['duplicate_verifier_usernames'] = list(set(dup_verifiers))
        
    finally:
        db.close()
    
    return duplicates

def check_table_existence():
    """Verify all required tables exist"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    required_tables = [
        'institutes',
        'students',
        'certificates',
        'verifiers',
        'verifications',
        'feedbacks',
        'audit_logs'
    ]
    
    results = {
        'existing_tables': existing_tables,
        'required_tables': required_tables,
        'missing_tables': [t for t in required_tables if t not in existing_tables],
        'extra_tables': [t for t in existing_tables if t not in required_tables]
    }
    
    return results

def check_relationships():
    """Verify SQLAlchemy relationships are properly configured"""
    relationships = {}
    
    # Institute relationships
    relationships['Institute'] = {
        'students': hasattr(Institute, 'students'),
        'certificates': hasattr(Institute, 'certificates')
    }
    
    # Student relationships
    relationships['Student'] = {
        'institute': hasattr(Student, 'institute'),
        'certificates': hasattr(Student, 'certificates')
    }
    
    # Certificate relationships
    relationships['Certificate'] = {
        'student': hasattr(Certificate, 'student'),
        'institute': hasattr(Certificate, 'institute'),
        'verifications': hasattr(Certificate, 'verifications')
    }
    
    # Verifier relationships
    relationships['Verifier'] = {
        'verifications': hasattr(Verifier, 'verifications'),
        'feedbacks': hasattr(Verifier, 'feedbacks')
    }
    
    # Verification relationships
    relationships['Verification'] = {
        'certificate': hasattr(Verification, 'certificate'),
        'verifier': hasattr(Verification, 'verifier')
    }
    
    # Feedback relationships
    relationships['Feedback'] = {
        'verifier': hasattr(Feedback, 'verifier')
    }
    
    return relationships

def run_full_consistency_check():
    """Run complete database consistency check"""
    print("=" * 80)
    print("CertiSense AI v3.0 - Database Consistency Check")
    print("=" * 80)
    
    # Check 1: Table Existence
    print("\n1. Checking Table Existence...")
    tables = check_table_existence()
    print(f"   ✓ Existing tables: {len(tables['existing_tables'])}")
    print(f"   ✓ Required tables: {len(tables['required_tables'])}")
    print(f"   ✓ Missing tables: {len(tables['missing_tables'])}")
    if tables['missing_tables']:
        print(f"   ⚠ Missing: {tables['missing_tables']}")
    
    # Check 2: Primary Keys
    print("\n2. Checking Primary Keys...")
    pks = check_primary_keys()
    all_have_pk = all(v['has_primary_key'] for v in pks.values())
    print(f"   {'✓' if all_have_pk else '✗'} All tables have primary keys: {all_have_pk}")
    for table, info in pks.items():
        print(f"   - {table}: {info['primary_key_columns']}")
    
    # Check 3: Foreign Keys
    print("\n3. Checking Foreign Keys...")
    fks = check_foreign_keys()
    total_fks = sum(v['foreign_key_count'] for v in fks.values())
    print(f"   ✓ Total foreign keys: {total_fks}")
    for table, info in fks.items():
        if info['foreign_key_count'] > 0:
            print(f"   - {table}: {info['foreign_key_count']} foreign key(s)")
            for fk in info['foreign_keys']:
                print(f"     → {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
    
    # Check 4: Relationships
    print("\n4. Checking SQLAlchemy Relationships...")
    rels = check_relationships()
    all_rels_ok = all(all(v.values()) for v in rels.values())
    print(f"   {'✓' if all_rels_ok else '✗'} All relationships configured: {all_rels_ok}")
    for model, rel_dict in rels.items():
        for rel_name, exists in rel_dict.items():
            status = '✓' if exists else '✗'
            print(f"   {status} {model}.{rel_name}")
    
    # Check 5: Orphan Records
    print("\n5. Checking for Orphan Records...")
    orphans = check_orphan_records()
    total_orphans = sum(len(v) for v in orphans.values())
    print(f"   {'✓' if total_orphans == 0 else '⚠'} Total orphan records: {total_orphans}")
    for orphan_type, orphan_list in orphans.items():
        if orphan_list:
            print(f"   ⚠ {orphan_type}: {len(orphan_list)} record(s)")
    
    # Check 6: Duplicates
    print("\n6. Checking for Duplicate Records...")
    duplicates = check_duplicate_entities()
    total_dups = sum(len(v) for v in duplicates.values())
    print(f"   {'✓' if total_dups == 0 else '⚠'} Total duplicate records: {total_dups}")
    for dup_type, dup_list in duplicates.items():
        if dup_list:
            print(f"   ⚠ {dup_type}: {len(dup_list)} duplicate(s)")
    
    # Summary
    print("\n" + "=" * 80)
    print("CONSISTENCY CHECK SUMMARY")
    print("=" * 80)
    
    issues = []
    if tables['missing_tables']:
        issues.append(f"Missing tables: {len(tables['missing_tables'])}")
    if not all_have_pk:
        issues.append("Some tables missing primary keys")
    if not all_rels_ok:
        issues.append("Some relationships not configured")
    if total_orphans > 0:
        issues.append(f"Orphan records found: {total_orphans}")
    if total_dups > 0:
        issues.append(f"Duplicate records found: {total_dups}")
    
    if not issues:
        print("✓ DATABASE CONSISTENCY: PASS")
        print("✓ All checks passed successfully")
    else:
        print("⚠ DATABASE CONSISTENCY: ISSUES FOUND")
        for issue in issues:
            print(f"  - {issue}")
    
    print("=" * 80)
    
    return {
        'tables': tables,
        'primary_keys': pks,
        'foreign_keys': fks,
        'relationships': rels,
        'orphans': orphans,
        'duplicates': duplicates,
        'status': 'PASS' if not issues else 'ISSUES_FOUND',
        'issues': issues
    }

if __name__ == "__main__":
    results = run_full_consistency_check()
