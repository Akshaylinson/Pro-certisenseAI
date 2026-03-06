# 📋 SYNOPSIS.README - CertiSense AI v3.0 Complete Overview

## 🎯 Project Overview

**CertiSense AI v3.0** is an advanced blockchain-based certificate verification system with hierarchical role-based access control. It enables institutes to issue certificates to students, which can be verified by employers through AI-powered validation and blockchain confirmation.

**System Hierarchy**: Admin → Institutes → Students → Certificates → Verifiers

---

## 👥 Four User Types & Their Features

### 1️⃣ **ADMIN (System Administrator)**

#### **Role Definition**
- System-level manager responsible for institute management and system oversight
- Only login access (no public registration)
- Pre-configured credentials: admin/admin123

#### **Key Features**
| Feature | Description |
|---------|-------------|
| **Dashboard** | System-wide analytics with total institutes, students, certificates, verifications |
| **Manage Institutes** | Add new institutes, view all institutes, delete institutes |
| **Institute Statistics** | View student count and certificate count per institute |
| **System Reports** | Generate comprehensive reports on system activities |
| **Analytics** | Visual graphs and statistics for all entities |
| **Monitoring** | Track all system activities and verifications |

#### **Workflow**
```
Login (admin/admin123)
    ↓
View Dashboard (System Analytics)
    ↓
Manage Institutes (Add/View/Delete)
    ↓
View Reports & Statistics
    ↓
Monitor System Activities
    ↓
Logout
```

#### **API Endpoints**
- `POST /auth/admin/login` - Admin login
- `GET /admin/institutes` - List all institutes
- `POST /admin/institutes` - Add new institute
- `DELETE /admin/institutes/{id}` - Delete institute
- `GET /admin/reports` - Get system reports

#### **Responsibilities**
- Oversee entire system operations
- Manage institute registrations
- Monitor system health and statistics
- Generate reports for stakeholders

---

### 2️⃣ **INSTITUTE (Education Center)**

#### **Role Definition**
- Education center/university that issues certificates to students
- Registration + Login workflow
- Manages students and certificate issuance
- Operates independently within the system

#### **Key Features**
| Feature | Description |
|---------|-------------|
| **Dashboard** | Institute-specific analytics (students, certificates, verifications) |
| **Manage Students** | Add students with unique student IDs, view student list |
| **Issue Certificates** | Upload and issue certificates to registered students |
| **Student List** | View all registered students under the institute |
| **Analytics** | Track student count, certificates issued, verifications received |
| **Certificate Tracking** | Monitor all certificates issued by the institute |

#### **Workflow**
```
Register as Institute
    ↓
Login with Institute Credentials
    ↓
View Institute Dashboard
    ↓
Add Students (with unique Student IDs)
    ↓
Issue Certificates to Students
    ↓
View Analytics & Statistics
    ↓
Monitor Certificate Issuance
    ↓
Logout
```

#### **API Endpoints**
- `POST /auth/institute/register` - Institute registration
- `POST /auth/institute/login` - Institute login
- `GET /institute/students` - List students
- `POST /institute/students` - Add student
- `POST /institute/certificates` - Issue certificate
- `GET /institute/dashboard` - Get analytics

#### **Responsibilities**
- Register students with unique IDs
- Issue certificates to students
- Maintain student records
- Track certificate issuance
- Provide certificate data to blockchain

---

### 3️⃣ **STUDENT (Certificate Holder)**

#### **Role Definition**
- Certificate holder who receives certificates from institutes
- Registration by institute admin (not self-registration)
- Login using Student ID
- Can track and view their certificates

#### **Key Features**
| Feature | Description |
|---------|-------------|
| **Profile Management** | View and edit personal information (name, email) |
| **Certificate Tracking** | View all certificates issued to the student |
| **Certificate Details** | View certificate hash, chain hash, blockchain status |
| **Issuer Information** | See which institute issued the certificate |
| **Verification History** | Track all verifications performed on certificates |
| **Verifier Details** | See who verified the certificate and when |
| **Real-time Updates** | Monitor verification status in real-time |

