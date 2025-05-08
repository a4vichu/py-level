"""
Test services configuration
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestServices(unittest.TestCase):
    """Test services configuration"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file
        self.env_file.write_text("""
SERVICES_AUTO_DISCOVER=true
SERVICES_AUTO_DISCOVER_PATH=app/providers
SERVICES_AUTO_DISCOVER_NAMESPACE=app.providers
""")
        
        # Create test configuration file
        (self.config_dir / 'services.py').write_text("""
def config():
    return {
        'providers': [
            'DatabaseServiceProvider',
            'CacheServiceProvider',
            'QueueServiceProvider',
            'MailServiceProvider',
            'RouteServiceProvider',
            'ViewServiceProvider',
        ],
        
        'aliases': {
            'db': 'DatabaseServiceProvider',
            'cache': 'CacheServiceProvider',
            'queue': 'QueueServiceProvider',
            'mail': 'MailServiceProvider',
            'route': 'RouteServiceProvider',
            'view': 'ViewServiceProvider',
        },
        
        'auto_discover': env('SERVICES_AUTO_DISCOVER', True),
        'auto_discover_path': env('SERVICES_AUTO_DISCOVER_PATH', 'app/providers'),
        'auto_discover_namespace': env('SERVICES_AUTO_DISCOVER_NAMESPACE', 'app.providers'),
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
        
    def test_providers(self):
        """Test service providers"""
        providers = get('services.providers')
        self.assertIsInstance(providers, list)
        self.assertEqual(len(providers), 6)
        self.assertIn('DatabaseServiceProvider', providers)
        self.assertIn('CacheServiceProvider', providers)
        self.assertIn('QueueServiceProvider', providers)
        self.assertIn('MailServiceProvider', providers)
        self.assertIn('RouteServiceProvider', providers)
        self.assertIn('ViewServiceProvider', providers)
        
    def test_aliases(self):
        """Test service aliases"""
        aliases = get('services.aliases')
        self.assertIsInstance(aliases, dict)
        self.assertEqual(len(aliases), 6)
        self.assertEqual(aliases['db'], 'DatabaseServiceProvider')
        self.assertEqual(aliases['cache'], 'CacheServiceProvider')
        self.assertEqual(aliases['queue'], 'QueueServiceProvider')
        self.assertEqual(aliases['mail'], 'MailServiceProvider')
        self.assertEqual(aliases['route'], 'RouteServiceProvider')
        self.assertEqual(aliases['view'], 'ViewServiceProvider')
        
    def test_auto_discover(self):
        """Test auto discover settings"""
        self.assertTrue(get('services.auto_discover'))
        self.assertEqual(get('services.auto_discover_path'), 'app/providers')
        self.assertEqual(get('services.auto_discover_namespace'), 'app.providers')
        
    def test_environment_override(self):
        """Test environment variable override"""
        # Set environment variables
        os.environ['SERVICES_AUTO_DISCOVER'] = 'false'
        os.environ['SERVICES_AUTO_DISCOVER_PATH'] = 'custom/providers'
        os.environ['SERVICES_AUTO_DISCOVER_NAMESPACE'] = 'custom.providers'
        
        # Reload configuration
        reload()
        
        # Test overridden values
        self.assertFalse(get('services.auto_discover'))
        self.assertEqual(get('services.auto_discover_path'), 'custom/providers')
        self.assertEqual(get('services.auto_discover_namespace'), 'custom.providers')

if __name__ == '__main__':
    unittest.main() 