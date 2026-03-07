from sqlalchemy.orm import Session
from database import Verification, Certificate, Verifier
from datetime import datetime, timedelta
from typing import Dict

class VerifierChatbot:
    @staticmethod
    def get_verifier_data(verifier_id: str, db: Session) -> Dict:
        """Fetch verifier-specific data from database"""
        try:
            verifications = db.query(Verification).filter(
                Verification.verifier_id == verifier_id
            ).all()
            
            if not verifications:
                return {
                    'total_verifications': 0,
                    'valid_certificates': 0,
                    'invalid_certificates': 0,
                    'flagged_certificates': 0,
                    'recent_verifications': 0,
                    'certificate_hashes': [],
                    'success_rate': 0
                }
            
            valid_count = sum(1 for v in verifications if v.result == True)
            invalid_count = sum(1 for v in verifications if v.result == False)
            flagged_count = sum(1 for v in verifications if hasattr(v, 'is_suspicious') and v.is_suspicious)
            
            recent_verifications = [v for v in verifications 
                                   if (datetime.utcnow() - v.timestamp).days <= 7]
            
            certificate_hashes = [v.certificate_hash for v in verifications if v.certificate_hash]
            
            return {
                'total_verifications': len(verifications),
                'valid_certificates': valid_count,
                'invalid_certificates': invalid_count,
                'flagged_certificates': flagged_count,
                'recent_verifications': len(recent_verifications),
                'certificate_hashes': certificate_hashes[:10],
                'success_rate': (valid_count / len(verifications) * 100) if verifications else 0
            }
        except Exception as e:
            print(f"Error fetching verifier data: {str(e)}")
            return {
                'total_verifications': 0,
                'valid_certificates': 0,
                'invalid_certificates': 0,
                'flagged_certificates': 0,
                'recent_verifications': 0,
                'certificate_hashes': [],
                'success_rate': 0
            }
    
    @staticmethod
    def process_query(query: str, verifier_id: str, db: Session) -> str:
        """Process chat query with verifier data context"""
        query_lower = query.lower()
        data = VerifierChatbot.get_verifier_data(verifier_id, db)
        
        # Statistics queries
        if any(word in query_lower for word in ['total', 'how many', 'count', 'statistics', 'stats']):
            return f"""📊 Your Verification Statistics:
• Total Verifications: {data['total_verifications']}
• Valid Certificates: {data['valid_certificates']}
• Invalid Certificates: {data['invalid_certificates']}
• Flagged Certificates: {data['flagged_certificates']}
• Success Rate: {data['success_rate']:.1f}%
• Recent (Last 7 days): {data['recent_verifications']}"""
        
        # Valid certificates
        elif any(word in query_lower for word in ['valid', 'verified', 'authentic']):
            return f"""✅ Valid Certificates Information:
You have verified {data['valid_certificates']} valid certificates out of {data['total_verifications']} total verifications.
Success rate: {data['success_rate']:.1f}%

Valid certificates are those that:
• Match blockchain records
• Have correct hash values
• Are not revoked or tampered"""
        
        # Invalid certificates
        elif any(word in query_lower for word in ['invalid', 'fake', 'fraudulent']):
            return f"""❌ Invalid Certificates Information:
You have detected {data['invalid_certificates']} invalid certificates.
Flagged for review: {data['flagged_certificates']}

Invalid certificates may be:
• Not found in blockchain
• Hash mismatch detected
• Tampered or forged documents"""
        
        # Recent activity
        elif any(word in query_lower for word in ['recent', 'latest', 'last', 'today']):
            return f"""📅 Recent Activity (Last 7 days):
• Verifications performed: {data['recent_verifications']}
• Total all-time: {data['total_verifications']}

Your verification activity helps maintain certificate authenticity and trust in the system."""
        
        # Certificate hashes
        elif any(word in query_lower for word in ['hash', 'certificate id', 'certificates']):
            if data['certificate_hashes']:
                hashes = '\n'.join([f"• {h[:16]}..." for h in data['certificate_hashes'][:5]])
                return f"""🔐 Recent Certificate Hashes:\n{hashes}\n\nTotal certificates verified: {data['total_verifications']}"""
            return "No certificates verified yet."
        
        # Help/How to verify
        elif any(word in query_lower for word in ['help', 'how', 'verify', 'process']):
            return """🔍 Certificate Verification Process:

1. Upload Certificate: Go to 'Verify Certificate' section
2. AI Analysis: System analyzes document authenticity
3. Blockchain Check: Verifies hash against blockchain
4. Result: Get detailed verification report

You can ask me about:
• Your verification statistics
• Valid/Invalid certificates
• Recent activity
• Certificate hashes"""
        
        # Default response
        else:
            return f"""👋 Hello! I'm your verification assistant.

📊 Quick Stats:
• Total Verifications: {data['total_verifications']}
• Valid: {data['valid_certificates']} | Invalid: {data['invalid_certificates']}
• Success Rate: {data['success_rate']:.1f}%

Ask me about:
• "Show my statistics"
• "How many valid certificates?"
• "Recent activity"
• "Certificate hashes"
• "How to verify?"""
