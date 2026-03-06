# 🔐 CertiSense AI v3.0 - Enhanced Blockchain Certificate Verification System

A complete role-based blockchain certificate verification platform with hierarchical entity management: Admin → Institutes → Students → Certificates → Verifiers.

## 🏗️ System Architecture

```
Admin (System Manager)
  ├── Manage Institutes
  ├── View System Analytics
  └── Monitor All Activities

Institute (Education Center)
  ├── Manage Students
  ├── Issue Certificates
  ├── View Institute Dashboard
  └── Track Certificates

Student (Certificate Holder)
  ├── View Profile
  ├── Track Certificates
  ├── View Certificate Details
  ├── See Verifier Information
  └── Monitor Verification Status

Verifier (Employer/Third Party)
  ├── Verify Certificates
  ├── View Verification Results
  ├── Submit Feedback
  └── Access Blockchain Data
```

## 🎭 System Roles & Features

### 👨💼 Admin (System Administrator)
- **Dashboard**: System-wide analytics and statistics
- **Manage Institutes**: Add, view, delete institutes
- **Institute Statistics**: View student count and certificates per institute
- **System Reports**: Total institutes, students, certificates, verifications
- **Analytics**: Graphs and statistics for all entities

### 🏫 Institute (Education Center)
- **Dashboard**: Institute-specific analytics
- **Manage Students**: Add students with unique student IDs
- **Issue Certificates**: Upload and issue certificates to students
- **Student List**: View all registered students
- **Analytics**: Student count, certificates issued, verifications

### 👨🎓 Student (Certificate Holder)
- **Profile Management**: View and edit personal information
- **Certificate Tracking**: View all issued certificates
- **Certificate Details**: 
  - Certificate hash and chain hash
  - Blockchain status
  - Issuer information
  - Verification history
- **Verifier Details**: See who verified the certificate
- **Verification Updates**: Real-time verification status

### 🔍 Verifier (Employer/Third Party)
- **Certificate Verification**: Upload and verify certificate authenticity
- **Verification Results**: AI validation and blockchain confirmation
- **Blockchain Data**: View certificate chain and history
- **Feedback Submission**: Report issues or provide feedback
- **Verification History**: Track all verifications performed

## 📁 Project Structure

```
Pro-1-cert-verifier/
├── backend/
│   ├── certisense_main.py          # Main FastAPI application
│   ├── models.py                   # Pydantic data models
│   ├── auth.py                     # Authentication service
│   ├── blockchain_service.py       # Blockchain integration
│   ├── ai_service.py               # AI validation service
│   ├── chatbot_service.py          # Chatbot functionality
│   └── requirements.txt            # Python dependencies
├── frontend/web/
│   ├── src/
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx     # Authentication context
│   │   ├── components/
│   │   │   ├── LoginForm.jsx       # Multi-role login
│   │   │   ├── AdminDashboard.jsx  # Admin portal
│   │   │   ├── InstituteDashboard.jsx # Institute portal
│   │   │   ├── StudentDashboard.jsx # Student portal
│   │   │   └── VerifierDashboard.jsx # Verifier portal
│   │   └── App.jsx                 # Role-based routing
│   └── package.json
├── scripts/
│   ├── start_certisense.sh         # Linux/Mac startup
│   └── start_certisense.bat        # Windows startup
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v16+)
- Python (3.8+)
- Git

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn certisense_main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend/web
npm install
npm run dev
```

### Access System
- **Application**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Health**: http://localhost:8000/health

## 🔐 Default Credentials

### Admin Access
- **Username**: admin
- **Password**: admin123

### Institute
- **Registration**: Available through UI
- **Role**: Institute

### Student
- **Registration**: By institute admin
- **Login**: Using Student ID

### Verifier
- **Registration**: Available through UI
- **Role**: Verifier

## 🔄 Workflows

### Admin Workflow
1. Login with admin credentials
2. View system dashboard with analytics
3. Manage institutes (add, view, delete)
4. Monitor institute statistics
5. View system-wide reports
6. Logout

### Institute Workflow
1. Register as institute
2. Login to institute dashboard
3. Add students with unique IDs
4. Issue certificates to students
5. View institute analytics
6. Monitor certificate issuance
7. Logout

### Student Workflow
1. Receive login credentials from institute
2. Login to student dashboard
3. View and edit profile
4. Track all issued certificates
5. View certificate details:
   - Hash and chain hash
   - Blockchain status
   - Issuer information
   - Verification history
6. See verifier details
7. Logout

### Verifier Workflow
1. Register as verifier
2. Login to verifier portal
3. Upload certificate for verification
4. View verification results
5. See blockchain data
6. Submit feedback
7. Logout

## 🔧 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/admin/login` | Admin login |
| POST | `/auth/institute/register` | Institute registration |
| POST | `/auth/institute/login` | Institute login |
| POST | `/auth/student/register` | Student registration |
| POST | `/auth/student/login` | Student login |
| POST | `/auth/verifier/register` | Verifier registration |
| POST | `/auth/verifier/login` | Verifier login |

### Admin Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/institutes` | List all institutes |
| POST | `/admin/institutes` | Add new institute |
| DELETE | `/admin/institutes/{id}` | Delete institute |
| GET | `/admin/reports` | System reports |

### Institute Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/institute/students` | List students |
| POST | `/institute/students` | Add student |
| POST | `/institute/certificates` | Issue certificate |
| GET | `/institute/dashboard` | Institute analytics |

### Student Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/student/profile` | Get profile |
| PUT | `/student/profile` | Update profile |
| GET | `/student/certificates` | List certificates |
| GET | `/student/certificate/{hash}` | Certificate details |

### Verifier Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/verifier/verify` | Verify certificate |
| POST | `/verifier/feedback` | Submit feedback |

## 🤖 AI Features

- **Content Validation**: Format and keyword analysis
- **Confidence Scoring**: AI-based authenticity assessment
- **Validation Tokens**: Unique verification identifiers
- **Intelligent Explanations**: Verification result explanations

## 🔗 Blockchain Features

- **Certificate Hashing**: SHA256 hash generation
- **Chain Tracking**: Certificate chain hash storage
- **Verification History**: All verifications recorded
- **Immutable Registry**: Permanent certificate records
- **Certificate Revocation**: Support for certificate revocation

## 📊 Analytics & Reporting

### Admin Analytics
- Total institutes, students, certificates
- Institute-wise statistics
- Verification trends
- System-wide reports

### Institute Analytics
- Total students
- Certificates issued
- Verification count
- Student management

### Student Dashboard
- Certificate count
- Verification status
- Issuer information
- Verifier details

## 🔐 Security Features

- **JWT Authentication**: Secure token-based access
- **Role-Based Authorization**: Endpoint protection
- **Password Hashing**: SHA256 encryption
- **CORS Protection**: Cross-origin security
- **File Validation**: Upload restrictions

## 🚀 System Capabilities

- [x] Multi-role authentication and authorization
- [x] Hierarchical entity management
- [x] Certificate lifecycle management
- [x] Blockchain integration
- [x] AI-powered validation
- [x] Real-time analytics
- [x] Certificate tracking
- [x] Verification history
- [x] Feedback system
- [x] Secure API endpoints

---

**CertiSense AI v3.0 - Built with React, FastAPI, AI Validation, and Blockchain Technology**#   P r o - c e r t i s e n s e A I  
 