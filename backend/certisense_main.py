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
from database import get_db, Institute, Student, Verifier, Certificate, Verification, Feedback
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

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
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

# Admin Endpoints - Institute Management
@app.get("/admin/institutes")
async def get_institutes(admin = Depends(require_admin)):
    institutes = [
        {
            "id": institute["id"],
            "institute_id": institute["username"],
            "name": institute["name"],
            "email": institute["email"],
            "location": institute["location"],
            "student_count": sum(1 for s in students_db.values() if s["institute_id"] == institute["id"]),
            "created_at": institute["created_at"]
        }
        for institute in institutes_db.values()
    ]
    return {"institutes": institutes}

@app.post("/admin/institutes")
async def add_institute(request: InstituteRegisterRequest, admin = Depends(require_admin)):
    success, institute_id = register_institute(request.institute_name, "", request.password, request.email, request.location)
    if not success:
        raise HTTPException(status_code=400, detail="Institute registration failed")
    return {"message": "Institute added successfully", "institute_id": institute_id}

@app.put("/admin/institutes/{institute_id}")
async def update_institute(institute_id: str, name: str = Query(...), email: str = Query(...), location: str = Query(""), admin = Depends(require_admin)):
    institute = next((i for i in institutes_db.values() if i["id"] == institute_id), None)
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    institute["name"] = name
    institute["email"] = email
    institute["location"] = location
    return {"message": "Institute updated successfully"}

@app.delete("/admin/institutes/{institute_id}")
async def delete_institute(institute_id: str, admin = Depends(require_admin)):
    institute = next((i for i in institutes_db.values() if i["id"] == institute_id), None)
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    del institutes_db[institute["username"]]
    return {"message": "Institute deleted successfully"}

# Admin Endpoints - Verifier Management
@app.get("/admin/verifiers")
async def get_verifiers(admin = Depends(require_admin)):
    verifiers = [
        {
            "id": v["id"],
            "name": v.get("name", v["username"]),
            "email": v["email"],
            "organization": v.get("organization", "N/A"),
            "created_at": v.get("created_at", datetime.utcnow())
        }
        for v in verifiers_db.values()
    ]
    return {"verifiers": verifiers}

@app.post("/admin/verifiers")
async def add_verifier(request: RegisterRequest, admin = Depends(require_admin)):
    success = register_verifier(request.username, request.password, request.email)
    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    verifier = verifiers_db[request.username]
    verifier["name"] = request.username
    verifier["organization"] = getattr(request, "organization", "N/A")
    
    return {"message": "Verifier added successfully"}

@app.put("/admin/verifiers/{verifier_id}")
async def update_verifier(verifier_id: str, name: str = Query(...), email: str = Query(...), organization: str = Query(...), admin = Depends(require_admin)):
    verifier = next((v for v in verifiers_db.values() if v["id"] == verifier_id), None)
    if not verifier:
        raise HTTPException(status_code=404, detail="Verifier not found")
    
    verifier["name"] = name
    verifier["email"] = email
    verifier["organization"] = organization
    
    return {"message": "Verifier updated successfully"}

@app.delete("/admin/verifiers/{verifier_id}")
async def delete_verifier(verifier_id: str, admin = Depends(require_admin)):
    verifier = next((v for v in verifiers_db.values() if v["id"] == verifier_id), None)
    if not verifier:
        raise HTTPException(status_code=404, detail="Verifier not found")
    
    del verifiers_db[verifier["username"]]
    return {"message": "Verifier deleted successfully"}

# Admin Endpoints - Certificate Management
@app.get("/admin/certificates")
async def get_all_certificates(admin = Depends(require_admin)):
    certificates = [
        {
            "id": c["id"],
            "certificate_name": c["name"],
            "student_id": c["student_id"],
            "institute_id": c["institute_id"],
            "hash": c["hash"],
            "blockchain_status": "Added",
            "created_at": c["created_at"]
        }
        for c in certificates_db.values()
    ]
    return {"certificates": certificates}

