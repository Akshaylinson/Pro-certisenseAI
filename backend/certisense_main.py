from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Header, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional
import uuid
from datetime import datetime
import base64
from sqlalchemy.orm import Session

from models import *
from auth_db import (
    authenticate_admin, authenticate_institute, authenticate_student, authenticate_verifier,
    register_institute, register_student, register_verifier, verify_token
)
from database import get_db, Institute, Student, Verifier, Certificate, Verification, Feedback, CertificateStatusEnum, Base, engine
from blockchain_service import BlockchainService, generate_file_hash
from ai_service import AIValidationService
from chatbot_service import ChatbotService
from admin_api import router as admin_router
from ai_query_service import AIQueryService

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CertiSense AI - Enhanced Blockchain Certificate System", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for report images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include admin router
app.include_router(admin_router)

# In-memory storage
certificates_db = {}
verifications_db = {}
feedback_db = {}
blockchain_config = {"name": "CertiSense Blockchain"}

# Helper function to get database session
def get_db_session():
    from database import SessionLocal
    return SessionLocal()

def get_current_user(authorization: Optional[str] = Header(None)):
    print(f"Authorization header: {authorization}")
    if not authorization or not authorization.startswith("Bearer "):
        print("No authorization header or invalid format")
        raise HTTPException(status_code=401, detail="Authentication required")
    
    token = authorization.split(" ")[1]
    print(f"Token: {token[:20]}...")
    payload = verify_token(token)
    if not payload:
        print("Token verification failed")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    print(f"User payload: {payload}")
    return payload

