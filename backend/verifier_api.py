from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Header, Query
from typing import Optional, Dict, List
from datetime import datetime
import uuid
import time
import hashlib

from verifier_auth import verify_verifier_token, get_verifier_by_id
from blockchain_service import BlockchainService, generate_file_hash
from ai_service import AIValidationService
from chatbot_service import ChatbotService

router = APIRouter(prefix="/verifier", tags=["Verifier"])

# In-memory storage
verification_records = {}
verification_proofs = {}
verifier_feedbacks = {}
audit_logs = []

def get_current_verifier(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    token = authorization.split(" ")[1]
    payload = verify_verifier_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

def log_verification_audit(verifier_id: str, action: str, cert_hash: str = None, result: str = None):
    audit_logs.append({
        "id": str(uuid.uuid4()),
        "verifier_id": verifier_id,
        "action": action,
        "certificate_hash": cert_hash,
        "result": result,
        "timestamp": datetime.utcnow()
    })

# ==================== MODULE 1: VERIFY CERTIFICATE ====================

@router.post("/verify")
async def verify_certificate(
    file: UploadFile = File(...),
    verifier = Depends(get_current_verifier)
):
    """
    Verify certificate authenticity through blockchain and AI validation
    Returns: Valid, Invalid, Tampered, or Revoked
    """
    start_time = time.time()
    
    # Extract certificate data
    content = await file.read()
    certificate_hash = generate_file_hash(content)
    
    # Blockchain verification
    blockchain_data = BlockchainService.verify_certificate_hash(certificate_hash)
    blockchain_verified = blockchain_data is not None
    
    # AI validation
    ai_result = AIValidationService.validate_certificate_content(content, file.filename)
    
    # Determine verification result
    if not blockchain_verified:
        verification_result = "invalid"
    elif blockchain_data and not blockchain_data.get("valid", True):
        verification_result = "revoked"
    elif ai_result["confidence"] < 0.5:
        verification_result = "tampered"
    else:
        verification_result = "valid"
    
    # Calculate confidence score
    confidence_score = ai_result["confidence"] if blockchain_verified else 0.0
    
    processing_time = time.time() - start_time
    
    # Create verification record
    verification_id = str(uuid.uuid4())
    verification_records[verification_id] = {
        "id": verification_id,
        "verifier_id": verifier["verifier_id"],
        "certificate_hash": certificate_hash,
        "certificate_id": blockchain_data.get("certificate_id") if blockchain_data else None,
        "verification_result": verification_result,
        "confidence_score": confidence_score,
        "blockchain_verified": blockchain_verified,
        "blockchain_hash": blockchain_data.get("chain_hash") if blockchain_data else None,
        "blockchain_transaction": blockchain_data.get("transaction_id") if blockchain_data else None,
        "ai_analysis": ai_result,
        "timestamp": datetime.utcnow(),
        "processing_time": processing_time
    }
    
    # Log audit
    log_verification_audit(verifier["verifier_id"], "VERIFY_CERTIFICATE", certificate_hash, verification_result)
    
    return {
        "verification_id": verification_id,
        "certificate_hash": certificate_hash,
        "verification_result": verification_result,
        "confidence_score": confidence_score,
        "blockchain_verified": blockchain_verified,
        "blockchain_data": blockchain_data,
        "ai_analysis": ai_result,
        "processing_time": processing_time,
        "timestamp": datetime.utcnow()
    }

# ==================== MODULE 2: GENERATE VERIFICATION PROOF ====================

@router.post("/proof/generate/{verification_id}")
async def generate_verification_proof(
    verification_id: str,
    verifier = Depends(get_current_verifier)
):
    """Generate downloadable verification proof report"""
    
    verification = verification_records.get(verification_id)
    if not verification:
        raise HTTPException(status_code=404, detail="Verification record not found")
    
    if verification["verifier_id"] != verifier["verifier_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Generate proof hash
    proof_data = f"{verification_id}{verifier['verifier_id']}{datetime.utcnow()}"
    proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
    
    # Create proof report
    report_data = {
        "verification_id": verification_id,
        "certificate_id": verification["certificate_id"],
        "certificate_hash": verification["certificate_hash"],
        "verifier_id": verifier["verifier_id"],
        "verifier_username": verifier["username"],
        "verification_result": verification["verification_result"],
        "confidence_score": verification["confidence_score"],
        "blockchain_verified": verification["blockchain_verified"],
        "blockchain_transaction": verification["blockchain_transaction"],
        "verification_timestamp": verification["timestamp"].isoformat(),
        "proof_hash": proof_hash,
        "generated_at": datetime.utcnow().isoformat()
    }
    
    # Store proof
    proof_id = str(uuid.uuid4())
    verification_proofs[proof_id] = {
        "id": proof_id,
        "verification_id": verification_id,
        "verifier_id": verifier["verifier_id"],
        "certificate_id": verification["certificate_id"],
        "proof_hash": proof_hash,
        "report_data": report_data,
        "generated_at": datetime.utcnow()
    }
    
    log_verification_audit(verifier["verifier_id"], "GENERATE_PROOF", verification["certificate_hash"])
    
    return {
        "proof_id": proof_id,
        "proof_hash": proof_hash,
        "report": report_data,
        "download_url": f"/verifier/proof/download/{proof_id}"
    }

@router.get("/proof/download/{proof_id}")
async def download_verification_proof(
    proof_id: str,
    verifier = Depends(get_current_verifier)
):
    """Download verification proof report"""
    
    proof = verification_proofs.get(proof_id)
    if not proof:
        raise HTTPException(status_code=404, detail="Proof not found")
    
    if proof["verifier_id"] != verifier["verifier_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "proof_id": proof_id,
        "report": proof["report_data"],
        "format": "json"
    }

# ==================== MODULE 3: VIEW AI VERIFICATION ANALYSIS ====================

@router.get("/ai-analysis/{verification_id}")
async def get_ai_analysis(
    verification_id: str,
    verifier = Depends(get_current_verifier)
):
    """Get detailed AI verification analysis"""
    
    verification = verification_records.get(verification_id)
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    if verification["verifier_id"] != verifier["verifier_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    ai_analysis = verification["ai_analysis"]
    
    # Enhanced AI insights
    fraud_indicators = []
    if ai_analysis["confidence"] < 0.3:
        fraud_indicators.append("Very low confidence score")
    if not ai_analysis.get("format_valid", True):
        fraud_indicators.append("Invalid certificate format")
    if len(ai_analysis.get("issues", [])) > 3:
        fraud_indicators.append("Multiple validation issues detected")
    
    return {
        "verification_id": verification_id,
        "ai_validation_result": "authentic" if ai_analysis["valid"] else "suspicious",
        "confidence_score": ai_analysis["confidence"],
        "ai_model": "CertiSense AI v3.0",
        "fraud_indicators": fraud_indicators,
        "features_detected": ai_analysis.get("features_detected", []),
        "issues": ai_analysis.get("issues", []),
        "validation_token": ai_analysis.get("validation_token"),
        "detailed_analysis": ai_analysis
    }

# ==================== MODULE 4: VIEW VERIFICATION HISTORY ====================

@router.get("/history")
async def get_verification_history(
    status: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    verifier = Depends(get_current_verifier)
):
    """Get verifier's verification history with filtering"""
    
    verifier_id = verifier["verifier_id"]
    history = [v for v in verification_records.values() if v["verifier_id"] == verifier_id]
    
    # Apply filters
    if status:
        history = [v for v in history if v["verification_result"] == status]
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        history = [v for v in history if v["timestamp"] >= start]
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        history = [v for v in history if v["timestamp"] <= end]
    
    # Sort by timestamp (newest first)
    history.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Format response
    formatted_history = []
    for v in history:
        formatted_history.append({
            "verification_id": v["id"],
            "certificate_id": v["certificate_id"],
            "certificate_hash": v["certificate_hash"][:16] + "...",
            "verification_result": v["verification_result"],
            "confidence_score": v["confidence_score"],
            "blockchain_verified": v["blockchain_verified"],
            "timestamp": v["timestamp"].isoformat(),
            "processing_time": v["processing_time"]
        })
    
    return {
        "total_verifications": len(formatted_history),
        "history": formatted_history
    }

@router.get("/history/{verification_id}")
async def get_verification_details(
    verification_id: str,
    verifier = Depends(get_current_verifier)
):
    """Get detailed verification record"""
    
    verification = verification_records.get(verification_id)
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    if verification["verifier_id"] != verifier["verifier_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return verification

# ==================== MODULE 5: SUBMIT FEEDBACK ====================

@router.post("/feedback")
async def submit_feedback(
    certificate_id: str = Query(None),
    feedback_type: str = Query(...),
    message: str = Query(...),
    priority: str = Query("medium"),
    verifier = Depends(get_current_verifier)
):
    """Submit feedback about verification or certificate"""
    
    feedback_id = str(uuid.uuid4())
    verifier_feedbacks[feedback_id] = {
        "id": feedback_id,
        "verifier_id": verifier["verifier_id"],
        "certificate_id": certificate_id,
        "feedback_type": feedback_type,
        "message": message,
        "priority": priority,
        "status": "open",
        "timestamp": datetime.utcnow()
    }
    
    log_verification_audit(verifier["verifier_id"], "SUBMIT_FEEDBACK", certificate_id)
    
    return {
        "feedback_id": feedback_id,
        "message": "Feedback submitted successfully",
        "status": "open"
    }

@router.get("/feedback")
async def get_my_feedback(verifier = Depends(get_current_verifier)):
    """Get verifier's submitted feedback"""
    
    verifier_id = verifier["verifier_id"]
    feedbacks = [f for f in verifier_feedbacks.values() if f["verifier_id"] == verifier_id]
    feedbacks.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "total_feedback": len(feedbacks),
        "feedbacks": feedbacks
    }

# ==================== MODULE 6: VIEW BLOCKCHAIN DETAILS ====================

@router.get("/blockchain/{certificate_hash}")
async def get_blockchain_details(
    certificate_hash: str,
    verifier = Depends(get_current_verifier)
):
    """Get blockchain details for certificate"""
    
    blockchain_data = BlockchainService.get_certificate_chain(certificate_hash)
    
    if not blockchain_data:
        raise HTTPException(status_code=404, detail="Certificate not found on blockchain")
    
    log_verification_audit(verifier["verifier_id"], "VIEW_BLOCKCHAIN", certificate_hash)
    
    return {
        "certificate_hash": certificate_hash,
        "blockchain_hash": blockchain_data.get("chain_hash"),
        "transaction_hash": blockchain_data.get("transaction_id"),
        "timestamp": blockchain_data.get("timestamp"),
        "issuer_id": blockchain_data.get("issuer_id"),
        "student_id": blockchain_data.get("student_id"),
        "status": blockchain_data.get("status"),
        "valid": blockchain_data.get("valid"),
        "verifications": blockchain_data.get("verifications", []),
        "blockchain_integrity": "verified"
    }

# ==================== MODULE 7: CHATBOT INTERACTION ====================

@router.post("/chatbot")
async def chatbot_query(
    message: str = Query(...),
    context: Optional[str] = Query(None),
    verifier = Depends(get_current_verifier)
):
    """Interact with verification assistance chatbot"""
    
    response = ChatbotService.process_query(message, "verifier", verifier["verifier_id"])
    
    # Add verifier-specific context
    if "verify" in message.lower() or "certificate" in message.lower():
        verifier_stats = {
            "total_verifications": len([v for v in verification_records.values() if v["verifier_id"] == verifier["verifier_id"]]),
            "recent_verifications": len([v for v in verification_records.values() 
                                        if v["verifier_id"] == verifier["verifier_id"] 
                                        and (datetime.utcnow() - v["timestamp"]).days <= 7])
        }
        response["verifier_stats"] = verifier_stats
    
    return response

# ==================== VERIFIER DASHBOARD ====================

@router.get("/dashboard")
async def get_verifier_dashboard(verifier = Depends(get_current_verifier)):
    """Get verifier dashboard statistics"""
    
    verifier_id = verifier["verifier_id"]
    verifications = [v for v in verification_records.values() if v["verifier_id"] == verifier_id]
    
    total_verifications = len(verifications)
    valid_count = len([v for v in verifications if v["verification_result"] == "valid"])
    invalid_count = len([v for v in verifications if v["verification_result"] == "invalid"])
    tampered_count = len([v for v in verifications if v["verification_result"] == "tampered"])
    revoked_count = len([v for v in verifications if v["verification_result"] == "revoked"])
    
    recent_verifications = [v for v in verifications if (datetime.utcnow() - v["timestamp"]).days <= 30]
    
    return {
        "verifier_info": {
            "username": verifier["username"],
            "verifier_id": verifier_id
        },
        "statistics": {
            "total_verifications": total_verifications,
            "valid_certificates": valid_count,
            "invalid_certificates": invalid_count,
            "tampered_certificates": tampered_count,
            "revoked_certificates": revoked_count,
            "recent_verifications_30d": len(recent_verifications)
        },
        "success_rate": (valid_count / total_verifications * 100) if total_verifications > 0 else 0
    }
