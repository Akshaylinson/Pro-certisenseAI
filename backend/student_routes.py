# Student API Routes - CertiSense AI v3.0
# All 7 Modules: Profile, Manage, Certificates, Verification, Blockchain, Share, Feedback

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session

from database import get_db
from student_service import StudentService
from auth_db import verify_token, get_current_user

router = APIRouter(prefix="/api/student", tags=["Student"])

def get_current_student(user = Depends(get_current_user)):
    """Secure student authentication"""
    if user.get("role") != "student":
        raise HTTPException(status_code=403, detail="Student access required")
    return user

# ==================== MODULE 1: VIEW PROFILE ====================

@router.get("/profile")
async def get_profile(
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """View Profile - Read-only profile information"""
    try:
        profile = StudentService.get_profile(student["user_id"], db)
        return profile
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 2: MANAGE PROFILE ====================

@router.put("/profile")
async def update_profile(
    name: str = Query(...),
    email: str = Query(...),
    phone: Optional[str] = Query(None),
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Manage Profile - Update profile information"""
    try:
        result = StudentService.update_profile(
            student["user_id"], name, email, phone, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 3: VIEW CERTIFICATE ====================

@router.get("/certificates")
async def get_certificates(
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """View Certificate - List all student certificates"""
    try:
        certificates = StudentService.get_certificates(student["user_id"], db)
        return certificates
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/certificate/{cert_hash}")
async def get_certificate_details(
    cert_hash: str,
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """View Certificate Details - Get specific certificate information"""
    try:
        details = StudentService.get_certificate_details(
            student["user_id"], cert_hash, db
        )
        return details
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 4: MONITOR VERIFICATION STATUS ====================

@router.get("/verifications")
async def get_verification_history(
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Monitor Verification Status - View all verifications"""
    try:
        history = StudentService.get_verification_history(student["user_id"], db)
        return history
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/verifications/{verification_id}/flag")
async def flag_suspicious_verification(
    verification_id: str,
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Flag Suspicious Activity - Report suspicious verification"""
    try:
        result = StudentService.flag_suspicious_verification(
            student["user_id"], verification_id, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 5: VIEW BLOCKCHAIN DETAILS ====================

@router.get("/blockchain/{cert_hash}")
async def get_blockchain_details(
    cert_hash: str,
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """View Blockchain Details - Inspect blockchain information"""
    try:
        blockchain_data = StudentService.get_blockchain_details(
            student["user_id"], cert_hash, db
        )
        return blockchain_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 6: SHARE CERTIFICATE ====================

@router.post("/certificate/{cert_hash}/share")
async def generate_share_link(
    cert_hash: str,
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Share Certificate - Generate verification link and QR code"""
    try:
        share_data = StudentService.generate_share_link(
            student["user_id"], cert_hash, db
        )
        return share_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 7: SUBMIT FEEDBACK ====================

@router.post("/feedback")
async def submit_feedback(
    certificate_id: Optional[str] = Query(None),
    message: str = Query(...),
    category: str = Query(..., description="suspicious_verification, incorrect_info, general"),
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Submit Feedback - Report issues or provide feedback"""
    try:
        result = StudentService.submit_feedback(
            student["user_id"], certificate_id, message, category, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/feedback")
async def get_my_feedback(
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get student's submitted feedback"""
    from database import Feedback
    
    feedbacks = db.query(Feedback).filter(
        Feedback.verifier_id == student["user_id"]
    ).order_by(Feedback.timestamp.desc()).all()
    
    return {
        "total_feedback": len(feedbacks),
        "feedbacks": [
            {
                "id": f.id,
                "certificate_id": f.certificate_id,
                "message": f.message,
                "category": f.category,
                "status": f.status,
                "timestamp": f.timestamp.isoformat()
            }
            for f in feedbacks
        ]
    }

# ==================== DASHBOARD ====================

@router.get("/dashboard")
async def get_dashboard(
    student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Get student dashboard statistics"""
    try:
        stats = StudentService.get_dashboard_stats(student["user_id"], db)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== LOGOUT ====================

@router.post("/logout")
async def logout(student = Depends(get_current_student)):
    """Secure logout - invalidate session"""
    return {
        "message": "Logged out successfully",
        "student_id": student["user_id"]
    }

# ==================== HEALTH CHECK ====================

@router.get("/health")
async def health_check():
    """Student module health check"""
    return {
        "status": "healthy",
        "module": "student",
        "version": "3.0.0",
        "features": [
            "View Profile",
            "Manage Profile",
            "View Certificates",
            "Monitor Verifications",
            "View Blockchain",
            "Share Certificate",
            "Submit Feedback"
        ]
    }
