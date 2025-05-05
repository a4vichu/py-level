from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
import re
import uuid

class Route:
    def __init__(self, method: str, uri: str, action: Callable, name: Optional[str] = None):
        self.method = method.upper()
        self.uri = uri
        self.action = action
        self.name = name
        self.middleware = []
        
    def middleware(self, middleware: Any):
        """Register middleware for the route"""
        self.middleware.append(middleware)
        return self
        
    def name(self, name: str):
        """Set the name of the route"""
        self.name = name
        return self
        
class Router:
    def __init__(self):
        self._routes: Dict[str, List[Route]] = {
            'GET': [],
            'POST': [],
            'PUT': [],
            'PATCH': [],
            'DELETE': [],
            'OPTIONS': []
        }
        self._named_routes: Dict[str, Route] = {}
        
    def get(self, uri: str, action: Callable) -> Route:
        """Register a GET route"""
        return self._add_route('GET', uri, action)
        
    def post(self, uri: str, action: Callable) -> Route:
        """Register a POST route"""
        return self._add_route('POST', uri, action)
        
    def put(self, uri: str, action: Callable) -> Route:
        """Register a PUT route"""
        return self._add_route('PUT', uri, action)
        
    def patch(self, uri: str, action: Callable) -> Route:
        """Register a PATCH route"""
        return self._add_route('PATCH', uri, action)
        
    def delete(self, uri: str, action: Callable) -> Route:
        """Register a DELETE route"""
        return self._add_route('DELETE', uri, action)
        
    def options(self, uri: str, action: Callable) -> Route:
        """Register an OPTIONS route"""
        return self._add_route('OPTIONS', uri, action)
        
    def match(self, methods: List[str], uri: str, action: Callable) -> Route:
        """Register a route that matches multiple methods"""
        route = None
        for method in methods:
            route = self._add_route(method, uri, action)
        return route
        
    def any(self, uri: str, action: Callable) -> Route:
        """Register a route that matches any method"""
        return self.match(['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'], uri, action)
        
    def _add_route(self, method: str, uri: str, action: Callable) -> Route:
        """Add a route to the router"""
        route = Route(method, uri, action)
        self._routes[method].append(route)
        return route
        
    def find_route(self, method: str, uri: str) -> Optional[Route]:
        """Find a route that matches the given method and URI"""
        if method not in self._routes:
            return None
            
        for route in self._routes[method]:
            if self._uri_matches(route.uri, uri):
                return route
        return None
        
    def _uri_matches(self, pattern: str, uri: str) -> bool:
        """Determine if the URI matches the given pattern"""
        pattern = re.sub(r'\{([^}]+)\}', r'(?P<\1>[^/]+)', pattern)
        pattern = f'^{pattern}$'
        return bool(re.match(pattern, uri))
        
    def get_named_route(self, name: str) -> Optional[Route]:
        """Get a route by name"""
        return self._named_routes.get(name)
        
    def url(self, name: str, parameters: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Generate a URL for a named route"""
        route = self.get_named_route(name)
        if route is None:
            return None
            
        uri = route.uri
        if parameters:
            for key, value in parameters.items():
                uri = uri.replace(f'{{{key}}}', str(value))
        return uri 