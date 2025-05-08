# Middleware Documentation

## Overview
Middleware provides a convenient mechanism for filtering HTTP requests entering your application. For example, middleware can be used to verify that a user is authenticated, log all requests, or ensure CSRF protection.

## Built-in Middleware

### Authentication Middleware
Verifies that a user is authenticated before allowing access to a route.

```python
from core.http.middleware import Authenticate

# Single middleware
router.get('/profile', ProfileController.show).middleware(Authenticate())

# With guard
router.get('/admin', AdminController.dashboard).middleware(Authenticate(guard='admin'))
```

### CSRF Protection
Protects against Cross-Site Request Forgery attacks.

```python
from core.http.middleware import VerifyCsrfToken

router.post('/users', UserController.store).middleware(VerifyCsrfToken())
```

### Rate Limiting
Limits the number of requests a client can make in a given time period.

```python
from core.http.middleware import ThrottleRequests

router.get('/api', ApiController.index).middleware(
    ThrottleRequests(max_attempts=60, decay_minutes=1)
)
```

### Session Handling
Manages user sessions for web routes.

```python
from core.http.middleware import StartSession

router.get('/dashboard', DashboardController.show).middleware(StartSession())
```

## Creating Custom Middleware

### Basic Structure
```python
from core.http.middleware import Middleware

class CustomMiddleware(Middleware):
    def handle(self, request, next):
        # Perform actions before the request is handled
        
        response = next(request)
        
        # Perform actions after the request is handled
        
        return response
```

### Example: Logging Middleware
```python
from core.http.middleware import Middleware
import logging

class LogRequests(Middleware):
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
    
    def handle(self, request, next):
        # Log incoming request
        self.logger.info(f"Incoming {request.method} request to {request.path}")
        
        # Process request
        response = next(request)
        
        # Log response
        self.logger.info(f"Returning response with status {response.status_code}")
        return response
```

### Example: API Key Middleware
```python
from core.http.middleware import Middleware
from core.http.exceptions import UnauthorizedException

class ValidateApiKey(Middleware):
    def handle(self, request, next):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            raise UnauthorizedException('API key is required')
            
        if not self.is_valid_api_key(api_key):
            raise UnauthorizedException('Invalid API key')
            
        return next(request)
        
    def is_valid_api_key(self, key):
        # Implement API key validation logic
        pass
```

## Middleware Groups

### Defining Middleware Groups
```python
# config/middleware.py
MIDDLEWARE_GROUPS = {
    'web': [
        StartSession(),
        VerifyCsrfToken(),
        ShareErrorsFromSession(),
    ],
    'api': [
        ThrottleRequests(max_attempts=60, decay_minutes=1),
        ValidateApiKey(),
    ]
}
```

### Using Middleware Groups
```python
# routes/web.py
with router.group(middleware='web'):
    router.get('/', HomeController.index)
    router.get('/dashboard', DashboardController.show)

# routes/api.py
with router.group(middleware='api'):
    router.get('/users', UserController.index)
    router.post('/users', UserController.store)
```

## Global Middleware
Global middleware is run on every HTTP request to your application.

```python
# config/middleware.py
GLOBAL_MIDDLEWARE = [
    TrimStrings(),
    ConvertEmptyStringsToNull(),
]
```

## Middleware Parameters
Middleware can accept parameters in their constructor for configuration:

```python
class CacheResponse(Middleware):
    def __init__(self, ttl=3600):
        self.ttl = ttl
        
    def handle(self, request, next):
        # Check cache
        cached = cache.get(request.cache_key)
        if cached:
            return cached
            
        response = next(request)
        
        # Store in cache
        cache.set(request.cache_key, response, ttl=self.ttl)
        return response

# Usage
router.get('/posts', PostController.index).middleware(
    CacheResponse(ttl=1800)  # Cache for 30 minutes
)
```

## Best Practices

1. **Keep Middleware Focused**: Each middleware should have a single responsibility.
2. **Order Matters**: Consider the order of middleware execution, especially for authentication and session handling.
3. **Error Handling**: Always handle potential errors in middleware and provide clear error messages.
4. **Performance**: Be mindful of performance impact when adding middleware to routes.
 