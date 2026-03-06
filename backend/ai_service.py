from typing import Dict, Optional
from app.ai.enhanced_model import CertificateAIModel

class AIValidationService:
    def __init__(self):
        self.ai_model = CertificateAIModel()
    
    @staticmethod
    def validate_certificate_content(file_content: bytes, filename: str) -> Dict:
        """AI-based certificate content validation using enhanced model"""
        
        # Initialize AI model
        ai_model = CertificateAIModel()
        
        # Use enhanced AI analysis
        analysis = ai_model.analyze_certificate_content(file_content, filename)
        
        # Format response for compatibility
        return {
            "valid": analysis['valid'],
            "confidence": analysis['confidence_score'],
            "format_valid": filename.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')),
            "keywords_found": len(analysis['features_detected']) > 0,
            "ai_score": analysis['confidence_score'],
            "reason": "Certificate validated successfully" if analysis['valid'] else "Certificate validation failed",
            "validation_token": analysis['validation_token'],
            "issues": analysis['issues'],
            "features_detected": analysis['features_detected'],
            "detailed_analysis": analysis
        }
    
    @staticmethod
    def explain_verification_result(verification_result: bool, blockchain_data: Optional[Dict]) -> str:
        """Generate AI explanation for verification result"""
        if verification_result and blockchain_data:
            issuer = blockchain_data.get('issuer_id', 'Unknown')
            timestamp = blockchain_data.get('timestamp', 'Unknown date')
            return f"✅ Certificate verified successfully! This certificate was issued by {issuer} on {timestamp}. The blockchain hash matches and AI validation confirms authenticity."
        
        elif not verification_result and blockchain_data is None:
            return "❌ Certificate verification failed. This certificate's hash was not found in the blockchain registry, indicating it may be invalid, forged, or not properly registered."
        
        elif not verification_result:
            return "⚠️ Certificate verification inconclusive. While some data was found, the verification process could not confirm authenticity. Please contact the issuing institution for clarification."
        
        else:
            return "🔍 Verification process completed with mixed results. Please review the detailed analysis and contact support if needed."
    
    @staticmethod
    def analyze_certificate_quality(file_content: bytes, filename: str) -> Dict:
        """Analyze certificate quality and provide recommendations"""
        ai_model = CertificateAIModel()
        analysis = ai_model.analyze_certificate_content(file_content, filename)
        
        recommendations = []
        quality_score = analysis['confidence_score']
        
        if quality_score < 0.3:
            recommendations.append("Consider re-uploading with higher quality scan")
            recommendations.append("Ensure all text is clearly visible")
        elif quality_score < 0.6:
            recommendations.append("Certificate quality is acceptable but could be improved")
        else:
            recommendations.append("Certificate quality is excellent")
        
        return {
            "quality_score": quality_score,
            "recommendations": recommendations,
            "analysis": analysis
        }
    
    @staticmethod
    def get_validation_insights(validation_history: list) -> Dict:
        """Provide insights based on validation history"""
        if not validation_history:
            return {"message": "No validation history available"}
        
        total_validations = len(validation_history)
        successful_validations = sum(1 for v in validation_history if v.get('valid', False))
        success_rate = successful_validations / total_validations if total_validations > 0 else 0
        
        insights = {
            "total_validations": total_validations,
            "successful_validations": successful_validations,
            "success_rate": success_rate,
            "insights": []
        }
        
        if success_rate > 0.8:
            insights["insights"].append("High success rate indicates good certificate quality")
        elif success_rate < 0.5:
            insights["insights"].append("Low success rate - consider improving certificate quality")
        
        return insights