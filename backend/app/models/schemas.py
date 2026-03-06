from pydantic import BaseModel

class StoreResponse(BaseModel):
    tx_hash: str
    cert_hash: str

class VerifyResponse(BaseModel):
    cert_hash: str
    stored: bool
    issuer: str | None = None
    timestamp: int | None = None
