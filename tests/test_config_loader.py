"""
Test configuration loader
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestConfigLoader(unittest.TestCase):
    """Test configuration loader"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.env_test_file = self.temp_dir / '.env.testing'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment files
        self.env_file.write_text("""
APP_NAME=PyLevel
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000
APP_KEY=base64:test_key_32_bytes_long_for_testing
APP_TIMEZONE=UTC
APP_LOCALE=en
APP_FALLBACK_LOCALE=en
APP_FAKER_LOCALE=en_US
APP_CIPHER=AES-256-CBC

DB_CONNECTION=sqlite
DB_DATABASE=:memory:
DB_PREFIX=test_

CACHE_DRIVER=file
CACHE_PREFIX=test_
CACHE_TTL=3600
CACHE_TAGS=true

QUEUE_CONNECTION=sync
QUEUE_FAILED_DRIVER=database
QUEUE_FAILED_TABLE=failed_jobs

MAIL_DRIVER=array
MAIL_FROM_ADDRESS=test@example.com
MAIL_FROM_NAME=Test

SESSION_DRIVER=file
SESSION_LIFETIME=120

LOG_CHANNEL=stack
LOG_LEVEL=debug
LOG_FILE=storage/logs/app.log
""")
        
        self.env_test_file.write_text("""
APP_ENV=testing
APP_DEBUG=true
DB_CONNECTION=sqlite
DB_DATABASE=:memory:
CACHE_DRIVER=file
QUEUE_CONNECTION=sync
""")
        
        # Create test configuration files
        (self.config_dir / 'app.py').write_text("""
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
    }
""")
        
        (self.config_dir / 'database.py').write_text("""
def config():
    return {
        'default': env('DB_CONNECTION', 'mysql'),
        'connections': {
            'sqlite': {
                'driver': 'sqlite',
                'database': env('DB_DATABASE', ':memory:'),
                'prefix': env('DB_PREFIX', ''),
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
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_load_environment(self):
        """Test loading environment variables"""
        # Test loading default .env file
        self.loader.load_environment(str(self.env_file))
        self.assertEqual(os.getenv('APP_NAME'), 'PyLevel')
        self.assertEqual(os.getenv('APP_ENV'), 'development')
        
        # Test loading environment-specific .env file
        os.environ.clear()  # Clear all environment variables
        os.environ['APP_ENV'] = 'testing'  # Set environment before loading
        self.loader.load_environment(str(self.env_test_file))  # Load testing env file directly
        self.assertEqual(os.getenv('APP_ENV'), 'testing')
        
    def test_load_config(self):
        """Test loading configuration files"""
        # Load configuration files
        self.loader.load_config(str(self.config_dir))
        
        # Test app configuration
        self.assertEqual(self.loader.get('app.name'), 'PyLevel')
        self.assertEqual(self.loader.get('app.env'), 'development')
        self.assertTrue(self.loader.get('app.debug'))
        
        # Test database configuration
        self.assertEqual(self.loader.get('database.default'), 'sqlite')
        self.assertEqual(self.loader.get('database.connections.sqlite.driver'), 'sqlite')
        self.assertEqual(self.loader.get('database.connections.sqlite.database'), ':memory:')
        
    def test_get(self):
        """Test getting configuration values"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Test getting values
        self.assertEqual(self.loader.get('app.name'), 'PyLevel')
        self.assertEqual(self.loader.get('app.nonexistent', 'default'), 'default')
        
    def test_set(self):
        """Test setting configuration values"""
        # Set value
        self.loader.set('app.name', 'Test')
        self.assertEqual(self.loader.get('app.name'), 'Test')
        
        # Set nested value
        self.loader.set('app.server.host', '127.0.0.1')
        self.assertEqual(self.loader.get('app.server.host'), '127.0.0.1')
        
    def test_has(self):
        """Test checking configuration keys"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Test checking keys
        self.assertTrue(self.loader.has('app.name'))
        self.assertFalse(self.loader.has('app.nonexistent'))
        
    def test_all(self):
        """Test getting all configuration values"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Test getting all values
        config = self.loader.all()
        self.assertIn('app', config)
        self.assertIn('database', config)
        
    def test_clear(self):
        """Test clearing configuration values"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Clear configuration
        self.loader.clear()
        self.assertEqual(self.loader.all(), {})
        
    def test_reload(self):
        """Test reloading configuration values"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Clear configuration
        self.loader.clear()
        
        # Reload configuration
        self.loader.reload()
        self.assertIn('app', self.loader.all())
        self.assertIn('database', self.loader.all())
        
    def test_env(self):
        """Test getting environment variables"""
        # Test getting existing variable
        self.assertEqual(env('APP_NAME', 'default'), 'PyLevel')
        
        # Test getting nonexistent variable
        self.assertEqual(env('NONEXISTENT', 'default'), 'default')
        
    def test_get_function(self):
        """Test getting configuration values using function"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Test getting values
        self.assertEqual(get('app.name'), 'PyLevel')
        self.assertEqual(get('app.nonexistent', 'default'), 'default')
        
    def test_set_function(self):
        """Test setting configuration values using function"""
        # Set value
        set('app.name', 'Test')
        self.assertEqual(get('app.name'), 'Test')
        
        # Set nested value
        set('app.server.host', '127.0.0.1')
        self.assertEqual(get('app.server.host'), '127.0.0.1')
        
    def test_has_function(self):
        """Test checking configuration keys using function"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Test checking keys
        self.assertTrue(has('app.name'))
        self.assertFalse(has('app.nonexistent'))
        
    def test_all_function(self):
        """Test getting all configuration values using function"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Test getting all values
        config = all()
        self.assertIn('app', config)
        self.assertIn('database', config)
        
    def test_clear_function(self):
        """Test clearing configuration values using function"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Clear configuration
        clear()
        self.assertEqual(all(), {})
        
    def test_reload_function(self):
        """Test reloading configuration values using function"""
        # Load configuration
        self.loader.load_environment(str(self.env_file))
        self.loader.load_config(str(self.config_dir))
        
        # Clear configuration
        clear()
        
        # Reload configuration
        reload()
        self.assertIn('app', all())
        self.assertIn('database', all())

if __name__ == '__main__':
    unittest.main() 