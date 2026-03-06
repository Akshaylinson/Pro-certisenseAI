# Institute Service - CertiSense AI v3.0
# All 7 Modules Implementation

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session

from database import Institute, Student, Certificate, Verification, Feedback, AuditLog
from blockchain_service import BlockchainService, generate_file_hash
from ai_service import AIValidationService

class InstituteService:
    """Complete Institute Service with all 7 modules"""
    
    @staticmethod
    def manage_students_add(institute_id: str, name: str, email: str, password_hash: str, db: Session) -> Dict:
        """MODULE 1: Manage Students - Add Student"""
        from auth_db import hash_password
        
        # Generate unique student ID
        institute = db.query(Institute).filter(Institute.id == institute_id).first()
        if not institute:
            raise ValueError("Institute not found")
        
        student_count = db.query(Student).filter(Student.institute_id == institute_id).count()
        student_id = f"{institute.institute_id}-{str(student_count + 1).zfill(5)}"
        
        student = Student(
            id=str(uuid.uuid4()),
            student_id=student_id,
            name=name,
            email=email,
            password_hash=hash_password(password_hash),
            institute_id=institute_id,
            created_at=datetime.utcnow()
        )
        
        db.add(student)
        
        # Log activity
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=institute_id,
            user_role="institute",
            action="ADD_STUDENT",
            entity_type="student",
            entity_id=student.id,
            details=f"Added student: {name} ({student_id})",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        db.commit()
        
        return {"student_id": student_id, "message": "Student added successfully"}
    
    @staticmethod
    def manage_students_list(institute_id: str, db: Session) -> Dict:
        """MODULE 1: Manage Students - View Students"""
        students = db.query(Student).filter(Student.institute_id == institute_id).all()
        
        return {
            "total_students": len(students),
            "students": [
                {
                    "id": s.id,
                    "student_id": s.student_id,
                    "name": s.name,
                    "email": s.email,
                    "phone": s.phone,
                    "program": s.program,
                    "department": s.department,
                    "enrollment_date": s.created_at.isoformat(),
                    "status": "active"
                }
                for s in students
            ]
        }
    
    @staticmethod
    def manage_students_update(institute_id: str, student_id: str, name: str, email: str, phone: str, db: Session) -> Dict:
        """MODULE 1: Manage Students - Update Student"""
        student = db.query(Student).filter(
            Student.id == student_id,
            Student.institute_id == institute_id
        ).first()
        
        if not student:
            raise ValueError("Student not found or unauthorized")
        
        student.name = name
        student.email = email
        if phone:
            student.phone = phone
        
        # Log activity
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=institute_id,
            user_role="institute",
            action="UPDATE_STUDENT",
            entity_type="student",
            entity_id=student_id,
            details=f"Updated student: {name}",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        db.commit()
        
        return {"message": "Student updated successfully"}
    
    @staticmethod
    def manage_students_remove(institute_id: str, student_id: str, db: Session) -> Dict:
        """MODULE 1: Manage Students - Remove Student"""
        student = db.query(Student).filter(
            Student.id == student_id,
            Student.institute_id == institute_id
        ).first()
        
        if not student:
            raise ValueError("Student not found or unauthorized")
        
        # Log activity before deletion
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=institute_id,
            user_role="institute",
            action="REMOVE_STUDENT",
            entity_type="student",
            entity_id=student_id,
            details=f"Removed student: {student.name} ({student.student_id})",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        
        db.delete(student)
        db.commit()
        
        return {"message": "Student removed successfully"}
    
    @staticmethod
    def manage_certificates_list(institute_id: str, db: Session) -> Dict:
        """MODULE 2: Manage Certificates - View Certificates"""
        certificates = db.query(Certificate).filter(Certificate.institute_id == institute_id).all()
        
        cert_list = []
        for cert in certificates:
            student = db.query(Student).filter(Student.id == cert.student_id).first()
            cert_list.append({
                "certificate_id": cert.id,
                "certificate_title": cert.name,
                "student_id": student.student_id if student else "Unknown",
                "student_name": student.name if student else "Unknown",
                "certificate_hash": cert.hash,
                "certificate_type": cert.certificate_type,
                "issue_date": cert.issue_date.isoformat() if cert.issue_date else None,
                "status": cert.status.value if hasattr(cert.status, 'value') else str(cert.status),
                "verification_count": cert.verification_count,
                "created_at": cert.created_at.isoformat()
            })
        
        return {
            "total_certificates": len(cert_list),
            "certificates": cert_list
        }
    
    @staticmethod
    def issue_certificate(institute_id: str, student_id: str, file_content: bytes, filename: str, db: Session) -> Dict:
        """MODULE 3: Issue Certificate - Complete issuance workflow"""
        
        # Validate certificate with AI
        ai_result = AIValidationService.validate_certificate_content(file_content, filename)
        if not ai_result["valid"]:
            raise ValueError(f"Invalid certificate: {ai_result.get('reason', 'Validation failed')}")
        
        # Generate certificate hash
        certificate_hash = generate_file_hash(file_content)
        
        # Store on blockchain
        chain_hash = BlockchainService.store_certificate_hash(
            certificate_hash, student_id, institute_id, institute_id
        )
        
        # Store certificate record
        certificate = Certificate(
            id=str(uuid.uuid4()),
            name=filename,
            hash=certificate_hash,
            chain_hash=chain_hash,
            student_id=student_id,
            institute_id=institute_id,
            issuer_id=institute_id,
            certificate_type="general",
            status="active",
            issue_date=datetime.utcnow(),
            verification_count=0,
            created_at=datetime.utcnow()
        )
        
        db.add(certificate)
        
        # Log activity
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=institute_id,
            user_role="institute",
            action="ISSUE_CERTIFICATE",
            entity_type="certificate",
            entity_id=certificate.id,
            details=f"Issued certificate to student {student_id}",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        db.commit()
        
        return {
            "certificate_id": certificate.id,
            "certificate_hash": certificate_hash,
            "blockchain_transaction_hash": chain_hash,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Certificate issued successfully"
        }
    
    @staticmethod
    def track_student_certificates(institute_id: str, db: Session) -> Dict:
        """MODULE 4: Track Student Certificates - Monitor verification activity"""
        certificates = db.query(Certificate).filter(Certificate.institute_id == institute_id).all()
        cert_ids = [c.id for c in certificates]
        
        verifications = db.query(Verification).filter(
            Verification.certificate_id.in_(cert_ids)
        ).order_by(Verification.timestamp.desc()).all()
        
        verification_list = []
        suspicious_count = 0
        
        for v in verifications:
            cert = db.query(Certificate).filter(Certificate.id == v.certificate_id).first()
            if v.is_suspicious:
                suspicious_count += 1
            
            verification_list.append({
                "verification_id": v.id,
                "certificate_id": v.certificate_id,
                "certificate_name": cert.name if cert else "Unknown",
                "verifier_id": v.verifier_id,
                "verification_status": v.status.value if hasattr(v.status, 'value') else str(v.status),
                "result": v.result,
                "confidence_score": v.confidence_score,
                "is_suspicious": v.is_suspicious,
                "timestamp": v.timestamp.isoformat()
            })
        
        return {
            "total_certificates": len(certificates),
            "total_verifications": len(verification_list),
            "suspicious_activity_count": suspicious_count,
            "verifications": verification_list
        }
    
    @staticmethod
    def view_system_analysis(institute_id: str, db: Session) -> Dict:
        """MODULE 5: View System Analysis - Analytics dashboard"""
        students = db.query(Student).filter(Student.institute_id == institute_id).all()
        certificates = db.query(Certificate).filter(Certificate.institute_id == institute_id).all()
        cert_ids = [c.id for c in certificates]
        
        verifications = db.query(Verification).filter(
            Verification.certificate_id.in_(cert_ids)
        ).all()
        
        successful_verifications = sum(1 for v in verifications if v.result)
        verification_success_rate = (successful_verifications / len(verifications) * 100) if verifications else 0
        
        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_certs = [c for c in certificates if c.created_at >= thirty_days_ago]
        recent_verifications = [v for v in verifications if v.timestamp >= thirty_days_ago]
        
        return {
            "total_students_registered": len(students),
            "total_certificates_issued": len(certificates),
            "total_verification_requests": len(verifications),
            "verification_success_rate": round(verification_success_rate, 2),
            "recent_activity_30d": {
                "certificates_issued": len(recent_certs),
                "verifications": len(recent_verifications)
            },
            "analytics": {
                "avg_verifications_per_certificate": round(len(verifications) / max(1, len(certificates)), 2),
                "active_certificates": sum(1 for c in certificates if c.status.value == "active" if hasattr(c.status, 'value') else str(c.status) == "active")
            }
        }
    
    @staticmethod
    def generate_reports(institute_id: str, report_type: str, start_date: Optional[str], end_date: Optional[str], db: Session) -> Dict:
        """MODULE 6: Generate Reports - Operational reports"""
        
        # Parse dates
        start = datetime.fromisoformat(start_date) if start_date else datetime.utcnow() - timedelta(days=30)
        end = datetime.fromisoformat(end_date) if end_date else datetime.utcnow()
        
        if report_type == "student":
            students = db.query(Student).filter(
                Student.institute_id == institute_id,
                Student.created_at >= start,
                Student.created_at <= end
            ).all()
            
            return {
                "report_type": "Student Report",
                "period": f"{start.date()} to {end.date()}",
                "total_students": len(students),
                "data": [
                    {
                        "student_id": s.student_id,
                        "name": s.name,
                        "email": s.email,
                        "enrollment_date": s.created_at.isoformat()
                    }
                    for s in students
                ]
            }
        
        elif report_type == "certificate":
            certificates = db.query(Certificate).filter(
                Certificate.institute_id == institute_id,
                Certificate.created_at >= start,
                Certificate.created_at <= end
            ).all()
            
            return {
                "report_type": "Certificate Issuance Report",
                "period": f"{start.date()} to {end.date()}",
                "total_certificates": len(certificates),
                "data": [
                    {
                        "certificate_id": c.id,
                        "certificate_name": c.name,
                        "student_id": c.student_id,
                        "issue_date": c.issue_date.isoformat() if c.issue_date else None,
                        "status": c.status.value if hasattr(c.status, 'value') else str(c.status)
                    }
                    for c in certificates
                ]
            }
        
        elif report_type == "verification":
            certificates = db.query(Certificate).filter(Certificate.institute_id == institute_id).all()
            cert_ids = [c.id for c in certificates]
            
            verifications = db.query(Verification).filter(
                Verification.certificate_id.in_(cert_ids),
                Verification.timestamp >= start,
                Verification.timestamp <= end
            ).all()
            
            return {
                "report_type": "Verification Activity Report",
                "period": f"{start.date()} to {end.date()}",
                "total_verifications": len(verifications),
                "data": [
                    {
                        "verification_id": v.id,
                        "certificate_id": v.certificate_id,
                        "verifier_id": v.verifier_id,
                        "result": v.result,
                        "timestamp": v.timestamp.isoformat()
                    }
                    for v in verifications
                ]
            }
        
        else:
            raise ValueError("Invalid report type")
    
    @staticmethod
    def feedback_management(institute_id: str, db: Session) -> Dict:
        """MODULE 7: Feedback Management - View and review feedback"""
        
        # Get all certificates for this institute
        certificates = db.query(Certificate).filter(Certificate.institute_id == institute_id).all()
        cert_ids = [c.id for c in certificates]
        
        # Get feedback related to these certificates
        feedbacks = db.query(Feedback).filter(
            Feedback.certificate_id.in_(cert_ids)
        ).order_by(Feedback.timestamp.desc()).all()
        
        feedback_list = []
        for fb in feedbacks:
            cert = db.query(Certificate).filter(Certificate.id == fb.certificate_id).first()
            feedback_list.append({
                "feedback_id": fb.id,
                "user_id": fb.verifier_id,
                "certificate_id": fb.certificate_id,
                "certificate_name": cert.name if cert else "Unknown",
                "message": fb.message,
                "category": fb.category,
                "priority": fb.priority,
                "status": fb.status,
                "flagged": fb.flagged,
                "timestamp": fb.timestamp.isoformat()
            })
        
        return {
            "total_feedback": len(feedback_list),
            "flagged_count": sum(1 for fb in feedbacks if fb.flagged),
            "feedbacks": feedback_list
        }
    
    @staticmethod
    def get_dashboard_stats(institute_id: str, db: Session) -> Dict:
        """Get institute dashboard statistics"""
        institute = db.query(Institute).filter(Institute.id == institute_id).first()
        if not institute:
            raise ValueError("Institute not found")
        
        students = db.query(Student).filter(Student.institute_id == institute_id).count()
        certificates = db.query(Certificate).filter(Certificate.institute_id == institute_id).count()
        
        cert_list = db.query(Certificate).filter(Certificate.institute_id == institute_id).all()
        cert_ids = [c.id for c in cert_list]
        verifications = db.query(Verification).filter(Verification.certificate_id.in_(cert_ids)).count()
        
        return {
            "institute_info": {
                "name": institute.name,
                "institute_id": institute.institute_id,
                "email": institute.email
            },
            "statistics": {
                "total_students": students,
                "total_certificates": certificates,
                "total_verifications": verifications
            }
        }
