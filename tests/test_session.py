"""
Test session functionality
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestSession(unittest.TestCase):
    """Test session functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file
        self.env_file.write_text("""
# Session Settings
SESSION_DRIVER=file
SESSION_LIFETIME=120
SESSION_EXPIRE_ON_CLOSE=true
SESSION_ENCRYPT=true
SESSION_FILES=storage/framework/sessions
SESSION_CONNECTION=default
SESSION_STORE=
SESSION_PREFIX=test_
SESSION_SECURE=true
SESSION_HTTP_ONLY=true
SESSION_SAME_SITE=lax
SESSION_COOKIE=pylevel_session
SESSION_PATH=/
SESSION_DOMAIN=null
SESSION_SECURE_COOKIE=true

# File Session
SESSION_FILE_PATH=storage/framework/sessions
SESSION_FILE_PERMISSIONS=0644

# Redis Session
SESSION_REDIS_CONNECTION=default
SESSION_REDIS_HOST=127.0.0.1
SESSION_REDIS_PORT=6379
SESSION_REDIS_PASSWORD=null
SESSION_REDIS_DB=0
SESSION_REDIS_PREFIX=test_

# Database Session
SESSION_DB_CONNECTION=default
SESSION_DB_TABLE=sessions
SESSION_DB_LOTTERY=2
SESSION_DB_LOCK_TIMEOUT=10

# Cookie Session
SESSION_COOKIE_NAME=session
SESSION_COOKIE_PATH=/
SESSION_COOKIE_DOMAIN=null
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTP_ONLY=true
SESSION_COOKIE_SAME_SITE=strict
SESSION_COOKIE_MAX_AGE=7200

# Array Session
SESSION_ARRAY_LIFETIME=120
SESSION_ARRAY_PREFIX=test_

# Null Session
SESSION_NULL_LIFETIME=120
SESSION_NULL_PREFIX=test_
""")
        
        # Create session configuration file
        (self.config_dir / 'session.py').write_text("""
def config():
    store = env('SESSION_STORE', '')
    return {
        'driver': env('SESSION_DRIVER', 'file'),
        'lifetime': env('SESSION_LIFETIME', 120),
        'expire_on_close': env('SESSION_EXPIRE_ON_CLOSE', True),
        'encrypt': env('SESSION_ENCRYPT', True),
        'files': env('SESSION_FILES', 'storage/framework/sessions'),
        'connection': env('SESSION_CONNECTION', 'default'),
        'store': None if not store else store,
        'prefix': env('SESSION_PREFIX', ''),
        'secure': env('SESSION_SECURE', True),
        'http_only': env('SESSION_HTTP_ONLY', True),
        'same_site': env('SESSION_SAME_SITE', 'lax'),
        'cookie': env('SESSION_COOKIE', 'pylevel_session'),
        'path': env('SESSION_PATH', '/'),
        'domain': env('SESSION_DOMAIN'),
        'secure_cookie': env('SESSION_SECURE_COOKIE', True),
        'partitioned': False,
        'lottery': [2, 100],
        'table': env('SESSION_DB_TABLE', 'sessions'),
        
        'stores': {
            'file': {
                'driver': 'file',
                'path': env('SESSION_FILE_PATH', 'storage/framework/sessions'),
                'permissions': env('SESSION_FILE_PERMISSIONS', '0644'),
            },
            
            'redis': {
                'driver': 'redis',
                'connection': env('SESSION_REDIS_CONNECTION', 'default'),
                'host': env('SESSION_REDIS_HOST', '127.0.0.1'),
                'port': env('SESSION_REDIS_PORT', 6379),
                'password': env('SESSION_REDIS_PASSWORD'),
                'database': env('SESSION_REDIS_DB', 0),
                'prefix': 'pylevel_session:',
            },
            
            'memcached': {
                'driver': 'memcached',
                'persistent_id': 'pylevel_session',
                'sasl': [],
                'options': {},
                'servers': [
                    {'host': '127.0.0.1', 'port': 11211, 'weight': 100}
                ],
            },
            
            'dynamodb': {
                'driver': 'dynamodb',
                'key': 'your-key',
                'secret': 'your-secret',
                'region': 'us-east-1',
                'table': 'sessions',
                'endpoint': None,
            },
            
            'database': {
                'driver': 'database',
                'connection': env('SESSION_DB_CONNECTION', 'default'),
                'table': env('SESSION_DB_TABLE', 'sessions'),
                'lottery': env('SESSION_DB_LOTTERY', 2),
                'lock_timeout': env('SESSION_DB_LOCK_TIMEOUT', 10),
            },
            
            'cookie': {
                'driver': 'cookie',
                'name': env('SESSION_COOKIE_NAME', 'session'),
                'path': env('SESSION_COOKIE_PATH', '/'),
                'domain': env('SESSION_COOKIE_DOMAIN'),
                'secure': env('SESSION_COOKIE_SECURE', True),
                'http_only': env('SESSION_COOKIE_HTTP_ONLY', True),
                'same_site': env('SESSION_COOKIE_SAME_SITE', 'strict'),
                'max_age': env('SESSION_COOKIE_MAX_AGE', 7200),
                'encrypt': env('SESSION_ENCRYPT', True),
            },
            
            'array': {
                'driver': 'array',
                'lifetime': env('SESSION_ARRAY_LIFETIME', 120),
                'prefix': env('SESSION_ARRAY_PREFIX', ''),
            },
            
            'null': {
                'driver': 'null',
                'lifetime': env('SESSION_NULL_LIFETIME', 120),
                'prefix': env('SESSION_NULL_PREFIX', ''),
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
        """Test default session settings"""
        self.assertEqual(get('session.driver'), 'file')
        self.assertEqual(get('session.lifetime'), 120)
        self.assertTrue(get('session.expire_on_close'))
        self.assertTrue(get('session.encrypt'))
        self.assertEqual(get('session.files'), 'storage/framework/sessions')
        self.assertEqual(get('session.connection'), 'default')
        self.assertEqual(get('session.table'), 'sessions')
        self.assertEqual(get('session.store'), None)
        self.assertEqual(get('session.lottery'), [2, 100])
        self.assertEqual(get('session.cookie'), 'pylevel_session')
        self.assertEqual(get('session.path'), '/')
        self.assertEqual(get('session.domain'), 'null')
        self.assertTrue(get('session.secure'))
        self.assertTrue(get('session.http_only'))
        self.assertEqual(get('session.same_site'), 'lax')
        self.assertEqual(get('session.partitioned'), False)
        
        print("✅ Default Settings")
        
    def test_stores(self):
        """Test session stores"""
        # Test file store
        file = get('session.stores.file')
        self.assertEqual(file['driver'], 'file')
        self.assertEqual(file['path'], 'storage/framework/sessions')
        
        # Test cookie store
        cookie = get('session.stores.cookie')
        self.assertEqual(cookie['driver'], 'cookie')
        self.assertTrue(cookie['encrypt'])
        
        # Test database store
        database = get('session.stores.database')
        self.assertEqual(database['driver'], 'database')
        self.assertEqual(database['table'], 'sessions')
        self.assertEqual(database['connection'], 'default')
        
        # Test Redis store
        redis = get('session.stores.redis')
        self.assertEqual(redis['driver'], 'redis')
        self.assertEqual(redis['connection'], 'default')
        self.assertEqual(redis['host'], '127.0.0.1')
        self.assertEqual(redis['password'], 'null')
        self.assertEqual(redis['port'], 6379)
        self.assertEqual(redis['database'], 0)
        self.assertEqual(redis['prefix'], 'pylevel_session:')
        
        # Test memcached store
        memcached = get('session.stores.memcached')
        self.assertEqual(memcached['driver'], 'memcached')
        self.assertEqual(memcached['persistent_id'], 'pylevel_session')
        self.assertEqual(memcached['sasl'], [])
        self.assertEqual(memcached['options'], {})
        self.assertEqual(memcached['servers'], [
            {'host': '127.0.0.1', 'port': 11211, 'weight': 100}
        ])
        
        # Test dynamodb store
        dynamodb = get('session.stores.dynamodb')
        self.assertEqual(dynamodb['driver'], 'dynamodb')
        self.assertEqual(dynamodb['key'], 'your-key')
        self.assertEqual(dynamodb['secret'], 'your-secret')
        self.assertEqual(dynamodb['region'], 'us-east-1')
        self.assertEqual(dynamodb['table'], 'sessions')
        self.assertEqual(dynamodb['endpoint'], None)
        
        print("✅ Session Stores")
        
    def test_store_override(self):
        """Test store override"""
        # Set environment variables
        os.environ['SESSION_DRIVER'] = 'redis'
        os.environ['SESSION_REDIS_HOST'] = 'redis.example.com'
        os.environ['SESSION_REDIS_PORT'] = '6380'
        
        # Reload configuration
        reload()
        
        # Test overridden values
        self.assertEqual(get('session.driver'), 'redis')
        self.assertEqual(get('session.stores.redis.host'), 'redis.example.com')
        self.assertEqual(get('session.stores.redis.port'), 6380)
        
        print("✅ Store Override")

if __name__ == '__main__':
    unittest.main() 