# Environment Variables Reference

## Application Settings
```ini
# Basic Application
APP_NAME=PyLevel
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000
APP_KEY=

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
SERVER_WORKERS=4
```

## Database Settings
```ini
# Database Connection
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
DB_ENGINE=

# Testing Database
DB_TESTING_DRIVER=sqlite
DB_TESTING_DATABASE=:memory:
DB_TESTING_PREFIX=

# Migration Settings
DB_MIGRATIONS_PATH=database/migrations
DB_MIGRATIONS_TABLE=migrations

# Model Settings
DB_MODEL_NAMESPACE=app.models
DB_MODEL_PATH=app/models
DB_MODEL_SUFFIX=

# Query Settings
DB_QUERY_LOG=true
DB_QUERY_LOG_PATH=storage/logs/queries.log
```

## Cache Settings
```ini
# Cache Configuration
CACHE_DRIVER=file
CACHE_PREFIX=pylevel_
CACHE_TTL=3600
CACHE_TAGS=true

# File Cache
CACHE_FILE_PATH=storage/framework/cache

# Redis Cache
CACHE_REDIS_HOST=127.0.0.1
CACHE_REDIS_PORT=6379
CACHE_REDIS_PASSWORD=null
CACHE_REDIS_DB=0

# Memcached
CACHE_MEMCACHED_HOST=127.0.0.1
CACHE_MEMCACHED_PORT=11211
CACHE_MEMCACHED_WEIGHT=100
```

## Session Settings
```ini
SESSION_DRIVER=file
SESSION_LIFETIME=120
```

## Logging Settings
```ini
LOG_CHANNEL=stack
LOG_LEVEL=debug
LOG_FILE=storage/logs/app.log
```

## Mail Settings
```ini
# Mail Configuration
MAIL_DRIVER=smtp
MAIL_FROM_ADDRESS=null
MAIL_FROM_NAME=null

# SMTP Mailer
MAIL_SMTP_HOST=smtp.mailtrap.io
MAIL_SMTP_PORT=2525
MAIL_SMTP_USERNAME=
MAIL_SMTP_PASSWORD=
MAIL_SMTP_ENCRYPTION=tls
MAIL_SMTP_TIMEOUT=
MAIL_SMTP_LOCAL_DOMAIN=

# AWS SES Mailer
MAIL_SES_KEY=
MAIL_SES_SECRET=
MAIL_SES_REGION=us-east-1

# Mailgun Mailer
MAIL_MAILGUN_DOMAIN=
MAIL_MAILGUN_SECRET=
MAIL_MAILGUN_ENDPOINT=api.mailgun.net
```

## Queue Settings
```ini
# Queue Configuration
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
```

## Service Settings
```ini
# Service Configuration
SERVICE_AUTO_DISCOVER=true
SERVICE_AUTO_DISCOVER_PATH=app/providers

# Service Providers (comma-separated)
SERVICE_PROVIDERS=core.providers.DatabaseServiceProvider,core.providers.CacheServiceProvider,core.providers.QueueServiceProvider,core.providers.MailServiceProvider,core.providers.RouteServiceProvider,core.providers.ViewServiceProvider

# Service Aliases
SERVICE_ALIAS_DB=core.database.Database
SERVICE_ALIAS_CACHE=core.cache.Cache
SERVICE_ALIAS_QUEUE=core.queue.Queue
SERVICE_ALIAS_MAIL=core.mail.Mail
SERVICE_ALIAS_ROUTE=core.routing.Router
SERVICE_ALIAS_VIEW=core.view.View
```

## Environment-Specific Variables

### Development
```ini
APP_ENV=development
APP_DEBUG=true
DB_CONNECTION=mysql
CACHE_DRIVER=file
QUEUE_CONNECTION=sync
```

### Testing
```ini
APP_ENV=testing
APP_DEBUG=true
DB_CONNECTION=sqlite
DB_DATABASE=:memory:
CACHE_DRIVER=file
QUEUE_CONNECTION=sync
```

### Production
```ini
APP_ENV=production
APP_DEBUG=false
DB_CONNECTION=mysql
CACHE_DRIVER=redis
QUEUE_CONNECTION=redis
```

## Security-Sensitive Variables
These variables should be set in production and never committed to version control:

```ini
# Application
APP_KEY=base64:your-secret-key-here

# Database
DB_PASSWORD=your-database-password

# Mail
MAIL_SMTP_USERNAME=your-mail-username
MAIL_SMTP_PASSWORD=your-mail-password
MAIL_SES_KEY=your-aws-key
MAIL_SES_SECRET=your-aws-secret
MAIL_MAILGUN_DOMAIN=your-mailgun-domain
MAIL_MAILGUN_SECRET=your-mailgun-secret

# Cache
CACHE_REDIS_PASSWORD=your-redis-password

# AWS
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

## Usage Notes

1. Create environment-specific files:
   - `.env.development`
   - `.env.testing`
   - `.env.production`

2. Set the environment:
   ```bash
   export APP_ENV=production
   ```

3. Load the appropriate file:
   ```bash
   cp .env.$APP_ENV .env
   ```

4. Update sensitive values:
   ```bash
   # Generate a new app key
   python slave key:generate
   
   # Set database password
   echo "DB_PASSWORD=your-secure-password" >> .env
   ```

5. Access in code:
   ```python
   from core.config.loader import get
   
   app_name = get('app.name')
   db_password = get('database.password')
   ``` 