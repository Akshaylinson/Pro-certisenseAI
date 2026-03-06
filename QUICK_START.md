# 🚀 CertiSense AI v3.0 - Quick Start Guide

## System Overview

CertiSense AI is now a complete hierarchical certificate management system:

```
Admin (System Manager)
  ↓
Schools/Institutes (Education Centers)
  ↓
Students (Certificate Holders)
  ↓
Certificates (Blockchain Tracked)
  ↓
Verifiers (Employers/Third Parties)
```

## 🏃 Quick Start (5 Minutes)

### 1. Start Backend
```bash
cd backend
python -m uvicorn certisense_main:app --reload --port 8000
```

### 2. Start Frontend
```bash
cd frontend/web
npm run dev
```

### 3. Open Browser
```
http://localhost:5173
```

## 👤 Login as Admin

**First Time Setup**:
1. Select "Admin" from User Type dropdown
2. Enter credentials:
   - Username: `admin`
   - Password: `admin123`
3. Click "Sign In"

**Admin Dashboard Features**:
- View system analytics
- Add new schools
- Manage schools
- View school statistics
- System-wide reports

## 🏫 Create a School

**As Admin**:
1. Go to "Manage Schools" tab
2. Fill in school details:
   - School Name: e.g., "MIT"
   - Username: e.g., "mit_admin"
   - Email: e.g., "admin@mit.edu"
   - Location: e.g., "Cambridge, MA"
   - Password: e.g., "secure123"
3. Click "Add School"

## 🔐 Login as School

**After School is Created**:
1. Logout from admin
2. Select "School/Institute" from User Type
3. Click "Need an account? Register" (if first time)
4. Or login with credentials created by admin
5. Enter username and password
6. Click "Sign In"

**School Dashboard Features**:
- View school analytics
- Add students
- Issue certificates
- Manage student list

## 👨🎓 Add Students (As School)

**In School Dashboard**:
1. Go to "Manage Students" tab
2. Fill in student details:
   - Student ID: e.g., "STU001"
   - Full Name: e.g., "John Doe"
   - Email: e.g., "john@mit.edu"
   - Password: e.g., "student123"
3. Click "Add Student"

## 📜 Issue Certificate (As School)

**In School Dashboard**:
1. Go to "Issue Certificates" tab
2. Select student from dropdown
3. Upload certificate file (PDF/JPG/PNG)
4. Click "Issue Certificate"
5. Certificate is now on blockchain!

## 👨🎓 Login as Student

**After Student is Added**:
1. Logout from school
2. Select "Student" from User Type
3. Enter credentials:
   - Student ID: e.g., "STU001"
   - Password: e.g., "student123"
4. Click "Sign In"

**Student Dashboard Features**:
- View and edit profile
- Track all certificates
- View certificate details:
  - Hash and chain hash
  - Blockchain status
  - Issuer information
  - Verification history
- See verifier details

## 🔍 Verify Certificate (As Verifier)

**First Time**:
1. Logout from student
2. Select "Verifier" from User Type
3. Click "Need an account? Register"
4. Fill in details:
   - Username: e.g., "employer1"
   - Email: e.g., "hr@company.com"
   - Password: e.g., "verify123"
5. Click "Register"

**Login and Verify**:
1. Login with verifier credentials
2. Go to "Verify Certificate" tab
3. Upload certificate file
4. View verification results:
   - AI validation score
   - Blockchain confirmation
   - Certificate details
   - Issuer information

## 📊 View Analytics

### Admin Analytics
- Total schools, students, certificates
- School-wise statistics
- System-wide reports

### School Analytics
- Total students
- Certificates issued
- Verifications received

### Student Dashboard
- Certificate count
- Verification status
- Issuer and verifier details

## 🔄 Complete Workflow Example

### Step 1: Admin Setup
```
1. Login as admin (admin/admin123)
2. Add school "Harvard University"
3. School credentials: harvard_admin / harvard123
```

### Step 2: School Setup
```
1. Logout and login as school (harvard_admin / harvard123)
2. Add student "Alice Smith" (STU001 / alice123)
3. Add student "Bob Johnson" (STU002 / bob123)
```

### Step 3: Issue Certificate
```
1. In school dashboard, go to "Issue Certificates"
2. Select "Alice Smith"
3. Upload certificate PDF
4. Certificate issued and on blockchain!
```

### Step 4: Student Views Certificate
```
1. Logout and login as student (STU001 / alice123)
2. Go to "My Certificates"
3. Click on certificate to see details
4. View hash, chain hash, issuer info
```

### Step 5: Verifier Verifies
```
1. Logout and register as verifier
2. Login as verifier
3. Upload same certificate
4. See verification results
5. Certificate confirmed on blockchain!
```

### Step 6: Student Sees Verification
```
1. Logout and login as student again
2. Go to "My Certificates"
3. Click certificate to see details
4. See verifier information
5. See verification timestamp
```

## 🎯 Key Features to Try

### Admin
- [ ] Add multiple schools
- [ ] View school statistics
- [ ] Check system reports
- [ ] Delete a school

### School
- [ ] Add multiple students
- [ ] Issue certificates to different students
- [ ] View school analytics
- [ ] Check student list

### Student
- [ ] Edit profile
- [ ] View all certificates
- [ ] Click certificate for details
- [ ] See verifier information

### Verifier
- [ ] Verify multiple certificates
- [ ] View verification results
- [ ] Submit feedback
- [ ] Check blockchain data

## 🐛 Troubleshooting

### Backend Not Starting
```bash
# Kill existing Python processes
taskkill /F /IM python.exe

# Restart backend
python -m uvicorn certisense_main:app --reload --port 8000
```

### Frontend Not Loading
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### CORS Errors
- Make sure backend is running on http://localhost:8000
- Make sure frontend is running on http://localhost:5173

### Login Issues
- Check credentials are correct
- Make sure you're selecting the right user type
- Clear browser cache and try again

## 📱 API Testing with cURL

### Admin Login
```bash
curl -X POST http://localhost:8000/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Register School
```bash
curl -X POST http://localhost:8000/auth/school/register \
  -H "Content-Type: application/json" \
  -d '{
    "school_name": "MIT",
    "username": "mit_admin",
    "password": "mit123",
    "email": "admin@mit.edu",
    "location": "Cambridge"
  }'
```

### Add Student
```bash
curl -X POST http://localhost:8000/school/students \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "name": "John Doe",
    "email": "john@mit.edu",
    "password": "john123"
  }'
```

## 🎓 Learning Path

1. **Start with Admin**: Understand system overview
2. **Create School**: Learn school management
3. **Add Students**: Understand student hierarchy
4. **Issue Certificate**: See blockchain integration
5. **Login as Student**: Track certificates
6. **Verify Certificate**: Complete the workflow

## 📞 Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review RESTRUCTURING_SUMMARY.md for architecture details
3. Check API endpoints in README.md
4. Review error messages in browser console

---

**Happy Certificate Verification! 🎉**