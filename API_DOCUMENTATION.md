# CertiSense AI v3.0 - Complete API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <token>
```

---

## 🔐 Authentication Endpoints

### 1. Admin Login
```
POST /auth/admin/login
Content-Type: application/json

Request:
{
  "username": "admin",
  "password": "admin123"
}

Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "role": "admin"
}

Error (401):
{
  "detail": "Invalid admin credentials"
}
```

### 2. School Register
```
POST /auth/school/register
Content-Type: application/json

Request:
{
  "school_name": "MIT",
  "username": "mit_admin",
  "password": "secure123",
  "email": "admin@mit.edu",
  "location": "Cambridge, MA"
}

Response (200):
{
  "message": "School registered successfully"
}

Error (400):
{
  "detail": "Username already exists"
}
```

### 3. School Login
```
POST /auth/school/login
Content-Type: application/json

Request:
{
  "username": "mit_admin",
  "password": "secure123"
}

Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "role": "school"
}

Error (401):
{
  "detail": "Invalid school credentials"
}
```

### 4. Student Register
```
POST /auth/student/register?school_id=school-1
Content-Type: application/json

Request:
{
  "student_id": "STU001",
  "name": "John Doe",
  "email": "john@mit.edu",
  "password": "student123"
}

Response (200):
{
  "message": "Student registered successfully"
}

Error (400):
{
  "detail": "Student ID already exists"
}
```

### 5. Student Login
```
POST /auth/student/login
Content-Type: application/json

Request:
{
  "username": "STU001",
  "password": "student123"
}

Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "role": "student"
}

Error (401):
{
  "detail": "Invalid student credentials"
}
```

### 6. Verifier Register
```
POST /auth/verifier/register
Content-Type: application/json

Request:
{
  "username": "employer1",
  "password": "verify123",
  "email": "hr@company.com"
}

Response (200):
{
  "message": "Verifier registered successfully"
}

Error (400):
{
  "detail": "Username already exists"
}
```

### 7. Verifier Login
```
POST /auth/verifier/login
Content-Type: application/json

Request:
{
  "username": "employer1",
  "password": "verify123"
}

Response (200):
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "role": "verifier"
}

Error (401):
{
  "detail": "Invalid verifier credentials"
}
```

---

## 👨💼 Admin Endpoints

### 1. Get All Schools
```
GET /admin/schools
Authorization: Bearer <admin_token>

Response (200):
{
  "schools": [
    {
      "id": "school-1",
      "name": "MIT",
      "email": "admin@mit.edu",
      "location": "Cambridge, MA",
      "student_count": 5,
      "created_at": "2024-01-19T10:05:00"
    }
  ]
}

Error (403):
{
  "detail": "Admin access required"
}
```

### 2. Add New School
```
POST /admin/schools
Authorization: Bearer <admin_token>
Content-Type: application/json

Request:
{
  "school_name": "Harvard",
  "username": "harvard_admin",
  "password": "harvard123",
  "email": "admin@harvard.edu",
  "location": "Boston, MA"
}

Response (200):
{
  "message": "School added successfully"
}

Error (400):
{
  "detail": "Username already exists"
}
```

### 3. Delete School
```
DELETE /admin/schools/{school_id}
Authorization: Bearer <admin_token>

Response (200):
{
  "message": "School deleted successfully"
}

Error (404):
{
  "detail": "School not found"
}
```

### 4. Get System Reports
```
GET /admin/reports
Authorization: Bearer <admin_token>

Response (200):
{
  "total_schools": 2,
  "total_students": 10,
  "total_certificates": 15,
  "total_verifications": 8,
  "school_stats": {
    "MIT": {
      "students": 5,
      "certificates": 8
    },
    "Harvard": {
      "students": 5,
      "certificates": 7
    }
  }
}

Error (403):
{
  "detail": "Admin access required"
}
```

---

## 🏫 School Endpoints

### 1. Get All Students
```
GET /school/students
Authorization: Bearer <school_token>

