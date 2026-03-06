import jwt
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict
import uuid

SECRET_KEY = "certisense-verifier-secret-v3"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# In-memory verifier database (production: use database)
verifiers_db = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_verifier_token(verifier_id: str, username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "verifier_id": verifier_id,
        "username": username,
        "role": "verifier",
        "exp": expire,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_verifier_token(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_verifier(username: str, email: str, password: str, company_name: str = None) -> tuple[bool, str]:
    if username in verifiers_db or any(v["email"] == email for v in verifiers_db.values()):
        return False, None
    
    verifier_id = str(uuid.uuid4())
    verifiers_db[username] = {
        "id": verifier_id,
        "username": username,
        "email": email,
        "password": hash_password(password),
        "company_name": company_name,
        "verifier_type": "employer",
        "status": "active",
        "created_at": datetime.utcnow()
    }
    return True, verifier_id

def authenticate_verifier(username: str, password: str) -> Optional[str]:
    verifier = verifiers_db.get(username)
    if verifier and verify_password(password, verifier["password"]) and verifier["status"] == "active":
        return create_verifier_token(verifier["id"], username)
    return None

def get_verifier_by_id(verifier_id: str) -> Optional[Dict]:
    for verifier in verifiers_db.values():
        if verifier["id"] == verifier_id:
            return verifier
    return None
