from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from verifier_auth import register_verifier, authenticate_verifier, get_current_verifier
from verifier_api import router as verifier_router

app = FastAPI(
    title="CertiSense AI v3.0 - Verifier Module",
    version="3.0.0",
    description="Certificate Verification Platform for Employers and Third Parties"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Verifier Router
app.include_router(verifier_router)

# Request Models
class VerifierRegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    company_name: str = None

class VerifierLoginRequest(BaseModel):
    username: str
    password: str

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/auth/verifier/register")
async def verifier_register(request: VerifierRegisterRequest):
    """Register new verifier account"""
    success, verifier_id = register_verifier(
        request.username,
        request.email,
        request.password,
        request.company_name
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    return {
        "message": "Verifier registered successfully",
        "verifier_id": verifier_id
    }

@app.post("/auth/verifier/login")
async def verifier_login(request: VerifierLoginRequest):
    """Verifier authentication"""
    token = authenticate_verifier(request.username, request.password)
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "verifier",
        "username": request.username
    }

@app.post("/auth/verifier/logout")
async def verifier_logout():
    """Logout verifier (client-side token removal)"""
    return {"message": "Logged out successfully"}

# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "application": "CertiSense AI v3.0",
        "module": "Verifier System",
        "version": "3.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "blockchain": "connected",
        "ai_engine": "active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
