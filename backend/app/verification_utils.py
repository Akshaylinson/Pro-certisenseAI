def get_verification_message(content_valid: bool, blockchain_result: dict) -> str:
    """Generate verification message based on checks"""
    if not content_valid:
        return "Invalid certificate format or content"
    elif not blockchain_result.get("exists"):
        return "Certificate not found on blockchain registry"
    elif not blockchain_result.get("valid"):
        return "Certificate has been revoked"
    else:
        issuer = blockchain_result.get("issuer", "Unknown")
        return f"Certificate verified successfully - Issued by {issuer}"