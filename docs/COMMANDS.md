# Framework Commands

This document provides detailed information about all available commands in the framework CLI.

## Global Options

`--debug/--no-debug`
- Enable or disable debug mode
- Default: `--no-debug`
- Example: `python app.py --debug serve`

## Server Commands

### `python app.py serve`
Start the development server.

Options:
- `--port INTEGER` - Port to run the server on (default: 8000)
- `--workers INTEGER` - Number of worker processes (default: 4)
- `--host TEXT` - Host to bind to (default: 127.0.0.1)

Example:
```bash
python app.py serve --port 8000 --workers 4 --host 0.0.0.0
```

Environment variables:
- `APP_PORT` - Override default port
- `APP_WORKERS` - Override default worker count
- `APP_HOST` - Override default host

### `python app.py stop`
Stop the running server.

Example:
```bash
python app.py stop
```

### `python app.py status`
Check the current server status.

Output includes:
- Server running state
- Command queue size
- Active workers (if any)

Example:
```bash
python app.py status
```

### `python app.py restart`
Restart the server with current configuration.

Example:
```bash
python app.py restart
```

## Controller Commands

### `python app.py make:controller`
Create a new controller.

Arguments:
- `NAME` - Name of the controller (must end with 'Controller')

Options:
- `--methods TEXT` - Comma-separated list of HTTP methods to implement (default: get,post,put,delete)

Example:
```bash
python app.py make:controller UserController --methods get,post
python app.py make:controller ProductController --methods get,post,put,delete
```

### `python app.py list:controllers`
List all available controllers.

Example:
```bash
python app.py list:controllers
```

### `python app.py remove:controller`
Remove an existing controller.

Arguments:
- `NAME` - Name of the controller to remove

Example:
```bash
python app.py remove:controller UserController
```

## Configuration Commands

### `python app.py config:set`
Set a configuration value.

Arguments:
- `KEY_VALUE` - Configuration key-value pair in format `key=value`

Example:
```bash
python app.py config:set port=8000
python app.py config:set workers=4
python app.py config:set debug=true
```

### `python app.py config:get`
Get a configuration value.

Arguments:
- `KEY` - Configuration key to retrieve

Example:
```bash
python app.py config:get port
```

### `python app.py config:list`
List all current configuration values.

Example:
```bash
python app.py config:list
```

## Process Management Commands

### `python app.py process:start`
Start a worker process.

Arguments:
- `WORKER_NAME` - Name of the worker to start

Example:
```bash
python app.py process:start worker1
```

### `python app.py process:stop`
Stop a worker process.

Arguments:
- `WORKER_NAME` - Name of the worker to stop

Example:
```bash
python app.py process:stop worker1
```

### `python app.py process:list`
List all active worker processes.

Example:
```bash
python app.py process:list
```

## Using Environment Variables

All configuration options can be set using environment variables prefixed with `APP_`.
The variables take precedence over configuration file values.

Example:
```bash
# Set server configuration
export APP_PORT=8000
export APP_WORKERS=4
export APP_HOST=0.0.0.0
export APP_DEBUG=true

# Run the server (will use the environment variables)
python app.py serve
```

## Exit Codes

- `0` - Command completed successfully
- `1` - Command failed with an error
- `130` - Command interrupted by user (Ctrl+C)

## Common Patterns

1. Development Setup:
```bash
export APP_DEBUG=true
python app.py serve --port 8000
```

2. Production Setup:
```bash
export APP_PORT=80
export APP_WORKERS=8
export APP_HOST=0.0.0.0
python app.py serve
```

3. Controller Development:
```bash
# Create controller
python app.py make:controller UserController

# Test controller
python app.py serve --debug

# Remove controller if needed
python app.py remove:controller UserController
```

4. Configuration Management:
```bash
# Set multiple configurations
python app.py config:set port=8000
python app.py config:set workers=4

# Verify configuration
python app.py config:list

# Start server with new configuration
python app.py restart
``` 