Response (200):
{
  "students": [
    {
      "id": "student-1",
      "student_id": "STU001",
      "name": "John Doe",
      "email": "john@mit.edu",
      "created_at": "2024-01-19T10:10:00"
    }
  ]
}

Error (403):
{
  "detail": "School access required"
}
```

### 2. Add Student
```
POST /school/students
Authorization: Bearer <school_token>
Content-Type: application/json

Request:
{
  "student_id": "STU002",
  "name": "Jane Smith",
  "email": "jane@mit.edu",
  "password": "jane123"
}

Response (200):
{
  "message": "Student added successfully"
}

Error (400):
{
  "detail": "Student ID already exists"
}
```

### 3. Issue Certificate
```
POST /school/certificates?student_id=STU001
Authorization: Bearer <school_token>
Content-Type: multipart/form-data

Request:
- file: <certificate_file.pdf>

Response (200):
{
  "message": "Certificate issued successfully",
  "certificate_id": "cert-uuid-1",
  "hash": "sha256_hash_of_file",
  "chain_hash": "blockchain_hash"
}

Error (400):
{
  "detail": "Invalid certificate: File too small to be a valid certificate"
}
```

### 4. Get School Dashboard
```
GET /school/dashboard
Authorization: Bearer <school_token>

Response (200):
{
  "total_students": 5,
  "total_certificates": 8,
  "total_verifications": 3
}

Error (403):
{
  "detail": "School access required"
}
```

---

## 👨🎓 Student Endpoints

### 1. Get Student Profile
```
GET /student/profile
Authorization: Bearer <student_token>

Response (200):
{
  "student_id": "STU001",
  "name": "John Doe",
  "email": "john@mit.edu",
  "school_id": "school-1",
  "created_at": "2024-01-19T10:10:00"
}

Error (403):
{
  "detail": "Student access required"
}
```

### 2. Update Student Profile
```
PUT /student/profile?name=John%20Smith&email=john.smith@mit.edu
Authorization: Bearer <student_token>

Response (200):
{
  "message": "Profile updated successfully"
}

Error (403):
{
  "detail": "Student access required"
}
```

### 3. Get Student Certificates
```
GET /student/certificates
Authorization: Bearer <student_token>

Response (200):
{
  "certificates": [
    {
      "hash": "sha256_hash",
      "chain_hash": "blockchain_hash",
      "timestamp": "2024-01-19T10:15:00",
      "verifications": [
        {
          "verifier_id": "verifier-1",
          "result": true,
          "timestamp": "2024-01-19T10:20:00"
        }
      ],
      "valid": true
    }
  ]
}

Error (403):
{
  "detail": "Student access required"
}
```

### 4. Get Certificate Details
```
GET /student/certificate/{cert_hash}
Authorization: Bearer <student_token>

Response (200):
{
  "hash": "sha256_hash",
  "chain_hash": "blockchain_hash",
  "student_id": "STU001",
  "school_id": "school-1",
  "issuer_id": "school-1",
  "timestamp": "2024-01-19T10:15:00",
  "status": "added",
  "verifications": [
    {
      "verifier_id": "verifier-1",
      "result": true,
      "timestamp": "2024-01-19T10:20:00"
    }
  ],
  "valid": true
}

Error (404):
{
  "detail": "Certificate not found"
}
```

---

## 🔍 Verifier Endpoints

### 1. Verify Certificate
```
POST /verifier/verify
Authorization: Bearer <verifier_token>
Content-Type: multipart/form-data

Request:
- file: <certificate_file.pdf>

Response (200):
{
  "verification_id": "verification-uuid-1",
  "result": true,
  "hash": "sha256_hash",
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
  "explanation": "Certificate verified successfully..."
}

Error (403):
{
  "detail": "Verifier access required"
}
```

### 2. Submit Feedback
```
POST /verifier/feedback?message=Great%20system&category=verification
Authorization: Bearer <verifier_token>

