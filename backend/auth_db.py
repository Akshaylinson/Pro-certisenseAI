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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate_admin(username: str, password: str) -> Optional[str]:
    admin = ADMIN_CREDENTIALS.get(username)
    if admin and verify_password(password, admin["password"]):
        return create_access_token(admin["id"], admin["role"], admin["username"])
    return None

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    token = authorization.split(" ")[1]
    return verify_token(token)

def require_admin(user: Dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

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
