# Student Module Integration Guide
# CertiSense AI v3.0

## Quick Start

### 1. Backend Integration

Update `certisense_main.py` to include student routes:

```python
from student_routes import router as student_router

# Add student router
app.include_router(student_router)
```

### 2. Frontend Integration

Update `App.jsx` to include the enhanced student dashboard:

```javascript
import StudentDashboardEnhanced from './components/StudentDashboardEnhanced';

// Add route
{user?.role === 'student' && <StudentDashboardEnhanced />}
```

### 3. Start Services

```bash
# Backend
cd backend
python -m uvicorn certisense_main:app --reload --port 8000

# Frontend
cd frontend/web
npm run dev
```

## API Endpoints Summary

### Authentication
- POST `/auth/student/login` - Login student

### Profile Management
- GET `/api/student/profile` - View profile
- PUT `/api/student/profile` - Update profile

### Certificate Management
- GET `/api/student/certificates` - List certificates
- GET `/api/student/certificate/{hash}` - Get certificate details

### Verification Monitoring
- GET `/api/student/verifications` - Get verification history
- POST `/api/student/verifications/{id}/flag` - Flag suspicious

### Blockchain
- GET `/api/student/blockchain/{hash}` - Get blockchain details

### Sharing
- POST `/api/student/certificate/{hash}/share` - Generate share link

### Feedback
- POST `/api/student/feedback` - Submit feedback
- GET `/api/student/feedback` - Get my feedback

### Dashboard
- GET `/api/student/dashboard` - Get dashboard stats
- POST `/api/student/logout` - Logout

## Testing

### Test Student Account
Create a test student through institute:
```
Student ID: STU001
Password: student123
Email: student@test.com
```

### Test Workflow

1. **Login as Student**
```bash
curl -X POST http://localhost:8000/auth/student/login \
  -H "Content-Type: application/json" \
  -d '{"username":"STU001","password":"student123"}'
```

2. **View Profile**
```bash
curl -X GET http://localhost:8000/api/student/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

3. **Get Certificates**
```bash
curl -X GET http://localhost:8000/api/student/certificates \
  -H "Authorization: Bearer YOUR_TOKEN"
```

4. **View Verifications**
```bash
curl -X GET http://localhost:8000/api/student/verifications \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Configuration

### Environment Variables

Add to `.env` file:

```
# Student Module
STUDENT_TOKEN_EXPIRE_HOURS=24
MAX_CERTIFICATES_PER_STUDENT=100
SHARE_LINK_EXPIRY_DAYS=30
```

## Security Checklist

- [x] JWT authentication implemented
- [x] Password hashing (SHA256)
- [x] Role-based access control
- [x] Data isolation (students only see own data)
- [x] Input validation
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] XSS protection
- [x] CORS configuration
- [x] Activity audit logging
- [x] Secure certificate sharing

## Module Features Checklist

- [x] Module 1: View Profile
- [x] Module 2: Manage Profile
- [x] Module 3: View Certificate
- [x] Module 4: Monitor Verification Status
- [x] Module 5: View Blockchain Details
- [x] Module 6: Share Certificate
- [x] Module 7: Submit Feedback
- [x] Dashboard with Statistics
- [x] Secure Authentication
- [x] Activity Logging

## Troubleshooting

### Issue: "Authentication required"
**Solution**: Ensure JWT token is included in Authorization header

### Issue: "Student not found"
**Solution**: Verify student account exists in database

### Issue: "Certificate not found"
**Solution**: Ensure certificate is issued to the logged-in student

### Issue: "Unauthorized access"
**Solution**: Students can only access their own certificates

## Performance Optimization

### Database Indexes
```sql
CREATE INDEX idx_certificates_student ON certificates(student_id);
CREATE INDEX idx_verifications_certificate ON verifications(certificate_id);
CREATE INDEX idx_feedback_student ON feedbacks(verifier_id);
```

### Caching Strategy
- Cache profile data (5 minutes)
- Cache certificate list (2 minutes)
- Cache blockchain data (10 minutes)

## Monitoring

### Key Metrics to Track
- Profile updates per day
- Certificate views per day
- Verification monitoring activity
- Share link generations
- Feedback submissions

### Logging
All student actions are logged in `audit_logs` table:
- Profile updates
- Certificate access
- Verification monitoring
- Share link generation
- Feedback submissions

## Support

For issues or questions:
1. Check documentation
2. Review error logs
3. Test with provided test account
4. Verify database tables exist
5. Ensure all services are running

---

**Integration Complete!** 🎉

The Student Module is now fully integrated with CertiSense AI v3.0.