Response (200):
{
  "message": "Feedback submitted successfully",
  "feedback_id": "feedback-uuid-1"
}

Error (403):
{
  "detail": "Verifier access required"
}
```

---

## 💬 Shared Endpoints

### 1. Chatbot Query
```
POST /chatbot
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
  "message": "How many certificates are registered?",
  "context": "blockchain"
}

Response (200):
{
  "response": "There are currently 15 certificates registered on the blockchain.",
  "type": "blockchain_stats",
  "data": {
    "count": 15
  }
}

Error (401):
{
  "detail": "Authentication required"
}
```

### 2. Health Check
```
GET /health

Response (200):
{
  "status": "healthy",
  "blockchain_connected": true
}
```

### 3. Root Endpoint
```
GET /

Response (200):
{
  "message": "CertiSense AI - Enhanced Blockchain Certificate System",
  "version": "3.0.0"
}
```

---

## 📋 Error Codes

| Code | Message | Meaning |
|------|---------|---------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Access denied (role mismatch) |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

---

## 🔄 Request/Response Examples

### Complete Workflow Example

#### 1. Admin Login
```bash
curl -X POST http://localhost:8000/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### 2. Add School
```bash
curl -X POST http://localhost:8000/admin/schools \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "school_name": "MIT",
    "username": "mit_admin",
    "password": "mit123",
    "email": "admin@mit.edu",
    "location": "Cambridge"
  }'
```

#### 3. School Login
```bash
curl -X POST http://localhost:8000/auth/school/login \
  -H "Content-Type: application/json" \
  -d '{"username": "mit_admin", "password": "mit123"}'
```

#### 4. Add Student
```bash
curl -X POST http://localhost:8000/school/students \
  -H "Authorization: Bearer <school_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "name": "John Doe",
    "email": "john@mit.edu",
    "password": "john123"
  }'
```

#### 5. Issue Certificate
```bash
curl -X POST "http://localhost:8000/school/certificates?student_id=STU001" \
  -H "Authorization: Bearer <school_token>" \
  -F "file=@certificate.pdf"
```

#### 6. Student Login
```bash
curl -X POST http://localhost:8000/auth/student/login \
  -H "Content-Type: application/json" \
  -d '{"username": "STU001", "password": "john123"}'
```

#### 7. Get Student Certificates
```bash
curl -X GET http://localhost:8000/student/certificates \
  -H "Authorization: Bearer <student_token>"
```

#### 8. Verifier Register
```bash
curl -X POST http://localhost:8000/auth/verifier/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "employer1",
    "password": "verify123",
    "email": "hr@company.com"
  }'
```

#### 9. Verifier Login
```bash
curl -X POST http://localhost:8000/auth/verifier/login \
  -H "Content-Type: application/json" \
  -d '{"username": "employer1", "password": "verify123"}'
```

#### 10. Verify Certificate
```bash
curl -X POST http://localhost:8000/verifier/verify \
  -H "Authorization: Bearer <verifier_token>" \
  -F "file=@certificate.pdf"
```

---

## 📊 Response Data Types

### Certificate Object
```json
{
  "id": "string",
  "name": "string",
  "hash": "string (SHA256)",
  "student_id": "string",
  "school_id": "string",
  "issuer_id": "string",
  "chain_hash": "string",
  "created_at": "datetime",
  "metadata": "object"
}
```

### Verification Object
```json
{
  "id": "string",
  "certificate_hash": "string",
  "verifier_id": "string",
  "result": "boolean",
  "ai_validation": "object",
  "blockchain_data": "object",
  "explanation": "string",
  "timestamp": "datetime"
}
```

### School Object
```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "location": "string",
  "student_count": "integer",
  "created_at": "datetime"
}
```

### Student Object
```json
{
  "id": "string",
  "student_id": "string",
  "name": "string",
  "email": "string",
  "school_id": "string",
  "created_at": "datetime"
}
```

---

**API Documentation Complete - Ready for Integration! 🚀**