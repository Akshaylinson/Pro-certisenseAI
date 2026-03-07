#!/usr/bin/env python3
"""
Database Reset Script for CertiSense AI v3.0
Removes all data and generated certificate files for fresh testing.
"""

import os
import sys
import glob
from sqlalchemy import text

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, Institute, Student, Certificate, Verifier, Verification, Feedback, AuditLog

class DatabaseResetter:
    def __init__(self):
        self.db = SessionLocal()
        self.stats = {
            'institutes': 0,
            'students': 0,
            'certificates': 0,
            'verifiers': 0,
            'verifications': 0,
            'feedbacks': 0,
            'audit_logs': 0,
            'pdf_files': 0
        }

    def get_confirmation(self):
        """Get user confirmation before proceeding with reset"""
        print("WARNING: This will permanently delete ALL database data and certificate files.")
        print("This action cannot be undone!")
        print()
        confirmation = input("Type YES to continue: ").strip()
        
        if confirmation != "YES":
            print("Reset cancelled.")
            return False
        
        print("Proceeding with database reset...")
        return True

    def count_existing_records(self):
        """Count existing records before deletion"""
        try:
            self.stats['verifications'] = self.db.query(Verification).count()
            self.stats['feedbacks'] = self.db.query(Feedback).count()
            self.stats['certificates'] = self.db.query(Certificate).count()
            self.stats['students'] = self.db.query(Student).count()
            self.stats['verifiers'] = self.db.query(Verifier).count()
            self.stats['institutes'] = self.db.query(Institute).count()
            self.stats['audit_logs'] = self.db.query(AuditLog).count()
            
            # Count PDF files
            cert_dir = "uploads/certificates"
            if os.path.exists(cert_dir):
                pdf_files = glob.glob(os.path.join(cert_dir, "*.pdf"))
                self.stats['pdf_files'] = len(pdf_files)
            
            print("Current database state:")
            print(f"   Institutes: {self.stats['institutes']}")
            print(f"   Students: {self.stats['students']}")
            print(f"   Certificates: {self.stats['certificates']}")
            print(f"   Verifiers: {self.stats['verifiers']}")
            print(f"   Verifications: {self.stats['verifications']}")
            print(f"   Feedbacks: {self.stats['feedbacks']}")
            print(f"   Audit Logs: {self.stats['audit_logs']}")
            print(f"   PDF Files: {self.stats['pdf_files']}")
            print()
            
        except Exception as e:
            print("Warning: Could not count existing records: {}".format(str(e)))

    def delete_certificate_files(self):
        """Delete all certificate PDF files"""
        cert_dir = "uploads/certificates"
        deleted_count = 0
        
        if not os.path.exists(cert_dir):
            print("Certificate directory does not exist")
            return
        
        try:
            # Get all PDF files in the certificates directory
            pdf_files = glob.glob(os.path.join(cert_dir, "*.pdf"))
            
            for pdf_file in pdf_files:
                try:
                    os.remove(pdf_file)
                    deleted_count += 1
                except OSError as e:
                    print("Warning: Could not delete {}: {}".format(pdf_file, str(e)))
            
            print("Deleted {} certificate PDF files".format(deleted_count))
            
        except Exception as e:
            print("Error deleting certificate files: {}".format(str(e)))

    def delete_database_records(self):
        """Delete all database records in correct dependency order"""
        try:
            # Delete in reverse dependency order to avoid foreign key conflicts
            
            # 1. Delete audit logs (no dependencies)
            audit_count = self.db.query(AuditLog).count()
            self.db.query(AuditLog).delete()
            print("Deleted {} audit log records".format(audit_count))
            
            # 2. Delete verifications (depends on certificates and verifiers)
            verification_count = self.db.query(Verification).count()
            self.db.query(Verification).delete()
            print("Deleted {} verification records".format(verification_count))
            
            # 3. Delete feedback (depends on verifiers)
            feedback_count = self.db.query(Feedback).count()
            self.db.query(Feedback).delete()
            print("Deleted {} feedback records".format(feedback_count))
            
            # 4. Delete certificates (depends on students and institutes)
            certificate_count = self.db.query(Certificate).count()
            self.db.query(Certificate).delete()
            print("Deleted {} certificate records".format(certificate_count))
            
            # 5. Delete students (depends on institutes)
            student_count = self.db.query(Student).count()
            self.db.query(Student).delete()
            print("Deleted {} student records".format(student_count))
            
            # 6. Delete verifiers (no dependencies from other tables)
            verifier_count = self.db.query(Verifier).count()
            self.db.query(Verifier).delete()
            print("Deleted {} verifier records".format(verifier_count))
            
            # 7. Delete institutes (no dependencies from other tables)
            institute_count = self.db.query(Institute).count()
            self.db.query(Institute).delete()
            print("Deleted {} institute records".format(institute_count))
            
            # Commit all deletions
            self.db.commit()
            print("All database records deleted successfully")
            
        except Exception as e:
            print("Error deleting database records: {}".format(str(e)))
            self.db.rollback()
            raise

    def reset_auto_increment(self):
        """Reset auto-increment counters (if any)"""
        try:
            # For SQLite, we can reset the sqlite_sequence table
            self.db.execute(text("DELETE FROM sqlite_sequence"))
            self.db.commit()
            print("Reset auto-increment sequences")
        except Exception as e:
            # This is not critical, so we just warn
            print("Warning: Could not reset auto-increment sequences: {}".format(str(e)))

    def verify_cleanup(self):
        """Verify that all data has been cleaned up"""
        try:
            # Check database tables
            remaining_records = {
                'institutes': self.db.query(Institute).count(),
                'students': self.db.query(Student).count(),
                'certificates': self.db.query(Certificate).count(),
                'verifiers': self.db.query(Verifier).count(),
                'verifications': self.db.query(Verification).count(),
                'feedbacks': self.db.query(Feedback).count(),
                'audit_logs': self.db.query(AuditLog).count()
            }
            
            # Check for remaining PDF files
            cert_dir = "uploads/certificates"
            remaining_files = 0
            if os.path.exists(cert_dir):
                pdf_files = glob.glob(os.path.join(cert_dir, "*.pdf"))
                remaining_files = len(pdf_files)
            
            # Report verification results
            total_remaining = sum(remaining_records.values()) + remaining_files
            
            if total_remaining == 0:
                print("Cleanup verification: All data successfully removed")
            else:
                print("Cleanup verification: Some data may remain:")
                for table, count in remaining_records.items():
                    if count > 0:
                        print(f"   {table}: {count} records")
                if remaining_files > 0:
                    print(f"   PDF files: {remaining_files} files")
            
        except Exception as e:
            print("Warning: Could not verify cleanup: {}".format(str(e)))

    def run_reset(self):
        """Execute the complete reset process"""
        print("CertiSense AI v3.0 - Database Reset Script")
        print("=" * 50)
        
        try:
            # Get user confirmation
            if not self.get_confirmation():
                return
            
            # Count existing records
            self.count_existing_records()
            
            # Perform cleanup
            print("Starting cleanup process...")
            self.delete_database_records()
            self.delete_certificate_files()
            self.reset_auto_increment()
            
            # Verify cleanup
            self.verify_cleanup()
            
            print("=" * 50)
            print("Database Reset Complete")
            print(f"Institutes removed: {self.stats['institutes']}")
            print(f"Students removed: {self.stats['students']}")
            print(f"Certificates removed: {self.stats['certificates']}")
            print(f"Verifiers removed: {self.stats['verifiers']}")
            print(f"Verifications removed: {self.stats['verifications']}")
            print(f"Feedbacks removed: {self.stats['feedbacks']}")
            print(f"Audit logs removed: {self.stats['audit_logs']}")
            print(f"PDF files deleted: {self.stats['pdf_files']}")
            print("=" * 50)
            print("System is now ready for fresh data")
            
        except Exception as e:
            print("Error during reset: {}".format(str(e)))
            self.db.rollback()
            raise
        finally:
            self.db.close()

def main():
    """Main execution function"""
    resetter = DatabaseResetter()
    resetter.run_reset()

if __name__ == "__main__":
    main()