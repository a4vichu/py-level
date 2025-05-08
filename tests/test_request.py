import unittest
from unittest.mock import MagicMock
from core.http.request import Request
from core.exceptions.validation import ValidationException

class TestRequest(unittest.TestCase):
    def setUp(self):
        # Create a mock application
        self.app = MagicMock()
        self.request = Request(
            app=self.app,
            method='POST',
            path='/test',
            headers={}
        )

    def test_required_validation(self):
        """Test required field validation"""
        class TestRequiredRequest(Request):
            def __init__(self, app):
                super().__init__(app=app, method='POST', path='/test', headers={})

            def rules(self):
                return {
                    'name': ['required']
                }

        request = TestRequiredRequest(self.app)
        
        # Test with missing field
        with self.assertRaises(ValidationException) as context:
            request.validate({})
        self.assertIn('name', context.exception.errors)
        
        # Test with empty string
        with self.assertRaises(ValidationException) as context:
            request.validate({'name': ''})
        self.assertIn('name', context.exception.errors)
        
        # Test with valid data
        data = request.validate({'name': 'John'})
        self.assertEqual(data['name'], 'John')

    def test_string_validation(self):
        """Test string field validation"""
        class TestStringRequest(Request):
            def __init__(self, app):
                super().__init__(app=app, method='POST', path='/test', headers={})

            def rules(self):
                return {
                    'name': ['string']
                }

        request = TestStringRequest(self.app)
        
        # Test with non-string value
        with self.assertRaises(ValidationException) as context:
            request.validate({'name': 123})
        self.assertIn('name', context.exception.errors)
        
        # Test with valid string
        data = request.validate({'name': 'John'})
        self.assertEqual(data['name'], 'John')

    def test_numeric_validation(self):
        """Test numeric field validation"""
        class TestNumericRequest(Request):
            def __init__(self, app):
                super().__init__(app=app, method='POST', path='/test', headers={})

            def rules(self):
                return {
                    'age': ['numeric']
                }

        request = TestNumericRequest(self.app)
        
        # Test with non-numeric value
        with self.assertRaises(ValidationException) as context:
            request.validate({'age': 'not a number'})
        self.assertIn('age', context.exception.errors)
        
        # Test with valid integer
        data = request.validate({'age': 25})
        self.assertEqual(data['age'], 25)
        
        # Test with valid float
        data = request.validate({'age': 25.5})
        self.assertEqual(data['age'], 25.5)

    def test_email_validation(self):
        """Test email field validation"""
        class TestEmailRequest(Request):
            def __init__(self, app):
                super().__init__(app=app, method='POST', path='/test', headers={})

            def rules(self):
                return {
                    'email': ['email']
                }

        request = TestEmailRequest(self.app)
        
        # Test with invalid email
        with self.assertRaises(ValidationException) as context:
            request.validate({'email': 'not-an-email'})
        self.assertIn('email', context.exception.errors)
        
        # Test with valid email
        data = request.validate({'email': 'test@example.com'})
        self.assertEqual(data['email'], 'test@example.com')

    def test_custom_messages(self):
        """Test custom validation messages"""
        class TestCustomMessageRequest(Request):
            def __init__(self, app):
                super().__init__(app=app, method='POST', path='/test', headers={})

            def rules(self):
                return {
                    'name': ['required']
                }
            
            def messages(self):
                return {
                    'name': {
                        'required': 'Please enter your name'
                    }
                }

        request = TestCustomMessageRequest(self.app)
        
        with self.assertRaises(ValidationException) as context:
            request.validate({})
        self.assertEqual(context.exception.errors['name'], 'Please enter your name')

    def test_authorization(self):
        """Test request authorization"""
        class TestAuthRequest(Request):
            def __init__(self, app):
                super().__init__(app=app, method='POST', path='/test', headers={})

            def authorize(self):
                return False

        request = TestAuthRequest(self.app)
        
        # Test that validation fails when not authorized
        data = request.validate({})
        self.assertEqual(data, {})
        self.assertFalse(request.is_authorized)

    def test_multiple_rules(self):
        """Test multiple validation rules on a single field"""
        class TestMultipleRulesRequest(Request):
            def __init__(self, app):
                super().__init__(app=app, method='POST', path='/test', headers={})

            def rules(self):
                return {
                    'email': ['required', 'email'],
                    'age': ['required', 'numeric']
                }

        request = TestMultipleRulesRequest(self.app)
        
        # Test with missing required fields
        with self.assertRaises(ValidationException) as context:
            request.validate({})
        self.assertIn('email', context.exception.errors)
        self.assertIn('age', context.exception.errors)
        
        # Test with invalid email
        with self.assertRaises(ValidationException) as context:
            request.validate({
                'email': 'not-an-email',
                'age': 25
            })
        self.assertIn('email', context.exception.errors)
        
        # Test with invalid age
        with self.assertRaises(ValidationException) as context:
            request.validate({
                'email': 'test@example.com',
                'age': 'not-a-number'
            })
        self.assertIn('age', context.exception.errors)
        
        # Test with valid data
        data = request.validate({
            'email': 'test@example.com',
            'age': 25
        })
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['age'], 25)

    def test_custom_validation(self):
        """Test custom validation logic"""
        class TestCustomValidationRequest(Request):
            def __init__(self, app):
                super().__init__(app=app, method='POST', path='/test', headers={})

            def rules(self):
                return {
                    'name': ['required']
                }
            
            def validate(self, data):
                validated_data = super().validate(data)
                
                if validated_data.get('name') == 'admin':
                    self._errors['name'] = 'This name is not allowed'
                    raise ValidationException(self._errors)
                
                return validated_data

        request = TestCustomValidationRequest(self.app)
        
        # Test with forbidden name
        with self.assertRaises(ValidationException) as context:
            request.validate({'name': 'admin'})
        self.assertEqual(context.exception.errors['name'], 'This name is not allowed')
        
        # Test with allowed name
        data = request.validate({'name': 'John'})
        self.assertEqual(data['name'], 'John')

if __name__ == '__main__':
    unittest.main() 