import jwt
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import HTTPException, Depends, Header
from sqlalchemy.orm import Session
from database import get_db, AuditLog

SECRET_KEY = "certisense-admin-secret-key-v3"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# In-memory admin credentials (in production, use database)
ADMIN_CREDENTIALS = {
    "admin": {
        "id": "admin-001",
        "username": "admin",
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
        "email": "admin@certisense.ai"
    }
}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_access_token(user_id: str, role: str, username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "user_id": user_id,
        "role": role,
        "username": username,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[Dict]:
    try:
        print(f"[verify_token] Decoding token with SECRET_KEY: {SECRET_KEY[:10]}...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"[verify_token] Token decoded successfully: {payload}")
        return payload
    except jwt.ExpiredSignatureError as e:
        print(f"[verify_token] Token expired: {str(e)}")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        print(f"[verify_token] Invalid token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"[verify_token] Unexpected error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate_admin(username: str, password: str) -> Optional[str]:
    admin = ADMIN_CREDENTIALS.get(username)
    if admin and verify_password(password, admin["password"]):
        return create_access_token(admin["id"], admin["role"], admin["username"])
    return None

def get_current_user(authorization: Optional[str] = Header(None)):
    print(f"[auth_db] Authorization header: {authorization}")
    if not authorization or not authorization.startswith("Bearer "):
        print("[auth_db] No authorization header or invalid format")
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    print(f"[auth_db] Token extracted: {token[:20]}...")
    
    try:
        payload = verify_token(token)
        print(f"[auth_db] Token verified successfully: {payload}")
        return payload
    except Exception as e:
        print(f"[auth_db] Token verification failed: {str(e)}")
        raise

def require_admin(user: Dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_institute(user: Dict = Depends(get_current_user)):
    if user["role"] != "institute":
        raise HTTPException(status_code=403, detail="Institute access required")
    return user

def require_student(user: Dict = Depends(get_current_user)):
    if user["role"] != "student":
        raise HTTPException(status_code=403, detail="Student access required")
    return user

def require_verifier(user: Dict = Depends(get_current_user)):
    if user["role"] != "verifier":
        raise HTTPException(status_code=403, detail="Verifier access required")
    return user

def authenticate_institute(username: str, password: str) -> Optional[str]:
    from database import SessionLocal, Institute
    db = SessionLocal()
    try:
        institute = db.query(Institute).filter(Institute.email == username).first()
        if institute and verify_password(password, institute.password_hash):
            return create_access_token(institute.id, "institute", institute.email)
        return None
    finally:
        db.close()

def authenticate_student(username: str, password: str) -> Optional[str]:
    from database import SessionLocal, Student
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.student_id == username).first()
        if student and verify_password(password, student.password_hash):
            return create_access_token(student.id, "student", student.student_id)
        return None
    finally:
        db.close()

def authenticate_verifier(username: str, password: str) -> Optional[str]:
    from database import SessionLocal, Verifier
    db = SessionLocal()
    try:
        verifier = db.query(Verifier).filter(Verifier.username == username).first()
        if verifier and verify_password(password, verifier.password_hash):
            return create_access_token(verifier.id, "verifier", verifier.username)
        return None
    finally:
        db.close()

def register_institute(name: str, institute_id: str, password: str, email: str, location: str = None):
    from database import SessionLocal, Institute
    db = SessionLocal()
    try:
        existing = db.query(Institute).filter(Institute.email == email).first()
        if existing:
            return False, None
        
        count = db.query(Institute).count() + 1
        new_id = str(uuid.uuid4())
        inst_id = f"INST{count:05d}"
        
        institute = Institute(
            id=new_id,
            institute_id=inst_id,
            name=name,
            email=email,
            password_hash=hash_password(password),
            location=location,
            approval_status="approved",
            is_verified=True,
            created_at=datetime.utcnow()
        )
        db.add(institute)
        db.commit()
        return True, inst_id
    finally:
        db.close()

def register_student(name: str, email: str, password: str, institute_id: str):
    from database import SessionLocal, Student, Institute
    db = SessionLocal()
    try:
        institute = db.query(Institute).filter(Institute.id == institute_id).first()
        if not institute:
            return False, None
        
        student_count = db.query(Student).filter(Student.institute_id == institute_id).count()
        student_id = f"{institute.institute_id}-{str(student_count + 1).zfill(5)}"
        
        student = Student(
            id=str(uuid.uuid4()),
            student_id=student_id,
            name=name,
            email=email,
            password_hash=hash_password(password),
            institute_id=institute_id,
            created_at=datetime.utcnow()
        )
        db.add(student)
        db.commit()
        return True, student_id
    finally:
        db.close()

def register_verifier(username: str, password: str, email: str):
    from database import SessionLocal, Verifier
    db = SessionLocal()
    try:
        existing = db.query(Verifier).filter(Verifier.email == email).first()
        if existing:
            return False
        
        verifier = Verifier(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=hash_password(password),
            status="active",
            created_at=datetime.utcnow()
        )
        db.add(verifier)
        db.commit()
        return True
    finally:
        db.close()

def log_audit(db: Session, user_id: str, user_role: str, action: str, 
              entity_type: str, entity_id: str, details: str, ip_address: str = None):
    audit = AuditLog(
        id=str(uuid.uuid4()),
        user_id=user_id,
        user_role=user_role,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details,
        ip_address=ip_address,
        timestamp=datetime.utcnow()
    )
    db.add(audit)
    db.commit()
