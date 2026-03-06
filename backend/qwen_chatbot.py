import os
import csv
import requests
from typing import Dict, List
import json

class QwenChatbotService:
    def __init__(self):
        self.csv_data = self._load_csv_data()
    
    def _load_csv_data(self) -> List[Dict]:
        """Load CSV data for image generation"""
        csv_path = "backend/models/chatbot_data.csv"
        data = []
        try:
            with open(csv_path, 'r') as file:
                reader = csv.DictReader(file)
                data = list(reader)
        except FileNotFoundError:
            data = []
        return data
    
    def chat(self, message: str, user_role: str) -> Dict:
        """Enhanced rule-based chat with CSV data lookup"""
        message_lower = message.lower()
        
        # Search CSV data for relevant responses
        for item in self.csv_data:
            keywords = item.get('keywords', '').lower().split()
            if any(keyword in message_lower for keyword in keywords):
                response_template = item.get('response_template', item.get('description', ''))
                return {
                    "response": response_template,
                    "model": "csv-enhanced",
                    "role_context": user_role,
                    "matched_item": item['name']
                }
        
        # Fallback responses
        if any(word in message_lower for word in ['verify', 'certificate', 'validation']):
            return {
                "response": "Certificate verification involves: 1) Upload file 2) Generate SHA256 hash 3) Check blockchain registry 4) AI content analysis 5) Return results",
                "model": "rule-based",
                "role_context": user_role
            }
        
        elif any(word in message_lower for word in ['blockchain', 'hash', 'immutable']):
            return {
                "response": "Blockchain provides immutable storage where each certificate hash is permanently recorded and cannot be altered or deleted",
                "model": "rule-based",
                "role_context": user_role
            }
        
        elif user_role == 'admin' and any(word in message_lower for word in ['manage', 'verifier', 'report']):
            return {
                "response": "Admin dashboard allows universities to manage verifiers, add certificates, generate reports, and view feedback. Use the dashboard navigation.",
                "model": "rule-based",
                "role_context": user_role
            }
        
        else:
            return {
                "response": "I'm CertiSense AI assistant. I can help with certificate verification, blockchain queries, and system guidance. Try asking about: verification process, blockchain security, AI validation, or system features.",
                "model": "rule-based",
                "role_context": user_role
            }
    
    def web_scrape(self, url: str) -> Dict:
        """Basic web scraping for certificate-related information"""
        try:
            headers = {'User-Agent': 'CertiSense-Bot/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text[:1000]  # Limit content
                return {
                    "success": True,
                    "content": content,
                    "url": url,
                    "status": response.status_code
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "url": url
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    def generate_image_from_csv(self, item_name: str) -> Dict:
        """Generate simple text response from CSV data"""
        item = next((row for row in self.csv_data if row['name'] == item_name), None)
        
        if not item:
            return {"success": False, "error": "Item not found in CSV"}
        
        return {
            "success": True,
            "text_visualization": f"📊 {item['name'].replace('_', ' ').title()}\n\n📝 {item['description']}\n\n🎨 Visualization: {item['image_prompt']}",
            "item": item
        }
    
    def process_command(self, message: str, user_role: str) -> Dict:
        """Process special commands"""
        message_lower = message.lower()
        
        # Web scraping command
        if message_lower.startswith('/scrape '):
            url = message[8:].strip()
            return self.web_scrape(url)
        
        # Image generation command
        elif message_lower.startswith('/image '):
            item_name = message[7:].strip()
            return self.generate_image_from_csv(item_name)
        
        # List CSV items command
        elif message_lower == '/list':
            items = [f"{row['name']} - {row['description']}" for row in self.csv_data]
            return {
                "response": f"Available knowledge items ({len(items)}): \n" + "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)]),
                "items": [row['name'] for row in self.csv_data]
            }
        
        # Regular chat
        else:
            return self.chat(message, user_role)