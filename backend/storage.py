import json
import os
from datetime import datetime
from typing import Dict, Any

class JSONStorage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    def _get_file_path(self, filename: str) -> str:
        return os.path.join(self.data_dir, f"{filename}.json")
    
    def save(self, filename: str, data: Dict[str, Any]) -> None:
        # Convert datetime objects to strings for JSON serialization
        serializable_data = self._serialize_data(data)
        with open(self._get_file_path(filename), 'w') as f:
            json.dump(serializable_data, f, indent=2, default=str)
    
    def load(self, filename: str) -> Dict[str, Any]:
        file_path = self._get_file_path(filename)
        if not os.path.exists(file_path):
            return {}
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            return self._deserialize_data(data)
    
    def _serialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        serialized = {}
        for key, value in data.items():
            if isinstance(value, dict):
                serialized[key] = self._serialize_dict(value)
            else:
                serialized[key] = value
        return serialized
    
    def _serialize_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        serialized = {}
        for k, v in d.items():
            if isinstance(v, datetime):
                serialized[k] = v.isoformat()
            elif isinstance(v, dict):
                serialized[k] = self._serialize_dict(v)
            else:
                serialized[k] = v
        return serialized
    
    def _deserialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        deserialized = {}
        for key, value in data.items():
            if isinstance(value, dict):
                deserialized[key] = self._deserialize_dict(value)
            else:
                deserialized[key] = value
        return deserialized
    
    def _deserialize_dict(self, d: Dict[str, Any]) -> Dict[str, Any]:
        deserialized = {}
        for k, v in d.items():
            if k == 'created_at' and isinstance(v, str):
                try:
                    deserialized[k] = datetime.fromisoformat(v)
                except:
                    deserialized[k] = datetime.utcnow()
            elif isinstance(v, dict):
                deserialized[k] = self._deserialize_dict(v)
            else:
                deserialized[k] = v
        return deserialized

# Global storage instance
storage = JSONStorage()