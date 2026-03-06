import hashlib

def sha256_bytes(data: bytes) -> str:
    """Return 0x-prefixed hex sha256 (32 bytes)"""
    h = hashlib.sha256()
    h.update(data)
    return "0x" + h.hexdigest()
