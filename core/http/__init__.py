"""
HTTP module with Controller, Request, and Response classes
"""

from typing import Dict, Any, Optional

class Request:
    """HTTP request class"""
    def __init__(self, method: str, path: str, headers: dict = None, body: dict = None):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body or {}
        self._json = {}

    def json(self) -> Dict[str, Any]:
        """Get JSON data from request"""
        return self._json

class Response:
    """HTTP response class"""
    def __init__(self, data: dict = None, status_code: int = 200, headers: dict = None):
        self.data = data or {}
        self.status_code = status_code
        self.headers = headers or {}

class Controller:
    """Base controller class"""
    def __init__(self):
        pass
    
    def get(self, request: Request) -> Response:
        """Handle GET request"""
        return Response({'message': 'Method not implemented'}, 501)
    
    def post(self, request: Request) -> Response:
        """Handle POST request"""
        return Response({'message': 'Method not implemented'}, 501)
    
    def put(self, request: Request) -> Response:
        """Handle PUT request"""
        return Response({'message': 'Method not implemented'}, 501)
    
    def delete(self, request: Request) -> Response:
        """Handle DELETE request"""
        return Response({'message': 'Method not implemented'}, 501)

    def success(self, data: Any = None, message: str = None, status: int = 200) -> Dict[str, Any]:
        """Return a success response"""
        response = {'success': True, 'status': status}
        if data is not None:
            response['data'] = data
        if message is not None:
            response['message'] = message
        return response

    def error(self, message: str, status: int = 400) -> Dict[str, Any]:
        """Return an error response"""
        return {
            'success': False,
            'status': status,
            'message': message
        }

    def not_found(self, message: str = 'Not found') -> Dict[str, Any]:
        """Return a not found response"""
        return self.error(message, status=404) 