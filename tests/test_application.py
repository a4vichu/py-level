"""
Test application core functionality
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestApplication(unittest.TestCase):
    """Test application core functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file
        self.env_file.write_text("""
# Application Settings
APP_NAME=PyLevel
APP_ENV=testing
APP_DEBUG=true
APP_URL=http://localhost:8000
APP_KEY=base64:test_key_32_bytes_long_for_testing
APP_TIMEZONE=UTC
APP_LOCALE=en
APP_FALLBACK_LOCALE=en
APP_FAKER_LOCALE=en_US

# Service Providers
SERVICE_PROVIDERS=app.providers.AppServiceProvider,app.providers.RouteServiceProvider

# Middleware
MIDDLEWARE=app.middleware.CorsMiddleware,app.middleware.CsrfMiddleware

# Error Handling
ERROR_REPORTING=true
ERROR_LOG_PATH=storage/logs/error.log
ERROR_VIEW_PATH=resources/views/errors

# Cache
CACHE_DRIVER=file
CACHE_PREFIX=test_
CACHE_TTL=3600

# Session
SESSION_DRIVER=file
SESSION_LIFETIME=120
SESSION_PATH=storage/framework/sessions

# View
VIEW_PATH=resources/views
VIEW_CACHE=true
VIEW_CACHE_PATH=storage/framework/views

# Storage
STORAGE_PATH=storage
PUBLIC_PATH=public
UPLOAD_PATH=storage/app/public
""")
        
        # Create application configuration file
        (self.config_dir / 'app.py').write_text("""
def config():
    return {
        'name': env('APP_NAME', 'PyLevel'),
        'env': env('APP_ENV', 'development'),
        'debug': env('APP_DEBUG', False),
        'url': env('APP_URL', 'http://localhost:8000'),
        'key': env('APP_KEY'),
        'timezone': env('APP_TIMEZONE', 'UTC'),
        'locale': env('APP_LOCALE', 'en'),
        'fallback_locale': env('APP_FALLBACK_LOCALE', 'en'),
        'faker_locale': env('APP_FAKER_LOCALE', 'en_US'),
        
        'providers': env('SERVICE_PROVIDERS', '').split(','),
        'middleware': env('MIDDLEWARE', '').split(','),
        
        'error': {
            'reporting': env('ERROR_REPORTING', True),
            'log_path': env('ERROR_LOG_PATH', 'storage/logs/error.log'),
            'view_path': env('ERROR_VIEW_PATH', 'resources/views/errors'),
        },
        
        'cache': {
            'driver': env('CACHE_DRIVER', 'file'),
            'prefix': env('CACHE_PREFIX', ''),
            'ttl': env('CACHE_TTL', 3600),
        },
        
        'session': {
            'driver': env('SESSION_DRIVER', 'file'),
            'lifetime': env('SESSION_LIFETIME', 120),
            'path': env('SESSION_PATH', 'storage/framework/sessions'),
        },
        
        'view': {
            'path': env('VIEW_PATH', 'resources/views'),
            'cache': env('VIEW_CACHE', False),
            'cache_path': env('VIEW_CACHE_PATH', 'storage/framework/views'),
        },
        
        'storage': {
            'path': env('STORAGE_PATH', 'storage'),
            'public_path': env('PUBLIC_PATH', 'public'),
            'upload_path': env('UPLOAD_PATH', 'storage/app/public'),
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
        
    def test_app_settings(self):
        """Test application settings"""
        # Test basic settings
        self.assertEqual(get('app.name'), 'PyLevel')
        self.assertEqual(get('app.env'), 'testing')
        self.assertTrue(get('app.debug'))
        self.assertEqual(get('app.url'), 'http://localhost:8000')
        
        # Test app key
        app_key = get('app.key')
        self.assertTrue(app_key)
        self.assertTrue(app_key.startswith('base64:'))
        self.assertTrue(len(app_key.split(':')[1]) >= 32)
        
        # Test localization settings
        self.assertEqual(get('app.timezone'), 'UTC')
        self.assertEqual(get('app.locale'), 'en')
        self.assertEqual(get('app.fallback_locale'), 'en')
        self.assertEqual(get('app.faker_locale'), 'en_US')
        
        print("✅ Application Settings")
        
    def test_service_providers(self):
        """Test service providers configuration"""
        providers = get('app.providers')
        self.assertIsInstance(providers, list)
        self.assertEqual(len(providers), 2)
        self.assertIn('app.providers.AppServiceProvider', providers)
        self.assertIn('app.providers.RouteServiceProvider', providers)
        
        print("✅ Service Providers")
        
    def test_middleware(self):
        """Test middleware configuration"""
        middleware = get('app.middleware')
        self.assertIsInstance(middleware, list)
        self.assertEqual(len(middleware), 2)
        self.assertIn('app.middleware.CorsMiddleware', middleware)
        self.assertIn('app.middleware.CsrfMiddleware', middleware)
        
        print("✅ Middleware")
        
    def test_error_handling(self):
        """Test error handling configuration"""
        # Test error reporting
        self.assertTrue(get('app.error.reporting'))
        
        # Test error paths
        self.assertEqual(get('app.error.log_path'), 'storage/logs/error.log')
        self.assertEqual(get('app.error.view_path'), 'resources/views/errors')
        
        print("✅ Error Handling")
        
    def test_cache_settings(self):
        """Test cache configuration"""
        # Test cache driver
        self.assertEqual(get('app.cache.driver'), 'file')
        
        # Test cache settings
        self.assertEqual(get('app.cache.prefix'), 'test_')
        self.assertEqual(get('app.cache.ttl'), 3600)
        
        print("✅ Cache Settings")
        
    def test_session_settings(self):
        """Test session configuration"""
        # Test session driver
        self.assertEqual(get('app.session.driver'), 'file')
        
        # Test session settings
        self.assertEqual(get('app.session.lifetime'), 120)
        self.assertEqual(get('app.session.path'), 'storage/framework/sessions')
        
        print("✅ Session Settings")
        
    def test_view_settings(self):
        """Test view configuration"""
        # Test view paths
        self.assertEqual(get('app.view.path'), 'resources/views')
        self.assertEqual(get('app.view.cache_path'), 'storage/framework/views')
        
        # Test view cache
        self.assertTrue(get('app.view.cache'))
        
        print("✅ View Settings")
        
    def test_storage_settings(self):
        """Test storage configuration"""
        # Test storage paths
        self.assertEqual(get('app.storage.path'), 'storage')
        self.assertEqual(get('app.storage.public_path'), 'public')
        self.assertEqual(get('app.storage.upload_path'), 'storage/app/public')
        
        print("✅ Storage Settings")
        
    def test_environment_override(self):
        """Test environment variable override"""
        # Set environment variables
        os.environ['APP_NAME'] = 'TestApp'
        os.environ['APP_DEBUG'] = 'false'
        os.environ['APP_URL'] = 'https://test.com'
        
        # Reload configuration
        reload()
        
        # Test overridden values
        self.assertEqual(get('app.name'), 'TestApp')
        self.assertFalse(get('app.debug'))
        self.assertEqual(get('app.url'), 'https://test.com')
        
        print("✅ Environment Override")

if __name__ == '__main__':
    unittest.main() 