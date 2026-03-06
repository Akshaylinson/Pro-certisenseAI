# CertiSense AI v3.0 - Admin Module Documentation

## Overview
The Admin Module is the system governance layer for CertiSense AI v3.0, providing complete control over institutes, certificates, verifiers, and system monitoring.

## Architecture

### Technology Stack
- **Frontend**: React with Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: SQLite/PostgreSQL
- **Authentication**: JWT tokens
- **Blockchain**: Certificate hash storage
- **AI Engine**: Fraud detection and validation

## Installation & Setup

### Backend Setup

1. **Install Dependencies**
```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] python-multipart
```

2. **Start Admin Server**
```bash
python admin_main.py
```

Server runs on: `http://localhost:8000`

### Frontend Setup

1. **Install Dependencies**
```bash
cd frontend/web
npm install axios
```

2. **Start Frontend**
```bash
npm run dev
```

Application runs on: `http://localhost:5173`

## Default Admin Credentials

```
Username: admin
Password: admin123
```

## Admin Module Features

### Module 1: Manage Institutes
- **Add Institute**: Register new educational institutions
- **Edit Institute**: Modify institute information
- **Delete Institute**: Remove institutes (with dependency checks)
- **View Institutes**: List all institutes with metadata

**API Endpoints:**
- `GET /admin/institutes` - List all institutes
- `POST /admin/institutes` - Add new institute
- `PUT /admin/institutes/{id}` - Update institute
- `DELETE /admin/institutes/{id}` - Delete institute

### Module 2: Manage Certificates
- **View Certificates**: List all issued certificates
- **Monitor Certificates**: Track certificate lifecycle
- **Approve Certificates**: Approve pending certificates
- **Audit Certificates**: Perform integrity checks

**API Endpoints:**
- `GET /admin/certificates` - List certificates
- `PUT /admin/certificates/{id}/approve` - Approve certificate
- `PUT /admin/certificates/{id}/audit` - Audit certificate

### Module 3: View Students
- **View Profiles**: Read-only access to student data
- **View Certificates**: See student certificates
- **View Activity**: Monitor verification activity

**API Endpoints:**
- `GET /admin/students` - List all students

### Module 4: Manage Verifiers
- **Add Verifier**: Register verification authorities
- **Edit Verifier**: Update verifier details
- **Delete Verifier**: Remove verifiers
- **View Verifiers**: List all verifiers

**API Endpoints:**
- `GET /admin/verifiers` - List verifiers
- `POST /admin/verifiers` - Add verifier
- `PUT /admin/verifiers/{id}` - Update verifier
- `DELETE /admin/verifiers/{id}` - Delete verifier

### Module 5: Monitor Verifications
- **View Verifications**: Display all verification requests
- **Track Verifications**: Monitor verification lifecycle
- **Detect Anomalies**: Identify suspicious patterns
- **Flag Activity**: Mark suspicious verifications

**API Endpoints:**
- `GET /admin/verifications` - List verifications
- `PUT /admin/verifications/{id}/flag` - Flag verification

### Module 6: System Analytics
- **Dashboard Metrics**: Real-time system statistics
- **Performance Analytics**: Success rates and trends
- **Certificate Distribution**: Status breakdown
- **Activity Monitoring**: 30-day activity tracking

**API Endpoints:**
- `GET /admin/analytics` - Get system analytics

### Module 7: Generate Reports
- **Institute Reports**: Comprehensive institute data
- **Certificate Reports**: Certificate issuance analysis
- **Verification Reports**: Verification activity
- **System Reports**: Complete system overview

**API Endpoints:**
- `GET /admin/reports/institutes` - Institute report
- `GET /admin/reports/certificates` - Certificate report
- `GET /admin/reports/verifications` - Verification report

### Module 8: Feedback Management
- **View Feedback**: Display verifier feedback
- **Review Feedback**: Analyze complaints
- **Flag Feedback**: Mark for follow-up
- **Resolve Feedback**: Close feedback items

**API Endpoints:**
- `GET /admin/feedback` - List feedback
- `PUT /admin/feedback/{id}/flag` - Flag feedback
- `PUT /admin/feedback/{id}/resolve` - Resolve feedback

## Security Features

### Authentication
- JWT token-based authentication
- 24-hour token expiration
- Secure password hashing (SHA256)

### Authorization
- Role-based access control (RBAC)
- Admin-only endpoint protection
- Token validation on all requests

### Audit Logging
All admin actions are logged with:
- User ID
- Action type
- Entity affected
- Timestamp
- IP address

### API Security
- CORS protection
- Input validation
- SQL injection prevention
- Rate limiting (recommended for production)

## Database Schema

### Tables
1. **institutes** - Institute information
2. **students** - Student records
3. **certificates** - Certificate data
4. **verifiers** - Verifier accounts
5. **verifications** - Verification records
6. **feedbacks** - Feedback submissions
7. **audit_logs** - System audit trail

## API Authentication

All admin endpoints require JWT token in header:

```javascript
headers: {
  'Authorization': 'Bearer <token>'
}
```

## Usage Examples

### Login
```javascript
const response = await axios.post('http://localhost:8000/auth/admin/login', {
  username: 'admin',
  password: 'admin123'
});
const token = response.data.access_token;
```

### Get Analytics
```javascript
const analytics = await axios.get('http://localhost:8000/admin/analytics', {
  headers: { Authorization: `Bearer ${token}` }
});
```

### Delete Institute
```javascript
await axios.delete(`http://localhost:8000/admin/institutes/${instituteId}`, {
  headers: { Authorization: `Bearer ${token}` }
});
```

## Error Handling

### Common Error Codes
- `401` - Unauthorized (invalid/expired token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (entity doesn't exist)
- `400` - Bad Request (validation error)
- `500` - Internal Server Error

## Deployment

### Production Checklist
- [ ] Change default admin credentials
- [ ] Enable HTTPS
- [ ] Configure PostgreSQL database
- [ ] Set up rate limiting
- [ ] Enable audit log archiving
- [ ] Configure backup strategy
- [ ] Set up monitoring alerts
- [ ] Enable CORS for specific domains only

## Troubleshooting

### Cannot Login
- Verify credentials
- Check backend server is running
- Verify database connection

### Token Expired
- Re-login to get new token
- Check token expiration settings

### Permission Denied
- Verify user role is 'admin'
- Check token is valid

## Support

For issues or questions:
- Check logs in `backend/logs/`
- Review audit logs for admin actions
- Verify database connectivity

## Version History

### v3.0.0 (Current)
- Complete admin module implementation
- 8 functional modules
- JWT authentication
- Audit logging
- Analytics dashboard
- Report generation
- Feedback management

---

**CertiSense AI v3.0 - Admin Module**
Built with React, FastAPI, and Blockchain Technology
