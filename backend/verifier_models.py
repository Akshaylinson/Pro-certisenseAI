from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class VerifierAccount(Base):
    __tablename__ = "verifier_accounts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    company_name = Column(String)
    verifier_type = Column(String, default="employer")
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class VerificationRecord(Base):
    __tablename__ = "verification_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    verifier_id = Column(String, ForeignKey("verifier_accounts.id"), nullable=False)
    certificate_hash = Column(String, nullable=False, index=True)
    certificate_id = Column(String)
    verification_result = Column(String, nullable=False)  # valid, invalid, tampered, revoked
    confidence_score = Column(Float)
    blockchain_verified = Column(Boolean, default=False)
    blockchain_hash = Column(String)
    blockchain_transaction = Column(String)
    ai_analysis = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)

class VerificationProof(Base):
    __tablename__ = "verification_proofs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    verification_id = Column(String, ForeignKey("verification_records.id"), nullable=False)
    verifier_id = Column(String, ForeignKey("verifier_accounts.id"), nullable=False)
    certificate_id = Column(String)
    proof_hash = Column(String, unique=True)
    report_data = Column(JSON)
    generated_at = Column(DateTime, default=datetime.utcnow)

class VerifierFeedback(Base):
    __tablename__ = "verifier_feedbacks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    verifier_id = Column(String, ForeignKey("verifier_accounts.id"), nullable=False)
    certificate_id = Column(String)
    feedback_type = Column(String)  # suspicious, issue, general
    message = Column(Text, nullable=False)
    priority = Column(String, default="medium")
    status = Column(String, default="open")
    timestamp = Column(DateTime, default=datetime.utcnow)

class VerificationAuditLog(Base):
    __tablename__ = "verification_audit_logs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    verifier_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    certificate_hash = Column(String)
    result = Column(String)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
