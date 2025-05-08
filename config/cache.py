"""
Cache configuration
"""
from core.config.loader import env

def config():
    return {
        'default': env('CACHE_DRIVER', 'file'),
        
        'stores': {
            'file': {
                'driver': 'file',
                'path': env('CACHE_FILE_PATH', 'storage/framework/cache'),
            },
            
            'redis': {
                'driver': 'redis',
                'connection': env('CACHE_REDIS_CONNECTION', 'default'),
                'host': env('CACHE_REDIS_HOST', '127.0.0.1'),
                'port': env('CACHE_REDIS_PORT', 6379),
                'password': env('CACHE_REDIS_PASSWORD'),
                'database': env('CACHE_REDIS_DB', 0),
            },
            
            'memcached': {
                'driver': 'memcached',
                'persistent_id': env('MEMCACHED_PERSISTENT_ID'),
                'sasl': [
                    env('MEMCACHED_USERNAME'),
                    env('MEMCACHED_PASSWORD'),
                ],
                'options': {
                    'connect_timeout': 2000,
                },
                'servers': [
                    {
                        'host': env('MEMCACHED_HOST', '127.0.0.1'),
                        'port': env('MEMCACHED_PORT', 11211),
                        'weight': env('MEMCACHED_WEIGHT', 100),
                    }
                ],
            },
        },
        
        'prefix': env('CACHE_PREFIX', 'pylevel_'),
        'ttl': env('CACHE_TTL', 3600),  # 1 hour
        'tags': env('CACHE_TAGS', True),
    } 