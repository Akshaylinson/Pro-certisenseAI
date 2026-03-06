from typing import Dict
from blockchain_service import BlockchainService
from auth import verifiers_db
from qwen_chatbot import QwenChatbotService

class ChatbotService:
    def __init__(self):
        self.qwen_bot = QwenChatbotService()
    
    @staticmethod
    def process_query(message: str, user_role: str, user_id: str) -> Dict:
        """Process chatbot queries using Qwen model"""
        
        # Initialize Qwen chatbot
        qwen_bot = QwenChatbotService()
        
        # Process with Qwen model
        response = qwen_bot.process_command(message, user_role)
        
        # Add system context if regular chat
        if 'response' in response and not message.startswith('/'):
            context = ChatbotService._gather_context(user_role, user_id)
            response = ChatbotService._enhance_with_real_data(response, message, user_role)
        
        return response
    
    @staticmethod
    def _gather_context(user_role: str, user_id: str) -> Dict:
        """Gather contextual information for better responses"""
        context = {
            'user_role': user_role,
            'user_id': user_id,
            'timestamp': None
        }
        
        try:
            # Get blockchain statistics
            registry = BlockchainService.get_all_certificates()
            context['total_certificates'] = len(registry)
            
            # Get verifier count
            context['total_verifiers'] = len(verifiers_db)
            
            # Get latest certificate info
            if registry:
                latest = max(registry.values(), key=lambda x: x.get('timestamp', ''))
                context['latest_certificate'] = latest
            
        except Exception as e:
            context['error'] = str(e)
        
        return context
    
    @staticmethod
    def _enhance_with_real_data(ai_response: Dict, message: str, user_role: str) -> Dict:
        """Enhance AI response with real-time system data"""
        message_lower = message.lower()
        
        # Handle statistics queries with real data
        if any(keyword in message_lower for keyword in ['count', 'number', 'statistics', 'how many']):
            try:
                registry = BlockchainService.get_all_certificates()
                verifier_count = len(verifiers_db)
                
                if 'certificate' in message_lower:
                    ai_response['response'] = f"There are currently {len(registry)} certificates registered on the blockchain. {ai_response['response']}"
                    ai_response['data'] = {'certificate_count': len(registry)}
                
                elif 'verifier' in message_lower:
                    ai_response['response'] = f"There are {verifier_count} registered verifiers in the system. {ai_response['response']}"
                    ai_response['data'] = {'verifier_count': verifier_count}
                
                else:
                    ai_response['response'] = f"System Statistics: {len(registry)} certificates, {verifier_count} verifiers. {ai_response['response']}"
                    ai_response['data'] = {
                        'certificate_count': len(registry),
                        'verifier_count': verifier_count
                    }
            
            except Exception as e:
                ai_response['response'] += f" (Note: Unable to fetch real-time statistics: {str(e)})"
        
        # Handle latest/recent queries
        elif any(keyword in message_lower for keyword in ['latest', 'recent', 'last']):
            try:
                registry = BlockchainService.get_all_certificates()
                if registry:
                    latest = max(registry.values(), key=lambda x: x.get('timestamp', ''))
                    ai_response['response'] = f"Latest certificate: Registered on {latest.get('timestamp', 'unknown')} by {latest.get('issuer_id', 'unknown')}. {ai_response['response']}"
                    ai_response['data'] = {'latest_certificate': latest}
                else:
                    ai_response['response'] = f"No certificates have been registered yet. {ai_response['response']}"
            
            except Exception as e:
                ai_response['response'] += f" (Note: Unable to fetch latest certificate info: {str(e)})"
        
        # Add role-specific enhancements
        if user_role == 'admin':
            ai_response['admin_actions'] = [
                "Manage Verifiers",
                "View Reports",
                "Handle Feedback",
                "Certificate Management"
            ]
        else:
            ai_response['verifier_actions'] = [
                "Verify Certificate",
                "Submit Feedback",
                "View History"
            ]
        
        return ai_response
    
    @staticmethod
    def get_system_status() -> Dict:
        """Get comprehensive system status for AI responses"""
        try:
            registry = BlockchainService.get_all_certificates()
            return {
                'status': 'operational',
                'certificates': len(registry),
                'verifiers': len(verifiers_db),
                'blockchain_connected': True,
                'ai_model_loaded': True
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'blockchain_connected': False,
                'ai_model_loaded': True
            }