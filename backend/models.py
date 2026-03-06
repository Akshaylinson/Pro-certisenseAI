from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    INSTITUTE = "institute"
    STUDENT = "student"
    VERIFIER = "verifier"

class CertificateStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    PENDING = "pending"
    EXPIRED = "expired"

class VerificationStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    PENDING = "pending"
    ERROR = "error"

class FeedbackCategory(str, Enum):
    BUG_REPORT = "bug_report"
    FEATURE_REQUEST = "feature_request"
    GENERAL_FEEDBACK = "general_feedback"
    TECHNICAL_ISSUE = "technical_issue"
    IMPROVEMENT_SUGGESTION = "improvement_suggestion"

# Core Entity Models
class User(BaseModel):
    id: str
    username: str
    role: UserRole
    email: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True

class Institute(BaseModel):
    id: str
    name: str
    institute_id: str
    admin_id: str
    email: str
    location: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    established_year: Optional[int] = None
    accreditation: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_verified: bool = False
    student_count: int = 0
    certificate_count: int = 0

class Student(BaseModel):
    id: str
    student_id: str
    name: str
    institute_id: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    enrollment_date: Optional[datetime] = None
    graduation_date: Optional[datetime] = None
    program: Optional[str] = None
    department: Optional[str] = None
    gpa: Optional[float] = None
    profile_image: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True

class Certificate(BaseModel):
    id: str
    name: str
    hash: str
    student_id: str
    institute_id: str
    issuer_id: str
    certificate_type: Optional[str] = None
    course_name: Optional[str] = None
    grade: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    credits: Optional[int] = None
    description: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    status: CertificateStatus = CertificateStatus.ACTIVE
    created_at: datetime
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = {}
    verification_count: int = 0

class CertificateChain(BaseModel):
    id: str
    certificate_id: str
    hash: str
    chain_hash: str
    previous_hash: Optional[str] = None
    block_number: Optional[int] = None
    transaction_id: Optional[str] = None
    gas_used: Optional[int] = None
    timestamp: datetime
    status: str
    network: Optional[str] = "local"
    confirmations: int = 0

class Verification(BaseModel):
    id: str
    certificate_hash: str
    verifier_id: str
    result: bool
    status: VerificationStatus
    confidence_score: Optional[float] = None
    verification_method: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[str] = None
    ai_validation: Optional[Dict[str, Any]] = {}
    blockchain_data: Optional[Dict[str, Any]] = {}
    timestamp: datetime
    processing_time: Optional[float] = None
    notes: Optional[str] = None

class Feedback(BaseModel):
    id: str
    verifier_id: str
    message: str
    category: FeedbackCategory
    priority: Optional[str] = "medium"
    status: Optional[str] = "open"
    admin_response: Optional[str] = None
    timestamp: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    attachments: Optional[List[str]] = []

# AI and Analytics Models
class AIValidationResult(BaseModel):
    valid: bool
    confidence_score: float
    validation_token: str
    features_detected: List[str]
    issues: List[str]
    processing_time: float
    model_version: str
    analysis_details: Dict[str, Any]

class SystemAnalytics(BaseModel):
    total_institutes: int
    total_students: int
    total_certificates: int
    total_verifications: int
    total_verifiers: int
    success_rate: float
    avg_processing_time: float
    popular_certificate_types: List[Dict[str, Any]]
    monthly_stats: Dict[str, int]
    system_health: Dict[str, Any]

# Request/Response Models
class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None
    user_role: Optional[str] = None
    session_id: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: bool = False

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None
    organization: Optional[str] = None

class InstituteRegisterRequest(BaseModel):
    institute_name: str
    password: str
    email: str
    location: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None

class StudentRegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None
    program: Optional[str] = None
    department: Optional[str] = None

class CertificateUploadRequest(BaseModel):
    student_id: str
    certificate_name: str
    certificate_type: Optional[str] = None
    course_name: Optional[str] = None
    grade: Optional[str] = None
    issue_date: Optional[datetime] = None
    description: Optional[str] = None

class VerificationRequest(BaseModel):
    certificate_hash: Optional[str] = None
    verification_method: str = "file_upload"
    notes: Optional[str] = None

class FeedbackRequest(BaseModel):
    message: str
    category: FeedbackCategory
    priority: Optional[str] = "medium"
    attachments: Optional[List[str]] = []

# Response Models
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400
    role: str
    user_id: str
    username: str

class VerificationResponse(BaseModel):
    verification_id: str
    result: bool
    status: VerificationStatus
    certificate_hash: str
    confidence_score: Optional[float] = None
    ai_validation: Optional[AIValidationResult] = None
    blockchain_data: Optional[Dict[str, Any]] = None
    explanation: str
    timestamp: datetime
    processing_time: Optional[float] = None

class CertificateResponse(BaseModel):
    certificate_id: str
    name: str
    hash: str
    chain_hash: str
    status: CertificateStatus
    created_at: datetime
    verification_count: int
    blockchain_status: str

class DashboardStats(BaseModel):
    total_count: int
    active_count: int
    recent_activity: List[Dict[str, Any]]
    growth_rate: Optional[float] = None
    success_rate: Optional[float] = None

# Configuration Models
class SystemConfig(BaseModel):
    blockchain_network: str = "local"
    ai_model_version: str = "v1.0"
    max_file_size: int = 10485760  # 10MB
    allowed_file_types: List[str] = ["pdf", "jpg", "jpeg", "png"]
    session_timeout: int = 3600  # 1 hour
    rate_limit: int = 100  # requests per minute
    maintenance_mode: bool = False