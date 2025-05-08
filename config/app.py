"""
Application configuration
"""
from core.config.loader import env

def config():
    return {
        'name': env('APP_NAME', 'PyLevel'),
        'env': env('APP_ENV', 'development'),
        'debug': env('APP_DEBUG', True),
        'url': env('APP_URL', 'http://localhost:8000'),
        'key': env('APP_KEY'),
        'timezone': env('APP_TIMEZONE', 'UTC'),
        'locale': env('APP_LOCALE', 'en'),
        'fallback_locale': env('APP_FALLBACK_LOCALE', 'en'),
        'faker_locale': env('APP_FAKER_LOCALE', 'en_US'),
        'cipher': env('APP_CIPHER', 'AES-256-CBC'),
        
        'server': {
            'host': env('SERVER_HOST', '127.0.0.1'),
            'port': env('SERVER_PORT', 8000),
            'workers': env('SERVER_WORKERS', 4),
        },
        
        'database': {
            'connection': env('DB_CONNECTION', 'mysql'),
            'host': env('DB_HOST', '127.0.0.1'),
            'port': env('DB_PORT', 3306),
            'database': env('DB_DATABASE', 'pylevel'),
            'username': env('DB_USERNAME', 'root'),
            'password': env('DB_PASSWORD', ''),
            'charset': env('DB_CHARSET', 'utf8mb4'),
            'collation': env('DB_COLLATION', 'utf8mb4_unicode_ci'),
            'prefix': env('DB_PREFIX', ''),
            'strict': env('DB_STRICT', True),
            'engine': env('DB_ENGINE'),
        },
        
        'cache': {
            'driver': env('CACHE_DRIVER', 'file'),
            'prefix': env('CACHE_PREFIX', 'pylevel_'),
            'ttl': env('CACHE_TTL', 3600),
        },
        
        'session': {
            'driver': env('SESSION_DRIVER', 'file'),
            'lifetime': env('SESSION_LIFETIME', 120),
            'expire_on_close': env('SESSION_EXPIRE_ON_CLOSE', False),
            'encrypt': env('SESSION_ENCRYPT', False),
            'cookie': env('SESSION_COOKIE', 'pylevel_session'),
            'path': env('SESSION_PATH', '/'),
            'domain': env('SESSION_DOMAIN'),
            'secure': env('SESSION_SECURE', False),
            'http_only': env('SESSION_HTTP_ONLY', True),
            'same_site': env('SESSION_SAME_SITE', 'lax'),
        },
        
        'logging': {
            'channel': env('LOG_CHANNEL', 'stack'),
            'level': env('LOG_LEVEL', 'debug'),
            'file': env('LOG_FILE', 'storage/logs/app.log'),
            'days': env('LOG_DAYS', 14),
        },
        
        'mail': {
            'driver': env('MAIL_DRIVER', 'smtp'),
            'host': env('MAIL_HOST', 'smtp.mailtrap.io'),
            'port': env('MAIL_PORT', 2525),
            'username': env('MAIL_USERNAME'),
            'password': env('MAIL_PASSWORD'),
            'encryption': env('MAIL_ENCRYPTION', 'tls'),
            'from_address': env('MAIL_FROM_ADDRESS'),
            'from_name': env('MAIL_FROM_NAME'),
            'timeout': env('MAIL_TIMEOUT'),
            'local_domain': env('MAIL_LOCAL_DOMAIN'),
        }
    } 