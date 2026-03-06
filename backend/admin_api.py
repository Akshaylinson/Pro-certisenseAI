from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from database import get_db, Institute, Student, Certificate, Verifier, Verification, Feedback
from auth_db import require_admin, log_audit, hash_password
from blockchain_service import BlockchainService, generate_file_hash
from ai_service import AIValidationService

router = APIRouter(prefix="/admin", tags=["Admin"])

# ==================== MODULE 1: MANAGE INSTITUTES ====================

@router.get("/institutes")
async def get_institutes(admin=Depends(require_admin), db: Session = Depends(get_db)):
    """List all institutes with metadata"""
    institutes = db.query(Institute).all()
    result = []
    for inst in institutes:
        student_count = db.query(Student).filter(Student.institute_id == inst.id).count()
        cert_count = db.query(Certificate).filter(Certificate.institute_id == inst.id).count()
        result.append({
            "id": inst.id,
            "institute_id": inst.institute_id,
            "name": inst.name,
            "registration_number": inst.registration_number,
            "email": inst.email,
            "location": inst.location,
            "approval_status": inst.approval_status,
            "is_verified": inst.is_verified,
            "student_count": student_count,
            "certificate_count": cert_count,
            "created_at": inst.created_at
        })
    log_audit(db, admin["user_id"], "admin", "VIEW", "institutes", "all", "Viewed institutes list")
    return {"institutes": result, "total": len(result)}

