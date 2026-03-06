import hashlib
from typing import Optional, Dict
from datetime import datetime

blockchain_registry = {}
certificate_chains = {}

class BlockchainService:
    @staticmethod
    def store_certificate_hash(cert_hash: str, student_id: str, school_id: str, issuer_id: str) -> str:
        """Store certificate hash on blockchain"""
        chain_hash = hashlib.sha256(f"{cert_hash}{datetime.utcnow()}".encode()).hexdigest()
        
        blockchain_registry[cert_hash] = {
            "student_id": student_id,
            "school_id": school_id,
            "issuer_id": issuer_id,
            "chain_hash": chain_hash,
            "timestamp": datetime.utcnow(),
            "valid": True,
            "verifications": []
        }
        
        certificate_chains[cert_hash] = {
            "hash": cert_hash,
            "chain_hash": chain_hash,
            "timestamp": datetime.utcnow(),
            "status": "added"
        }
        
        return chain_hash
    
    @staticmethod
    def verify_certificate_hash(cert_hash: str) -> Optional[Dict]:
        """Verify certificate hash exists on blockchain"""
        return blockchain_registry.get(cert_hash)
    
    @staticmethod
    def revoke_certificate(cert_hash: str) -> bool:
        """Revoke certificate on blockchain"""
        if cert_hash in blockchain_registry:
            blockchain_registry[cert_hash]["valid"] = False
            return True
        return False
    
    @staticmethod
    def add_verification(cert_hash: str, verifier_id: str, result: bool) -> bool:
        """Add verification record to certificate"""
        if cert_hash in blockchain_registry:
            blockchain_registry[cert_hash]["verifications"].append({
                "verifier_id": verifier_id,
                "result": result,
                "timestamp": datetime.utcnow()
            })
            return True
        return False
    
    @staticmethod
    def get_certificate_chain(cert_hash: str) -> Optional[Dict]:
        """Get full certificate chain"""
        if cert_hash in blockchain_registry:
            cert = blockchain_registry[cert_hash]
            return {
                "hash": cert_hash,
                "chain_hash": cert["chain_hash"],
                "student_id": cert["student_id"],
                "school_id": cert["school_id"],
                "issuer_id": cert["issuer_id"],
                "timestamp": cert["timestamp"],
                "status": "added",
                "verifications": cert["verifications"],
                "valid": cert["valid"]
            }
        return None
    
    @staticmethod
    def get_student_certificates(student_id: str) -> list:
        """Get all certificates for a student"""
        return [
            {
                "hash": cert_hash,
                "chain_hash": cert["chain_hash"],
                "timestamp": cert["timestamp"],
                "verifications": cert["verifications"],
                "valid": cert["valid"]
            }
            for cert_hash, cert in blockchain_registry.items()
            if cert["student_id"] == student_id
        ]
    
    @staticmethod
    def get_all_certificates() -> Dict:
        """Get all certificates from blockchain"""
        return blockchain_registry

def generate_file_hash(file_content: bytes) -> str:
    """Generate SHA256 hash for file content"""
    return hashlib.sha256(file_content).hexdigest()