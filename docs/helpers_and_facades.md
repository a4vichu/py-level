# Helpers and Facades Documentation

This document describes the available helpers and facades in the framework, with usage examples.

## Helpers

### 1. `view`
Renders a view template with optional data.
```python
from slave import view
html = view('welcome', {'name': 'Alice'})
```

### 2. `dump`
Pretty-prints data as formatted JSON in the browser (wrapped in <pre> tags).
```python
from slave import dump
data = {'foo': 'bar'}
html = dump(data)
```

## Facades

### 1. `Response`
Standardizes API responses.
```python
from slave.response import Response

# Success response
data = {'foo': 'bar'}
resp = Response.success('cmd123', data)
json_str = resp.to_json()

# Error response
err = Response.error('cmd123', 'Something went wrong')
json_str = err.to_json()
```

### 2. `ResponseFormatter`
Formats responses for output.
```python
from slave.response import ResponseFormatter
ResponseFormatter.format_success('cmd123', {'foo': 'bar'})
ResponseFormatter.format_error('cmd123', 'error message')
```

### 3. `ResponseValidator`
Validates and constructs Response objects from dicts.
```python
from slave.response import ResponseValidator
resp = ResponseValidator.validate({'command_id': 'cmd123', 'status': 'success', 'data': {}})
```

### 4. View Class
Advanced view rendering and sharing data across views.
```python
from slave.view import View
View.add_path('resources/views')
View.share('app_name', 'MyApp')
html = View.make('welcome', {'user': 'Alice'})
```

## CLI Helpers

- `cli`: Command-line interface for server management
- `create_controller`, `list_controllers`, `remove_controller`: Controller management
- `create_model`: Model file generator
- `create_migration`: Migration file generator

## Example Usage

```python
from slave import view, dump
from slave.response import Response

# Render a view
html = view('home', {'user': 'Bob'})

# Dump data for debugging
print(dump({'foo': 'bar'}))

# Return a standardized response
resp = Response.success('cmd1', {'foo': 'bar'})
print(resp.to_json())
``` 