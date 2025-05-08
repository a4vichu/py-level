from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
import re
import uuid
from core.http.middleware.middleware import Middleware
from core.http import Request

class Route:
    """Route class for handling HTTP routes"""
    def __init__(self, uri: str, method: str, action: Callable):
        self.uri = uri
        self.method = method
        self.action = action
        self._middleware: List[Middleware] = []
        self._parameters: Dict[str, Any] = {}

    def add_middleware(self, middleware_list: List[Middleware]) -> 'Route':
        """Add middleware to the route"""
        self._middleware.extend(middleware_list)
        return self

    @property
    def middleware(self) -> List[Middleware]:
        """Get middleware list"""
        return self._middleware

    def handle(self, request: Request) -> Any:
        """Handle the request through middleware and execute the action"""
        # Extract route parameters
        self._parameters = self._extract_parameters(request.path)
        
        # Create middleware chain
        def run_action(req: Request) -> Any:
            # Check if action is a bound method
            if hasattr(self.action, '__self__'):
                # Set request on controller instance
                self.action.__self__.request = req
                # Call method with parameters
                if len(self._parameters) > 0:
                    return self.action(**self._parameters)
                return self.action()
            else:
                # Regular function call
                if len(self._parameters) > 0:
                    return self.action(req, **self._parameters)
                return self.action(req)

        # Build middleware chain
        handler = run_action
        for middleware in reversed(self._middleware):
            next_handler = handler
            handler = lambda req, m=middleware, n=next_handler: m.handle(req, n)

        return handler(request)

    def _extract_parameters(self, path: str) -> Dict[str, str]:
        """Extract parameters from the request path"""
        params = {}
        route_parts = self.uri.split('/')
        path_parts = path.split('/')

        if len(route_parts) != len(path_parts):
            return params

        for route_part, path_part in zip(route_parts, path_parts):
            if route_part.startswith('{') and route_part.endswith('}'):
                param_name = route_part[1:-1]
                params[param_name] = path_part

        return params

class Router:
    """Router class for managing routes"""
    def __init__(self):
        self.routes: Dict[str, List[Route]] = {
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
        route = Route(uri, 'GET', action)
        self.routes['GET'].append(route)
        return route
        
    def post(self, uri: str, action: Callable) -> Route:
        """Register a POST route"""
        route = Route(uri, 'POST', action)
        self.routes['POST'].append(route)
        return route
        
    def put(self, uri: str, action: Callable) -> Route:
        """Register a PUT route"""
        route = Route(uri, 'PUT', action)
        self.routes['PUT'].append(route)
        return route
        
    def patch(self, uri: str, action: Callable) -> Route:
        """Register a PATCH route"""
        route = Route(uri, 'PATCH', action)
        self.routes['PATCH'].append(route)
        return route
        
    def delete(self, uri: str, action: Callable) -> Route:
        """Register a DELETE route"""
        route = Route(uri, 'DELETE', action)
        self.routes['DELETE'].append(route)
        return route
        
    def options(self, uri: str, action: Callable) -> Route:
        """Register an OPTIONS route"""
        route = Route(uri, 'OPTIONS', action)
        self.routes['OPTIONS'].append(route)
        return route
        
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
        route = Route(uri, method, action)
        self.routes[method].append(route)
        return route
        
    def find_route(self, method: str, uri: str) -> Optional[Route]:
        """Find a route matching the method and URI"""
        for route in self.routes.get(method, []):
            if self._match_uri(route.uri, uri):
                return route
        return None
        
    def _match_uri(self, route_uri: str, request_uri: str) -> bool:
        """Match a route URI against a request URI"""
        route_parts = route_uri.split('/')
        request_parts = request_uri.split('/')
        
        if len(route_parts) != len(request_parts):
            return False
            
        for route_part, request_part in zip(route_parts, request_parts):
            if route_part.startswith('{') and route_part.endswith('}'):
                continue
            if route_part != request_part:
                return False
                
        return True
        
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

    class RouteGroup:
        """Route group for managing grouped routes"""
        def __init__(self, router: 'Router', prefix: str):
            self.router = router
            self.prefix = prefix.rstrip('/')
            self._middleware: List[Middleware] = []

        def middleware(self, middleware_list: List[Middleware]) -> 'Router.RouteGroup':
            """Add middleware to all routes in this group"""
            self._middleware.extend(middleware_list)
            return self

        def get(self, uri: str, action: Callable) -> Route:
            """Register a GET route in the group"""
            full_uri = f"{self.prefix}/{uri.lstrip('/')}" if uri else self.prefix
            route = self.router.get(full_uri, action)
            if self._middleware:
                route.add_middleware(self._middleware)
            return route

        def post(self, uri: str, action: Callable) -> Route:
            """Register a POST route in the group"""
            full_uri = f"{self.prefix}/{uri.lstrip('/')}" if uri else self.prefix
            route = self.router.post(full_uri, action)
            if self._middleware:
                route.add_middleware(self._middleware)
            return route

        def put(self, uri: str, action: Callable) -> Route:
            """Register a PUT route in the group"""
            full_uri = f"{self.prefix}/{uri.lstrip('/')}" if uri else self.prefix
            route = self.router.put(full_uri, action)
            if self._middleware:
                route.add_middleware(self._middleware)
            return route

        def patch(self, uri: str, action: Callable) -> Route:
            """Register a PATCH route in the group"""
            full_uri = f"{self.prefix}/{uri.lstrip('/')}" if uri else self.prefix
            route = self.router.patch(full_uri, action)
            if self._middleware:
                route.add_middleware(self._middleware)
            return route

        def delete(self, uri: str, action: Callable) -> Route:
            """Register a DELETE route in the group"""
            full_uri = f"{self.prefix}/{uri.lstrip('/')}" if uri else self.prefix
            route = self.router.delete(full_uri, action)
            if self._middleware:
                route.add_middleware(self._middleware)
            return route

        def options(self, uri: str, action: Callable) -> Route:
            """Register an OPTIONS route in the group"""
            full_uri = f"{self.prefix}/{uri.lstrip('/')}" if uri else self.prefix
            route = self.router.options(full_uri, action)
            if self._middleware:
                route.add_middleware(self._middleware)
            return route

        def group(self, prefix: str) -> 'Router.RouteGroup':
            """Create a nested route group with the given prefix"""
            group = Router.RouteGroup(self.router, f"{self.prefix}/{prefix.lstrip('/')}")
            group._middleware = self._middleware.copy()  # Inherit middleware from parent group
            return group

    def group(self, prefix: str) -> RouteGroup:
        """Create a new route group with the given prefix"""
        return self.RouteGroup(self, prefix) 