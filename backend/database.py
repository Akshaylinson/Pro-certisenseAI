from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

DATABASE_URL = "sqlite:///./data/certisense.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserRoleEnum(enum.Enum):
    ADMIN = "admin"
    INSTITUTE = "institute"
    STUDENT = "student"
    VERIFIER = "verifier"

class CertificateStatusEnum(enum.Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    SUSPICIOUS = "suspicious"
    PENDING = "pending"

class VerificationStatusEnum(enum.Enum):
    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"
    FLAGGED = "flagged"

class Institute(Base):
    __tablename__ = "institutes"
    id = Column(String, primary_key=True)
    institute_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    registration_number = Column(String)
    location = Column(String)
    phone = Column(String)
    website = Column(String)
    approval_status = Column(String, default="approved")
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    students = relationship("Student", back_populates="institute")
    certificates = relationship("Certificate", back_populates="institute")

class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    institute_id = Column(String, ForeignKey("institutes.id"))
    phone = Column(String)
    program = Column(String)
    department = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    institute = relationship("Institute", back_populates="students")
    certificates = relationship("Certificate", back_populates="student")

class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    hash = Column(String, unique=True, index=True)
    chain_hash = Column(String)
    student_id = Column(String, ForeignKey("students.id"))
    institute_id = Column(String, ForeignKey("institutes.id"))
    issuer_id = Column(String)
    certificate_type = Column(String)
    status = Column(SQLEnum(CertificateStatusEnum), default=CertificateStatusEnum.ACTIVE)
    issue_date = Column(DateTime)
    verification_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("Student", back_populates="certificates")
    institute = relationship("Institute", back_populates="certificates")
    verifications = relationship("Verification", back_populates="certificate")

class Verifier(Base):
    __tablename__ = "verifiers"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    company_name = Column(String)
    verifier_type = Column(String)
    status = Column(String, default="active")
    verification_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    verifications = relationship("Verification", back_populates="verifier")
    feedbacks = relationship("Feedback", back_populates="verifier")

class Verification(Base):
    __tablename__ = "verifications"
    id = Column(String, primary_key=True)
    certificate_id = Column(String, ForeignKey("certificates.id"))
    certificate_hash = Column(String)
    verifier_id = Column(String, ForeignKey("verifiers.id"))
    result = Column(Boolean)
    status = Column(SQLEnum(VerificationStatusEnum))
    confidence_score = Column(Float)
    blockchain_integrity = Column(Boolean)
    is_suspicious = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    certificate = relationship("Certificate", back_populates="verifications")
    verifier = relationship("Verifier", back_populates="verifications")

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(String, primary_key=True)
    verifier_id = Column(String, ForeignKey("verifiers.id"))
    certificate_id = Column(String)
    message = Column(Text)
    category = Column(String)
    priority = Column(String, default="medium")
    status = Column(String, default="open")
    flagged = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    verifier = relationship("Verifier", back_populates="feedbacks")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    user_role = Column(String)
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(String)
    details = Column(Text)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