@router.post("/institutes")
async def add_institute(
    institute_name: str = Query(...),
    email: str = Query(...),
    password: str = Query(...),
    location: str = Query(None),
    registration_number: str = Query(None),
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Add new institute"""
    # Check if email exists
    existing = db.query(Institute).filter(Institute.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate institute ID
    count = db.query(Institute).count() + 1
    institute_id = f"INST{count:05d}"
    
    new_institute = Institute(
        id=str(uuid.uuid4()),
        institute_id=institute_id,
        name=institute_name,
        email=email,
        password_hash=hash_password(password),
        location=location,
        registration_number=registration_number or f"REG{count:05d}",
        approval_status="approved",
        is_verified=True,
        created_at=datetime.utcnow()
    )
    db.add(new_institute)
    db.commit()
    log_audit(db, admin["user_id"], "admin", "CREATE", "institute", new_institute.id, f"Added institute: {institute_name}")
    return {"message": "Institute added successfully", "institute_id": institute_id}

@router.put("/institutes/{institute_id}")
async def edit_institute(
    institute_id: str,
    name: str = Query(None),
    email: str = Query(None),
    location: str = Query(None),
    approval_status: str = Query(None),
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Edit institute information"""
    institute = db.query(Institute).filter(Institute.id == institute_id).first()
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    if name:
        institute.name = name
    if email:
        institute.email = email
    if location:
        institute.location = location
    if approval_status:
        institute.approval_status = approval_status
    institute.updated_at = datetime.utcnow()
    
    db.commit()
    log_audit(db, admin["user_id"], "admin", "UPDATE", "institute", institute_id, f"Updated institute: {institute.name}")
    return {"message": "Institute updated successfully"}

@router.delete("/institutes/{institute_id}")
async def delete_institute(institute_id: str, admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Delete institute"""
    institute = db.query(Institute).filter(Institute.id == institute_id).first()
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    # Check for dependencies
    student_count = db.query(Student).filter(Student.institute_id == institute_id).count()
    if student_count > 0:
        raise HTTPException(status_code=400, detail=f"Cannot delete institute with {student_count} students")
    
    log_audit(db, admin["user_id"], "admin", "DELETE", "institute", institute_id, f"Deleted institute: {institute.name}")
    db.delete(institute)
    db.commit()
    return {"message": "Institute deleted successfully"}

# ==================== MODULE 2: MANAGE CERTIFICATES ====================

@router.get("/certificates")
async def get_certificates(
    status: str = Query(None),
    institute_id: str = Query(None),
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """View all certificates with filtering"""
    query = db.query(Certificate)
    if status:
        query = query.filter(Certificate.status == status)
    if institute_id:
        query = query.filter(Certificate.institute_id == institute_id)
    
    certificates = query.order_by(desc(Certificate.created_at)).all()
    result = []
    for cert in certificates:
        student = db.query(Student).filter(Student.id == cert.student_id).first()
        institute = db.query(Institute).filter(Institute.id == cert.institute_id).first()
        result.append({
            "id": cert.id,
            "certificate_id": cert.id,
            "name": cert.name,
            "hash": cert.hash,
            "chain_hash": cert.chain_hash,
            "student_id": student.student_id if student else None,
            "student_name": student.name if student else None,
            "institute_id": institute.institute_id if institute else None,
            "institute_name": institute.name if institute else None,
            "status": cert.status.value,
            "issue_date": cert.issue_date,
            "verification_count": cert.verification_count,
            "created_at": cert.created_at
        })
    
    log_audit(db, admin["user_id"], "admin", "VIEW", "certificates", "all", "Viewed certificates")
    return {"certificates": result, "total": len(result)}

@router.put("/certificates/{cert_id}/approve")
async def approve_certificate(cert_id: str, admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Approve certificate"""
    cert = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    cert.status = "active"
    db.commit()
    log_audit(db, admin["user_id"], "admin", "APPROVE", "certificate", cert_id, f"Approved certificate: {cert.name}")
    return {"message": "Certificate approved"}

@router.put("/certificates/{cert_id}/audit")
async def audit_certificate(cert_id: str, admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Audit certificate integrity"""
    cert = db.query(Certificate).filter(Certificate.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    # Verify blockchain integrity
    blockchain_data = BlockchainService.verify_certificate_hash(cert.hash)
    integrity_check = blockchain_data is not None
    
    # Check for anomalies
    anomalies = []
    if cert.verification_count > 100:
        anomalies.append("High verification count")
    if not integrity_check:
        anomalies.append("Blockchain integrity failed")
        cert.status = "suspicious"
        db.commit()
    
    log_audit(db, admin["user_id"], "admin", "AUDIT", "certificate", cert_id, f"Audited certificate: {cert.name}")
    return {
        "certificate_id": cert_id,
        "integrity_check": integrity_check,
        "anomalies": anomalies,
        "status": cert.status.value
    }

# ==================== MODULE 3: VIEW STUDENTS ====================

@router.get("/students")
async def get_students(institute_id: str = Query(None), admin=Depends(require_admin), db: Session = Depends(get_db)):
    """View all students (read-only)"""
    query = db.query(Student)
    if institute_id:
        query = query.filter(Student.institute_id == institute_id)
    
    students = query.all()
    result = []
    for student in students:
        institute = db.query(Institute).filter(Institute.id == student.institute_id).first()
        cert_count = db.query(Certificate).filter(Certificate.student_id == student.id).count()
        verif_count = db.query(Verification).join(Certificate).filter(Certificate.student_id == student.id).count()
        
        result.append({
            "id": student.id,
            "student_id": student.student_id,
            "name": student.name,
            "email": student.email,
            "institute_id": institute.institute_id if institute else None,
            "institute_name": institute.name if institute else None,
            "program": student.program,
            "certificate_count": cert_count,
            "verification_count": verif_count,
            "created_at": student.created_at
        })
    
    log_audit(db, admin["user_id"], "admin", "VIEW", "students", "all", "Viewed students")
    return {"students": result, "total": len(result)}

# ==================== MODULE 4: MANAGE VERIFIERS ====================

@router.get("/verifiers")
async def get_verifiers(admin=Depends(require_admin), db: Session = Depends(get_db)):
    """List all verifiers"""
    verifiers = db.query(Verifier).all()
    result = []
    for verifier in verifiers:
        verif_count = db.query(Verification).filter(Verification.verifier_id == verifier.id).count()
        result.append({
            "id": verifier.id,
            "verifier_id": verifier.id,
            "username": verifier.username,
            "company_name": verifier.company_name,
            "email": verifier.email,
            "verifier_type": verifier.verifier_type,
            "status": verifier.status,
            "verification_count": verif_count,
            "created_at": verifier.created_at
        })
    
    log_audit(db, admin["user_id"], "admin", "VIEW", "verifiers", "all", "Viewed verifiers")
    return {"verifiers": result, "total": len(result)}

@router.post("/verifiers")
async def add_verifier(
    username: str = Query(...),
    email: str = Query(...),
    password: str = Query(...),
    company_name: str = Query(None),
    verifier_type: str = Query("employer"),
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Add new verifier"""
    existing = db.query(Verifier).filter(Verifier.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_verifier = Verifier(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        password_hash=hash_password(password),
        company_name=company_name,
        verifier_type=verifier_type,
        status="active",
        created_at=datetime.utcnow()
    )
    db.add(new_verifier)
    db.commit()
    log_audit(db, admin["user_id"], "admin", "CREATE", "verifier", new_verifier.id, f"Added verifier: {username}")
    return {"message": "Verifier added successfully", "verifier_id": new_verifier.id}

@router.put("/verifiers/{verifier_id}")
async def edit_verifier(
    verifier_id: str,
    company_name: str = Query(None),
    status: str = Query(None),
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Edit verifier details"""
    verifier = db.query(Verifier).filter(Verifier.id == verifier_id).first()
    if not verifier:
        raise HTTPException(status_code=404, detail="Verifier not found")
    
    if company_name:
        verifier.company_name = company_name
    if status:
        verifier.status = status
    
    db.commit()
    log_audit(db, admin["user_id"], "admin", "UPDATE", "verifier", verifier_id, f"Updated verifier: {verifier.username}")
    return {"message": "Verifier updated successfully"}

@router.delete("/verifiers/{verifier_id}")
async def delete_verifier(verifier_id: str, admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Delete verifier"""
    verifier = db.query(Verifier).filter(Verifier.id == verifier_id).first()
    if not verifier:
        raise HTTPException(status_code=404, detail="Verifier not found")
    
    log_audit(db, admin["user_id"], "admin", "DELETE", "verifier", verifier_id, f"Deleted verifier: {verifier.username}")
    db.delete(verifier)
    db.commit()
    return {"message": "Verifier deleted successfully"}

# ==================== MODULE 5: MONITOR VERIFICATIONS ====================

@router.get("/verifications")
async def get_verifications(
    status: str = Query(None),
    flagged: bool = Query(None),
    admin=Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Monitor all verifications"""
    query = db.query(Verification)
    if status:
        query = query.filter(Verification.status == status)
    if flagged is not None:
        query = query.filter(Verification.is_suspicious == flagged)
    
    verifications = query.order_by(desc(Verification.timestamp)).limit(100).all()
    result = []
    for verif in verifications:
        cert = db.query(Certificate).filter(Certificate.id == verif.certificate_id).first()
        verifier = db.query(Verifier).filter(Verifier.id == verif.verifier_id).first()
        result.append({
            "id": verif.id,
            "verification_id": verif.id,
            "certificate_id": cert.id if cert else None,
            "certificate_hash": verif.certificate_hash,
            "verifier_id": verifier.username if verifier else None,
            "result": verif.result,
            "status": verif.status.value,
            "confidence_score": verif.confidence_score,
            "blockchain_integrity": verif.blockchain_integrity,
            "is_suspicious": verif.is_suspicious,
            "timestamp": verif.timestamp
        })
    
    log_audit(db, admin["user_id"], "admin", "VIEW", "verifications", "all", "Viewed verifications")
    return {"verifications": result, "total": len(result)}

@router.put("/verifications/{verif_id}/flag")
async def flag_verification(verif_id: str, admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Flag suspicious verification"""
    verif = db.query(Verification).filter(Verification.id == verif_id).first()
    if not verif:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    verif.is_suspicious = True
    verif.status = "flagged"
    db.commit()
    log_audit(db, admin["user_id"], "admin", "FLAG", "verification", verif_id, "Flagged suspicious verification")
    return {"message": "Verification flagged as suspicious"}

# ==================== MODULE 6: SYSTEM ANALYTICS ====================

@router.get("/analytics")
async def get_analytics(admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Get system-wide analytics"""
    total_institutes = db.query(Institute).count()
    total_students = db.query(Student).count()
    total_certificates = db.query(Certificate).count()
    total_verifications = db.query(Verification).count()
    total_verifiers = db.query(Verifier).count()
    
    # Success rate
    successful_verifs = db.query(Verification).filter(Verification.result == True).count()
    success_rate = (successful_verifs / total_verifications * 100) if total_verifications > 0 else 0
    
    # Recent trends (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_certs = db.query(Certificate).filter(Certificate.created_at >= thirty_days_ago).count()
    recent_verifs = db.query(Verification).filter(Verification.timestamp >= thirty_days_ago).count()
    
    # Certificate status distribution
    active_certs = db.query(Certificate).filter(Certificate.status == "active").count()
    revoked_certs = db.query(Certificate).filter(Certificate.status == "revoked").count()
    suspicious_certs = db.query(Certificate).filter(Certificate.status == "suspicious").count()
    
    log_audit(db, admin["user_id"], "admin", "VIEW", "analytics", "system", "Viewed system analytics")
    
    return {
        "total_institutes": total_institutes,
        "total_students": total_students,
        "total_certificates": total_certificates,
        "total_verifications": total_verifications,
        "total_verifiers": total_verifiers,
        "verification_success_rate": round(success_rate, 2),
        "recent_certificates_30d": recent_certs,
        "recent_verifications_30d": recent_verifs,
        "certificate_status": {
            "active": active_certs,
            "revoked": revoked_certs,
            "suspicious": suspicious_certs
        }
    }

# ==================== MODULE 7: GENERATE REPORTS ====================

@router.get("/reports/institutes")
async def generate_institute_report(admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Generate institute report"""
    institutes = db.query(Institute).all()
    report_data = []
    for inst in institutes:
        student_count = db.query(Student).filter(Student.institute_id == inst.id).count()
        cert_count = db.query(Certificate).filter(Certificate.institute_id == inst.id).count()
        report_data.append({
            "institute_name": inst.name,
            "institute_id": inst.institute_id,
            "students": student_count,
            "certificates": cert_count,
            "status": inst.approval_status
        })
    
    log_audit(db, admin["user_id"], "admin", "GENERATE", "report", "institutes", "Generated institute report")
    return {"report_type": "institutes", "data": report_data, "generated_at": datetime.utcnow()}

@router.get("/reports/certificates")
async def generate_certificate_report(admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Generate certificate report"""
    certificates = db.query(Certificate).all()
    report_data = []
    for cert in certificates:
        student = db.query(Student).filter(Student.id == cert.student_id).first()
        institute = db.query(Institute).filter(Institute.id == cert.institute_id).first()
        report_data.append({
            "certificate_id": cert.id,
            "student_name": student.name if student else "Unknown",
            "institute_name": institute.name if institute else "Unknown",
            "status": cert.status.value,
            "verifications": cert.verification_count,
            "issue_date": cert.issue_date
        })
    
    log_audit(db, admin["user_id"], "admin", "GENERATE", "report", "certificates", "Generated certificate report")
    return {"report_type": "certificates", "data": report_data, "generated_at": datetime.utcnow()}

@router.get("/reports/verifications")
async def generate_verification_report(admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Generate verification report"""
    verifications = db.query(Verification).order_by(desc(Verification.timestamp)).limit(500).all()
    report_data = []
    for verif in verifications:
        verifier = db.query(Verifier).filter(Verifier.id == verif.verifier_id).first()
        report_data.append({
            "verification_id": verif.id,
            "verifier": verifier.username if verifier else "Unknown",
            "result": "Valid" if verif.result else "Invalid",
            "confidence": verif.confidence_score,
            "timestamp": verif.timestamp
        })
    
    log_audit(db, admin["user_id"], "admin", "GENERATE", "report", "verifications", "Generated verification report")
    return {"report_type": "verifications", "data": report_data, "generated_at": datetime.utcnow()}

# ==================== MODULE 8: FEEDBACK MANAGEMENT ====================

@router.get("/feedback")
async def get_feedback(flagged: bool = Query(None), admin=Depends(require_admin), db: Session = Depends(get_db)):
    """View all feedback"""
    query = db.query(Feedback)
    if flagged is not None:
        query = query.filter(Feedback.flagged == flagged)
    
    feedbacks = query.order_by(desc(Feedback.timestamp)).all()
    result = []
    for fb in feedbacks:
        verifier = db.query(Verifier).filter(Verifier.id == fb.verifier_id).first()
        result.append({
            "id": fb.id,
            "feedback_id": fb.id,
            "verifier_id": verifier.username if verifier else "Unknown",
            "verifier_email": verifier.email if verifier else None,
            "certificate_id": fb.certificate_id,
            "message": fb.message,
            "category": fb.category,
            "priority": fb.priority,
            "status": fb.status,
            "flagged": fb.flagged,
            "timestamp": fb.timestamp
        })
    
    log_audit(db, admin["user_id"], "admin", "VIEW", "feedback", "all", "Viewed feedback")
    return {"feedbacks": result, "total": len(result)}

@router.put("/feedback/{feedback_id}/flag")
async def flag_feedback(feedback_id: str, admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Flag feedback for follow-up"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.flagged = True
    db.commit()
    log_audit(db, admin["user_id"], "admin", "FLAG", "feedback", feedback_id, "Flagged feedback for follow-up")
    return {"message": "Feedback flagged for follow-up"}

@router.put("/feedback/{feedback_id}/resolve")
async def resolve_feedback(feedback_id: str, admin=Depends(require_admin), db: Session = Depends(get_db)):
    """Resolve feedback"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.status = "resolved"
    db.commit()
    log_audit(db, admin["user_id"], "admin", "RESOLVE", "feedback", feedback_id, "Resolved feedback")
    return {"message": "Feedback resolved"}
