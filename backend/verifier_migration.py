# Database Migration Script for Verifier Module
# CertiSense AI v3.0

"""
This script creates all necessary database tables for the Verifier Module
Run this before starting the verifier service
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()

# Verifier Account Model
class VerifierAccount(Base):
    __tablename__ = "verifiers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    company_name = Column(String)
    verifier_type = Column(String, default="employer")
    status = Column(String, default="active")
    verification_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

# Verification Record Model
class VerificationRecord(Base):
    __tablename__ = "verifications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    verifier_id = Column(String, ForeignKey("verifiers.id"), nullable=False, index=True)
    certificate_hash = Column(String, nullable=False, index=True)
    certificate_id = Column(String, index=True)
    verification_result = Column(String, nullable=False)  # valid, invalid, tampered, revoked
    result = Column(Boolean, default=False)
    status = Column(String, nullable=False)
    confidence_score = Column(Float)
    blockchain_verified = Column(Boolean, default=False)
    blockchain_integrity = Column(Boolean, default=False)
    blockchain_hash = Column(String)
    blockchain_transaction = Column(String)
    ai_analysis = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    processing_time = Column(Float)
    ip_address = Column(String)

# Verification Proof Model
class VerificationProof(Base):
    __tablename__ = "verification_proofs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_id = Column(String, ForeignKey("verifications.id"), nullable=False)
    verifier_id = Column(String, ForeignKey("verifiers.id"), nullable=False)
    certificate_id = Column(String)
    proof_hash = Column(String, unique=True, index=True)
    report_data = Column(JSON)
    generated_at = Column(DateTime, default=datetime.utcnow)

# Verifier Feedback Model
class VerifierFeedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    verifier_id = Column(String, ForeignKey("verifiers.id"), nullable=False, index=True)
    certificate_id = Column(String)
    feedback_type = Column(String)
    category = Column(String)
    message = Column(Text, nullable=False)
    priority = Column(String, default="medium")
    status = Column(String, default="open")
    flagged = Column(Boolean, default=False)
    admin_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime)
    resolved_by = Column(String)

# Verification Audit Log Model
class VerificationAuditLog(Base):
    __tablename__ = "verification_audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    verifier_id = Column(String, nullable=False, index=True)
    action = Column(String, nullable=False)
    certificate_hash = Column(String)
    result = Column(String)
    ip_address = Column(String)
    user_agent = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    details = Column(JSON)

def create_verifier_tables(database_url="sqlite:///./data/certisense.db"):
    """Create all verifier module tables"""
    
    print("Creating Verifier Module Database Tables...")
    
    # Create engine
    engine = create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Verifier tables created successfully!")
    print("\nTables created:")
    print("  - verifiers")
    print("  - verifications")
    print("  - verification_proofs")
    print("  - feedbacks")
    print("  - verification_audit_logs")
    
    return engine

def seed_test_verifier(database_url="sqlite:///./data/certisense.db"):
    """Create a test verifier account"""
    import hashlib
    
    engine = create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if test verifier exists
        existing = db.query(VerifierAccount).filter(VerifierAccount.username == "testverifier").first()
        if existing:
            print("Test verifier already exists")
            return
        
        # Create test verifier
        password_hash = hashlib.sha256("verifier123".encode()).hexdigest()
        test_verifier = VerifierAccount(
            id=str(uuid.uuid4()),
            username="testverifier",
            email="verifier@test.com",
            password_hash=password_hash,
            company_name="Test Verification Company",
            verifier_type="employer",
            status="active"
        )
        
        db.add(test_verifier)
        db.commit()
        
        print("\n✅ Test verifier created successfully!")
        print("Username: testverifier")
        print("Password: verifier123")
        print("Email: verifier@test.com")
        
    except Exception as e:
        print(f"Error creating test verifier: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables
    engine = create_verifier_tables()
    
    # Seed test data
    seed_test_verifier()
    
    print("\n🎉 Verifier Module database setup complete!")