#### **Workflow**
```
Receive Credentials from Institute
    ↓
Login with Student ID & Password
    ↓
View Profile
    ↓
View All Certificates
    ↓
Click Certificate for Details
    ↓
See Verification History
    ↓
See Verifier Information
    ↓
Edit Profile (if needed)
    ↓
Logout
```

#### **API Endpoints**
- `POST /auth/student/login` - Student login
- `GET /student/profile` - Get profile
- `PUT /student/profile` - Update profile
- `GET /student/certificates` - List certificates
- `GET /student/certificate/{hash}` - Get certificate details

#### **Certificate Details Visible**
- Certificate Hash (SHA256)
- Chain Hash (Blockchain)
- Blockchain Status (Added/Verified/Revoked)
- Issuer Information (Institute name, ID)
- Verification History (All verifiers, timestamps, results)
- Verifier Details (Who verified, when, result)

#### **Responsibilities**
- Maintain accurate profile information
- Track issued certificates
- Monitor verification status
- Share certificate information with verifiers

---

### 4️⃣ **VERIFIER (Employer/Third Party)**

#### **Role Definition**
- Employer or third-party entity that verifies certificate authenticity
- Registration + Login workflow (ALT flow)
- Can verify certificates and provide feedback
- Limited access (verification-only features)

#### **Key Features**
| Feature | Description |
|---------|-------------|
| **Certificate Verification** | Upload certificate file for verification |
| **AI Validation** | AI-powered content analysis and validation |
| **Blockchain Confirmation** | Verify certificate against blockchain registry |
| **Verification Results** | View detailed verification results |
| **Blockchain Data** | Access certificate chain and history |
| **Confidence Scoring** | See AI confidence score for verification |
| **Validation Tokens** | Receive unique validation tokens |
| **Feedback Submission** | Submit feedback on verification process |
| **Verification History** | Track all verifications performed |

#### **Workflow**
```
Register as Verifier
    ↓
Login with Verifier Credentials
    ↓
Upload Certificate for Verification
    ↓
View Verification Results
    ↓
See AI Validation Details
    ↓
See Blockchain Confirmation
    ↓
View Certificate Chain
    ↓
Submit Feedback (optional)
    ↓
Logout
```

#### **API Endpoints**
- `POST /auth/verifier/register` - Verifier registration
- `POST /auth/verifier/login` - Verifier login
- `POST /verifier/verify` - Verify certificate
- `POST /verifier/feedback` - Submit feedback

#### **Verification Results Include**
- Verification Status (Valid/Invalid)
- Certificate Hash
- AI Validation Score (0-100%)
- Format Validation (PDF/JPG/PNG)
- Keyword Detection (Certificate-related keywords)
- Validation Token (Unique identifier)
- Blockchain Data (Issuer, timestamp, status)
- Explanation (AI-generated explanation)

#### **Responsibilities**
- Verify certificate authenticity
- Provide feedback on verification process
- Report issues or concerns
- Access blockchain data for verification

---

## 🔄 Major Working of the Project

### **1. Authentication & Authorization Flow**

```
User Selects Role
    ↓
Enters Credentials
    ↓
Backend Validates
    ↓
JWT Token Generated
    ↓
Token Stored in Frontend
    ↓
Role-Based Dashboard Loaded
    ↓
All Requests Include Token
    ↓
Backend Verifies Token & Role
    ↓
Access Granted/Denied
```

### **2. Certificate Issuance Flow**

```
Institute Admin Uploads Certificate
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
Blockchain Registry Updated
    ↓
Student Can View Certificate
    ↓
Certificate Ready for Verification
```

### **3. Certificate Verification Flow**

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
Verification Added to Blockchain
    ↓
Verification Result Returned
    ↓
Student Sees Verification Update
```

### **4. Data Flow Architecture**

```
Frontend (React)
    ↓
API Requests (HTTP/JSON)
    ↓
Backend (FastAPI)
    ↓
Authentication Service
    ↓
Business Logic
    ↓
Blockchain Service
    ↓
AI Validation Service
    ↓
In-Memory Database
    ↓
Response to Frontend
```

### **5. Blockchain Integration**

```
Certificate File
    ↓
