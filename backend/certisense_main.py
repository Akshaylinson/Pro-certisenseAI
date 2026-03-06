from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Header, Query, Form
from fastapi.middleware.cors import CORSMiddleware
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
from database import get_db, Institute, Student, Verifier, Certificate, Verification, Feedback, CertificateStatusEnum
from blockchain_service import BlockchainService, generate_file_hash
from ai_service import AIValidationService
from chatbot_service import ChatbotService
from admin_api import router as admin_router

app = FastAPI(title="CertiSense AI - Enhanced Blockchain Certificate System", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def add_student(name: str = Query(...), email: str = Query(...), password: str = Query(...), institute = Depends(require_institute)):
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
async def issue_certificate(file: UploadFile = File(...), student_id: str = Query(...), institute = Depends(require_institute)):
    db = get_db_session()
    try:
        content = await file.read()
        file_hash = generate_file_hash(content)
        
        # Validate certificate content
        ai_result = AIValidationService.validate_certificate_content(content, file.filename)
        if not ai_result["valid"]:
            raise HTTPException(status_code=400, detail=f"Invalid certificate: {ai_result['reason']}")
        
        # Find student by student_id string (e.g., "INST00001-00001")
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")
        
        # Verify student belongs to this institute
        if student.institute_id != institute["user_id"]:
            raise HTTPException(status_code=403, detail="Student does not belong to your institute")
        
        # Store certificate hash in blockchain
        chain_hash = BlockchainService.store_certificate_hash(file_hash, student_id, institute["user_id"], institute["user_id"])
        
        # Save certificate to DATABASE
        cert_id = str(uuid.uuid4())
        new_cert = Certificate(
            id=cert_id,
            name=file.filename,
            hash=file_hash,
            chain_hash=chain_hash,
            student_id=student.id,  # Use student UUID, not student_id string
            institute_id=institute["user_id"],
            issuer_id=institute["user_id"],
            status=CertificateStatusEnum.ACTIVE,
            issue_date=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        db.add(new_cert)
        db.commit()
        
        print(f"Certificate saved to database: {cert_id} for student {student.student_id}")
        
        return {
            "message": "Certificate issued successfully",
            "certificate_id": cert_id,
            "hash": file_hash,
            "chain_hash": chain_hash
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error issuing certificate: {str(e)}")
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
        
        certificates = BlockchainService.get_student_certificates(student_data.student_id)
        return {"certificates": certificates}
    finally:
        db.close()

@app.get("/student/certificate/{cert_hash}")
async def get_certificate_details(cert_hash: str, student = Depends(require_student)):
    chain_data = BlockchainService.get_certificate_chain(cert_hash)
    if not chain_data:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    return chain_data

# Verifier Endpoints
@app.post("/verifier/verify")
async def verify_certificate(file: UploadFile = File(...), verifier = Depends(require_verifier)):
    content = await file.read()
    file_hash = generate_file_hash(content)
    
    ai_result = AIValidationService.validate_certificate_content(content, file.filename)
    blockchain_data = BlockchainService.verify_certificate_hash(file_hash)
    is_valid = blockchain_data is not None and blockchain_data.get("valid", False)
    
    explanation = AIValidationService.explain_verification_result(is_valid, blockchain_data)
    
    BlockchainService.add_verification(file_hash, verifier["user_id"], is_valid)
    
    verification_id = str(uuid.uuid4())
    verifications_db[verification_id] = {
        "id": verification_id,
        "certificate_hash": file_hash,
        "verifier_id": verifier["user_id"],
        "result": is_valid,
        "ai_validation": ai_result,
        "blockchain_data": blockchain_data,
        "explanation": explanation,
        "timestamp": datetime.utcnow()
    }
    
    return {
        "verification_id": verification_id,
        "result": is_valid,
        "hash": file_hash,
        "ai_validation": ai_result,
        "blockchain_data": blockchain_data,
        "explanation": explanation
    }

@app.post("/verifier/feedback")
async def submit_feedback(message: str = Query(...), category: str = Query(...), verifier = Depends(require_verifier)):
    feedback_id = str(uuid.uuid4())
    feedback_db[feedback_id] = {
        "id": feedback_id,
        "verifier_id": verifier["user_id"],
        "message": message,
        "category": category,
        "timestamp": datetime.utcnow()
    }
    return {"message": "Feedback submitted successfully", "feedback_id": feedback_id}

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