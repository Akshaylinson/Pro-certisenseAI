from typing import Dict
from blockchain_service import BlockchainService

class ChatbotService:
    @staticmethod
    def process_query(message: str, user_role: str, user_id: str) -> Dict:
        """Process chatbot queries"""
        message_lower = message.lower()
        
        # Basic responses
        if "verify" in message_lower:
            return {"response": "To verify a certificate, upload the certificate file in the Verify Certificate section."}
        elif "certificate" in message_lower:
            return {"response": "Certificates are validated using blockchain and AI. Each certificate has a unique hash."}
        elif "blockchain" in message_lower:
            return {"response": "Our blockchain ensures certificate authenticity and prevents tampering."}
        elif "help" in message_lower:
            return {"response": f"As a {user_role}, you can verify certificates, view history, and submit feedback."}
        else:
            return {"response": "I'm here to help with certificate verification. Ask me about verifying certificates or blockchain validation."}