SHA256 Hash Generation
    ↓
Blockchain Hash Creation
    ↓
Chain Hash Storage
    ↓
Immutable Registry
    ↓
Verification Records Added
    ↓
Certificate Chain Maintained
    ↓
Revocation Support
```

### **6. AI Validation Process**

```
Certificate Content
    ↓
Format Detection (PDF/JPG/PNG)
    ↓
Keyword Analysis (Certificate-related)
    ↓
Content Validation
    ↓
Confidence Scoring (0-100%)
    ↓
Validation Token Generation
    ↓
Explanation Generation
    ↓
Result Returned
```

---

## 🔐 Security Architecture

### **Authentication**
- JWT Token-based authentication
- 24-hour token expiration
- Secure token storage in localStorage

### **Authorization**
- Role-based access control (RBAC)
- Endpoint-level role verification
- User isolation and data access control

### **Data Protection**
- SHA256 password hashing
- CORS configuration (localhost:5173)
- File upload validation
- Input validation on all endpoints

---

## 📊 System Statistics & Analytics

### **Admin Dashboard Shows**
- Total Institutes Count
- Total Students Count
- Total Certificates Count
- Total Verifications Count
- Institute-wise Statistics (Students & Certificates per institute)

### **Institute Dashboard Shows**
- Total Students
- Certificates Issued
- Verifications Received

### **Student Dashboard Shows**
- Certificate Count
- Verification Status
- Issuer Information
- Verifier Details

---

## 🔧 Technology Stack

### **Backend**
- FastAPI (Python web framework)
- Pydantic (Data validation)
- JWT (Authentication)
- SHA256 (Hashing)

### **Frontend**
- React 18.2.0
- Tailwind CSS (Styling)
- Context API (State management)
- Fetch API (HTTP requests)

### **Blockchain**
- Mock blockchain (In-memory storage)
- SHA256 hashing
- Immutable registry

### **AI**
- Content validation
- Confidence scoring
- Keyword analysis

---

## 📈 Key Metrics

| Metric | Description |
|--------|-------------|
| **Total Endpoints** | 26 API endpoints |
| **User Roles** | 4 (Admin, Institute, Student, Verifier) |
| **Authentication Methods** | 7 (Login/Register endpoints) |
| **Certificate Operations** | Issue, Verify, Track, Revoke |
| **Verification Methods** | AI + Blockchain |
| **Security Layers** | JWT + RBAC + Hashing |

---

## 🚀 System Capabilities

✅ Multi-role authentication and authorization
✅ Hierarchical entity management (Admin → Institutes → Students)
✅ Certificate lifecycle management (Issue → Verify → Track)
✅ Blockchain integration with immutable registry
✅ AI-powered validation with confidence scoring
✅ Real-time analytics and reporting
✅ Certificate tracking and verification history
✅ Feedback collection system
✅ Secure API endpoints with role-based access
✅ Responsive UI for all user types

---

## 📝 Default Credentials

| User Type | Username | Password |
|-----------|----------|----------|
| Admin | admin | admin123 |
| Institute | (Register) | (Set during registration) |
| Student | (Student ID) | (Set by institute) |
| Verifier | (Register) | (Set during registration) |

---

## 🎯 Use Cases

### **Admin Use Case**
Admin monitors system health, adds new institutes, views statistics, and generates reports for stakeholders.

### **Institute Use Case**
Institute registers students, issues certificates, tracks issuance, and manages student records.

### **Student Use Case**
Student views issued certificates, tracks verification status, and shares certificate information with employers.

### **Verifier Use Case**
Verifier uploads certificates, verifies authenticity through AI and blockchain, and provides feedback.

---

## 📞 Support & Documentation

- **README.md** - Complete system documentation
- **QUICK_START.md** - 5-minute quick start guide
- **API_DOCUMENTATION.md** - All endpoints documented
- **DATABASE_SCHEMA.md** - Data model documentation
- **IMPLEMENTATION_SUMMARY.md** - Project completion details

---

**CertiSense AI v3.0 - Blockchain-Powered Certificate Verification System**
**Built with React, FastAPI, AI Validation, and Blockchain Technology**