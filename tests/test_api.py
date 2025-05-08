import unittest
from unittest.mock import patch, MagicMock
from app.Http.Controllers.user_controller import UserController
from core.http import Request
from core.routing.router import Router, Route
from core.http.middleware.middleware import Middleware, Authenticate, VerifyCsrfToken

class TestMiddleware(Middleware):
    def handle(self, request, next):
        request['test_middleware'] = True
        return next(request)

class TestUserController(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.controller = UserController()
        self.mock_request = MagicMock()
        self.mock_request.json = MagicMock(return_value={})
        self.router = Router()

    def test_index_method(self):
        """Test index method returns correct response"""
        response = self.controller.index(self.mock_request)
        self.assertTrue(response['success'])
        self.assertEqual(response['data'], [])
        self.assertEqual(response['message'], 'Users retrieved successfully')

    def test_store_method(self):
        """Test store method returns correct response"""
        self.mock_request.json.return_value = {'name': 'Test User'}
        response = self.controller.store(self.mock_request)
        self.assertTrue(response['success'])
        self.assertEqual(response['message'], 'User created successfully')
        self.assertEqual(response['status'], 201)

    def test_show_method(self):
        """Test show method returns correct response"""
        response = self.controller.show(self.mock_request, 1)
        self.assertFalse(response['success'])
        self.assertEqual(response['status'], 404)
        self.assertEqual(response['message'], 'User not found')

    def test_update_method(self):
        """Test update method returns correct response"""
        self.mock_request.json.return_value = {'name': 'Updated User'}
        response = self.controller.update(self.mock_request, 1)
        self.assertTrue(response['success'])
        self.assertEqual(response['message'], 'User updated successfully')

    def test_delete_method(self):
        """Test delete method returns correct response"""
        response = self.controller.delete(self.mock_request, 1)
        self.assertTrue(response['success'])
        self.assertEqual(response['message'], 'User deleted successfully')

    def test_profile_method(self):
        """Test profile method returns correct response"""
        response = self.controller.profile(self.mock_request)
        self.assertTrue(response['success'])
        self.assertEqual(response['data'], {})

    def test_analytics_method(self):
        """Test analytics method returns correct response"""
        response = self.controller.analytics(self.mock_request)
        self.assertTrue(response['success'])
        self.assertEqual(response['data'], {
            'total_users': 0,
            'active_users': 0,
            'new_users_today': 0
        })

    def test_docs_method(self):
        """Test docs method returns correct response"""
        response = self.controller.docs(self.mock_request)
        self.assertEqual(response['openapi'], '3.0.0')
        self.assertEqual(response['info']['version'], '1.0.0')

    def test_route_middleware(self):
        """Test that middleware is properly attached to routes"""
        # Create a route with middleware
        route = self.router.get('/test', lambda: 'test')
        route.middleware.append(TestMiddleware())
        
        # Verify middleware was attached
        self.assertEqual(len(route.middleware), 1)
        self.assertIsInstance(route.middleware[0], TestMiddleware)

    def test_multiple_middleware(self):
        """Test multiple middleware on a route"""
        route = self.router.get('/multi', lambda: 'test')
        route.middleware.append(TestMiddleware())
        route.middleware.append(Authenticate())
        
        self.assertEqual(len(route.middleware), 2)
        self.assertIsInstance(route.middleware[0], TestMiddleware)
        self.assertIsInstance(route.middleware[1], Authenticate)

    def test_middleware_execution(self):
        """Test middleware execution order"""
        request = {}
        
        # Create middleware that adds to request
        class FirstMiddleware(Middleware):
            def handle(self, request, next):
                request['first'] = True
                return next(request)
                
        class SecondMiddleware(Middleware):
            def handle(self, request, next):
                request['second'] = True
                return next(request)
        
        # Create route with multiple middleware
        route = self.router.get('/exec', lambda: 'test')
        route.middleware.append(FirstMiddleware())
        route.middleware.append(SecondMiddleware())
        
        # Execute middleware chain
        result = request
        for middleware in route.middleware:
            result = middleware.handle(result, lambda x: x)
            
        self.assertTrue(result.get('first'))
        self.assertTrue(result.get('second'))

if __name__ == '__main__':
    unittest.main() 