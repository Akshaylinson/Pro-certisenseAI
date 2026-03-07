import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from database import Institute, Student, Certificate, Verifier, Verification, Feedback, CertificateStatusEnum, VerificationStatusEnum

class AIQueryService:
    def __init__(self):
        self.session_contexts = {}  # Store conversation context
    
    def detect_intent(self, query: str) -> str:
        """Detect user intent from query"""
        query_lower = query.lower()
        
        # Count queries - more flexible matching
        if any(word in query_lower for word in ["institute", "institution", "school", "college", "university"]) and any(word in query_lower for word in ["how many", "total", "number", "count", "show me"]):
            return "count_institutes"
        if any(word in query_lower for word in ["student", "students", "learner", "learners"]) and any(word in query_lower for word in ["how many", "total", "number", "count", "show me"]):
            return "count_students"
        if any(word in query_lower for word in ["certificate", "certificates", "cert", "certs"]) and any(word in query_lower for word in ["how many", "total", "number", "count", "show me"]):
            return "count_certificates"
        if any(word in query_lower for word in ["verifier", "verifiers", "validator", "validators"]) and any(word in query_lower for word in ["how many", "total", "number", "count", "show me"]):
            return "count_verifiers"
        if any(word in query_lower for word in ["verification", "verifications", "validation", "validations"]) and any(word in query_lower for word in ["how many", "total", "number", "count", "show me"]):
            return "count_verifications"
        
        # Student details - more flexible patterns
        if any(word in query_lower for word in ["student", "learner"]) and (any(id_part in query_lower for id_part in ['inst', '-']) or any(word in query_lower for word in ["details", "info", "information", "about"])):
            return "student_details"
        
        # Institute performance
        if any(word in query_lower for word in ["institute", "institution", "school"]) and any(word in query_lower for word in ["most", "highest", "top", "best", "leading"]):
            return "top_institute"
        
        # Verifier list
        if any(word in query_lower for word in ["verifier", "validator"]) and any(word in query_lower for word in ["list", "show", "display", "who are"]):
            return "list_verifiers"
        
        # Certificate check - more flexible
        if any(word in query_lower for word in ["certificate", "cert"]) and ("cert-" in query_lower or any(word in query_lower for word in ["check", "details", "info", "status", "about"])):
            return "certificate_details"
        
        # History queries
        if any(word in query_lower for word in ["history", "past", "previous", "recent"]):
            return "verification_history"
        
        # Today's activities - more patterns
        if any(word in query_lower for word in ["today", "today's", "daily", "current day"]):
            return "today_activity"
        
        # Help and general queries
        if any(word in query_lower for word in ["help", "what can you do", "features", "capabilities", "assist"]):
            return "help"
        
        # Statistics and analytics
        if any(word in query_lower for word in ["statistics", "stats", "analytics", "data", "overview", "summary"]):
            return "general_stats"
        
        return "general"
    
    def execute_database_query(self, intent: str, query: str, db: Session, user_id: str = None, role: str = None) -> Dict[str, Any]:
        """Execute database queries based on detected intent"""
        data = {}
        
        try:
            if intent == "count_institutes":
                data['total_institutes'] = db.query(Institute).count()
                
            elif intent == "count_students":
                if role == "INSTITUTE":
                    data['student_count'] = db.query(Student).filter(Student.institute_id == user_id).count()
                else:
                    data['total_students'] = db.query(Student).count()
                    
            elif intent == "count_certificates":
                if role == "INSTITUTE":
                    data['certificate_count'] = db.query(Certificate).filter(Certificate.institute_id == user_id).count()
                else:
                    data['total_certificates'] = db.query(Certificate).count()
                    
            elif intent == "count_verifiers":
                data['total_verifiers'] = db.query(Verifier).count()
                
            elif intent == "count_verifications":
                if role == "VERIFIER":
                    data['verification_count'] = db.query(Verification).filter(Verification.verifier_id == user_id).count()
                else:
                    data['total_verifications'] = db.query(Verification).count()
                    
            elif intent == "student_details":
                # Extract student ID from query
                words = query.split()
                for word in words:
                    if 'INST' in word.upper() and '-' in word:
                        student_query = db.query(Student).filter(Student.student_id == word.upper())
                        if role == "INSTITUTE":
                            student_query = student_query.filter(Student.institute_id == user_id)
                        student = student_query.first()
                        if student:
                            institute = db.query(Institute).filter(Institute.id == student.institute_id).first()
                            data['student_details'] = {
                                'student_id': student.student_id,
                                'name': student.name,
                                'email': student.email,
                                'institute': institute.name if institute else 'Unknown',
                                'program': student.program
                            }
                        break
                        
            elif intent == "top_institute":
                if role == "ADMIN":
                    top_institute = db.query(
                        Institute.name,
                        func.count(Certificate.id).label('cert_count')
                    ).join(Certificate).group_by(Institute.id).order_by(desc('cert_count')).first()
                    
                    if top_institute:
                        data['top_institute'] = {
                            'name': top_institute[0],
                            'certificate_count': top_institute[1]
                        }
                        
            elif intent == "list_verifiers":
                if role == "ADMIN":
                    verifiers = db.query(Verifier).limit(10).all()
                    data['verifiers'] = [
                        {
                            'username': v.username,
                            'company': v.company_name,
                            'verification_count': v.verification_count or 0
                        }
                        for v in verifiers
                    ]
                    
            elif intent == "certificate_details":
                words = query.split()
                for word in words:
                    if 'CERT-' in word.upper():
                        cert = db.query(Certificate).filter(Certificate.id == word.upper()).first()
                        if cert:
                            data['certificate_status'] = {
                                'certificate_id': cert.id,
                                'name': cert.name,
                                'status': cert.status.value,
                                'verification_count': cert.verification_count or 0
                            }
                        break
                        
            elif intent == "verification_history":
                if role == "VERIFIER":
                    verifications = db.query(Verification).filter(
                        Verification.verifier_id == user_id
                    ).order_by(desc(Verification.timestamp)).limit(5).all()
                    
                    data['recent_verifications'] = [
                        {
                            'certificate_hash': v.certificate_hash[:16] + '...',
                            'result': 'Valid' if v.result else 'Invalid',
                            'timestamp': v.timestamp.strftime('%Y-%m-%d %H:%M')
                        }
                        for v in verifications
                    ]
                    
            elif intent == "today_activity":
                today = datetime.utcnow().date()
                if role == "INSTITUTE":
                    data['certificates_today'] = db.query(Certificate).filter(
                        Certificate.institute_id == user_id,
                        func.date(Certificate.created_at) == today
                    ).count()
                else:
                    data['certificates_today'] = db.query(Certificate).filter(
                        func.date(Certificate.created_at) == today
                    ).count()
                    
            elif intent == "help":
                data['help_requested'] = True
                
            elif intent == "general_stats":
                if role == "ADMIN":
                    data['total_institutes'] = db.query(Institute).count()
                    data['total_students'] = db.query(Student).count()
                    data['total_certificates'] = db.query(Certificate).count()
                    data['total_verifiers'] = db.query(Verifier).count()
                    data['total_verifications'] = db.query(Verification).count()
                elif role == "INSTITUTE":
                    data['student_count'] = db.query(Student).filter(Student.institute_id == user_id).count()
                    data['certificate_count'] = db.query(Certificate).filter(Certificate.institute_id == user_id).count()
                elif role == "VERIFIER":
                    data['verification_count'] = db.query(Verification).filter(Verification.verifier_id == user_id).count()
                    
        except Exception as e:
            print(f"Database query error: {str(e)}")
            data['error'] = str(e)
            
        return data
    
    def process_admin_query(self, query: str, db: Session, session_id: str = None) -> str:
        """Process admin queries with full database access"""
        try:
            print(f"AI Query: {query}")
            
            # Step 1: Detect intent
            intent = self.detect_intent(query)
            print(f"Detected intent: {intent}")
            
            # Step 2: Execute database query
            data = self.execute_database_query(intent, query, db, None, "ADMIN")
            print(f"DB result: {data}")
            
            # Step 3: Generate AI response with structured context
            response = self._generate_ai_response_with_data(query, data, "ADMIN", intent, session_id)
            return response
        except Exception as e:
            print(f"Error in admin query: {str(e)}")
            return f"I apologize, but I encountered an error processing your request: {str(e)}"
    
    def process_institute_query(self, query: str, db: Session, institute_id: str, session_id: str = None) -> str:
        """Process institute queries with restricted access"""
        try:
            print(f"AI Query: {query}")
            
            # Step 1: Detect intent
            intent = self.detect_intent(query)
            print(f"Detected intent: {intent}")
            
            # Step 2: Execute database query
            data = self.execute_database_query(intent, query, db, institute_id, "INSTITUTE")
            print(f"DB result: {data}")
            
            # Step 3: Generate AI response with structured context
            response = self._generate_ai_response_with_data(query, data, "INSTITUTE", intent, session_id)
            return response
        except Exception as e:
            print(f"Error in institute query: {str(e)}")
            return f"I apologize, but I encountered an error processing your request: {str(e)}"
    
    def process_verifier_query(self, query: str, db: Session, verifier_id: str, session_id: str = None) -> str:
        """Process verifier queries with restricted access"""
        try:
            print(f"AI Query: {query}")
            
            # Step 1: Detect intent
            intent = self.detect_intent(query)
            print(f"Detected intent: {intent}")
            
            # Step 2: Execute database query
            data = self.execute_database_query(intent, query, db, verifier_id, "VERIFIER")
            print(f"DB result: {data}")
            
            # Step 3: Generate AI response with structured context
            response = self._generate_ai_response_with_data(query, data, "VERIFIER", intent, session_id)
            return response
        except Exception as e:
            print(f"Error in verifier query: {str(e)}")
            return f"I apologize, but I encountered an error processing your request: {str(e)}"
    
    def _generate_ai_response_with_data(self, query: str, data: Dict[str, Any], role: str, intent: str, session_id: str = None) -> str:
        """Generate AI response using structured database data"""
        
        # If no data found, return appropriate message
        if not data or 'error' in data:
            return "I do not have data available for that query."
        
        # Always use direct response for better accuracy and database integration
        return self._generate_direct_response(query, data, intent)
    
    def _generate_direct_response(self, query: str, data: Dict[str, Any], intent: str) -> str:
        """Generate direct response from database data without LLM"""
        
        # Direct responses based on intent and data
        if intent == "count_institutes" and 'total_institutes' in data:
            count = data['total_institutes']
            return f"There are currently {count} institutes registered in the system. {'This includes all educational institutions that can issue certificates.' if count > 0 else 'No institutes are currently registered.'}"
            
        elif intent == "count_students":
            if 'student_count' in data:
                count = data['student_count']
                return f"Your institute has {count} students registered. {'You can manage students and issue certificates to them from the Students section.' if count > 0 else 'You can add students using the Add Student feature.'}"
            elif 'total_students' in data:
                count = data['total_students']
                return f"There are currently {count} students registered across all institutes in the system. {'Students can receive and track their certificates through their dashboard.' if count > 0 else 'No students are currently registered.'}"
                
        elif intent == "count_certificates":
            if 'certificate_count' in data:
                count = data['certificate_count']
                return f"Your institute has issued {count} certificates. {'Each certificate is secured with blockchain technology and can be verified by employers.' if count > 0 else 'You can start issuing certificates to your students from the Certificates section.'}"
            elif 'total_certificates' in data:
                count = data['total_certificates']
                return f"There are currently {count} certificates stored in the system. {'All certificates are protected by blockchain and AI validation.' if count > 0 else 'No certificates have been issued yet.'}"
                
        elif intent == "count_verifiers" and 'total_verifiers' in data:
            count = data['total_verifiers']
            return f"There are currently {count} verifiers registered in the system. {'Verifiers can authenticate certificates and provide feedback on the verification process.' if count > 0 else 'No verifiers are currently registered.'}"
            
        elif intent == "count_verifications":
            if 'verification_count' in data:
                count = data['verification_count']
                return f"You have performed {count} verifications. {'Your verification history shows your activity in validating certificates.' if count > 0 else 'You can start verifying certificates by uploading them in the Verify section.'}"
            elif 'total_verifications' in data:
                count = data['total_verifications']
                return f"There have been {count} verifications performed in the system. {'This shows the level of certificate validation activity.' if count > 0 else 'No verifications have been performed yet.'}"
                
        elif intent == "student_details" and 'student_details' in data:
            details = data['student_details']
            return f"Student Information:\n• ID: {details['student_id']}\n• Name: {details['name']}\n• Email: {details['email']}\n• Institute: {details['institute']}\n• Program: {details.get('program', 'Not specified')}\n\nThis student can receive certificates and track their verification status."
            
        elif intent == "top_institute" and 'top_institute' in data:
            top = data['top_institute']
            return f"Top Performing Institute: {top['name']}\n\nThey have issued {top['certificate_count']} certificates, making them the most active institute in the system. This demonstrates their commitment to digital certification."
            
        elif intent == "list_verifiers" and 'verifiers' in data:
            verifiers = data['verifiers']
            if verifiers:
                response = f"Registered Verifiers ({len(verifiers)}):" + "\n\n"
                for i, v in enumerate(verifiers, 1):
                    response += f"{i}. {v['username']} ({v['company']}) - {v['verification_count']} verifications\n"
                response += "\nVerifiers help maintain certificate authenticity by validating documents."
                return response
            else:
                return "No verifiers are currently registered in the system. Verifiers can register to help validate certificates."
                
        elif intent == "certificate_details" and 'certificate_status' in data:
            cert = data['certificate_status']
            return f"Certificate Details:\n\n• ID: {cert['certificate_id']}\n• Name: {cert['name']}\n• Status: {cert['status']}\n• Verifications: {cert['verification_count']}\n\nThis certificate is secured on the blockchain and can be verified by employers."
            
        elif intent == "verification_history" and 'recent_verifications' in data:
            verifs = data['recent_verifications']
            if verifs:
                response = f"Your Recent Verifications ({len(verifs)}):" + "\n\n"
                for i, v in enumerate(verifs, 1):
                    status_emoji = "[VALID]" if v['result'] == 'Valid' else "[INVALID]"
                    response += f"{i}. {status_emoji} {v['certificate_hash']} - {v['result']} ({v['timestamp']})\n"
                response += "\nYour verification history helps track your validation activity."
                return response
            else:
                return "You haven't performed any verifications yet. Upload a certificate to start verifying documents."
                
        elif intent == "today_activity" and 'certificates_today' in data:
            count = data['certificates_today']
            return f"Today's Activity: {count} certificates were issued today. {'Great progress in digital certification!' if count > 0 else 'No certificates issued today yet.'}"
        
        elif intent == "help" and 'help_requested' in data:
            return "I can help you with:\n• System statistics (institutes, students, certificates)\n• Student and certificate details\n• Verification history\n• Today's activities\n• Institute performance data\n\nJust ask me questions like 'How many students?' or 'Show me certificate details'."
        
        elif intent == "general_stats":
            if 'total_institutes' in data:  # Admin stats
                return f"System Overview:\n\n• Institutes: {data['total_institutes']}\n• Students: {data['total_students']}\n• Certificates: {data['total_certificates']}\n• Verifiers: {data['total_verifiers']}\n• Verifications: {data['total_verifications']}\n\nThe system is actively managing digital certificates with blockchain security."
            elif 'student_count' in data:  # Institute stats
                return f"Your Institute Statistics:\n\n• Students: {data['student_count']}\n• Certificates Issued: {data['certificate_count']}\n\nYou can manage students and issue certificates from your dashboard."
            elif 'verification_count' in data:  # Verifier stats
                return f"Your Verification Statistics:\n\n• Total Verifications: {data['verification_count']}\n\nYou help maintain certificate authenticity through verification."
        
        # Enhanced general responses for common queries
        query_lower = query.lower()
        if any(word in query_lower for word in ['help', 'what can you do', 'features']):
            return "I can help you with:\n• System statistics (institutes, students, certificates)\n• Student and certificate details\n• Verification history\n• Today's activities\n• Institute performance data\n\nJust ask me questions like 'How many students?' or 'Show me certificate details'."
        
        # Default response when no specific data found
        return "I don't have specific data for that query. Try asking about:\n• Total number of institutes/students/certificates\n• Student details (use student ID)\n• Certificate information\n• Verification statistics\n• Today's activities"