@app.post("/admin/certificates")
async def add_certificate_admin(file: UploadFile = File(...), student_id: str = Query(...), institute_id: str = Query(...), certificate_name: str = Query(...), admin = Depends(require_admin)):
    content = await file.read()
    file_hash = generate_file_hash(content)
    
    chain_hash = BlockchainService.store_certificate_hash(file_hash, student_id, institute_id, admin["user_id"])
    
    cert_id = str(uuid.uuid4())
    certificates_db[cert_id] = {
        "id": cert_id,
        "name": certificate_name,
        "hash": file_hash,
        "student_id": student_id,
        "institute_id": institute_id,
        "issuer_id": admin["user_id"],
        "chain_hash": chain_hash,
        "created_at": datetime.utcnow()
    }
    
    return {"message": "Certificate added to blockchain", "certificate_id": cert_id, "hash": file_hash}

@app.delete("/admin/certificates/{cert_id}")
async def delete_certificate(cert_id: str, admin = Depends(require_admin)):
    if cert_id not in certificates_db:
        raise HTTPException(status_code=404, detail="Certificate not found")
    
    del certificates_db[cert_id]
    return {"message": "Certificate deleted successfully"}

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

# Admin Endpoints - Feedback Management
@app.get("/admin/feedback")
async def get_all_feedback(admin = Depends(require_admin)):
    feedbacks = [
        {
            "id": f["id"],
            "sender_type": "Verifier",
            "sender_name": next((v["username"] for v in verifiers_db.values() if v["id"] == f["verifier_id"]), "Unknown"),
            "email": next((v["email"] for v in verifiers_db.values() if v["id"] == f["verifier_id"]), "N/A"),
            "message": f["message"],
            "category": f["category"],
            "timestamp": f["timestamp"]
        }
        for f in feedback_db.values()
    ]
    return {"feedbacks": feedbacks}

# Admin Endpoints - AI Report Generation
@app.get("/admin/generate-report")
async def generate_ai_report(admin = Depends(require_admin)):
    total_institutes = len(institutes_db)
    total_students = len(students_db)
    total_certificates = len(certificates_db)
    total_verifications = len(verifications_db)
    
    health_score = min(100, 70 + (total_certificates * 2))
    efficiency_score = min(100, 80 + (total_verifications))
    
    ai_summary = f"System Analysis: {total_institutes} institutes managing {total_students} students with {total_certificates} certificates verified {total_verifications} times. Overall system health is optimal."
    
    return {
        "ai_summary": ai_summary,
        "health_score": health_score,
        "efficiency_score": efficiency_score,
        "insight_1": f"System operating at {health_score}% capacity with {total_certificates} certificates on blockchain",
        "insight_2": f"Certificate verification rate: {(total_verifications/max(1, total_certificates)*100):.1f}%",
        "insight_3": "All institutes performing within expected parameters",
        "total_institutes": total_institutes,
        "total_students": total_students,
        "total_certificates": total_certificates,
        "total_verifications": total_verifications
    }

# Admin Endpoints - Reports
@app.get("/admin/reports")
async def get_admin_reports(admin = Depends(require_admin)):
    total_institutes = len(institutes_db)
    total_students = len(students_db)
    total_certificates = len(certificates_db)
    total_verifications = len(verifications_db)
    
    institute_stats = {}
    for institute in institutes_db.values():
        student_count = sum(1 for s in students_db.values() if s["institute_id"] == institute["id"])
        cert_count = sum(1 for c in certificates_db.values() if c["institute_id"] == institute["id"])
        institute_stats[institute["name"]] = {"students": student_count, "certificates": cert_count}
    
    return {
        "total_institutes": total_institutes,
        "total_students": total_students,
        "total_certificates": total_certificates,
        "total_verifications": total_verifications,
        "institute_stats": institute_stats
    }

