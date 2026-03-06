from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from sqlalchemy.orm import Session
from models import *
from auth_db import authenticate_admin, verify_token, register_institute, register_verifier
from database import get_db, Institute, Student, Verifier

app = FastAPI(title="CertiSense AI", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/auth/admin/login")
async def admin_login(request: LoginRequest):
    token = authenticate_admin(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    return {"access_token": token, "token_type": "bearer", "role": "admin"}

@app.get("/admin/reports")
@app.post("/admin/reports")
async def get_admin_reports(admin = Depends(require_admin), db: Session = Depends(get_db)):
    total_institutes = db.query(Institute).count()
    total_students = db.query(Student).count()
    total_verifiers = db.query(Verifier).count()
    
    return {
        "total_institutes": total_institutes,
        "total_students": total_students,
        "total_certificates": 0,
        "total_verifications": 0,
        "total_verifiers": total_verifiers,
        "institute_stats": {}
    }

@app.get("/admin/institutes")
async def get_institutes(admin = Depends(require_admin), db: Session = Depends(get_db)):
    institutes = db.query(Institute).all()
    print(f"Found {len(institutes)} institutes in database")
    return {
        "institutes": [
            {
                "id": inst.id,
                "institute_id": inst.institute_id or inst.username,
                "name": inst.name,
                "email": inst.email,
                "location": inst.location or "",
                "student_count": 0,
                "created_at": inst.created_at
            }
            for inst in institutes
        ]
    }

@app.post("/admin/institutes")
async def add_institute(request: InstituteRegisterRequest, admin = Depends(require_admin)):
    success, institute_id = register_institute(request.institute_name, "", request.password, request.email, request.location)
    if not success:
        raise HTTPException(status_code=400, detail="Institute registration failed")
    return {"message": "Institute added successfully", "institute_id": institute_id}

@app.get("/admin/verifiers")
@app.post("/admin/verifiers")
async def handle_verifiers(request: RegisterRequest = None, admin = Depends(require_admin), db: Session = Depends(get_db)):
    if request:  # POST request
        success = register_verifier(request.username, request.password, request.email)
        if not success:
            raise HTTPException(status_code=400, detail="Username already exists")
        return {"message": "Verifier added successfully"}
    else:  # GET request
        verifiers = db.query(Verifier).all()
        return {
            "verifiers": [
                {
                    "id": v.id,
                    "name": v.name,
                    "email": v.email,
                    "organization": v.organization or "N/A",
                    "created_at": v.created_at
                }
                for v in verifiers
            ]
        }

@app.get("/admin/certificates")
@app.post("/admin/certificates")
async def handle_certificates(admin = Depends(require_admin)):
    return {"certificates": []}

@app.get("/admin/feedback")
@app.post("/admin/feedback")
async def handle_feedback(admin = Depends(require_admin)):
    return {"feedbacks": []}

@app.delete("/admin/institutes/{institute_id}")
async def delete_institute(institute_id: str, admin = Depends(require_admin), db: Session = Depends(get_db)):
    institute = db.query(Institute).filter(Institute.id == institute_id).first()
    if not institute:
        raise HTTPException(status_code=404, detail="Institute not found")
    db.delete(institute)
    db.commit()
    return {"message": "Institute deleted successfully"}

@app.delete("/admin/verifiers/{verifier_id}")
async def delete_verifier(verifier_id: str, admin = Depends(require_admin), db: Session = Depends(get_db)):
    verifier = db.query(Verifier).filter(Verifier.id == verifier_id).first()
    if not verifier:
        raise HTTPException(status_code=404, detail="Verifier not found")
    db.delete(verifier)
    db.commit()
    return {"message": "Verifier deleted successfully"}

@app.get("/test/db")
async def test_db(db: Session = Depends(get_db)):
    institutes = db.query(Institute).all()
    return {
        "institutes_count": len(institutes),
        "institutes": [{
            "id": inst.id,
            "name": inst.name,
            "username": inst.username,
            "institute_id": inst.institute_id
        } for inst in institutes]
    }

@app.get("/")
async def root():
    return {"message": "CertiSense AI", "version": "3.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)