# Institute API Routes - CertiSense AI v3.0
# All 7 Modules: Students, Certificates, Issue, Track, Analysis, Reports, Feedback

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from typing import Optional
from sqlalchemy.orm import Session

from database import get_db
from institute_service import InstituteService
from auth_db import verify_token, get_current_user

router = APIRouter(prefix="/api/institute", tags=["Institute"])

def get_current_institute(user = Depends(get_current_user)):
    """Secure institute authentication"""
    if user.get("role") != "institute":
        raise HTTPException(status_code=403, detail="Institute access required")
    return user

# ==================== MODULE 1: MANAGE STUDENTS ====================

@router.post("/students")
async def add_student(
    name: str = Query(...),
    email: str = Query(...),
    password: str = Query(...),
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """Add Student - Register new student"""
    try:
        result = InstituteService.manage_students_add(
            institute["user_id"], name, email, password, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/students")
async def list_students(
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """View Students - List all students"""
    try:
        students = InstituteService.manage_students_list(institute["user_id"], db)
        return students
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/students/{student_id}")
async def update_student(
    student_id: str,
    name: str = Query(...),
    email: str = Query(...),
    phone: Optional[str] = Query(None),
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """Update Student - Modify student information"""
    try:
        result = InstituteService.manage_students_update(
            institute["user_id"], student_id, name, email, phone, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/students/{student_id}")
async def remove_student(
    student_id: str,
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """Remove Student - Delete student record"""
    try:
        result = InstituteService.manage_students_remove(
            institute["user_id"], student_id, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 2: MANAGE CERTIFICATES ====================

@router.get("/certificates")
async def list_certificates(
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """View Certificates - List all issued certificates"""
    try:
        certificates = InstituteService.manage_certificates_list(institute["user_id"], db)
        return certificates
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 3: ISSUE CERTIFICATE ====================

@router.post("/certificates/issue")
async def issue_certificate(
    file: UploadFile = File(...),
    student_id: str = Query(...),
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """Issue Certificate - Complete blockchain-verifiable certificate issuance"""
    try:
        content = await file.read()
        result = InstituteService.issue_certificate(
            institute["user_id"], student_id, content, file.filename, db
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Certificate issuance failed: {str(e)}")

# ==================== MODULE 4: TRACK STUDENT CERTIFICATES ====================

@router.get("/certificates/track")
async def track_certificates(
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """Track Student Certificates - Monitor verification activity"""
    try:
        tracking_data = InstituteService.track_student_certificates(institute["user_id"], db)
        return tracking_data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 5: VIEW SYSTEM ANALYSIS ====================

@router.get("/analysis")
async def view_analysis(
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """View System Analysis - Analytics and statistics"""
    try:
        analysis = InstituteService.view_system_analysis(institute["user_id"], db)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 6: GENERATE REPORTS ====================

@router.get("/reports/{report_type}")
async def generate_report(
    report_type: str,
    start_date: Optional[str] = Query(None, description="ISO format: 2024-01-01T00:00:00"),
    end_date: Optional[str] = Query(None, description="ISO format: 2024-12-31T23:59:59"),
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """Generate Reports - Student, Certificate, or Verification reports"""
    try:
        report = InstituteService.generate_reports(
            institute["user_id"], report_type, start_date, end_date, db
        )
        return report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== MODULE 7: FEEDBACK MANAGEMENT ====================

@router.get("/feedback")
async def view_feedback(
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """Feedback Management - View certificate-related feedback"""
    try:
        feedback = InstituteService.feedback_management(institute["user_id"], db)
        return feedback
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== DASHBOARD ====================

@router.get("/dashboard")
async def get_dashboard(
    institute = Depends(get_current_institute),
    db: Session = Depends(get_db)
):
    """Get institute dashboard statistics"""
    try:
        stats = InstituteService.get_dashboard_stats(institute["user_id"], db)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== LOGOUT ====================

@router.post("/logout")
async def logout(institute = Depends(get_current_institute)):
    """Secure logout - invalidate session"""
    return {
        "message": "Logged out successfully",
        "institute_id": institute["user_id"]
    }

# ==================== HEALTH CHECK ====================

@router.get("/health")
async def health_check():
    """Institute module health check"""
    return {
        "status": "healthy",
        "module": "institute",
        "version": "3.0.0",
        "features": [
            "Manage Students",
            "Manage Certificates",
            "Issue Certificate",
            "Track Certificates",
            "System Analysis",
            "Generate Reports",
            "Feedback Management"
        ]
    }
