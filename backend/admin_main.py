from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from database import get_db, Base, engine
from auth_db import authenticate_admin, get_current_user
from admin_api import router as admin_router
from models import LoginRequest, AuthResponse

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CertiSense AI v3.0 - Admin Module",
    version="3.0.0",
    description="Blockchain Certificate Verification Platform - Admin Control System"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Admin Router
app.include_router(admin_router)

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/auth/admin/login", response_model=AuthResponse)
async def admin_login(request: LoginRequest, db: Session = Depends(get_db)):
    """Admin authentication endpoint"""
    token = authenticate_admin(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        expires_in=86400,
        role="admin",
        user_id="admin-001",
        username=request.username
    )

@app.post("/auth/admin/logout")
async def admin_logout(user=Depends(get_current_user)):
    """Admin logout endpoint"""
    return {"message": "Logged out successfully"}

@app.get("/auth/verify")
async def verify_auth(user=Depends(get_current_user)):
    """Verify authentication token"""
    return {"valid": True, "user": user}

# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "application": "CertiSense AI v3.0",
        "module": "Admin Control System",
        "version": "3.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "blockchain": "active",
        "ai_engine": "operational"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
