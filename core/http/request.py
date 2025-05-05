from typing import Dict, Any, Optional
from core.foundation.application import Application

class Request:
    """HTTP request class"""
    
    _current_request = None
    
    def __init__(self, app: Application, method: str, path: str, headers: Dict[str, str], body: Optional[str] = None):
        self.app = app
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self._previous = None
        
    @classmethod
    def current(cls) -> 'Request':
        """Get the current request instance"""
        return cls._current_request
        
    def set_current(self):
        """Set this request as the current request"""
        self._previous = self._current_request
        self.__class__._current_request = self
        
    def clear_current(self):
        """Clear the current request"""
        self.__class__._current_request = self._previous 