def require_admin(user = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_institute(user = Depends(get_current_user)):
    if user["role"] != "institute":
        raise HTTPException(status_code=403, detail="Institute access required")
    return user

def require_student(user = Depends(get_current_user)):
    if user["role"] != "student":
        raise HTTPException(status_code=403, detail="Student access required")
    return user

def require_verifier(user = Depends(get_current_user)):
    if user["role"] != "verifier":
        raise HTTPException(status_code=403, detail="Verifier access required")
    return user

# Authentication Endpoints
@app.post("/auth/admin/login")
async def admin_login(request: LoginRequest):
    token = authenticate_admin(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    return {"access_token": token, "token_type": "bearer", "role": "admin"}

@app.post("/auth/institute/register")
async def institute_register(request: InstituteRegisterRequest):
    success, institute_id = register_institute(request.institute_name, "", request.password, request.email, request.location)
    if not success:
        raise HTTPException(status_code=400, detail="Institute registration failed")
    return {"message": "Institute registered successfully", "institute_id": institute_id}

@app.post("/auth/institute/login")
async def institute_login(request: LoginRequest):
    # Institute uses email as username
    token = authenticate_institute(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid institute credentials")
    return {"access_token": token, "token_type": "bearer", "role": "institute"}

@app.post("/auth/student/login")
async def student_login(request: LoginRequest):
    token = authenticate_student(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid student credentials")
    return {"access_token": token, "token_type": "bearer", "role": "student"}

@app.post("/auth/verifier/register")
async def verifier_register(request: RegisterRequest):
    success = register_verifier(request.username, request.password, request.email)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "Verifier registered successfully"}

@app.post("/auth/verifier/login")
async def verifier_login(request: LoginRequest):
    token = authenticate_verifier(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid verifier credentials")
    return {"access_token": token, "token_type": "bearer", "role": "verifier"}

# Admin router is included from admin_api.py
# All admin endpoints are handled by the admin_api router

# Admin Endpoints - Blockchain Management
@app.get("/admin/blockchain/history")
async def get_blockchain_history(admin = Depends(require_admin)):
    history = [
        {
            "certificate_name": c["name"],
            "hash": c["hash"],
            "timestamp": c["created_at"]
        }
        for c in sorted(certificates_db.values(), key=lambda x: x["created_at"], reverse=True)[:20]
    ]
    return {"history": history}

@app.put("/admin/blockchain/name")
async def update_blockchain_name(name: str = Query(...), admin = Depends(require_admin)):
    blockchain_config["name"] = name
    return {"message": "Blockchain name updated", "name": name}

# Admin Endpoints - Reports (kept for backward compatibility)
@app.get("/admin/reports")
async def get_admin_reports(admin = Depends(require_admin)):
    db = get_db_session()
    try:
        total_institutes = db.query(Institute).count()
        total_students = db.query(Student).count()
        total_certificates = len(certificates_db)
        total_verifications = len(verifications_db)
        
        institute_stats = {}
        institutes = db.query(Institute).all()
        for institute in institutes:
            student_count = db.query(Student).filter(Student.institute_id == institute.id).count()
            cert_count = sum(1 for c in certificates_db.values() if c["institute_id"] == institute.id)
            institute_stats[institute.name] = {"students": student_count, "certificates": cert_count}
        
        return {
            "total_institutes": total_institutes,
            "total_students": total_students,
            "total_certificates": total_certificates,
            "total_verifications": total_verifications,
            "institute_stats": institute_stats
        }
    finally:
        db.close()

# Institute Endpoints - Profile Management
@app.get("/institute/profile")
async def get_institute_profile(institute = Depends(require_institute)):
    print(f"Institute profile accessed by: {institute}")
    db = get_db_session()
    try:
        institute_data = db.query(Institute).filter(Institute.id == institute["user_id"]).first()
        if not institute_data:
            print(f"Institute not found with ID: {institute['user_id']}")
            raise HTTPException(status_code=404, detail="Institute not found")
        
        result = {
            "institute_name": institute_data.name,
            "institute_id": institute_data.institute_id or "",
            "email": institute_data.email,
            "location": institute_data.location or "",
            "description": "",  # Add description field to database if needed
            "image": None,  # Add image field to database if needed
            "created_at": institute_data.created_at
        }
        print(f"Profile result: {result}")
        return result
    except Exception as e:
        print(f"Error in institute profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Profile error: {str(e)}")
    finally:
        db.close()

@app.put("/institute/profile")
async def update_institute_profile_endpoint(
    institute_name: str = Form(...),
    institute_id: str = Form(...),
    email: str = Form(...),
    location: str = Form(""),
    description: str = Form(""),
    image: Optional[UploadFile] = File(None),
    institute = Depends(require_institute)
):
    db = get_db_session()
    try:
        institute_data = db.query(Institute).filter(Institute.id == institute["user_id"]).first()
        if not institute_data:
            raise HTTPException(status_code=404, detail="Institute not found")
        
        institute_data.name = institute_name
        institute_data.institute_id = institute_id
        institute_data.email = email
        institute_data.location = location
        # Note: description and image fields would need to be added to database schema
        
        db.commit()
        return {"message": "Profile updated successfully"}
    finally:
        db.close()

# Institute Endpoints - Student Management
@app.get("/institute/students")
async def get_institute_students(institute = Depends(require_institute)):
    print(f"Institute students accessed by: {institute}")
    db = get_db_session()
    try:
        students = db.query(Student).filter(Student.institute_id == institute["user_id"]).all()
        result = [
            {
                "id": s.id,
                "student_id": s.student_id,
                "name": s.name,
                "email": s.email,
                "created_at": s.created_at
            }
            for s in students
        ]
        print(f"Students result: {len(result)} students found")
        return {"students": result}
    except Exception as e:
        print(f"Error in institute students: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Students error: {str(e)}")
    finally:
        db.close()

@app.post("/institute/students")
async def add_student(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    institute = Depends(require_institute)
):
    try:
        success, student_id = register_student(name, email, password, institute["user_id"])
        if not success:
            raise HTTPException(status_code=400, detail="Student registration failed - unable to generate student ID")
        return {"message": "Student added successfully", "student_id": student_id}
    except Exception as e:
        print(f"Error in add_student: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Student registration failed: {str(e)}")

@app.put("/institute/students/{student_id}")
async def update_student(student_id: str, name: str = Query(...), email: str = Query(...), institute = Depends(require_institute)):
    db = get_db_session()
    try:
        student = db.query(Student).filter(Student.id == student_id, Student.institute_id == institute["user_id"]).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found or not authorized")
        
        student.name = name
        student.email = email
        db.commit()
        
        return {"message": "Student updated successfully"}
    finally:
        db.close()

@app.post("/institute/certificates")
async def issue_certificate(
    file: UploadFile = File(...),
    student_id: str = Query(...),
    institute = Depends(require_institute)
):
    """Issue a certificate to a student"""
    db = get_db_session()
    try:
        print(f"\n=== Certificate Issuance Started ===")
        print(f"Institute ID: {institute['user_id']}")
        print(f"Student ID: {student_id}")
        print(f"File: {file.filename}")
        
        # Validate file
        if not file:
            raise HTTPException(status_code=400, detail="Certificate file missing")
        
        # Read file content
        content = await file.read()
        print(f"File size: {len(content)} bytes")
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Certificate file is empty")
        
        # Generate hash
        file_hash = generate_file_hash(content)
        print(f"File hash: {file_hash}")
        
        # Check for duplicate certificate hash
        existing_cert = db.query(Certificate).filter(Certificate.hash == file_hash).first()
        if existing_cert:
            print(f"❌ Duplicate certificate hash detected: {file_hash}")
            raise HTTPException(status_code=400, detail="This certificate has already been issued")
        
        # Validate certificate content
        print("Validating certificate content...")
        ai_result = AIValidationService.validate_certificate_content(content, file.filename)
        if not ai_result["valid"]:
            print(f"AI validation failed: {ai_result['reason']}")
            raise HTTPException(status_code=400, detail=f"Invalid certificate: {ai_result['reason']}")
        print("AI validation passed")
        
        # Find student by student_id string (e.g., "INST00001-00001")
        print(f"Looking up student with ID: {student_id}")
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            print(f"Student not found: {student_id}")
            raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
        print(f"Student found: {student.name} (UUID: {student.id})")
        
        # Verify student belongs to this institute
        if student.institute_id != institute["user_id"]:
            print(f"Student belongs to different institute: {student.institute_id}")
            raise HTTPException(status_code=403, detail="Student does not belong to your institute")
        print("Student ownership verified")
        
        # Store certificate hash in blockchain
        print("Storing certificate in blockchain...")
        chain_hash = BlockchainService.store_certificate_hash(
            file_hash, 
            student_id, 
            institute["user_id"], 
            institute["user_id"]
        )
        print(f"Blockchain chain hash: {chain_hash}")
        
        # Generate unique certificate ID
        cert_id = f"CERT-{uuid.uuid4().hex[:12].upper()}"
        print(f"Creating certificate record with ID: {cert_id}")
        
        # Save certificate file to disk
        import os
        os.makedirs("uploads/certificates", exist_ok=True)
        file_path = f"uploads/certificates/{cert_id}.pdf"
        with open(file_path, "wb") as f:
            f.write(content)
        print(f"Certificate file saved: {file_path}")
        
        new_cert = Certificate(
            id=cert_id,
            name=file.filename,
            hash=file_hash,
            chain_hash=chain_hash,
            student_id=student.id,
            institute_id=institute["user_id"],
            issuer_id=institute["user_id"],
            status=CertificateStatusEnum.ACTIVE,
            issue_date=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        
        db.add(new_cert)
        db.commit()
        db.refresh(new_cert)
        
        print(f"✅ Certificate saved successfully: {cert_id}")
        print(f"=== Certificate Issuance Completed ===\n")
        
        return {
            "message": "Certificate issued successfully",
            "certificate_id": cert_id,
            "hash": file_hash,
            "chain_hash": chain_hash
        }
        
    except HTTPException as he:
        print(f"❌ HTTP Exception: {he.detail}")
        db.rollback()
        raise
    except Exception as e:
        print(f"❌ Unexpected error issuing certificate: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Certificate issuance failed: {str(e)}")
    finally:
        db.close()

@app.get("/institute/dashboard")
async def institute_dashboard(institute = Depends(require_institute)):
    print(f"Institute dashboard accessed by: {institute}")
    db = get_db_session()
    try:
        students = db.query(Student).filter(Student.institute_id == institute["user_id"]).count()
        certificates = db.query(Certificate).filter(Certificate.institute_id == institute["user_id"]).count()
        
        # Count verifications for this institute's certificates
        institute_cert_ids = [c.id for c in db.query(Certificate).filter(Certificate.institute_id == institute["user_id"]).all()]
        verifications = db.query(Verification).filter(Verification.certificate_id.in_(institute_cert_ids)).count() if institute_cert_ids else 0
        
        result = {
            "total_students": students,
            "total_certificates": certificates,
            "total_verifications": verifications
        }
        print(f"Dashboard result: {result}")
        return result
    except Exception as e:
        print(f"Error in institute dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")
    finally:
        db.close()

# Student Endpoints
@app.get("/student/profile")
async def get_student_profile(student = Depends(require_student)):
    db = get_db_session()
    try:
        student_data = db.query(Student).filter(Student.id == student["user_id"]).first()
        if not student_data:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {
            "student_id": student_data.student_id,
            "name": student_data.name,
            "email": student_data.email,
            "institute_id": student_data.institute_id,
            "created_at": student_data.created_at
        }
    finally:
        db.close()

@app.put("/student/profile")
async def update_student_profile(name: str = Query(...), email: str = Query(...), student = Depends(require_student)):
    db = get_db_session()
    try:
        student_data = db.query(Student).filter(Student.id == student["user_id"]).first()
        if student_data:
            student_data.name = name
            student_data.email = email
            db.commit()
        return {"message": "Profile updated successfully"}
    finally:
        db.close()

@app.get("/student/certificates")
async def get_student_certificates(student = Depends(require_student)):
    db = get_db_session()
    try:
        student_data = db.query(Student).filter(Student.id == student["user_id"]).first()
        if not student_data:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Get certificates from database
        certs = db.query(Certificate).filter(Certificate.student_id == student_data.id).all()
        certificates = [
            {
                "certificate_id": c.id,
                "name": c.name,
                "hash": c.hash,
                "chain_hash": c.chain_hash,
                "status": c.status.value,
                "issue_date": c.issue_date.isoformat() if c.issue_date else None,
                "verification_count": c.verification_count or 0
            }
            for c in certs
        ]
        return {"certificates": certificates}
    finally:
        db.close()

@app.get("/student/certificates/{certificate_id}/download")
async def download_certificate(certificate_id: str, student = Depends(require_student)):
    """Download certificate PDF file"""
    db = get_db_session()
    try:
        student_data = db.query(Student).filter(Student.id == student["user_id"]).first()
        if not student_data:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Find certificate
        cert = db.query(Certificate).filter(
            Certificate.id == certificate_id,
            Certificate.student_id == student_data.id
        ).first()
        
        if not cert:
            raise HTTPException(status_code=404, detail="Certificate not found or access denied")
        
        # Check if file exists
        import os
        file_path = f"uploads/certificates/{certificate_id}.pdf"
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Certificate file not found")
        
        from fastapi.responses import FileResponse
        return FileResponse(
            path=file_path,
            filename=f"{cert.name}",
            media_type="application/pdf"
        )
    finally:
        db.close()

@app.get("/student/certificate/{cert_hash}")
async def get_certificate_details(cert_hash: str, student = Depends(require_student)):
    chain_data = BlockchainService.get_certificate_chain(cert_hash)
    if not chain_data:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    return chain_data

# Verifier Endpoints
@app.get("/verifier/dashboard")
async def verifier_dashboard(verifier = Depends(require_verifier), db: Session = Depends(get_db)):
    """Get verifier dashboard statistics"""
    print(f"Verifier dashboard accessed by: {verifier}")
    
    try:
        # Get verifications from database
        verifications = db.query(Verification).filter(Verification.verifier_id == verifier["user_id"]).all()
        
        total_verifications = len(verifications)
        valid_certificates = sum(1 for v in verifications if v.result)
        invalid_certificates = sum(1 for v in verifications if not v.result)
        tampered_certificates = sum(1 for v in verifications if v.status == "tampered")
        
        success_rate = (valid_certificates / total_verifications * 100) if total_verifications > 0 else 0
        
        return {
            "statistics": {
                "total_verifications": total_verifications,
                "valid_certificates": valid_certificates,
                "invalid_certificates": invalid_certificates,
                "tampered_certificates": tampered_certificates
            },
            "success_rate": success_rate
        }
    except Exception as e:
        print(f"Error in verifier dashboard: {str(e)}")
        # Return default values if error
        return {
            "statistics": {
                "total_verifications": 0,
                "valid_certificates": 0,
                "invalid_certificates": 0,
                "tampered_certificates": 0
            },
            "success_rate": 0
        }
    finally:
        db.close()

@app.get("/verifier/history")
async def verifier_history(verifier = Depends(require_verifier), db: Session = Depends(get_db)):
    """Get verifier verification history"""
    try:
        verifications = db.query(Verification).filter(Verification.verifier_id == verifier["user_id"]).order_by(Verification.timestamp.desc()).all()
        
        verifier_verifications = [
            {
                "verification_id": v.id,
                "certificate_hash": v.certificate_hash,
                "verification_result": "valid" if v.result else "invalid",
                "confidence_score": v.confidence_score or 0.0,
                "timestamp": v.timestamp.isoformat()
            }
            for v in verifications
        ]
        
        return {"history": verifier_verifications}
    except Exception as e:
        print(f"Error in verifier history: {str(e)}")
        return {"history": []}
    finally:
        db.close()

@app.get("/verifier/feedback")
async def get_verifier_feedback(verifier = Depends(require_verifier), db: Session = Depends(get_db)):
    """Get verifier's submitted feedback"""
    try:
        feedbacks = db.query(Feedback).filter(Feedback.verifier_id == verifier["user_id"]).order_by(Feedback.timestamp.desc()).all()
        
        verifier_feedbacks = [
            {
                "id": f.id,
                "feedback_type": f.category,
                "message": f.message,
                "priority": f.priority,
                "timestamp": f.timestamp.isoformat(),
                "flagged": f.flagged
            }
            for f in feedbacks
        ]
        
        return {"feedbacks": verifier_feedbacks}
    except Exception as e:
        print(f"Error in verifier feedback: {str(e)}")
        return {"feedbacks": []}
    finally:
        db.close()

@app.post("/verifier/verify")
async def verify_certificate(file: UploadFile = File(...), verifier = Depends(require_verifier)):
    """Verify certificate by comparing uploaded file hash with stored hash"""
    db = get_db_session()
    try:
        print(f"\n=== Certificate Verification Started ===")
        print(f"Verifier ID: {verifier['user_id']}")
        print(f"File: {file.filename}")
        
        # Read uploaded file
        content = await file.read()
        print(f"File size: {len(content)} bytes")
        
        # Generate hash of uploaded file
        uploaded_hash = generate_file_hash(content)
        print(f"Uploaded file hash: {uploaded_hash}")
        
        # Search for certificate with matching hash
        cert = db.query(Certificate).filter(Certificate.hash == uploaded_hash).first()
        
        if cert:
            # Certificate found - VALID
            print(f"✅ Certificate found: {cert.id}")
            is_valid = True
            
            # Get student and institute details
            student = db.query(Student).filter(Student.id == cert.student_id).first()
            institute = db.query(Institute).filter(Institute.id == cert.institute_id).first()
            
            # AI validation
            ai_result = AIValidationService.validate_certificate_content(content, file.filename)
            
            # Blockchain verification
            blockchain_data = BlockchainService.verify_certificate_hash(uploaded_hash)
            
            explanation = f"Certificate verified successfully. Issued by {institute.name if institute else 'Unknown'} to {student.name if student else 'Unknown'}."
            
            # Update verification count
            cert.verification_count = (cert.verification_count or 0) + 1
            
            result_data = {
                "status": "valid",
                "certificate_id": cert.id,
                "certificate_name": cert.name,
                "student_id": student.student_id if student else None,
                "student_name": student.name if student else None,
                "institute_id": institute.institute_id if institute else None,
                "institute_name": institute.name if institute else None,
                "issue_date": cert.issue_date.isoformat() if cert.issue_date else None,
                "verification_count": cert.verification_count,
                "message": "Certificate verified successfully"
            }
        else:
            # Certificate not found - INVALID/FAKE
            print(f"❌ Certificate not found in database")
            is_valid = False
            ai_result = AIValidationService.validate_certificate_content(content, file.filename)
            blockchain_data = None
            explanation = "Certificate not found in database. This may be a fake or modified certificate."
            
            result_data = {
                "status": "invalid",
                "message": "Certificate not found or has been modified"
            }
        
        # Save verification to database
        from database import VerificationStatusEnum
        verification_id = str(uuid.uuid4())
        new_verification = Verification(
            id=verification_id,
            certificate_id=cert.id if cert else None,
            certificate_hash=uploaded_hash,
            verifier_id=verifier["user_id"],
            result=is_valid,
            confidence_score=ai_result.get("confidence", 0.0) if ai_result else 0.0,
            status=VerificationStatusEnum.VALID if is_valid else VerificationStatusEnum.INVALID,
            blockchain_integrity=is_valid,
            timestamp=datetime.utcnow()
        )
        db.add(new_verification)
        
        # Add to blockchain
        BlockchainService.add_verification(uploaded_hash, verifier["user_id"], is_valid)
        
        db.commit()
        
        print(f"Verification saved: {verification_id}")
        print(f"Result: {'VALID' if is_valid else 'INVALID'}")
        print(f"=== Certificate Verification Completed ===\n")
        
        return {
            "verification_id": verification_id,
            "verification_result": "valid" if is_valid else "invalid",
            "result": is_valid,
            "certificate_hash": uploaded_hash,
            "confidence_score": ai_result.get("confidence", 0.0) if ai_result else 0.0,
            "blockchain_verified": is_valid,
            "explanation": explanation,
            **result_data
        }
    except Exception as e:
        print(f"❌ Verification error: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")
    finally:
        db.close()

@app.post("/verifier/feedback")
async def submit_feedback(
    feedback_type: str = Form(...),
    message: str = Form(...),
    priority: str = Form("medium"),
    verifier = Depends(require_verifier)
):
    """Submit feedback"""
    db = get_db_session()
    try:
        feedback_id = str(uuid.uuid4())
        new_feedback = Feedback(
            id=feedback_id,
            verifier_id=verifier["user_id"],
            message=message,
            category=feedback_type,
            priority=priority,
            status="open",
            flagged=False,
            timestamp=datetime.utcnow()
        )
        db.add(new_feedback)
        db.commit()
        return {"message": "Feedback submitted successfully", "feedback_id": feedback_id}
    finally:
        db.close()

# AI Query Endpoints
ai_service = AIQueryService()

@app.post("/admin/ai-query")
async def admin_ai_query(request: dict, admin = Depends(require_admin), db: Session = Depends(get_db)):
    """AI assistant for admin dashboard"""
    query = request.get('query', '')
    session_id = request.get('session_id', 'default')
    
    if not query:
        return {"response": "Please ask me a question about the system."}
    
    response = ai_service.process_admin_query(query, db, session_id)
    return {"response": response}

@app.post("/institute/ai-query")
async def institute_ai_query(request: dict, institute = Depends(require_institute), db: Session = Depends(get_db)):
    """AI assistant for institute dashboard"""
    query = request.get('query', '')
    session_id = request.get('session_id', 'default')
    
    if not query:
        return {"response": "Please ask me a question about your institute."}
    
    response = ai_service.process_institute_query(query, db, institute["user_id"], session_id)
    return {"response": response}

@app.get("/verifier/ai-query")
async def verifier_ai_query(query: str = Query(...), verifier = Depends(require_verifier), db: Session = Depends(get_db)):
    """AI assistant for verifier dashboard with database context"""
    from verifier_chatbot import VerifierChatbot
    
    if not query:
        return {"response": "Please ask me a question about certificate verification."}
    
    try:
        response = VerifierChatbot.process_query(query, verifier["user_id"], db)
        return {"response": response, "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        print(f"Verifier AI Query Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"response": "Sorry, I encountered an error. Please try again.", "error": str(e)}

# Chatbot Endpoint
@app.post("/chatbot")
async def chatbot_query(request: ChatMessage, user = Depends(get_current_user)):
    response = ChatbotService.process_query(request.message, user["role"], user["user_id"])
    return response

# Public Endpoints
@app.get("/")
async def root():
    return {"message": "CertiSense AI - Enhanced Blockchain Certificate System", "version": "3.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "blockchain_connected": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)