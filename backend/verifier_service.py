# Verifier Service - Complete Implementation
# CertiSense AI v3.0 - Verifier Module

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid
import hashlib
import time
from sqlalchemy.orm import Session

from database import Verifier, Verification, Feedback, Certificate
from blockchain_service import BlockchainService, generate_file_hash
from ai_service import AIValidationService

class VerifierService:
    """Complete Verifier Service with all 7 modules"""
    
    @staticmethod
    def verify_certificate(
        file_content: bytes,
        filename: str,
        verifier_id: str,
        db: Session
    ) -> Dict:
        """MODULE 1: Verify Certificate - Complete verification workflow"""
        start_time = time.time()
        
        # Extract certificate hash
        certificate_hash = generate_file_hash(file_content)
        
        # Blockchain verification
        blockchain_data = BlockchainService.verify_certificate_hash(certificate_hash)
        blockchain_verified = blockchain_data is not None
        
        # AI validation
        ai_result = AIValidationService.validate_certificate_content(file_content, filename)
        
        # Determine verification result
        if not blockchain_verified:
            verification_result = "invalid"
            confidence_score = 0.0
        elif blockchain_data and not blockchain_data.get("valid", True):
            verification_result = "revoked"
            confidence_score = ai_result["confidence"]
        elif ai_result["confidence"] < 0.5:
            verification_result = "tampered"
            confidence_score = ai_result["confidence"]
        else:
            verification_result = "valid"
            confidence_score = ai_result["confidence"]
        
        processing_time = time.time() - start_time
        
        # Store verification record in database
        verification = Verification(
            id=str(uuid.uuid4()),
            certificate_hash=certificate_hash,
            certificate_id=blockchain_data.get("certificate_id") if blockchain_data else None,
            verifier_id=verifier_id,
            result=verification_result == "valid",
            status=verification_result,
            confidence_score=confidence_score,
            blockchain_integrity=blockchain_verified,
            timestamp=datetime.utcnow()
        )
        
        db.add(verification)
        
        # Update blockchain with verification
        if blockchain_verified:
            BlockchainService.add_verification(certificate_hash, verifier_id, verification_result == "valid")
        
        # Update verifier verification count
        verifier = db.query(Verifier).filter(Verifier.id == verifier_id).first()
        if verifier:
            verifier.verification_count = (verifier.verification_count or 0) + 1
        
        db.commit()
        
        return {
            "verification_id": verification.id,
            "certificate_hash": certificate_hash,
            "verification_result": verification_result,
            "confidence_score": confidence_score,
            "blockchain_verified": blockchain_verified,
            "blockchain_data": blockchain_data,
            "ai_analysis": ai_result,
            "processing_time": processing_time,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def generate_verification_proof(
        verification_id: str,
        verifier_id: str,
        db: Session
    ) -> Dict:
        """MODULE 2: Generate Verification Proof"""
        
        verification = db.query(Verification).filter(
            Verification.id == verification_id,
            Verification.verifier_id == verifier_id
        ).first()
        
        if not verification:
            raise ValueError("Verification record not found")
        
        verifier = db.query(Verifier).filter(Verifier.id == verifier_id).first()
        
        # Generate proof hash
        proof_data = f"{verification_id}{verifier_id}{datetime.utcnow().isoformat()}"
        proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
        
        # Create comprehensive proof report
        report_data = {
            "proof_id": str(uuid.uuid4()),
            "verification_id": verification_id,
            "certificate_id": verification.certificate_id,
            "certificate_hash": verification.certificate_hash,
            "verifier_id": verifier_id,
            "verifier_username": verifier.username if verifier else "Unknown",
            "verifier_company": verifier.company_name if verifier else "N/A",
            "verification_result": verification.status,
            "confidence_score": verification.confidence_score,
            "blockchain_verified": verification.blockchain_integrity,
            "blockchain_transaction": verification.certificate_hash,
            "verification_timestamp": verification.timestamp.isoformat(),
            "proof_hash": proof_hash,
            "generated_at": datetime.utcnow().isoformat(),
            "validity": "This proof certifies the verification was performed by an authorized verifier"
        }
        
        return {
            "proof_hash": proof_hash,
            "report": report_data,
            "message": "Verification proof generated successfully"
        }
    
    @staticmethod
    def get_ai_analysis(
        verification_id: str,
        verifier_id: str,
        db: Session
    ) -> Dict:
        """MODULE 3: View AI Verification Analysis"""
        
        verification = db.query(Verification).filter(
            Verification.id == verification_id,
            Verification.verifier_id == verifier_id
        ).first()
        
        if not verification:
            raise ValueError("Verification not found")
        
        # Enhanced AI insights
        fraud_indicators = []
        confidence = verification.confidence_score or 0.0
        
        if confidence < 0.3:
            fraud_indicators.append("Very low confidence score - high fraud risk")
        elif confidence < 0.5:
            fraud_indicators.append("Low confidence score - potential fraud")
        
        if not verification.blockchain_integrity:
            fraud_indicators.append("Certificate not found on blockchain")
        
        if verification.status == "tampered":
            fraud_indicators.append("Certificate content appears modified")
        
        return {
            "verification_id": verification_id,
            "ai_validation_result": "authentic" if verification.result else "suspicious",
            "confidence_score": confidence,
            "ai_model": "CertiSense AI v3.0 - Enhanced Validation Engine",
            "fraud_indicators": fraud_indicators,
            "risk_level": "low" if confidence > 0.7 else "medium" if confidence > 0.4 else "high",
            "blockchain_integrity": verification.blockchain_integrity,
            "verification_status": verification.status,
            "timestamp": verification.timestamp.isoformat()
        }
    
    @staticmethod
    def get_verification_history(
        verifier_id: str,
        db: Session,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> Dict:
        """MODULE 4: View Verification History with filtering"""
        
        query = db.query(Verification).filter(Verification.verifier_id == verifier_id)
        
        # Apply filters
        if status:
            query = query.filter(Verification.status == status)
        
        if start_date:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Verification.timestamp >= start)
        
        if end_date:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Verification.timestamp <= end)
        
        # Get results
        verifications = query.order_by(Verification.timestamp.desc()).limit(limit).all()
        
        history = []
        for v in verifications:
            history.append({
                "verification_id": v.id,
                "certificate_id": v.certificate_id,
                "certificate_hash": v.certificate_hash[:16] + "..." if v.certificate_hash else "N/A",
                "verification_result": v.status,
                "confidence_score": v.confidence_score,
                "blockchain_verified": v.blockchain_integrity,
                "timestamp": v.timestamp.isoformat()
            })
        
        return {
            "total_verifications": len(history),
            "history": history,
            "filters_applied": {
                "status": status,
                "start_date": start_date,
                "end_date": end_date
            }
        }
    
    @staticmethod
    def submit_feedback(
        verifier_id: str,
        feedback_type: str,
        message: str,
        certificate_id: Optional[str],
        priority: str,
        db: Session
    ) -> Dict:
        """MODULE 5: Submit Feedback"""
        
        feedback = Feedback(
            id=str(uuid.uuid4()),
            verifier_id=verifier_id,
            certificate_id=certificate_id,
            message=message,
            category=feedback_type,
            priority=priority,
            status="open",
            flagged=priority == "high",
            timestamp=datetime.utcnow()
        )
        
        db.add(feedback)
        db.commit()
        
        return {
            "feedback_id": feedback.id,
            "message": "Feedback submitted successfully",
            "status": "open",
            "priority": priority,
            "timestamp": feedback.timestamp.isoformat()
        }
    
    @staticmethod
    def get_blockchain_details(
        certificate_hash: str,
        verifier_id: str
    ) -> Dict:
        """MODULE 6: View Blockchain Details"""
        
        blockchain_data = BlockchainService.get_certificate_chain(certificate_hash)
        
        if not blockchain_data:
            raise ValueError("Certificate not found on blockchain")
        
        return {
            "certificate_hash": certificate_hash,
            "blockchain_hash": blockchain_data.get("chain_hash"),
            "transaction_hash": blockchain_data.get("transaction_id", "N/A"),
            "timestamp": blockchain_data.get("timestamp").isoformat() if blockchain_data.get("timestamp") else "N/A",
            "issuer_id": blockchain_data.get("issuer_id"),
            "student_id": blockchain_data.get("student_id"),
            "status": blockchain_data.get("status"),
            "valid": blockchain_data.get("valid"),
            "verifications": blockchain_data.get("verifications", []),
            "blockchain_integrity": "verified",
            "network": "CertiSense Blockchain Network"
        }
    
    @staticmethod
    def get_dashboard_stats(verifier_id: str, db: Session) -> Dict:
        """Get verifier dashboard statistics"""
        
        verifier = db.query(Verifier).filter(Verifier.id == verifier_id).first()
        verifications = db.query(Verification).filter(Verification.verifier_id == verifier_id).all()
        
        total_verifications = len(verifications)
        valid_count = sum(1 for v in verifications if v.status == "valid")
        invalid_count = sum(1 for v in verifications if v.status == "invalid")
        tampered_count = sum(1 for v in verifications if v.status == "tampered")
        revoked_count = sum(1 for v in verifications if v.status == "revoked")
        
        # Recent verifications (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_verifications = [v for v in verifications if v.timestamp >= thirty_days_ago]
        
        # Calculate success rate
        success_rate = (valid_count / total_verifications * 100) if total_verifications > 0 else 0
        
        return {
            "verifier_info": {
                "username": verifier.username if verifier else "Unknown",
                "verifier_id": verifier_id,
                "company_name": verifier.company_name if verifier else "N/A",
                "email": verifier.email if verifier else "N/A"
            },
            "statistics": {
                "total_verifications": total_verifications,
                "valid_certificates": valid_count,
                "invalid_certificates": invalid_count,
                "tampered_certificates": tampered_count,
                "revoked_certificates": revoked_count,
                "recent_verifications_30d": len(recent_verifications)
            },
            "success_rate": round(success_rate, 2),
            "performance": {
                "avg_confidence": round(sum(v.confidence_score or 0 for v in verifications) / max(1, total_verifications), 2),
                "blockchain_verification_rate": round(sum(1 for v in verifications if v.blockchain_integrity) / max(1, total_verifications) * 100, 2)
            }
        }
