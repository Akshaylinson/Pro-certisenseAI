# Student Module Documentation - CertiSense AI v3.0

## Overview

The Student Module represents the certificate owner layer, enabling students to manage profiles, access certificates, monitor verification activity, view blockchain data, and control certificate sharing.

## Architecture

**Frontend**: React with Tailwind CSS
**Backend**: FastAPI with SQLAlchemy ORM
**Database**: PostgreSQL/SQLite
**Blockchain**: Certificate validation layer
**AI Engine**: Fraud detection integration

## Module Structure

### 7 Core Modules

1. **View Profile** - Read-only profile information
2. **Manage Profile** - Update personal information
3. **View Certificate** - Access issued certificates
4. **Monitor Verification Status** - Track verification activity
5. **View Blockchain Details** - Inspect blockchain data
6. **Share Certificate** - Generate secure sharing links
7. **Submit Feedback** - Report issues and provide feedback

## Authentication Flow

### Login Process
```
1. Student enters credentials (student_id/password)
2. Backend validates against student database
3. JWT token issued with 24-hour expiration
4. Token stored in localStorage
5. Redirect to Student Dashboard
```

### Security Features
- JWT-based authentication
- Role-based access control (RBAC)
- Secure password hashing (SHA256)
- Token expiration and refresh
- Activity audit logging
- Data isolation (students only see their own data)

## Module 1: View Profile

### Features
- Read-only profile display
- Student ID
- Name and email
- Institute information
- Account status
- Program and department

### API Endpoint
```
GET /api/student/profile
Authorization: Bearer {token}

Response:
{
  "student_id": "STU001",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "program": "Computer Science",
  "department": "Engineering",
  "institute_name": "ABC University",
  "institute_id": "inst_123",
  "account_status": "active",
  "created_at": "2024-01-01T00:00:00"
}
```

## Module 2: Manage Profile

### Features
- Edit profile information
- Update name, email, phone
- View student ID (read-only)
- View institution details
- Activity logging

### API Endpoint
```
PUT /api/student/profile?name=John&email=john@example.com&phone=123456
Authorization: Bearer {token}

Response:
{
  "message": "Profile updated successfully"
}
```

### Audit Logging
All profile updates are logged with:
- User ID
- Action type
- Timestamp
- Details of changes

## Module 3: View Certificate

### Features
- List all issued certificates
- View certificate metadata
- Open certificate details
- Certificate status tracking

### Certificate Information
- Certificate ID
- Certificate Title/Name
- Certificate Hash
- Chain Hash
- Issuing Institute
- Issue Date
- Certificate Status (active/revoked)
- Verification Count
- Blockchain Status

### API Endpoints
```
GET /api/student/certificates
Authorization: Bearer {token}

Response:
{
  "total_certificates": 5,
  "certificates": [
    {
      "certificate_id": "cert_123",
      "certificate_name": "Degree Certificate",
      "certificate_hash": "abc123...",
      "chain_hash": "def456...",
      "certificate_type": "degree",
      "status": "active",
      "issue_date": "2024-01-01T00:00:00",
      "verification_count": 3,
      "blockchain_status": "verified",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}

GET /api/student/certificate/{cert_hash}
Authorization: Bearer {token}

Response:
{
  "certificate_id": "cert_123",
  "certificate_name": "Degree Certificate",
  "certificate_hash": "abc123...",
  "chain_hash": "def456...",
  "certificate_type": "degree",
  "status": "active",
  "issue_date": "2024-01-01T00:00:00",
  "issuing_institute": "ABC University",
  "verification_count": 3,
  "blockchain_data": {...},
  "created_at": "2024-01-01T00:00:00"
}
```

## Module 4: Monitor Verification Status

### Features
- View verification history
- Display verifier details
- Track verification results
- Flag suspicious activity
- Verification timestamps

### Verification Metadata
- Verification ID
- Certificate ID
- Verifier ID
- Verification Status
- Result (valid/invalid)
- Confidence Score
- Timestamp
- Suspicious flag

### API Endpoints
```
GET /api/student/verifications
Authorization: Bearer {token}

Response:
{
  "total_verifications": 10,
  "verifications": [
    {
      "verification_id": "ver_123",
      "certificate_id": "cert_123",
      "certificate_name": "Degree Certificate",
      "verifier_id": "verifier_456",
      "verification_status": "valid",
      "result": true,
      "confidence_score": 0.95,
      "is_suspicious": false,
      "timestamp": "2024-01-01T00:00:00"
    }
  ]
}

POST /api/student/verifications/{verification_id}/flag
Authorization: Bearer {token}

Response:
{
  "message": "Verification flagged as suspicious"
}
```

### Suspicious Activity Flagging
Students can flag verifications that appear suspicious:
- Unauthorized verification attempts
- Unusual verification patterns
- Unknown verifiers
- Multiple rapid verifications

## Module 5: View Blockchain Details

### Features
- Certificate hash display
- Blockchain transaction hash
- Timestamp information
- Smart contract address
- Blockchain validation status
- Hash match verification

