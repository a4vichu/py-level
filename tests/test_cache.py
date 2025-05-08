"""
Test cache functionality
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestCache(unittest.TestCase):
    """Test cache functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file
        self.env_file.write_text("""
# Cache Settings
CACHE_DRIVER=file
CACHE_PREFIX=laravel_cache
CACHE_TTL=3600

# File Cache Settings
CACHE_FILE_DRIVER=file
CACHE_FILE_PATH=storage/framework/cache
CACHE_FILE_PREFIX=file_cache
CACHE_FILE_TTL=3600

# Redis Cache Settings
CACHE_REDIS_DRIVER=redis
CACHE_REDIS_HOST=127.0.0.1
CACHE_REDIS_PASSWORD=
CACHE_REDIS_PORT=6379
CACHE_REDIS_DB=0
CACHE_REDIS_PREFIX=redis_cache
CACHE_REDIS_TTL=3600

# Memcached Cache Settings
CACHE_MEMCACHED_DRIVER=memcached
CACHE_MEMCACHED_HOST=127.0.0.1
CACHE_MEMCACHED_PORT=11211
CACHE_MEMCACHED_WEIGHT=100
CACHE_MEMCACHED_PREFIX=memcached_cache
CACHE_MEMCACHED_TTL=3600

# Database Cache Settings
CACHE_DATABASE_DRIVER=database
CACHE_DATABASE_TABLE=cache
CACHE_DATABASE_CONNECTION=mysql
CACHE_DATABASE_PREFIX=database_cache
CACHE_DATABASE_TTL=3600

# Array Cache Settings
CACHE_ARRAY_DRIVER=array
CACHE_ARRAY_PREFIX=array_cache
CACHE_ARRAY_TTL=3600

# Null Cache Settings
CACHE_NULL_DRIVER=null
CACHE_NULL_PREFIX=null_cache
CACHE_NULL_TTL=3600
""")
        
        # Create cache configuration file
        (self.config_dir / 'cache.py').write_text("""
def config():
    return {
        'default': env('CACHE_DRIVER', 'file'),
        'prefix': env('CACHE_PREFIX', 'laravel_cache'),
        'ttl': env('CACHE_TTL', 3600),
        
        'stores': {
            'file': {
                'driver': env('CACHE_FILE_DRIVER', 'file'),
                'path': env('CACHE_FILE_PATH', 'storage/framework/cache'),
                'prefix': env('CACHE_FILE_PREFIX', 'file_cache'),
                'ttl': env('CACHE_FILE_TTL', 3600),
            },
            
            'redis': {
                'driver': env('CACHE_REDIS_DRIVER', 'redis'),
                'host': env('CACHE_REDIS_HOST', '127.0.0.1'),
                'password': env('CACHE_REDIS_PASSWORD', None),
                'port': env('CACHE_REDIS_PORT', 6379),
                'database': env('CACHE_REDIS_DB', 0),
                'prefix': env('CACHE_REDIS_PREFIX', 'redis_cache'),
                'ttl': env('CACHE_REDIS_TTL', 3600),
            },
            
            'memcached': {
                'driver': env('CACHE_MEMCACHED_DRIVER', 'memcached'),
                'host': env('CACHE_MEMCACHED_HOST', '127.0.0.1'),
                'port': env('CACHE_MEMCACHED_PORT', 11211),
                'weight': env('CACHE_MEMCACHED_WEIGHT', 100),
                'prefix': env('CACHE_MEMCACHED_PREFIX', 'memcached_cache'),
                'ttl': env('CACHE_MEMCACHED_TTL', 3600),
            },
            
            'database': {
                'driver': env('CACHE_DATABASE_DRIVER', 'database'),
                'table': env('CACHE_DATABASE_TABLE', 'cache'),
                'connection': env('CACHE_DATABASE_CONNECTION', 'mysql'),
                'prefix': env('CACHE_DATABASE_PREFIX', 'database_cache'),
                'ttl': env('CACHE_DATABASE_TTL', 3600),
            },
            
            'array': {
                'driver': env('CACHE_ARRAY_DRIVER', 'array'),
                'prefix': env('CACHE_ARRAY_PREFIX', 'array_cache'),
                'ttl': env('CACHE_ARRAY_TTL', 3600),
            },
            
            'null': {
                'driver': env('CACHE_NULL_DRIVER', 'null'),
                'prefix': env('CACHE_NULL_PREFIX', 'null_cache'),
                'ttl': env('CACHE_NULL_TTL', 3600),
            },
        },
    }
""")
        
        # Create test module
        (self.temp_dir / '__init__.py').touch()
        (self.config_dir / '__init__.py').touch()
        
        # Add test directory to Python path
        import sys
        sys.path.insert(0, str(self.temp_dir))
        
        # Create config loader
        self.loader = ConfigLoader()
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_default_settings(self):
        """Test default cache settings"""
        self.assertEqual(get('cache.default'), 'file')
        self.assertEqual(get('cache.prefix'), 'laravel_cache')
        self.assertEqual(get('cache.ttl'), 3600)
        
        print("✅ Default Settings")
        
    def test_stores(self):
        """Test cache stores"""
        # Test file store
        file = get('cache.stores.file')
        self.assertEqual(file['driver'], 'file')
        self.assertEqual(file['path'], 'storage/framework/cache')
        self.assertEqual(file['prefix'], 'file_cache')
        self.assertEqual(file['ttl'], 3600)
        
        # Test Redis store
        redis = get('cache.stores.redis')
        self.assertEqual(redis['driver'], 'redis')
        self.assertEqual(redis['host'], '127.0.0.1')
        self.assertEqual(redis['password'], '')
        self.assertEqual(redis['port'], 6379)
        self.assertEqual(redis['database'], 0)
        self.assertEqual(redis['prefix'], 'redis_cache')
        self.assertEqual(redis['ttl'], 3600)
        
        # Test Memcached store
        memcached = get('cache.stores.memcached')
        self.assertEqual(memcached['driver'], 'memcached')
        self.assertEqual(memcached['host'], '127.0.0.1')
        self.assertEqual(memcached['port'], 11211)
        self.assertEqual(memcached['weight'], 100)
        self.assertEqual(memcached['prefix'], 'memcached_cache')
        self.assertEqual(memcached['ttl'], 3600)
        
        # Test database store
        database = get('cache.stores.database')
        self.assertEqual(database['driver'], 'database')
        self.assertEqual(database['table'], 'cache')
        self.assertEqual(database['connection'], 'mysql')
        self.assertEqual(database['prefix'], 'database_cache')
        self.assertEqual(database['ttl'], 3600)
        
        # Test array store
        array = get('cache.stores.array')
        self.assertEqual(array['driver'], 'array')
        self.assertEqual(array['prefix'], 'array_cache')
        self.assertEqual(array['ttl'], 3600)
        
        # Test null store
        null = get('cache.stores.null')
        self.assertEqual(null['driver'], 'null')
        self.assertEqual(null['prefix'], 'null_cache')
        self.assertEqual(null['ttl'], 3600)
        
        print("✅ Cache Stores")
        
    def test_store_override(self):
        """Test store override"""
        # Set environment variables
        os.environ['CACHE_DRIVER'] = 'redis'
        os.environ['CACHE_REDIS_HOST'] = 'redis.example.com'
        os.environ['CACHE_REDIS_TTL'] = '7200'
        
        # Reload configuration
        reload()
        
        # Test overridden values
        self.assertEqual(get('cache.default'), 'redis')
        self.assertEqual(get('cache.stores.redis.host'), 'redis.example.com')
        self.assertEqual(get('cache.stores.redis.ttl'), 7200)
        
        print("✅ Store Override")

if __name__ == '__main__':
    unittest.main() 