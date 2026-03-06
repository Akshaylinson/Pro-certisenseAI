# CertiSense AI v3.0 - Database Schema

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Admin (1) ──────────────────────────────────────────────────┐  │
│    │                                                          │  │
│    │ creates                                                 │  │
│    ▼                                                          │  │
│  Schools (*)                                                 │  │
│    │                                                          │  │
│    │ manages                                                 │  │
│    ▼                                                          │  │
│  Students (*)                                                │  │
│    │                                                          │  │
│    │ receives                                                │  │
│    ▼                                                          │  │
│  Certificates (*)                                            │  │
│    │                                                          │  │
│    │ tracked by                                              │  │
│    ▼                                                          │  │
│  CertificateChain (1)                                        │  │
│    │                                                          │  │
│    │ verified by                                             │  │
│    ▼                                                          │  │
│  Verifications (*)                                           │  │
│    │                                                          │  │
│    └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Models

### 1. Admin
```python
{
  "id": "admin-1",
  "username": "admin",
  "password": "hashed_password",
  "role": "admin",
  "email": "admin@certisense.edu",
  "created_at": "2024-01-19T10:00:00"
}
```

### 2. School
```python
{
  "id": "school-1",
  "name": "MIT",
  "username": "mit_admin",
  "password": "hashed_password",
  "role": "school",
  "email": "admin@mit.edu",
  "location": "Cambridge, MA",
  "created_at": "2024-01-19T10:05:00"
}
```

### 3. Student
```python
{
  "id": "student-1",
  "student_id": "STU001",
  "name": "John Doe",
  "school_id": "school-1",
  "email": "john@mit.edu",
  "password": "hashed_password",
  "role": "student",
  "created_at": "2024-01-19T10:10:00"
}
```

### 4. Certificate
```python
{
  "id": "cert-uuid-1",
  "name": "Bachelor_Degree.pdf",
  "hash": "sha256_hash_of_file",
  "student_id": "STU001",
  "school_id": "school-1",
  "issuer_id": "school-1",
  "chain_hash": "blockchain_hash",
  "created_at": "2024-01-19T10:15:00",
  "metadata": {
    "degree": "Bachelor of Science",
    "major": "Computer Science",
    "gpa": "3.8"
  }
}
```

### 5. CertificateChain
```python
{
  "id": "chain-uuid-1",
  "certificate_id": "cert-uuid-1",
  "hash": "sha256_hash_of_file",
  "chain_hash": "blockchain_hash",
  "timestamp": "2024-01-19T10:15:00",
  "status": "added",
  "verifications": [
    {
      "verifier_id": "verifier-1",
      "result": true,
      "timestamp": "2024-01-19T10:20:00"
    }
  ]
}
```

### 6. Verification
```python
{
  "id": "verification-uuid-1",
  "certificate_hash": "sha256_hash_of_file",
  "verifier_id": "verifier-1",
  "result": true,
  "ai_validation": {
    "valid": true,
    "confidence": 0.95,
    "format_valid": true,
    "keywords_found": true,
    "validation_token": "AI-1234"
  },
  "blockchain_data": {
    "student_id": "STU001",
    "school_id": "school-1",
    "issuer_id": "school-1",
    "chain_hash": "blockchain_hash",
    "timestamp": "2024-01-19T10:15:00",
    "valid": true,
    "verifications": [...]
  },
  "explanation": "Certificate verified successfully...",
  "timestamp": "2024-01-19T10:20:00"
}
```

### 7. Verifier
```python
{
  "id": "verifier-1",
  "username": "employer1",
  "password": "hashed_password",
  "role": "verifier",
  "email": "hr@company.com",
  "created_at": "2024-01-19T10:25:00"
}
```

### 8. Feedback
```python
{
  "id": "feedback-uuid-1",
  "verifier_id": "verifier-1",
  "message": "Certificate verification process is smooth",
  "category": "verification",
  "timestamp": "2024-01-19T10:30:00"
}
```

## Relationships & Multiplicity

### Admin → Schools
- **Type**: One-to-Many (1:*)
- **Description**: One admin can create multiple schools
- **Foreign Key**: school.admin_id → admin.id

### School → Students
- **Type**: One-to-Many (1:*)
- **Description**: One school can have multiple students
- **Foreign Key**: student.school_id → school.id

### School → Certificates
- **Type**: One-to-Many (1:*)
- **Description**: One school can issue multiple certificates
- **Foreign Key**: certificate.school_id → school.id

### Student → Certificates
- **Type**: One-to-Many (1:*)
- **Description**: One student can receive multiple certificates
- **Foreign Key**: certificate.student_id → student.id

### Certificate → CertificateChain
- **Type**: One-to-One (1:1)
- **Description**: Each certificate has one blockchain chain record
- **Foreign Key**: certificate_chain.certificate_id → certificate.id

### Certificate → Verifications
- **Type**: One-to-Many (1:*)
- **Description**: One certificate can have multiple verifications
- **Foreign Key**: verification.certificate_hash → certificate.hash

### Verifier → Verifications
- **Type**: One-to-Many (1:*)
- **Description**: One verifier can perform multiple verifications
- **Foreign Key**: verification.verifier_id → verifier.id

