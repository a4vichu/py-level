from core.routing.router import Router
from app.Http.Controllers.user_controller import UserController
from core.http.middleware.middleware import (
    Authenticate,
    VerifyCsrfToken,
    ThrottleRequests,
    StartSession
)

def register_api_routes(router: Router):
    """Register API routes with middleware"""
    
    # Create controller instance
    controller = UserController()
    
    # Group all API routes with common middleware
    api = router.group('/api').middleware([
        StartSession(),  # All API routes will have session support
        VerifyCsrfToken()  # All API routes will be CSRF protected
    ])
    
    # User routes group with authentication
    users = api.group('/users').middleware([
        Authenticate()  # All user routes require authentication
    ])
    
    # Basic user routes (already have authentication from group)
    users.get('', controller.index)  # GET /api/users
    users.post('', controller.store)  # POST /api/users
    users.get('/{id}', controller.show)  # GET /api/users/{id}
    users.put('/{id}', controller.update)  # PUT /api/users/{id}
    users.delete('/{id}', controller.delete)  # DELETE /api/users/{id}
    
    # Protected profile route (additional middleware)
    profile_route = users.get('/profile', controller.profile)  # GET /api/users/profile
    profile_route.add_middleware([
        ThrottleRequests(max_attempts=30, decay_minutes=1)  # Rate limit profile access
    ])
    
    # Analytics route with admin guard and rate limiting
    analytics_route = users.get('/analytics', controller.analytics)  # GET /api/users/analytics
    analytics_route.add_middleware([
        Authenticate(guard='admin'),  # Override group auth with admin guard
        ThrottleRequests(max_attempts=60, decay_minutes=1)  # Rate limit analytics access
    ])
    
    # API documentation (no auth required)
    api.get('/docs', controller.docs)  # GET /api/docs
    
    return router 