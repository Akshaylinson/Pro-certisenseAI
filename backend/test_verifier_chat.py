import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from verifier_chatbot import VerifierChatbot
from database import SessionLocal

# Test the chatbot
db = SessionLocal()
try:
    # Test with a dummy verifier ID
    response = VerifierChatbot.process_query("Show my statistics", "test-verifier-id", db)
    print("Response:", response)
except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()
finally:
    db.close()