## Database Collections/Tables

### In-Memory Storage (Current Implementation)

```python
# Authentication
users_db = {
  "admin": {...},
  "school_username": {...},
  "student_id": {...},
  "verifier_username": {...}
}

# Entity Storage
schools_db = {
  "school_username": {...}
}

students_db = {
  "student_id": {...}
}

verifiers_db = {
  "verifier_username": {...}
}

# Certificate Storage
certificates_db = {
  "cert_id": {...}
}

# Blockchain Storage
blockchain_registry = {
  "cert_hash": {
    "student_id": "...",
    "school_id": "...",
    "issuer_id": "...",
    "chain_hash": "...",
    "timestamp": "...",
    "valid": true,
    "verifications": [...]
  }
}

certificate_chains = {
  "cert_hash": {...}
}

# Verification Storage
verifications_db = {
  "verification_id": {...}
}

# Feedback Storage
feedback_db = {
  "feedback_id": {...}
}
```

## Data Flow

### Certificate Issuance Flow
```
School Admin Uploads Certificate
    ↓
File Content Read
    ↓
SHA256 Hash Generated
    ↓
AI Validation Performed
    ↓
Blockchain Hash Created
    ↓
Certificate Record Created
    ↓
CertificateChain Record Created
    ↓
Blockchain Registry Updated
    ↓
Certificate Stored in Database
    ↓
Student Can View Certificate
```

### Certificate Verification Flow
```
Verifier Uploads Certificate
    ↓
File Content Read
    ↓
SHA256 Hash Generated
    ↓
AI Validation Performed
    ↓
Blockchain Lookup (Hash Search)
    ↓
Certificate Found/Not Found
    ↓
Verification Record Created
    ↓
Verification Added to Certificate Chain
    ↓
Blockchain Registry Updated
    ↓
Verification Result Returned
    ↓
Student Sees Verification Update
```

## Indexes (For Future Database Implementation)

```sql
-- User Indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);

-- School Indexes
CREATE INDEX idx_schools_admin_id ON schools(admin_id);
CREATE INDEX idx_schools_username ON schools(username);

-- Student Indexes
CREATE INDEX idx_students_school_id ON students(school_id);
CREATE INDEX idx_students_student_id ON students(student_id);

-- Certificate Indexes
CREATE INDEX idx_certificates_student_id ON certificates(student_id);
CREATE INDEX idx_certificates_school_id ON certificates(school_id);
CREATE INDEX idx_certificates_hash ON certificates(hash);

-- Verification Indexes
CREATE INDEX idx_verifications_certificate_hash ON verifications(certificate_hash);
CREATE INDEX idx_verifications_verifier_id ON verifications(verifier_id);

-- Blockchain Indexes
CREATE INDEX idx_blockchain_registry_hash ON blockchain_registry(hash);
CREATE INDEX idx_blockchain_registry_student_id ON blockchain_registry(student_id);
```

## Query Examples

### Get All Students in a School
```python
students = [s for s in students_db.values() if s["school_id"] == school_id]
```

### Get All Certificates for a Student
```python
certificates = [c for c in certificates_db.values() if c["student_id"] == student_id]
```

### Get Certificate Chain
```python
chain = blockchain_registry.get(cert_hash)
```

### Get All Verifications for a Certificate
```python
verifications = [v for v in verifications_db.values() if v["certificate_hash"] == cert_hash]
```

### Get School Statistics
```python
{
  "total_students": len([s for s in students_db.values() if s["school_id"] == school_id]),
  "total_certificates": len([c for c in certificates_db.values() if c["school_id"] == school_id]),
  "total_verifications": len([v for v in verifications_db.values() if v["school_id"] == school_id])
}
```

## Migration to Production Database

### MongoDB Schema
```javascript
// Schools Collection
db.schools.createIndex({ "admin_id": 1 });
db.schools.createIndex({ "username": 1 });

// Students Collection
db.students.createIndex({ "school_id": 1 });
db.students.createIndex({ "student_id": 1 });

// Certificates Collection
db.certificates.createIndex({ "student_id": 1 });
db.certificates.createIndex({ "school_id": 1 });
db.certificates.createIndex({ "hash": 1 });

// Verifications Collection
db.verifications.createIndex({ "certificate_hash": 1 });
db.verifications.createIndex({ "verifier_id": 1 });
```

### PostgreSQL Schema
```sql
CREATE TABLE schools (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  admin_id VARCHAR(50) NOT NULL,
  email VARCHAR(255) NOT NULL,
  location VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (admin_id) REFERENCES users(id)
);

CREATE TABLE students (
  id VARCHAR(50) PRIMARY KEY,
  student_id VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  school_id VARCHAR(50) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (school_id) REFERENCES schools(id)
);

CREATE TABLE certificates (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  hash VARCHAR(64) UNIQUE NOT NULL,
  student_id VARCHAR(50) NOT NULL,
  school_id VARCHAR(50) NOT NULL,
  issuer_id VARCHAR(50) NOT NULL,
  chain_hash VARCHAR(64),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (school_id) REFERENCES schools(id)
);
```

---

**Database schema designed for scalability and efficient querying**