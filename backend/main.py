from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import hashlib

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage
registered_certificates = {}

@app.get("/")
def root():
    return {"message": "Certificate Verifier API - Working"}

@app.get("/test")
def test():
    return {"status": "API is working", "endpoints": ["/", "/test", "/status", "/verify", "/register"]}

@app.get("/status")
def get_status():
    return {
        "message": "Certificate Verifier API - Ready",
        "registered_certificates": len(registered_certificates),
        "certificates": registered_certificates
    }

@app.post("/register")
async def register_certificate(file: UploadFile = File(...)):
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    
    # Register certificate
    registered_certificates[file_hash] = {
        "filename": file.filename,
        "issuer": "University/Institution",
        "size": len(content)
    }
    
    return {
        "registered": True,
        "hash": file_hash,
        "filename": file.filename,
        "message": "Certificate registered successfully"
    }

@app.post("/verify")
async def verify_certificate(file: UploadFile = File(...)):
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    
    # Check if registered
    is_registered = file_hash in registered_certificates
    
    return {
        "status": "verified" if is_registered else "invalid",
        "filename": file.filename,
        "hash": file_hash,
        "message": "Certificate verified successfully" if is_registered else "Certificate not found in registry",
        "authentic": is_registered,
        "blockchain_data": {"exists": is_registered}
    }