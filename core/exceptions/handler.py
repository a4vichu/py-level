from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
import traceback
import sys

class ExceptionHandler(ABC):
    def __init__(self):
        self._handlers: Dict[Type[Exception], Callable] = {}
        
    def register(self, exception: Type[Exception], handler: Callable):
        """Register an exception handler"""
        self._handlers[exception] = handler
        
    def handle(self, exception: Exception) -> Any:
        """Handle an exception"""
        for exception_type, handler in self._handlers.items():
            if isinstance(exception, exception_type):
                return handler(exception)
                
        return self._default_handler(exception)
        
    def _default_handler(self, exception: Exception) -> Any:
        """Handle an unhandled exception"""
        traceback.print_exc()
        return {
            'error': str(exception),
            'traceback': traceback.format_exc()
        }
        
class HttpException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code
        
class NotFoundException(HttpException):
    def __init__(self, message: str = 'Not Found'):
        super().__init__(message, 404)
        
class UnauthorizedException(HttpException):
    def __init__(self, message: str = 'Unauthorized'):
        super().__init__(message, 401)
        
class ForbiddenException(HttpException):
    def __init__(self, message: str = 'Forbidden'):
        super().__init__(message, 403)
        
class ValidationException(HttpException):
    def __init__(self, message: str = 'Validation Failed', errors: Optional[Dict[str, Any]] = None):
        super().__init__(message, 422)
        self.errors = errors or {}
        
class ExceptionServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('exception_handler', ExceptionHandler)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot exception bindings
        pass 