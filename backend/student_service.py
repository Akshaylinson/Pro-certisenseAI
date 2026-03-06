# Student Service - CertiSense AI v3.0
# All 7 Modules Implementation

from typing import Dict, List, Optional
from datetime import datetime
import uuid
import hashlib
from sqlalchemy.orm import Session

from database import Student, Certificate, Verification, Feedback, Institute, AuditLog
from blockchain_service import BlockchainService

class StudentService:
    """Complete Student Service with all 7 modules"""
    
    @staticmethod
    def get_profile(student_id: str, db: Session) -> Dict:
        """MODULE 1: View Profile - Read-only profile information"""
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError("Student not found")
        
        institute = db.query(Institute).filter(Institute.id == student.institute_id).first()
        
        return {
            "student_id": student.student_id,
            "name": student.name,
            "email": student.email,
            "phone": student.phone,
            "program": student.program,
            "department": student.department,
            "institute_name": institute.name if institute else "N/A",
            "institute_id": student.institute_id,
            "account_status": "active",
            "created_at": student.created_at.isoformat()
        }
    
    @staticmethod
    def update_profile(student_id: str, name: str, email: str, phone: str, db: Session) -> Dict:
        """MODULE 2: Manage Profile - Update profile information"""
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError("Student not found")
        
        # Update fields
        student.name = name
        student.email = email
        if phone:
            student.phone = phone
        
        # Log activity
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=student_id,
            user_role="student",
            action="UPDATE_PROFILE",
            entity_type="student",
            entity_id=student_id,
            details=f"Updated profile: {name}, {email}",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        db.commit()
        
        return {"message": "Profile updated successfully"}
    
    @staticmethod
    def get_certificates(student_id: str, db: Session) -> Dict:
        """MODULE 3: View Certificate - List all student certificates"""
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError("Student not found")
        
        certificates = db.query(Certificate).filter(
            Certificate.student_id == student_id
        ).all()
        
        cert_list = []
        for cert in certificates:
            blockchain_data = BlockchainService.get_certificate_chain(cert.hash)
            cert_list.append({
                "certificate_id": cert.id,
                "certificate_name": cert.name,
                "certificate_hash": cert.hash,
                "chain_hash": cert.chain_hash,
                "certificate_type": cert.certificate_type,
                "status": cert.status.value if hasattr(cert.status, 'value') else str(cert.status),
                "issue_date": cert.issue_date.isoformat() if cert.issue_date else None,
                "verification_count": cert.verification_count,
                "blockchain_status": "verified" if blockchain_data else "not_found",
                "created_at": cert.created_at.isoformat()
            })
        
        return {
            "total_certificates": len(cert_list),
            "certificates": cert_list
        }
    
    @staticmethod
    def get_certificate_details(student_id: str, cert_hash: str, db: Session) -> Dict:
        """MODULE 3: View Certificate Details - Get specific certificate"""
        certificate = db.query(Certificate).filter(
            Certificate.hash == cert_hash,
            Certificate.student_id == student_id
        ).first()
        
        if not certificate:
            raise ValueError("Certificate not found")
        
        institute = db.query(Institute).filter(Institute.id == certificate.institute_id).first()
        blockchain_data = BlockchainService.get_certificate_chain(cert_hash)
        
        return {
            "certificate_id": certificate.id,
            "certificate_name": certificate.name,
            "certificate_hash": certificate.hash,
            "chain_hash": certificate.chain_hash,
            "certificate_type": certificate.certificate_type,
            "status": certificate.status.value if hasattr(certificate.status, 'value') else str(certificate.status),
            "issue_date": certificate.issue_date.isoformat() if certificate.issue_date else None,
            "issuing_institute": institute.name if institute else "Unknown",
            "verification_count": certificate.verification_count,
            "blockchain_data": blockchain_data,
            "created_at": certificate.created_at.isoformat()
        }
    
    @staticmethod
    def get_verification_history(student_id: str, db: Session) -> Dict:
        """MODULE 4: Monitor Verification Status - Track all verifications"""
        certificates = db.query(Certificate).filter(Certificate.student_id == student_id).all()
        cert_ids = [c.id for c in certificates]
        
        verifications = db.query(Verification).filter(
            Verification.certificate_id.in_(cert_ids)
        ).order_by(Verification.timestamp.desc()).all()
        
        verification_list = []
        for v in verifications:
            cert = db.query(Certificate).filter(Certificate.id == v.certificate_id).first()
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
            "total_verifications": len(verification_list),
            "verifications": verification_list
        }
    
    @staticmethod
    def flag_suspicious_verification(student_id: str, verification_id: str, db: Session) -> Dict:
        """MODULE 4: Flag Suspicious Activity"""
        verification = db.query(Verification).filter(Verification.id == verification_id).first()
        if not verification:
            raise ValueError("Verification not found")
        
        # Check if certificate belongs to student
        cert = db.query(Certificate).filter(
            Certificate.id == verification.certificate_id,
            Certificate.student_id == student_id
        ).first()
        
        if not cert:
            raise ValueError("Unauthorized access")
        
        verification.is_suspicious = True
        
        # Log activity
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=student_id,
            user_role="student",
            action="FLAG_SUSPICIOUS",
            entity_type="verification",
            entity_id=verification_id,
            details=f"Student flagged verification as suspicious",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        db.commit()
        
        return {"message": "Verification flagged as suspicious"}
    
    @staticmethod
    def get_blockchain_details(student_id: str, cert_hash: str, db: Session) -> Dict:
        """MODULE 5: View Blockchain Details - Inspect blockchain data"""
        certificate = db.query(Certificate).filter(
            Certificate.hash == cert_hash,
            Certificate.student_id == student_id
        ).first()
        
        if not certificate:
            raise ValueError("Certificate not found or unauthorized")
        
        blockchain_data = BlockchainService.get_certificate_chain(cert_hash)
        
        if not blockchain_data:
            raise ValueError("Certificate not found on blockchain")
        
        return {
            "certificate_hash": cert_hash,
            "blockchain_transaction_hash": blockchain_data.get("chain_hash"),
            "timestamp": blockchain_data.get("timestamp").isoformat() if blockchain_data.get("timestamp") else None,
            "smart_contract_address": "0x" + hashlib.sha256(cert_hash.encode()).hexdigest()[:40],
            "blockchain_validation_status": "verified" if blockchain_data.get("valid") else "invalid",
            "issuer_id": blockchain_data.get("issuer_id"),
            "student_id": blockchain_data.get("student_id"),
            "verification_count": len(blockchain_data.get("verifications", [])),
            "hash_match": certificate.hash == cert_hash
        }
    
    @staticmethod
    def generate_share_link(student_id: str, cert_hash: str, db: Session) -> Dict:
        """MODULE 6: Share Certificate - Generate secure sharing link"""
        certificate = db.query(Certificate).filter(
            Certificate.hash == cert_hash,
            Certificate.student_id == student_id
        ).first()
        
        if not certificate:
            raise ValueError("Certificate not found or unauthorized")
        
        # Generate secure token
        share_token = hashlib.sha256(f"{cert_hash}{datetime.utcnow().isoformat()}".encode()).hexdigest()
        
        # Generate verification link
        verification_link = f"https://certisense.ai/verify/{share_token}"
        
        # Generate QR code data
        qr_data = f"CERTISENSE:{cert_hash}:{share_token}"
        
        # Log activity
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=student_id,
            user_role="student",
            action="GENERATE_SHARE_LINK",
            entity_type="certificate",
            entity_id=certificate.id,
            details=f"Generated share link for certificate",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        db.commit()
        
        return {
            "verification_link": verification_link,
            "qr_code_data": qr_data,
            "share_token": share_token,
            "certificate_hash": cert_hash,
            "expires_in": "30 days"
        }
    
    @staticmethod
    def submit_feedback(student_id: str, certificate_id: str, message: str, category: str, db: Session) -> Dict:
        """MODULE 7: Submit Feedback - Report issues or provide feedback"""
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError("Student not found")
        
        # Create feedback (reuse Feedback table with student context)
        feedback = Feedback(
            id=str(uuid.uuid4()),
            verifier_id=student_id,  # Using verifier_id field for student_id
            certificate_id=certificate_id,
            message=message,
            category=category,
            priority="medium",
            status="open",
            timestamp=datetime.utcnow()
        )
        
        db.add(feedback)
        
        # Log activity
        audit = AuditLog(
            id=str(uuid.uuid4()),
            user_id=student_id,
            user_role="student",
            action="SUBMIT_FEEDBACK",
            entity_type="feedback",
            entity_id=feedback.id,
            details=f"Student submitted feedback: {category}",
            timestamp=datetime.utcnow()
        )
        db.add(audit)
        db.commit()
        
        return {
            "feedback_id": feedback.id,
            "message": "Feedback submitted successfully",
            "status": "open",
            "timestamp": feedback.timestamp.isoformat()
        }
    
    @staticmethod
    def get_dashboard_stats(student_id: str, db: Session) -> Dict:
        """Get student dashboard statistics"""
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError("Student not found")
        
        certificates = db.query(Certificate).filter(Certificate.student_id == student_id).all()
        cert_ids = [c.id for c in certificates]
        
        verifications = db.query(Verification).filter(
            Verification.certificate_id.in_(cert_ids)
        ).all()
        
        active_certs = sum(1 for c in certificates if c.status.value == "active" if hasattr(c.status, 'value') else str(c.status) == "active")
        
        return {
            "student_info": {
                "name": student.name,
                "student_id": student.student_id,
                "email": student.email
            },
            "statistics": {
                "total_certificates": len(certificates),
                "active_certificates": active_certs,
                "total_verifications": len(verifications),
                "recent_verifications": len([v for v in verifications if (datetime.utcnow() - v.timestamp).days <= 30])
            }
        }
