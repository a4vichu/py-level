from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
import json

class Controller(ABC):
    def __init__(self):
        self._middleware = []
        
    def middleware(self, middleware: Any):
        """Register middleware for the controller"""
        self._middleware.append(middleware)
        return self
        
    def json(self, data: Any, status: int = 200) -> Dict[str, Any]:
        """Return a JSON response"""
        return {
            'status': status,
            'data': data
        }
        
    def success(self, data: Any = None, message: str = 'Success') -> Dict[str, Any]:
        """Return a success response"""
        return self.json({
            'success': True,
            'message': message,
            'data': data
        })
        
    def error(self, message: str, status: int = 400, data: Any = None) -> Dict[str, Any]:
        """Return an error response"""
        return self.json({
            'success': False,
            'message': message,
            'data': data
        }, status)
        
    def not_found(self, message: str = 'Resource not found') -> Dict[str, Any]:
        """Return a not found response"""
        return self.error(message, 404)
        
    def unauthorized(self, message: str = 'Unauthorized') -> Dict[str, Any]:
        """Return an unauthorized response"""
        return self.error(message, 401)
        
    def forbidden(self, message: str = 'Forbidden') -> Dict[str, Any]:
        """Return a forbidden response"""
        return self.error(message, 403)
        
    def validate(self, data: Dict[str, Any], rules: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate request data"""
        errors = {}
        
        for field, rule in rules.items():
            if field not in data and 'required' in rule:
                errors[field] = f"{field} is required"
            elif field in data:
                value = data[field]
                
                if 'type' in rule:
                    if rule['type'] == 'string' and not isinstance(value, str):
                        errors[field] = f"{field} must be a string"
                    elif rule['type'] == 'integer' and not isinstance(value, int):
                        errors[field] = f"{field} must be an integer"
                    elif rule['type'] == 'float' and not isinstance(value, float):
                        errors[field] = f"{field} must be a float"
                    elif rule['type'] == 'boolean' and not isinstance(value, bool):
                        errors[field] = f"{field} must be a boolean"
                        
                if 'min' in rule and value < rule['min']:
                    errors[field] = f"{field} must be at least {rule['min']}"
                    
                if 'max' in rule and value > rule['max']:
                    errors[field] = f"{field} must be at most {rule['max']}"
                    
                if 'in' in rule and value not in rule['in']:
                    errors[field] = f"{field} must be one of {rule['in']}"
                    
        if errors:
            return self.error('Validation failed', 422, errors)
        return None 