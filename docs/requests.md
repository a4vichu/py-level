# Request Validation System

The Request validation system provides a clean and elegant way to validate incoming request data, similar to Laravel's Form Requests. It helps keep your controllers clean by moving validation logic into dedicated request classes.

## Creating a Request

To create a new request class, use the `make:request` command:

```bash
python slave make:request UserRegistration
```

This will create a new request class at `app/requests/user_registration.py`.

## Basic Usage

Here's a basic example of a request class:

```python
from core.http.request import Request

class UserRegistrationRequest(Request):
    def rules(self):
        return {
            'email': ['required', 'email'],
            'password': ['required', 'string', 'min:8'],
            'name': ['required', 'string', 'max:255']
        }

    def messages(self):
        return {
            'email': {
                'required': 'Please provide your email address',
                'email': 'Please provide a valid email address'
            },
            'password': {
                'required': 'Please provide a password',
                'min': 'Password must be at least 8 characters'
            },
            'name': {
                'required': 'Please provide your name'
            }
        }

    def authorize(self):
        return True
```

## Using in Controllers

Use the request class in your controllers like this:

```python
from app.requests.user_registration import UserRegistrationRequest

class UserController:
    def register(self, request):
        # Validate the request
        validated_data = UserRegistrationRequest().validate(request.data)
        
        # Use the validated data
        user = User.create(**validated_data)
        return user
```

## Available Validation Rules

The following validation rules are available:

- `required`: The field must be present and not empty
- `string`: The field must be a string
- `numeric`: The field must be a number (integer or float)
- `email`: The field must be a valid email address

## Custom Error Messages

You can define custom error messages for each validation rule using a nested dictionary structure:

```python
def messages(self):
    return {
        'field_name': {
            'rule_name': 'Custom error message'
        }
    }
```

Example:
```python
def messages(self):
    return {
        'email': {
            'required': 'Please provide your email address',
            'email': 'Please provide a valid email address'
        },
        'password': {
            'required': 'Please provide a password',
            'min': 'Password must be at least 8 characters'
        }
    }
```

## Authorization

The `authorize()` method determines if the user is authorized to make the request:

```python
def authorize(self):
    # Add your authorization logic here
    return True  # or False
```

If authorization fails:
1. The `is_authorized` property will be set to `False`
2. The `validate()` method will return an empty dictionary
3. No validation will be performed

## Accessing Validated Data

After validation, you can access the validated data:

```python
request = UserRegistrationRequest()
validated_data = request.validate(data)

# Access validated data
email = validated_data['email']
password = validated_data['password']
```

## Error Handling

If validation fails, a `ValidationException` is raised with the validation errors:

```python
from core.exceptions.validation import ValidationException

try:
    validated_data = request.validate(data)
except ValidationException as e:
    errors = e.errors
    # Handle validation errors
```

The errors dictionary will contain field names as keys and error messages as values:
```python
{
    'email': 'Please provide a valid email address',
    'password': 'Password must be at least 8 characters'
}
```

## Multiple Validation Rules

You can apply multiple validation rules to a single field:

```python
def rules(self):
    return {
        'email': ['required', 'email'],
        'password': ['required', 'string', 'min:8'],
        'age': ['required', 'numeric', 'min:18']
    }
```

Rules are validated in order, and validation stops at the first failed rule for each field.

## Custom Validation Logic

You can override the `validate()` method to add custom validation logic:

```python
def validate(self, data):
    # First, validate using the standard rules
    validated_data = super().validate(data)
    
    # Add custom validation
    if validated_data.get('name') == 'admin':
        self._errors['name'] = 'This name is not allowed'
        raise ValidationException(self._errors)
    
    return validated_data
```

## Complete Example

Here's a complete example showing all features:

```python
from core.http.request import Request
from core.exceptions.validation import ValidationException

class UpdateProfileRequest(Request):
    def rules(self):
        return {
            'name': ['required', 'string', 'max:255'],
            'email': ['required', 'email'],
            'bio': ['string', 'max:1000'],
            'age': ['numeric', 'min:18']
        }

    def messages(self):
        return {
            'name': {
                'required': 'Please provide your name',
                'max': 'Name cannot be longer than 255 characters'
            },
            'email': {
                'required': 'Please provide your email address',
                'email': 'Please provide a valid email address'
            },
            'bio': {
                'max': 'Bio cannot be longer than 1000 characters'
            },
            'age': {
                'numeric': 'Age must be a number',
                'min': 'You must be at least 18 years old'
            }
        }

    def authorize(self):
        # Example: Check if user is authenticated
        return self.app.auth.check()

    def validate(self, data):
        # You can override validate() to add custom validation logic
        validated_data = super().validate(data)
        
        # Add custom validation
        if validated_data.get('name') == 'admin':
            self._errors['name'] = 'This name is not allowed'
            raise ValidationException(self._errors)
            
        return validated_data
```

## Best Practices

1. Keep request classes focused on a single responsibility
2. Use meaningful names for request classes
3. Define clear validation rules
4. Provide helpful error messages
5. Use the `authorize()` method for authorization checks
6. Keep validation logic in the request class, not in controllers
7. Use custom validation for complex business rules
8. Group related validation rules together
9. Use descriptive error messages
10. Handle validation errors appropriately in your controllers

## Testing

The Request validation system includes a comprehensive test suite that covers:
- Required field validation
- String validation
- Numeric validation
- Email validation
- Custom error messages
- Authorization
- Multiple validation rules
- Custom validation logic

Run the tests using:
```bash
python -m unittest tests/test_request.py -v
``` 