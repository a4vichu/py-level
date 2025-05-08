# Validation Rules

This document provides detailed information about all available validation rules in the Request validation system.

## Basic Rules

### Required
Validates that a field is present and not empty.

```python
def rules(self):
    return {
        'name': ['required']
    }
```

### String
Validates that a field is a string.

```python
def rules(self):
    return {
        'name': ['string']
    }
```

### Numeric
Validates that a field is a number (integer or float).

```python
def rules(self):
    return {
        'age': ['numeric']
    }
```

### Email
Validates that a field is a valid email address.

```python
def rules(self):
    return {
        'email': ['email']
    }
```

## String Validation Rules

### Min Length
Validates that a string field has a minimum length.

```python
def rules(self):
    return {
        'password': ['string', 'min:8']  # Minimum 8 characters
    }
```

### Max Length
Validates that a string field has a maximum length.

```python
def rules(self):
    return {
        'name': ['string', 'max:255']  # Maximum 255 characters
    }
```

### Regex
Validates that a string field matches a regular expression pattern.

```python
def rules(self):
    return {
        'username': ['string', 'regex:/^[a-zA-Z0-9_]+$/']  # Alphanumeric and underscore only
    }
```

### Alpha
Validates that a string field contains only alphabetic characters.

```python
def rules(self):
    return {
        'name': ['string', 'alpha']  # Letters only
    }
```

### Alpha Numeric
Validates that a string field contains only alphanumeric characters.

```python
def rules(self):
    return {
        'username': ['string', 'alpha_num']  # Letters and numbers only
    }
```

### Alpha Dash
Validates that a string field contains only alphanumeric characters, dashes, and underscores.

```python
def rules(self):
    return {
        'slug': ['string', 'alpha_dash']  # Letters, numbers, dashes, and underscores
    }
```

## Numeric Validation Rules

### Min Value
Validates that a numeric field has a minimum value.

```python
def rules(self):
    return {
        'age': ['numeric', 'min:18']  # Minimum value of 18
    }
```

### Max Value
Validates that a numeric field has a maximum value.

```python
def rules(self):
    return {
        'price': ['numeric', 'max:1000']  # Maximum value of 1000
    }
```

### Between
Validates that a numeric field is between two values.

```python
def rules(self):
    return {
        'age': ['numeric', 'between:18,65']  # Between 18 and 65
    }
```

## Database Validation Rules

### Exists
Validates that a value exists in a database table.

```python
def rules(self):
    return {
        'user_id': ['required', 'exists:users,id'],  # Must exist in users table
        'category_id': ['required', 'exists:categories,id,status=active']  # With additional conditions
    }
```

### Unique
Validates that a value is unique in a database table.

```python
def rules(self):
    return {
        'email': ['required', 'email', 'unique:users,email'],  # Must be unique in users table
        'username': ['required', 'unique:users,username,id!=1']  # Ignore record with id=1
    }
```

### In
Validates that a value exists in a given list of values.

```python
def rules(self):
    return {
        'status': ['required', 'in:active,inactive,pending'],
        'role': ['required', 'in:admin,user,editor']
    }
```

## Date Validation Rules

### Date
Validates that a field is a valid date.

```python
def rules(self):
    return {
        'birth_date': ['required', 'date'],
        'start_date': ['required', 'date', 'after:today'],
        'end_date': ['required', 'date', 'after:start_date']
    }
```

### Date Format
Validates that a field matches a specific date format.

```python
def rules(self):
    return {
        'birth_date': ['required', 'date_format:Y-m-d'],
        'appointment': ['required', 'date_format:Y-m-d H:i:s']
    }
```

### Before/After
Validates that a date is before or after another date.

```python
def rules(self):
    return {
        'start_date': ['required', 'date', 'after:today'],
        'end_date': ['required', 'date', 'after:start_date'],
        'birth_date': ['required', 'date', 'before:today']
    }
```

## File Validation Rules

### File
Validates that a field is a valid file upload.

```python
def rules(self):
    return {
        'avatar': ['required', 'file', 'max:2048'],  # Max 2MB
        'document': ['required', 'file', 'mimes:pdf,doc,docx']
    }
```

### Image
Validates that a field is a valid image file.

```python
def rules(self):
    return {
        'avatar': ['required', 'image', 'max:2048', 'dimensions:min_width=100,min_height=100']
    }
```

## Array Validation Rules

### Array
Validates that a field is an array.

```python
def rules(self):
    return {
        'tags': ['required', 'array'],
        'tags.*': ['required', 'string', 'max:50']  # Validate each array item
    }
```

### Size
Validates that an array has a specific number of items.

```python
def rules(self):
    return {
        'tags': ['required', 'array', 'size:3']  # Must have exactly 3 items
    }
```

## Combining Rules

You can combine multiple rules for a single field. Rules are validated in order, and validation stops at the first failed rule.

```python
def rules(self):
    return {
        'email': ['required', 'string', 'email', 'unique:users,email'],
        'password': ['required', 'string', 'min:8', 'max:255', 'regex:/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/'],
        'age': ['required', 'numeric', 'between:18,65'],
        'username': ['required', 'string', 'alpha_dash', 'min:3', 'max:50', 'unique:users,username']
    }
```

## Custom Error Messages

You can provide custom error messages for each validation rule using a nested dictionary structure:

```python
def messages(self):
    return {
        'email': {
            'required': 'Please provide your email address',
            'string': 'Email must be a string',
            'email': 'Please provide a valid email address',
            'unique': 'This email address is already registered'
        },
        'password': {
            'required': 'Please provide a password',
            'string': 'Password must be a string',
            'min': 'Password must be at least 8 characters',
            'max': 'Password cannot be longer than 255 characters',
            'regex': 'Password must contain at least one uppercase letter, one lowercase letter, and one number'
        },
        'age': {
            'required': 'Please provide your age',
            'numeric': 'Age must be a number',
            'between': 'Age must be between 18 and 65'
        }
    }
```

