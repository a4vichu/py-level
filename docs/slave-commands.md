# PyLevel Slave Commands Tutorial

## Table of Contents
1. [Introduction](#introduction)
2. [Server Commands](#server-commands)
3. [Controller Commands](#controller-commands)
4. [Model Commands](#model-commands)
5. [Migration Commands](#migration-commands)
6. [Configuration Commands](#configuration-commands)
7. [Process Commands](#process-commands)
8. [Development Commands](#development-commands)

## Introduction

The PyLevel slave commands provide a powerful CLI interface for managing your application. These commands help you create, manage, and maintain your application components efficiently.

## Server Commands

### Start Server
```bash
python slave serve [--host HOST] [--port PORT] [--workers WORKERS]
```
Options:
- `--host`: Server host (default: 127.0.0.1)
- `--port`: Server port (default: 8000)
- `--workers`: Number of worker processes (default: 4)

### Stop Server
```bash
python slave stop
```
Stops the running slave server.

### Check Server Status
```bash
python slave status
```
Displays the current server status and command queue size.

### Restart Server
```bash
python slave restart
```
Restarts the slave server with current configuration.

## Controller Commands

### Create Controller
```bash
python slave make controller NAME [--methods METHODS]
```
Options:
- `NAME`: Name of the controller
- `--methods`: Comma-separated HTTP methods (default: get,post,put,delete)

Example:
```bash
python slave make controller UserController --methods get,post
```

### List Controllers
```bash
python slave list:controllers
```
Lists all available controllers in your application.

### Remove Controller
```bash
python slave remove:controller NAME
```
Removes a specified controller.

## Model Commands

### Create Model
```bash
python slave make:model NAME [-m] [-c]
```
Options:
- `NAME`: Name of the model
- `-m, --migration`: Create a migration file
- `-c, --controller`: Create a controller

Example:
```bash
python slave make:model User -m -c
```

### Create Form Request
```bash
python slave make:request NAME
```
Creates a new form request class for validation.

Example:
```bash
python slave make:request UserLogin
```

## Migration Commands

### Run Migrations
```bash
python slave migrate [--force] [--database DATABASE]
```
Options:
- `--force`: Force the operation in production
- `--database`: Specify database connection

### Refresh Migrations
```bash
python slave migrate:refresh [--force] [--database DATABASE]
```
Rolls back all migrations and re-runs them.

### Rollback Migrations
```bash
python slave migrate:rollback [--steps STEPS] [--force] [--database DATABASE]
```
Options:
- `--steps`: Number of migrations to rollback (default: 1)

### Fresh Migrations
```bash
python slave migrate:fresh [--force] [--database DATABASE]
```
Drops all tables and re-runs all migrations.

## Configuration Commands

### Set Configuration
```bash
python slave config set KEY=VALUE
```
Sets a configuration value.

Example:
```bash
python slave config set app.debug=true
```

### Get Configuration
```bash
python slave config get KEY
```
Retrieves a configuration value.

### List Configuration
```bash
python slave config list
```
Lists all configuration values.

## Process Commands

### Start Process
```bash
python slave process start WORKER_NAME
```
Starts a new worker process.

### Stop Process
```bash
python slave process stop WORKER_NAME
```
Stops a running worker process.

### List Processes
```bash
python slave process list
```
Lists all running worker processes.

## Development Commands

### Development Server with Live Reload
```bash
python slave dev [--watch PATH1] [--watch PATH2]
```
Starts the development server with live reload functionality.
Options:
- `--watch`: Paths to watch for changes (can be specified multiple times)

Example:
```bash
python slave dev --watch app --watch resources
```

## Best Practices

1. **Server Management**
   - Use `serve` for production
   - Use `dev` for development
   - Always check server status before operations

2. **Controllers and Models**
   - Create models with migrations when needed
   - Use form requests for validation
   - Keep controllers focused and thin

3. **Migrations**
   - Always backup before migrations
   - Use `--force` with caution
   - Test migrations in development first

4. **Configuration**
   - Keep sensitive data in environment variables
   - Use descriptive configuration keys
   - Document custom configurations

## Troubleshooting

Common issues and solutions:

1. **Server Won't Start**
   - Check if port is in use
   - Verify configuration
   - Check logs for errors

2. **Migration Issues**
   - Ensure database connection is correct
   - Check migration files for errors
   - Use `migrate:rollback` if needed

3. **Process Management**
   - Use `process list` to check status
   - Ensure proper permissions
   - Check system resources

## Next Steps

1. Explore the [API Documentation](docs/api.md)
2. Check out the [Advanced Topics](docs/advanced.md)
3. Join the [Community](https://github.com/yourusername/pylevelframework)

## Support

If you need help:
- Check the [Documentation](docs/)
- Join our [Discord Community](https://discord.gg/pylevel)
- Open an [Issue](https://github.com/yourusername/pylevelframework/issues) 