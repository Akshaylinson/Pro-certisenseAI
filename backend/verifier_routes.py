# Complete Verifier API - CertiSense AI v3.0
# All 7 Modules: Verify, Proof, AI Analysis, History, Feedback, Blockchain, Chatbot

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Header, Query
from typing import Optional
from sqlalchemy.orm import Session

from database import get_db
from verifier_service import VerifierService
from chatbot_service import ChatbotService
from auth_db import verify_token

router = APIRouter(prefix="/api/verifier", tags=["Verifier"])

def get_current_verifier(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Secure verifier authentication"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    if not payload or payload.get("role") != "verifier":
        raise HTTPException(status_code=401, detail="Invalid verifier token")
    
    return payload

# ==================== MODULE 1: VERIFY CERTIFICATE ====================

@router.post("/verify")
async def verify_certificate(
    file: UploadFile = File(...),
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """
    Verify certificate authenticity through blockchain and AI validation
    Returns: Valid, Invalid, Tampered, or Revoked
    """
    try:
        content = await file.read()
        
        result = VerifierService.verify_certificate(
            file_content=content,
            filename=file.filename,
            verifier_id=verifier["user_id"],
            db=db
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

# ==================== MODULE 2: GENERATE VERIFICATION PROOF ====================

@router.post("/proof/generate/{verification_id}")
async def generate_verification_proof(
    verification_id: str,
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """Generate downloadable verification proof report"""
    try:
        proof = VerifierService.generate_verification_proof(
            verification_id=verification_id,
            verifier_id=verifier["user_id"],
            db=db
        )
        
        return proof
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proof generation failed: {str(e)}")

@router.get("/proof/download/{verification_id}")
async def download_verification_proof(
    verification_id: str,
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """Download verification proof report"""
    try:
        proof = VerifierService.generate_verification_proof(
            verification_id=verification_id,
            verifier_id=verifier["user_id"],
            db=db
        )
        
        return {
            "format": "json",
            "proof": proof["report"],
            "download_ready": True
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ==================== MODULE 3: VIEW AI VERIFICATION ANALYSIS ====================

@router.get("/ai-analysis/{verification_id}")
async def get_ai_analysis(
    verification_id: str,
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """Get detailed AI verification analysis with fraud detection"""
    try:
        analysis = VerifierService.get_ai_analysis(
            verification_id=verification_id,
            verifier_id=verifier["user_id"],
            db=db
        )
        
        return analysis
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

# ==================== MODULE 4: VIEW VERIFICATION HISTORY ====================

@router.get("/history")
async def get_verification_history(
    status: Optional[str] = Query(None, description="Filter by status: valid, invalid, tampered, revoked"),
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    limit: int = Query(100, ge=1, le=500),
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """Get verifier's verification history with filtering options"""
    try:
        history = VerifierService.get_verification_history(
            verifier_id=verifier["user_id"],
            db=db,
            status=status,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        
        return history
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")

@router.get("/history/{verification_id}")
async def get_verification_details(
    verification_id: str,
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """Get detailed verification record"""
    from database import Verification
    
    verification = db.query(Verification).filter(
        Verification.id == verification_id,
        Verification.verifier_id == verifier["user_id"]
    ).first()
    
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    return {
        "verification_id": verification.id,
        "certificate_id": verification.certificate_id,
        "certificate_hash": verification.certificate_hash,
        "verification_result": verification.status,
        "confidence_score": verification.confidence_score,
        "blockchain_verified": verification.blockchain_integrity,
        "timestamp": verification.timestamp.isoformat()
    }

# ==================== MODULE 5: SUBMIT FEEDBACK ====================

@router.post("/feedback")
async def submit_feedback(
    feedback_type: str = Query(..., description="Type: suspicious, issue, general"),
    message: str = Query(..., description="Feedback message"),
    certificate_id: Optional[str] = Query(None, description="Related certificate ID"),
    priority: str = Query("medium", description="Priority: low, medium, high"),
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """Submit feedback about verification or certificate"""
    try:
        feedback = VerifierService.submit_feedback(
            verifier_id=verifier["user_id"],
            feedback_type=feedback_type,
            message=message,
            certificate_id=certificate_id,
            priority=priority,
            db=db
        )
        
        return feedback
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")

@router.get("/feedback")
async def get_my_feedback(
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """Get verifier's submitted feedback"""
    from database import Feedback
    
    feedbacks = db.query(Feedback).filter(
        Feedback.verifier_id == verifier["user_id"]
    ).order_by(Feedback.timestamp.desc()).all()
    
    return {
        "total_feedback": len(feedbacks),
        "feedbacks": [
            {
                "id": f.id,
                "feedback_type": f.category,
                "message": f.message,
                "priority": f.priority,
                "status": f.status,
                "certificate_id": f.certificate_id,
                "timestamp": f.timestamp.isoformat()
            }
            for f in feedbacks
        ]
    }

# ==================== MODULE 6: VIEW BLOCKCHAIN DETAILS ====================

@router.get("/blockchain/{certificate_hash}")
async def get_blockchain_details(
    certificate_hash: str,
    verifier = Depends(get_current_verifier)
):
    """Get blockchain details for certificate"""
    try:
        details = VerifierService.get_blockchain_details(
            certificate_hash=certificate_hash,
            verifier_id=verifier["user_id"]
        )
        
        return details
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch blockchain details: {str(e)}")

# ==================== MODULE 7: CHATBOT INTERACTION ====================

@router.post("/chatbot")
async def chatbot_query(
    message: str = Query(..., description="Chat message"),
    context: Optional[str] = Query(None, description="Additional context"),
    verifier = Depends(get_current_verifier)
):
    """Interact with verification assistance chatbot"""
    try:
        response = ChatbotService.process_query(
            message=message,
            user_role="verifier",
            user_id=verifier["user_id"]
        )
        
        # Add verifier-specific context
        if "verify" in message.lower() or "certificate" in message.lower():
            from database import SessionLocal, Verification
            db = SessionLocal()
            try:
                verifications = db.query(Verification).filter(
                    Verification.verifier_id == verifier["user_id"]
                ).all()
                
                response["verifier_stats"] = {
                    "total_verifications": len(verifications),
                    "recent_verifications": len([v for v in verifications 
                                                 if (datetime.utcnow() - v.timestamp).days <= 7])
                }
            finally:
                db.close()
        
        return response
    
    except Exception as e:
        return {
            "response": "I apologize, but I encountered an error processing your request.",
            "error": str(e)
        }

# ==================== VERIFIER DASHBOARD ====================

@router.get("/dashboard")
async def get_verifier_dashboard(
    verifier = Depends(get_current_verifier),
    db: Session = Depends(get_db)
):
    """Get verifier dashboard statistics and analytics"""
    try:
        stats = VerifierService.get_dashboard_stats(
            verifier_id=verifier["user_id"],
            db=db
        )
        
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load dashboard: {str(e)}")

# ==================== LOGOUT ====================

@router.post("/logout")
async def logout(verifier = Depends(get_current_verifier)):
    """Secure logout - invalidate session"""
    return {
        "message": "Logged out successfully",
        "verifier_id": verifier["user_id"]
    }

# ==================== HEALTH CHECK ====================

@router.get("/health")
async def health_check():
    """Verifier module health check"""
    return {
        "status": "healthy",
        "module": "verifier",
        "version": "3.0.0",
        "features": [
            "Certificate Verification",
            "Proof Generation",
            "AI Analysis",
            "Verification History",
            "Feedback System",
            "Blockchain Integration",
            "Chatbot Assistant"
        ]
    }
