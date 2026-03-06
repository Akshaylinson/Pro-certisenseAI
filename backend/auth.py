import jwt
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from models import UserRole
import re

SECRET_KEY = "certisense-ai-secret-key"
ALGORITHM = "HS256"

# Mock databases
users_db = {
    "admin": {
        "id": "admin-1",
        "username": "admin",
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": UserRole.ADMIN,
        "email": "admin@certisense.edu"
    }
}

institutes_db = {
    "INTT00001": {
        "id": "institute-1",
        "name": "Test Institute",
        "username": "INTT00001",
        "password": hashlib.sha256("institute123".encode()).hexdigest(),
        "role": UserRole.INSTITUTE,
        "email": "test@institute.edu",
        "location": "Test City",
        "institute_id": "INTT00001",
        "description": "A test institute for demonstration",
        "image": None,
        "created_at": datetime.utcnow()
    }
}

students_db = {}
verifiers_db = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {"user_id": user_id, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_student_id(institute_id: str) -> str:
    # Get institute data
    institute = next((inst for inst in institutes_db.values() if inst["id"] == institute_id), None)
    if not institute:
        return None
    
    # Use custom institute_id if available, otherwise clean institute name
    if institute.get("institute_id"):
        institute_prefix = institute["institute_id"].upper()
    else:
        institute_prefix = re.sub(r'[^A-Za-z0-9]', '', institute["name"]).upper()
    
    # Count existing students for this institute
    existing_students = [s for s in students_db.values() if s["institute_id"] == institute_id]
    next_number = len(existing_students) + 1
    
    # Generate student ID: INSTITUTEID-00001
    student_id = f"{institute_prefix}-{next_number:05d}"
    return student_id

def authenticate_admin(username: str, password: str) -> Optional[str]:
    user = users_db.get(username)
    if user and verify_password(password, user["password"]) and user["role"] == UserRole.ADMIN:
        return create_access_token(user["id"], user["role"])
    return None

def register_institute(institute_name: str, username: str, password: str, email: str, location: str = None) -> tuple[bool, str]:
    # Auto-generate Institute-ID in format INTT00001
    institute_count = len(institutes_db) + 1
    auto_username = f"INTT{institute_count:05d}"
    
    # Ensure unique Institute-ID
    while auto_username in institutes_db:
        institute_count += 1
        auto_username = f"INTT{institute_count:05d}"
    
    institute_id = f"institute-{institute_count}"
    
    institutes_db[auto_username] = {
        "id": institute_id,
        "name": institute_name,
        "username": auto_username,
        "password": hash_password(password),
        "role": UserRole.INSTITUTE,
        "email": email,
        "location": location,
        "institute_id": auto_username,
        "description": "",
        "image": None,
        "created_at": datetime.utcnow()
    }
    return True, auto_username

def authenticate_institute(username: str, password: str) -> Optional[str]:
    user = institutes_db.get(username)
    if user and verify_password(password, user["password"]):
        return create_access_token(user["id"], user["role"])
    return None

def update_institute_profile(institute_id: str, data: dict) -> bool:
    institute = next((inst for inst in institutes_db.values() if inst["id"] == institute_id), None)
    if not institute:
        return False
    
    # Update institute data
    if "institute_name" in data:
        institute["name"] = data["institute_name"]
    if "institute_id" in data:
        institute["institute_id"] = data["institute_id"].upper()
    if "email" in data:
        institute["email"] = data["email"]
    if "location" in data:
        institute["location"] = data["location"]
    if "description" in data:
        institute["description"] = data["description"]
    if "image" in data:
        institute["image"] = data["image"]
    
    return True

def register_student(name: str, email: str, password: str, institute_id: str) -> tuple[bool, str]:
    # Auto-generate student ID
    student_id = generate_student_id(institute_id)
    if not student_id:
        return False, None
    
    # Check if student ID already exists (shouldn't happen with auto-generation)
    if student_id in students_db:
        return False, None
    
    student_uuid = f"student-{len(students_db) + 1}"
    students_db[student_id] = {
        "id": student_uuid,
        "student_id": student_id,
        "name": name,
        "institute_id": institute_id,
        "email": email,
        "password": hash_password(password),
        "role": UserRole.STUDENT,
        "created_at": datetime.utcnow()
    }
    return True, student_id

def authenticate_student(student_id: str, password: str) -> Optional[str]:
    user = students_db.get(student_id)
    if user and verify_password(password, user["password"]):
        return create_access_token(user["id"], user["role"])
    return None

def register_verifier(username: str, password: str, email: str) -> bool:
    if username in verifiers_db:
        return False
    
    verifier_id = f"verifier-{len(verifiers_db) + 1}"
    verifiers_db[username] = {
        "id": verifier_id,
        "username": username,
        "password": hash_password(password),
        "role": UserRole.VERIFIER,
        "email": email,
        "created_at": datetime.utcnow()
    }
    return True

def authenticate_verifier(username: str, password: str) -> Optional[str]:
    user = verifiers_db.get(username)
    if user and verify_password(password, user["password"]):
        return create_access_token(user["id"], user["role"])
    return None