### Blockchain Information
- Certificate Hash
- Blockchain Transaction Hash
- Timestamp
- Smart Contract Address
- Blockchain Validation Status
- Issuer ID
- Student ID
- Verification Count
- Hash Match Confirmation

### API Endpoint
```
GET /api/student/blockchain/{cert_hash}
Authorization: Bearer {token}

Response:
{
  "certificate_hash": "abc123...",
  "blockchain_transaction_hash": "def456...",
  "timestamp": "2024-01-01T00:00:00",
  "smart_contract_address": "0x1234567890abcdef...",
  "blockchain_validation_status": "verified",
  "issuer_id": "inst_123",
  "student_id": "STU001",
  "verification_count": 3,
  "hash_match": true
}
```

## Module 6: Share Certificate

### Features
- Generate verification link
- Generate QR code data
- Secure certificate access
- Privacy-preserving sharing
- Expiration management

### Sharing Options
1. **Verification Link**: Secure URL for verifiers
2. **QR Code**: Scannable code for quick verification
3. **Share Token**: Unique token for access control

### API Endpoint
```
POST /api/student/certificate/{cert_hash}/share
Authorization: Bearer {token}

Response:
{
  "verification_link": "https://certisense.ai/verify/token123",
  "qr_code_data": "CERTISENSE:abc123:token123",
  "share_token": "token123...",
  "certificate_hash": "abc123...",
  "expires_in": "30 days"
}
```

### Privacy Features
- No unnecessary personal data exposed
- Verifiers only see certificate validity
- Secure token-based access
- Expiration controls

## Module 7: Submit Feedback

### Features
- Report suspicious verification activity
- Report incorrect certificate information
- Provide system feedback
- Track feedback status

### Feedback Categories
- **suspicious_verification**: Report suspicious verification attempts
- **incorrect_info**: Report incorrect certificate information
- **general**: General system feedback

### Feedback Data Fields
- Feedback ID
- Student ID
- Certificate ID (optional)
- Message
- Category
- Status (open/resolved)
- Timestamp

### API Endpoints
```
POST /api/student/feedback?message=...&category=suspicious_verification
Authorization: Bearer {token}

Response:
{
  "feedback_id": "fb_123",
  "message": "Feedback submitted successfully",
  "status": "open",
  "timestamp": "2024-01-01T00:00:00"
}

GET /api/student/feedback
Authorization: Bearer {token}

Response:
{
  "total_feedback": 3,
  "feedbacks": [
    {
      "id": "fb_123",
      "certificate_id": "cert_123",
      "message": "Suspicious verification detected",
      "category": "suspicious_verification",
      "status": "open",
      "timestamp": "2024-01-01T00:00:00"
    }
  ]
}
```

## Dashboard Statistics

### Metrics Displayed
- Total certificates
- Active certificates
- Total verifications
- Recent verifications (30 days)
- Student information

### API Endpoint
```
GET /api/student/dashboard
Authorization: Bearer {token}

Response:
{
  "student_info": {
    "name": "John Doe",
    "student_id": "STU001",
    "email": "john@example.com"
  },
  "statistics": {
    "total_certificates": 5,
    "active_certificates": 4,
    "total_verifications": 10,
    "recent_verifications": 3
  }
}
```

## Security Requirements

### Authentication
- JWT tokens with 24-hour expiration
- Secure password hashing
- Token refresh mechanism
- Session invalidation on logout

### Authorization
- Role-based access control
- Student-specific data isolation
- API endpoint protection
- Resource ownership validation

### Data Privacy
- Students only access their own data
- No cross-student data access
- Secure certificate sharing
- Privacy-preserving verification

### Activity Logging
- All profile updates logged
- Certificate access tracked
- Verification monitoring logged
- Feedback submissions recorded

## Error Handling

### Common Errors
- 401: Authentication required / Invalid token
- 403: Access denied / Insufficient permissions
- 404: Resource not found
- 500: Internal server error

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

## Integration Points

### Blockchain Service
- Certificate hash verification
- Chain data retrieval
- Verification recording
- Status checking

### Institute Service
- Institute information
- Certificate issuance
- Student management

### Verifier Service
- Verification tracking
- Verifier details
- Verification results

## Testing

### Test Scenarios
1. Login and authentication
2. View profile information
3. Update profile details
4. List certificates
5. View certificate details
6. Monitor verifications
7. Flag suspicious activity
8. View blockchain details
9. Generate share link
10. Submit feedback

### API Testing
```bash
# Login
curl -X POST http://localhost:8000/auth/student/login \
  -H "Content-Type: application/json" \
  -d '{"username":"STU001","password":"password"}'

# Get profile
curl -X GET http://localhost:8000/api/student/profile \
  -H "Authorization: Bearer {token}"

# Get certificates
curl -X GET http://localhost:8000/api/student/certificates \
  -H "Authorization: Bearer {token}"
```

## Performance Metrics

### Target Performance
- Profile load: < 300ms
- Certificate list: < 500ms
- Verification history: < 1 second
- Blockchain lookup: < 500ms
- Dashboard load: < 500ms

---

**Version**: 3.0.0
**Last Updated**: 2024
**Maintained By**: CertiSense AI Development Team
