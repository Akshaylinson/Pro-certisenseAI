import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .hash_util import sha256_bytes
from .contract_client import store_hash_onchain, get_record, w3
from .models.schemas import StoreResponse, VerifyResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Certificate Verifier API (local)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/store", response_model=StoreResponse)
async def store_certificate(file: UploadFile = File(...)):
    contents = await file.read()
    cert_hash = sha256_bytes(contents)  # 0x...
    try:
        tx_hash = store_hash_onchain(cert_hash)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chain error: {str(e)}")
    return {"tx_hash": tx_hash, "cert_hash": cert_hash}

@app.post("/verify", response_model=VerifyResponse)
async def verify_certificate(file: UploadFile = File(...)):
    contents = await file.read()
    cert_hash = sha256_bytes(contents)
    rec = get_record(cert_hash)
    if rec is None:
        return {"cert_hash": cert_hash, "stored": False}
    else:
        return {"cert_hash": cert_hash, "stored": True, "issuer": rec["issuer"], "timestamp": rec["timestamp"]}

@app.get("/health")
def health():
    return {"ok": True, "chain_connected": w3.is_connected()}
