import http.server
import socketserver
import json
import urllib.parse
from io import BytesIO
import hashlib

# Simple in-memory storage
registered_certificates = {}

class CertificateHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        
        if self.path == '/':
            response = {"message": "Certificate Verifier API - Working"}
        elif self.path == '/test':
            response = {"status": "API is working", "endpoints": ["/", "/test", "/status"]}
        elif self.path == '/status':
            response = {
                "message": "Certificate Verifier API - Ready",
                "registered_certificates": len(registered_certificates),
                "certificates": registered_certificates
            }
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"detail": "Not Found"}')
            return
            
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers()
        
        if self.path == '/register':
            # Simple mock registration
            response = {
                "registered": True,
                "hash": "mock_hash_123",
                "filename": "test.pdf",
                "message": "Certificate registered successfully"
            }
            registered_certificates["mock_hash_123"] = {"issuer": "Test University"}
            
        elif self.path == '/verify':
            # Simple mock verification
            response = {
                "status": "verified",
                "filename": "test.pdf",
                "hash": "mock_hash_123",
                "message": "Certificate verified successfully",
                "authentic": True,
                "blockchain_data": {"exists": True}
            }
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"detail": "Not Found"}')
            return
            
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), CertificateHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()