## Validation Rule Reference

### Basic Rules
| Rule | Description | Example |
|------|-------------|---------|
| `required` | Field must be present and not empty | `['required']` |
| `string` | Field must be a string | `['string']` |
| `numeric` | Field must be a number | `['numeric']` |
| `email` | Field must be a valid email address | `['email']` |

### String Rules
| Rule | Description | Example |
|------|-------------|---------|
| `min:N` | String must have minimum length N | `['string', 'min:8']` |
| `max:N` | String must have maximum length N | `['string', 'max:255']` |
| `regex:pattern` | String must match regex pattern | `['string', 'regex:/^[a-z]+$/']` |
| `alpha` | String must contain only letters | `['string', 'alpha']` |
| `alpha_num` | String must contain only letters and numbers | `['string', 'alpha_num']` |
| `alpha_dash` | String must contain only letters, numbers, dashes, and underscores | `['string', 'alpha_dash']` |

### Numeric Rules
| Rule | Description | Example |
|------|-------------|---------|
| `min:N` | Number must be greater than or equal to N | `['numeric', 'min:18']` |
| `max:N` | Number must be less than or equal to N | `['numeric', 'max:1000']` |
| `between:min,max` | Number must be between min and max | `['numeric', 'between:18,65']` |

### Database Rules
| Rule | Description | Example |
|------|-------------|---------|
| `exists:table,column` | Value must exist in database | `['exists:users,id']` |
| `unique:table,column` | Value must be unique in database | `['unique:users,email']` |
| `in:value1,value2,...` | Value must be in list | `['in:active,inactive']` |

### Date Rules
| Rule | Description | Example |
|------|-------------|---------|
| `date` | Field must be a valid date | `['date']` |
| `date_format:format` | Field must match date format | `['date_format:Y-m-d']` |
| `after:date` | Date must be after given date | `['date', 'after:today']` |
| `before:date` | Date must be before given date | `['date', 'before:today']` |

### File Rules
| Rule | Description | Example |
|------|-------------|---------|
| `file` | Field must be a file | `['file']` |
| `image` | Field must be an image | `['image']` |
| `mimes:ext1,ext2` | File must have given extensions | `['file', 'mimes:pdf,doc']` |
| `max:N` | File size must be less than N KB | `['file', 'max:2048']` |

### Array Rules
| Rule | Description | Example |
|------|-------------|---------|
| `array` | Field must be an array | `['array']` |
| `size:N` | Array must have N items | `['array', 'size:3']` |

## Common Use Cases

### User Registration with Advanced Rules
```python
def rules(self):
    return {
        'username': ['required', 'string', 'alpha_dash', 'min:3', 'max:50', 'unique:users,username'],
        'email': ['required', 'string', 'email', 'unique:users,email'],
        'password': ['required', 'string', 'min:8', 'max:255', 'regex:/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/'],
        'age': ['required', 'numeric', 'between:18,65'],
        'birth_date': ['required', 'date', 'before:today'],
        'avatar': ['image', 'max:2048', 'dimensions:min_width=100,min_height=100'],
        'interests': ['array', 'size:3'],
        'interests.*': ['required', 'string', 'in:sports,music,reading,travel']
    }
```

### Product Creation with Advanced Rules
```python
def rules(self):
    return {
        'name': ['required', 'string', 'max:255', 'unique:products,name'],
        'description': ['required', 'string', 'max:1000'],
        'price': ['required', 'numeric', 'min:0', 'max:1000000'],
        'stock': ['required', 'numeric', 'min:0'],
        'category_id': ['required', 'exists:categories,id,status=active'],
        'images': ['array', 'max:5'],
        'images.*': ['required', 'image', 'max:2048'],
        'tags': ['array'],
        'tags.*': ['required', 'string', 'max:50'],
        'start_date': ['required', 'date', 'after:today'],
        'end_date': ['required', 'date', 'after:start_date']
    }
```

## Best Practices

1. Always use `required` for mandatory fields
2. Use appropriate string length limits to prevent abuse
3. Validate email addresses for user-related forms
4. Use numeric validation with min/max for age, price, etc.
5. Provide clear and helpful error messages
6. Group related validation rules together
7. Use consistent validation rules across similar forms
8. Consider security implications of validation rules
9. Test validation rules with edge cases
10. Keep validation rules maintainable and readable
11. Use database validation rules for data integrity
12. Validate file uploads properly
13. Use array validation for multiple values
14. Implement proper date validation
15. Use regex for complex string patterns

## Testing Validation Rules

You can test validation rules using the test suite:

```python
def test_required_validation(self):
    request = TestRequiredRequest(self.app)
    with self.assertRaises(ValidationException) as context:
        request.validate({})
    self.assertIn('name', context.exception.errors)

def test_unique_validation(self):
    # Create a test user
    User.create(email='test@example.com')
    
    request = TestUniqueRequest(self.app)
    with self.assertRaises(ValidationException) as context:
        request.validate({'email': 'test@example.com'})
    self.assertIn('email', context.exception.errors)
    self.assertEqual(context.exception.errors['email'], 'This email is already taken')

def test_file_validation(self):
    request = TestFileRequest(self.app)
    with self.assertRaises(ValidationException) as context:
        request.validate({'avatar': 'not-a-file'})
    self.assertIn('avatar', context.exception.errors)
```

For more information about testing, see the [Request Validation System documentation](requests.md). 