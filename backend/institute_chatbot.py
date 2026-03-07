from sqlalchemy.orm import Session
from database import Student, Certificate, Institute, Verification
from datetime import datetime, timedelta
from typing import Dict

class InstituteChatbot:
    @staticmethod
    def get_institute_data(institute_id: str, db: Session) -> Dict:
        """Fetch institute-specific data from database"""
        try:
            students = db.query(Student).filter(Student.institute_id == institute_id).all()
            certificates = db.query(Certificate).filter(Certificate.institute_id == institute_id).all()
            
            if not students and not certificates:
                return {
                    'total_students': 0,
                    'total_certificates': 0,
                    'active_certificates': 0,
                    'revoked_certificates': 0,
                    'recent_students': 0,
                    'recent_certificates': 0,
                    'total_verifications': 0,
                    'student_names': []
                }
            
            active_certs = sum(1 for c in certificates if c.status.value == 'active')
            revoked_certs = sum(1 for c in certificates if c.status.value == 'revoked')
            
            recent_students = [s for s in students if (datetime.utcnow() - s.created_at).days <= 30]
            recent_certificates = [c for c in certificates if (datetime.utcnow() - c.created_at).days <= 30]
            
            cert_ids = [c.id for c in certificates]
            total_verifications = db.query(Verification).filter(Verification.certificate_id.in_(cert_ids)).count() if cert_ids else 0
            
            student_names = [s.name for s in students[:10]]
            
            return {
                'total_students': len(students),
                'total_certificates': len(certificates),
                'active_certificates': active_certs,
                'revoked_certificates': revoked_certs,
                'recent_students': len(recent_students),
                'recent_certificates': len(recent_certificates),
                'total_verifications': total_verifications,
                'student_names': student_names
            }
        except Exception as e:
            print(f"Error fetching institute data: {str(e)}")
            return {
                'total_students': 0,
                'total_certificates': 0,
                'active_certificates': 0,
                'revoked_certificates': 0,
                'recent_students': 0,
                'recent_certificates': 0,
                'total_verifications': 0,
                'student_names': []
            }
    
    @staticmethod
    def process_query(query: str, institute_id: str, db: Session) -> str:
        """Process chat query with institute data context"""
        query_lower = query.lower()
        data = InstituteChatbot.get_institute_data(institute_id, db)
        
        # Statistics queries
        if any(word in query_lower for word in ['total', 'how many', 'count', 'statistics', 'stats']):
            return f"""📊 Your Institute Statistics:
• Total Students: {data['total_students']}
• Total Certificates: {data['total_certificates']}
• Active Certificates: {data['active_certificates']}
• Revoked Certificates: {data['revoked_certificates']}
• Total Verifications: {data['total_verifications']}
• Recent Students (30 days): {data['recent_students']}
• Recent Certificates (30 days): {data['recent_certificates']}"""
        
        # Students queries
        elif any(word in query_lower for word in ['student', 'enrolled', 'registered']):
            if data['student_names']:
                names = '\n'.join([f"• {name}" for name in data['student_names'][:5]])
                return f"""👨‍🎓 Student Information:
Total Students: {data['total_students']}
Recent Enrollments (30 days): {data['recent_students']}

Recent Students:
{names}
{f"...and {data['total_students'] - 5} more" if data['total_students'] > 5 else ""}"""
            return f"You have {data['total_students']} students enrolled."
        
        # Certificates queries
        elif any(word in query_lower for word in ['certificate', 'issued', 'active']):
            return f"""📜 Certificate Information:
Total Certificates Issued: {data['total_certificates']}
• Active: {data['active_certificates']}
• Revoked: {data['revoked_certificates']}
• Recently Issued (30 days): {data['recent_certificates']}

Total Verifications: {data['total_verifications']}"""
        
        # Recent activity
        elif any(word in query_lower for word in ['recent', 'latest', 'last', 'today']):
            return f"""📅 Recent Activity (Last 30 days):
• New Students: {data['recent_students']}
• Certificates Issued: {data['recent_certificates']}
• Total Students: {data['total_students']}
• Total Certificates: {data['total_certificates']}"""
        
        # Verifications
        elif any(word in query_lower for word in ['verification', 'verified', 'verify']):
            return f"""✅ Verification Information:
Total verifications of your certificates: {data['total_verifications']}
Total certificates issued: {data['total_certificates']}

Your certificates have been verified by employers and organizations."""
        
        # Help
        elif any(word in query_lower for word in ['help', 'how', 'what can']):
            return """🏫 Institute Assistant Help:

I can help you with:
• Student statistics and enrollment
• Certificate issuance information
• Verification tracking
• Recent activity

Try asking:
• "Show my statistics"
• "How many students?"
• "Certificate information"
• "Recent activity"
• "Verification count" """
        
        # Default response
        else:
            return f"""👋 Hello! I'm your institute assistant.

📊 Quick Overview:
• Students: {data['total_students']}
• Certificates: {data['total_certificates']}
• Verifications: {data['total_verifications']}

Ask me about:
• "Show statistics"
• "Student information"
• "Certificate details"
• "Recent activity" """
