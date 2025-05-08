"""
Database configuration
"""
from core.config.loader import env

def config():
    return {
        'default': env('DB_CONNECTION', 'mysql'),
        
        'connections': {
            'mysql': {
                'driver': 'mysql',
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
            
            'sqlite': {
                'driver': 'sqlite',
                'database': env('DB_DATABASE', ':memory:'),
                'prefix': env('DB_PREFIX', ''),
            },
            
            'pgsql': {
                'driver': 'pgsql',
                'host': env('DB_HOST', '127.0.0.1'),
                'port': env('DB_PORT', 5432),
                'database': env('DB_DATABASE', 'pylevel'),
                'username': env('DB_USERNAME', 'root'),
                'password': env('DB_PASSWORD', ''),
                'charset': env('DB_CHARSET', 'utf8'),
                'prefix': env('DB_PREFIX', ''),
                'schema': env('DB_SCHEMA', 'public'),
                'sslmode': env('DB_SSL_MODE', 'prefer'),
            },
        },
        
        'migrations': {
            'path': env('DB_MIGRATIONS_PATH', 'database/migrations'),
            'table': env('DB_MIGRATIONS_TABLE', 'migrations'),
        },
        
        'model': {
            'namespace': env('DB_MODEL_NAMESPACE', 'app.models'),
            'path': env('DB_MODEL_PATH', 'app/models'),
            'suffix': env('DB_MODEL_SUFFIX', ''),
        },
        
        'query': {
            'log': env('DB_QUERY_LOG', True),
            'log_path': env('DB_QUERY_LOG_PATH', 'storage/logs/queries.log'),
        }
    } 