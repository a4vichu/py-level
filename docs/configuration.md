# Configuration System

## Environment Variables

The framework uses environment variables to configure various aspects of the application. You can create a `.env` file in your project root to set these variables. Here's a template of all available environment variables:

```ini
# Application
APP_NAME=PyLevel
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000
APP_KEY=

# Server
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
SERVER_WORKERS=4

# Database
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=pylevel
DB_USERNAME=root
DB_PASSWORD=
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_unicode_ci
DB_PREFIX=
DB_STRICT=true

# Cache
CACHE_DRIVER=file
CACHE_PREFIX=pylevel_
CACHE_TTL=3600
CACHE_TAGS=true

# Redis Cache
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=null
REDIS_DB=0

# Memcached
MEMCACHED_HOST=127.0.0.1
MEMCACHED_PORT=11211
MEMCACHED_WEIGHT=100

# Session
SESSION_DRIVER=file
SESSION_LIFETIME=120

# Logging
LOG_CHANNEL=stack
LOG_LEVEL=debug
LOG_FILE=storage/logs/app.log

# Mail
MAIL_DRIVER=smtp
MAIL_HOST=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=null
MAIL_FROM_NAME=null

# AWS SES
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1

# Mailgun
MAILGUN_DOMAIN=
MAILGUN_SECRET=
MAILGUN_ENDPOINT=api.mailgun.net

# Queue
QUEUE_CONNECTION=sync
QUEUE_FAILED_DRIVER=database
QUEUE_FAILED_TABLE=failed_jobs

# Database Queue
QUEUE_DATABASE_TABLE=jobs
QUEUE_DATABASE_QUEUE=default
QUEUE_DATABASE_RETRY_AFTER=90

# Redis Queue
QUEUE_REDIS_CONNECTION=default
QUEUE_REDIS_QUEUE=default
QUEUE_REDIS_RETRY_AFTER=90
QUEUE_REDIS_BLOCK_FOR=null

# Services
SERVICE_AUTO_DISCOVER=true
SERVICE_AUTO_DISCOVER_PATH=app/providers
```

## Using Environment Variables

1. Create a `.env` file in your project root:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your actual values:
```ini
APP_NAME=MyApp
APP_ENV=production
DB_PASSWORD=mysecretpassword
MAIL_USERNAME=myuser
MAIL_PASSWORD=mypassword
```

3. Access configuration in your code:
```python
from core.config.loader import get

# Get configuration values
app_name = get('app.name')  # Will use APP_NAME from .env
db_password = get('database.password')  # Will use DB_PASSWORD from .env
```

## Environment Variable Naming

Environment variables follow these naming conventions:

1. All uppercase
2. Words separated by underscores
3. Prefix matches the configuration section
4. Nested keys use underscores

Examples:
- `app.name` → `APP_NAME`
- `database.host` → `DB_HOST`
- `mail.smtp.username` → `MAIL_SMTP_USERNAME`

## Type Casting

The configuration system automatically casts environment variable values to appropriate types:

- `true`/`false` → boolean
- `null` → None
- `123` → integer
- `123.45` → float
- Other values → string

## Security Best Practices

1. Never commit `.env` file to version control
2. Always commit `.env.example` as a template
3. Use strong, unique values for sensitive data
4. Regularly rotate sensitive credentials
5. Use different values for different environments

## Environment-Specific Configuration

You can use different `.env` files for different environments:

```bash
.env.development
.env.testing
.env.production
```

The framework will load the appropriate file based on the `APP_ENV` value.

## Configuration Precedence

1. Environment variables (highest priority)
2. Configuration files
3. Default values (lowest priority)

## Accessing Configuration

```python
from core.config.loader import get

# Get a value with default
app_name = get('app.name', 'PyLevel')
db_host = get('database.host', '127.0.0.1')

# Get nested values
mail_username = get('mail.smtp.username')
redis_password = get('cache.redis.password')

# Check if value exists
if get('app.debug'):
    # Do something in debug mode
```

## Configuration Groups

You can group related configuration values:

```python
# Get all database configuration
db_config = get('database')

# Get all mail configuration
mail_config = get('mail')
```

## Configuration Validation

The framework validates configuration values:

1. Required values must be present
2. Values must be of correct type
3. Values must be within allowed ranges
4. Sensitive values must be properly set

## Configuration Caching

Configuration values are cached for better performance:

1. Environment variables are loaded once
2. Configuration files are cached
3. Default values are cached
4. Cache is cleared when configuration changes 