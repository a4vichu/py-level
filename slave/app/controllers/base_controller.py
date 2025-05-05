from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class BaseController(ABC):
    """Base controller class for all controllers"""
    
    def __init__(self):
        self.request: Optional[Dict[str, Any]] = None
        self.response: Dict[str, Any] = {
            'status': 'success',
            'data': None,
            'error': None
        }
        
    def set_request(self, request: Dict[str, Any]):
        """Set the current request"""
        self.request = request
        
    def get_request(self) -> Optional[Dict[str, Any]]:
        """Get the current request"""
        return self.request
        
    def set_response(self, data: Any = None, error: Optional[str] = None):
        """Set the response data"""
        if error:
            self.response['status'] = 'error'
            self.response['error'] = error
            self.response['data'] = None
        else:
            self.response['status'] = 'success'
            self.response['data'] = data
            self.response['error'] = None
            
    def get_response(self) -> Dict[str, Any]:
        """Get the current response"""
        return self.response
        
    def success(self, data: Any = None) -> Dict[str, Any]:
        """Return a success response"""
        self.set_response(data)
        return self.get_response()
        
    def error(self, message: str) -> Dict[str, Any]:
        """Return an error response"""
        self.set_response(error=message)
        return self.get_response()
        
    @abstractmethod
    async def handle(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the request"""
        pass
        
    def validate(self, rules: Dict[str, Any]) -> bool:
        """Validate request data against rules"""
        if not self.request:
            return False
            
        for field, rule in rules.items():
            # Check required fields
            if rule.get('required', False) and field not in self.request:
                self.error(f"Field '{field}' is required")
                return False
                
            # Check field type
            if field in self.request:
                value = self.request[field]
                expected_type = rule.get('type')
                if expected_type and not isinstance(value, expected_type):
                    self.error(f"Field '{field}' must be of type {expected_type.__name__}")
                    return False
                    
                # Check minimum length
                min_length = rule.get('min_length')
                if min_length and len(str(value)) < min_length:
                    self.error(f"Field '{field}' must be at least {min_length} characters long")
                    return False
                    
                # Check maximum length
                max_length = rule.get('max_length')
                if max_length and len(str(value)) > max_length:
                    self.error(f"Field '{field}' must be at most {max_length} characters long")
                    return False
                    
        return True 