from typing import Any, Dict, Optional, List
from abc import ABC, abstractmethod
import json
from core.http import Request

class Controller(ABC):
    """Base controller class"""
    
    def __init__(self):
        self._middleware = []
        self.request: Request = None
        
    def middleware(self, middleware: Any):
        """Add middleware to the controller"""
        self._middleware.append(middleware)
        return self
        
    def json(self, data: Any, status: int = 200) -> Dict[str, Any]:
        """Return a JSON response"""
        return {
            'status': status,
            'data': data
        }
        
    def success(self, data: Any = None, message: str = None, status: int = 200) -> Dict[str, Any]:
        """Return a success response"""
        response = {
            'status': 'success',
            'data': data
        }
        if message:
            response['message'] = message
        return response
        
    def error(self, message: str, status: int = 400, errors: List[str] = None) -> Dict[str, Any]:
        """Return an error response"""
        response = {
            'status': 'error',
            'message': message
        }
        if errors:
            response['errors'] = errors
        return response
        
    def not_found(self, message: str = 'Resource not found') -> Dict[str, Any]:
        """Return a not found response"""
        return self.error(message, 404)
        
    def unauthorized(self, message: str = 'Unauthorized') -> Dict[str, Any]:
        """Return an unauthorized response"""
        return self.error(message, 401)
        
    def forbidden(self, message: str = 'Forbidden') -> Dict[str, Any]:
        """Return a forbidden response"""
        return self.error(message, 403)
        
    def validate(self, data: Dict[str, Any], rules: Dict[str, Any]) -> List[str]:
        """Validate request data against rules"""
        errors = []
        for field, rule in rules.items():
            if field not in data:
                errors.append(f"{field} is required")
            elif not rule(data[field]):
                errors.append(f"{field} is invalid")
        return errors

    def __call__(self, request: Request, **kwargs) -> Any:
        """Handle the request and execute the controller method"""
        self.request = request
        method_name = request.method.lower()
        
        # Get the method to call
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(**kwargs)
            
        # If no method found, try to get the action from the route
        action = getattr(self, request.path.split('/')[-1], None)
        if action:
            return action(**kwargs)
            
        raise AttributeError(f"Method {method_name} not found in {self.__class__.__name__}") 