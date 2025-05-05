# Facades Documentation

Facades provide a clean, static interface to various services in the application. They serve as a convenient way to access services without having to manually resolve them from the service container.

## Available Facades

### Cache Facade

The Cache facade provides methods for interacting with the cache system.

```python
from core.facade import Cache

# Get a value from cache
value = Cache.get('key')

# Store a value in cache
Cache.put('key', 'value', ttl=3600)  # ttl in seconds

# Get or store a value using a callback
value = Cache.remember('key', 3600, lambda: 'computed_value')

# Remove a value from cache
Cache.forget('key')

# Clear all cache
Cache.flush()
```

### DB Facade

The DB facade provides methods for database operations.

```python
from core.facade import DB

# Execute a raw query
results = DB.query('SELECT * FROM users WHERE id = ?', [1])

# Get a table instance
users = DB.table('users')

# Execute a select query
results = DB.select('SELECT * FROM users')

# Execute an insert query
DB.insert('INSERT INTO users (name) VALUES (?)', ['John'])

# Execute an update query
DB.update('UPDATE users SET name = ? WHERE id = ?', ['John', 1])

# Execute a delete query
DB.delete('DELETE FROM users WHERE id = ?', [1])
```

### File Facade

The File facade provides methods for file system operations.

```python
from core.facade import File

# Check if a file exists
if File.exists('path/to/file.txt'):
    # Get file contents
    contents = File.get('path/to/file.txt')
    
    # Write to file
    File.put('path/to/file.txt', 'new contents')
    
    # Get file size
    size = File.size('path/to/file.txt')
    
    # Get last modified time
    modified = File.last_modified('path/to/file.txt')

# Copy a file
File.copy('source.txt', 'destination.txt')

# Move a file
File.move('old.txt', 'new.txt')

# Delete a file
File.delete('path/to/file.txt')
```

### App Facade

The App facade provides access to core application functionality.

```python
from core.facade import App

# Configuration helpers
value = App.config.get('app.name')
env_value = App.env.get('APP_ENV')
app_value = App.version

# Path helpers
base = App.path.base()
app = App.path.app()
config = App.path.config()
database = App.path.database()
resource = App.path.resource()
storage = App.path.storage()

# Logging helpers
App.log.info('User logged in')
App.log.error('Failed to process request')

# URL helpers
url = App.url.to('/users')
secure_url = App.url.secure('/login')
route_url = App.url.route('user.profile', {'id': 1})
asset_url = App.url.asset('css/app.css')

# Redirect helpers
App.redirect.to('/dashboard')
App.redirect.back()

# Request helpers
value = App.request.get('user_id')
old_value = App.request.old('name')
session_value = App.request.session('token')

# Translation helpers
text = App.trans.get('Welcome')
plural = App.trans.choice('apples', 5)

# Collection helpers
items = App.collection.make([1, 2, 3])
value = App.collection.get(data, 'user.name')
first = App.collection.first(items)
last = App.collection.last(items)

# Security helpers
hashed = App.security.hash('password')
is_valid = App.security.check('password', hashed)

# Event helpers
App.event.listen('user.created', callback)
App.event.dispatch('user.created', user)
```

## Helper Functions

The facades are backed by helper functions that can be used directly if preferred:

```python
from core.facade.helpers import (
    cache,
    db,
    file_exists,
    file_get,
    file_put,
    config,
    env,
    app,
    base_path,
    log,
    url,
    redirect,
    request,
    __,
    trans,
    trans_choice,
    collect,
    data_get,
    head,
    last,
    value,
    with_value,
    bcrypt_hash,
    bcrypt_check,
    event,
    dispatch
)

# Using helper functions directly
value = cache('key')
results = db('SELECT * FROM users')
exists = file_exists('path/to/file.txt')
app_name = config('app.name')
```

## Best Practices

1. Use facades for cleaner, more readable code
2. Prefer facades over direct helper function calls in application code
3. Use helper functions directly in framework code where appropriate
4. Remember that facades are static interfaces to underlying services
5. Facades should be used for commonly accessed services

## Implementation Details

Each facade:
- Inherits from the base `Facade` class
- Implements `get_facade_accessor()` to specify the service name
- Provides static methods that map to underlying service methods
- Uses helper functions for basic operations
- Directly accesses service managers for complex operations

## Error Handling

All facade methods will raise appropriate exceptions if operations fail:
- File operations may raise `FileNotFoundError` or `PermissionError`
- Database operations may raise database-specific exceptions
- Cache operations may raise cache-specific exceptions
- Application operations may raise `AppError` or `ConfigurationError`

## Performance Considerations

- Facades add a small overhead compared to direct service access
- The overhead is negligible for most use cases
- Consider direct service access for performance-critical code
- Template rendering should be cached when possible 