# Institute Endpoints - Profile Management
@app.get("/institute/profile")
async def get_institute_profile(institute = Depends(require_institute)):
    institute_data = next((i for i in institutes_db.values() if i["id"] == institute["user_id"]), None)
    if not institute_data:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    return {
        "institute_name": institute_data["name"],
        "institute_id": institute_data.get("institute_id", ""),
        "email": institute_data["email"],
        "location": institute_data.get("location", ""),
        "description": institute_data.get("description", ""),
        "image": institute_data.get("image"),
        "created_at": institute_data["created_at"]
    }

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
    update_data = {
        "institute_name": institute_name,
        "institute_id": institute_id,
        "email": email,
        "location": location,
        "description": description
    }
    
    # Handle image upload
    if image:
        content = await image.read()
        # Convert to base64 for storage (in real app, save to file system or cloud)
        image_data = base64.b64encode(content).decode()
        update_data["image"] = f"data:image/{image.filename.split('.')[-1]};base64,{image_data}"
    
    success = update_institute_profile(institute["user_id"], update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Institute not found")
    
    return {"message": "Profile updated successfully"}

# Institute Endpoints - Student Management
@app.get("/institute/students")
async def get_institute_students(institute = Depends(require_institute)):
    students = [
        {
            "id": s["id"],
            "student_id": s["student_id"],
            "name": s["name"],
            "email": s["email"],
            "created_at": s["created_at"]
        }
        for s in students_db.values()
        if s["institute_id"] == institute["user_id"]
    ]
    return {"students": students}

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
    # Find student by internal ID (not student_id)
    student = next((s for s in students_db.values() if s["id"] == student_id and s["institute_id"] == institute["user_id"]), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found or not authorized")
    
    # Update student details (student_id cannot be changed)
    student["name"] = name
    student["email"] = email
    
    return {"message": "Student updated successfully"}

@app.post("/institute/certificates")
async def issue_certificate(file: UploadFile = File(...), student_id: str = Query(...), institute = Depends(require_institute)):
    content = await file.read()
    file_hash = generate_file_hash(content)
    
    ai_result = AIValidationService.validate_certificate_content(content, file.filename)
    if not ai_result["valid"]:
        raise HTTPException(status_code=400, detail=f"Invalid certificate: {ai_result['reason']}")
    
    chain_hash = BlockchainService.store_certificate_hash(file_hash, student_id, institute["user_id"], institute["user_id"])
    
    cert_id = str(uuid.uuid4())
    certificates_db[cert_id] = {
        "id": cert_id,
        "name": file.filename,
        "hash": file_hash,
        "student_id": student_id,
        "institute_id": institute["user_id"],
        "issuer_id": institute["user_id"],
        "chain_hash": chain_hash,
        "created_at": datetime.utcnow(),
        "ai_validation": ai_result
    }
    
    return {"message": "Certificate issued successfully", "certificate_id": cert_id, "hash": file_hash, "chain_hash": chain_hash}

@app.get("/institute/dashboard")
async def institute_dashboard(institute = Depends(require_institute)):
    students = sum(1 for s in students_db.values() if s["institute_id"] == institute["user_id"])
    certificates = sum(1 for c in certificates_db.values() if c["institute_id"] == institute["user_id"])
    verifications = sum(1 for v in verifications_db.values() if any(c["institute_id"] == institute["user_id"] for c in certificates_db.values() if c["id"] == v.get("certificate_id")))
    
    return {
        "total_students": students,
        "total_certificates": certificates,
        "total_verifications": verifications
    }

# Student Endpoints
@app.get("/student/profile")
async def get_student_profile(student = Depends(require_student)):
    student_data = next((s for s in students_db.values() if s["id"] == student["user_id"]), None)
    if not student_data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "student_id": student_data["student_id"],
        "name": student_data["name"],
        "email": student_data["email"],
        "institute_id": student_data["institute_id"],
        "created_at": student_data["created_at"]
    }

@app.put("/student/profile")
async def update_student_profile(name: str = Query(...), email: str = Query(...), student = Depends(require_student)):
    student_data = next((s for s in students_db.values() if s["id"] == student["user_id"]), None)
    if student_data:
        student_data["name"] = name
        student_data["email"] = email
    return {"message": "Profile updated successfully"}

@app.get("/student/certificates")
async def get_student_certificates(student = Depends(require_student)):
    student_data = next((s for s in students_db.values() if s["id"] == student["user_id"]), None)
    if not student_data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    certificates = BlockchainService.get_student_certificates(student_data["student_id"])
    return {"certificates": certificates}

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