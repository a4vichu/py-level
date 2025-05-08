# API Versioning Guide

## Overview
API versioning is crucial for maintaining backward compatibility while allowing the API to evolve. This guide covers different versioning strategies and best practices.

## Versioning Strategies

### 1. URI Versioning
The most straightforward approach, including the version in the URL.

```python
# routes/api.py
def register_api_routes(router):
    # V1 Routes
    with router.prefix('/api/v1'):
        router.get('/users', UserControllerV1.index)
        router.post('/users', UserControllerV1.store)

    # V2 Routes
    with router.prefix('/api/v2'):
        router.get('/users', UserControllerV2.index)
        router.post('/users', UserControllerV2.store)
```

Example URLs:
```
GET /api/v1/users
GET /api/v2/users
```

### 2. Header Versioning
Using custom headers to specify the API version.

```python
class ApiController:
    def handle_request(self, request):
        version = request.headers.get('X-API-Version', '1')
        if version == '1':
            return self.handle_v1()
        elif version == '2':
            return self.handle_v2()
```

Example request:
```
GET /api/users
X-API-Version: 2
```

### 3. Accept Header Versioning
Using the Accept header with a custom media type.

```python
class ApiController:
    def handle_request(self, request):
        accept = request.headers.get('Accept')
        if 'application/vnd.api.v2+json' in accept:
            return self.handle_v2()
        return self.handle_v1()  # default
```

Example request:
```
GET /api/users
Accept: application/vnd.api.v2+json
```

## Version Control

### Directory Structure
```
app/
├── Http/
│   ├── Controllers/
│   │   ├── V1/
│   │   │   └── UserController.py
│   │   └── V2/
│   │       └── UserController.py
│   └── Resources/
│       ├── V1/
│       │   └── UserResource.py
│       └── V2/
│           └── UserResource.py
└── routes/
    └── api.py
```

### Controller Versioning
```python
# app/Http/Controllers/V1/UserController.py
class UserControllerV1:
    def index(self):
        users = User.all()
        return UserResourceV1.collection(users)

# app/Http/Controllers/V2/UserController.py
class UserControllerV2:
    def index(self):
        users = User.with_relations().all()
        return UserResourceV2.collection(users)
```

### Resource Versioning
```python
# app/Http/Resources/V1/UserResource.py
class UserResourceV1:
    def to_array(self, user):
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }

# app/Http/Resources/V2/UserResource.py
class UserResourceV2:
    def to_array(self, user):
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'profile': {
                'avatar': user.profile.avatar,
                'bio': user.profile.bio
            }
        }
```

## Version Deprecation

### Deprecation Headers
When a version is being deprecated, include appropriate headers:

```python
class UserControllerV1:
    def index(self):
        response = self.get_users()
        response.headers.update({
            'Deprecation': 'true',
            'Sunset': 'Sat, 31 Dec 2024 23:59:59 GMT',
            'Link': '<https://api.example.com/api/v2/users>; rel="successor-version"'
        })
        return response
```

### Deprecation Notice
```python
class ApiV1Middleware:
    def handle(self, request, next):
        response = next(request)
        if request.path.startswith('/api/v1'):
            response.headers['Warning'] = '299 - "This version will be deprecated soon. Please migrate to V2"'
        return response
```

## Best Practices

### 1. Version Selection
```python
class ApiController:
    def get_version_handler(self, request):
        # Priority order: URL > Header > Accept
        if '/v2/' in request.path:
            return self.handle_v2
        elif request.headers.get('X-API-Version') == '2':
            return self.handle_v2
        elif 'application/vnd.api.v2+json' in request.headers.get('Accept', ''):
            return self.handle_v2
        return self.handle_v1
```

### 2. Feature Toggles
```python
class FeatureManager:
    def __init__(self):
        self.features = {
            'v1': {'user_search': True},
            'v2': {'user_search': True, 'advanced_filters': True}
        }
    
    def is_enabled(self, version, feature):
        return self.features.get(version, {}).get(feature, False)
```

### 3. Documentation
Each version should have its own documentation:

```python
@router.get('/api/v1/docs')
def v1_docs():
    return {
        'openapi': '3.0.0',
        'info': {
            'version': '1.0.0',
            'title': 'API V1 Documentation'
        }
    }

@router.get('/api/v2/docs')
def v2_docs():
    return {
        'openapi': '3.0.0',
        'info': {
            'version': '2.0.0',
            'title': 'API V2 Documentation'
        }
    }
```

## Migration Guide

### 1. Version Migration Path
Document clear migration paths for users:

```markdown
## Migrating from V1 to V2

### Changes
- User endpoint now includes profile information
- Search endpoint supports advanced filters
- Authentication requires API key

### Steps
1. Update API version in requests
2. Update client code to handle new response format
3. Add API key to requests
```

### 2. Version Coexistence
Support both versions during migration:

```python
class UserController:
    def show(self, user_id):
        user = User.find(user_id)
        
        if self.is_v1_request():
            return {
                'id': user.id,
                'name': user.name
            }
            
        # V2 response
        return {
            'id': user.id,
            'name': user.name,
            'profile': user.profile.to_dict()
        }
``` 