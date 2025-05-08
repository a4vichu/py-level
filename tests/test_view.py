"""
Test view functionality
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestView(unittest.TestCase):
    """Test view functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file
        self.env_file.write_text("""
# View Settings
VIEW_DRIVER=blade
VIEW_PATH=resources/views
VIEW_CACHE=true
VIEW_CACHE_PATH=storage/framework/views
VIEW_COMPILED_PATH=storage/framework/views/compiled
VIEW_EXTENSION=.blade.php
VIEW_NAMESPACE=App\\Views
VIEW_SHARED_PATH=resources/views/shared
VIEW_LAYOUT_PATH=resources/views/layouts
VIEW_COMPONENT_PATH=resources/views/components
VIEW_PARTIAL_PATH=resources/views/partials
VIEW_ERROR_PATH=resources/views/errors
VIEW_MAIL_PATH=resources/views/mail
VIEW_NOTIFICATION_PATH=resources/views/notifications

# Blade Settings
VIEW_BLADE_CACHE=true
VIEW_BLADE_CACHE_PATH=storage/framework/views/blade
VIEW_BLADE_COMPILED_PATH=storage/framework/views/blade/compiled
VIEW_BLADE_EXTENSION=.blade.php
VIEW_BLADE_NAMESPACE=App\\Views\\Blade
VIEW_BLADE_SHARED_PATH=resources/views/blade/shared
VIEW_BLADE_LAYOUT_PATH=resources/views/blade/layouts
VIEW_BLADE_COMPONENT_PATH=resources/views/blade/components
VIEW_BLADE_PARTIAL_PATH=resources/views/blade/partials
VIEW_BLADE_ERROR_PATH=resources/views/blade/errors
VIEW_BLADE_MAIL_PATH=resources/views/blade/mail
VIEW_BLADE_NOTIFICATION_PATH=resources/views/blade/notifications

# Twig Settings
VIEW_TWIG_CACHE=true
VIEW_TWIG_CACHE_PATH=storage/framework/views/twig
VIEW_TWIG_COMPILED_PATH=storage/framework/views/twig/compiled
VIEW_TWIG_EXTENSION=.twig
VIEW_TWIG_NAMESPACE=App\\Views\\Twig
VIEW_TWIG_SHARED_PATH=resources/views/twig/shared
VIEW_TWIG_LAYOUT_PATH=resources/views/twig/layouts
VIEW_TWIG_COMPONENT_PATH=resources/views/twig/components
VIEW_TWIG_PARTIAL_PATH=resources/views/twig/partials
VIEW_TWIG_ERROR_PATH=resources/views/twig/errors
VIEW_TWIG_MAIL_PATH=resources/views/twig/mail
VIEW_TWIG_NOTIFICATION_PATH=resources/views/twig/notifications

# Jinja2 Settings
VIEW_JINJA2_CACHE=true
VIEW_JINJA2_CACHE_PATH=storage/framework/views/jinja2
VIEW_JINJA2_COMPILED_PATH=storage/framework/views/jinja2/compiled
VIEW_JINJA2_EXTENSION=.jinja2
VIEW_JINJA2_NAMESPACE=App\\Views\\Jinja2
VIEW_JINJA2_SHARED_PATH=resources/views/jinja2/shared
VIEW_JINJA2_LAYOUT_PATH=resources/views/jinja2/layouts
VIEW_JINJA2_COMPONENT_PATH=resources/views/jinja2/components
VIEW_JINJA2_PARTIAL_PATH=resources/views/jinja2/partials
VIEW_JINJA2_ERROR_PATH=resources/views/jinja2/errors
VIEW_JINJA2_MAIL_PATH=resources/views/jinja2/mail
VIEW_JINJA2_NOTIFICATION_PATH=resources/views/jinja2/notifications
""")
        
        # Create view configuration file
        (self.config_dir / 'view.py').write_text("""
def config():
    return {
        'driver': env('VIEW_DRIVER', 'blade'),
        'path': env('VIEW_PATH', 'resources/views'),
        'cache': env('VIEW_CACHE', False),
        'cache_path': env('VIEW_CACHE_PATH', 'storage/framework/views'),
        'compiled_path': env('VIEW_COMPILED_PATH', 'storage/framework/views/compiled'),
        'extension': env('VIEW_EXTENSION', '.blade.php'),
        'namespace': env('VIEW_NAMESPACE', 'App\\\\Views'),
        'shared_path': env('VIEW_SHARED_PATH', 'resources/views/shared'),
        'layout_path': env('VIEW_LAYOUT_PATH', 'resources/views/layouts'),
        'component_path': env('VIEW_COMPONENT_PATH', 'resources/views/components'),
        'partial_path': env('VIEW_PARTIAL_PATH', 'resources/views/partials'),
        'error_path': env('VIEW_ERROR_PATH', 'resources/views/errors'),
        'mail_path': env('VIEW_MAIL_PATH', 'resources/views/mail'),
        'notification_path': env('VIEW_NOTIFICATION_PATH', 'resources/views/notifications'),
        
        'engines': {
            'blade': {
                'driver': 'blade',
                'cache': env('VIEW_BLADE_CACHE', False),
                'cache_path': env('VIEW_BLADE_CACHE_PATH', 'storage/framework/views/blade'),
                'compiled_path': env('VIEW_BLADE_COMPILED_PATH', 'storage/framework/views/blade/compiled'),
                'extension': env('VIEW_BLADE_EXTENSION', '.blade.php'),
                'namespace': env('VIEW_BLADE_NAMESPACE', 'App\\\\Views\\\\Blade'),
                'shared_path': env('VIEW_BLADE_SHARED_PATH', 'resources/views/blade/shared'),
                'layout_path': env('VIEW_BLADE_LAYOUT_PATH', 'resources/views/blade/layouts'),
                'component_path': env('VIEW_BLADE_COMPONENT_PATH', 'resources/views/blade/components'),
                'partial_path': env('VIEW_BLADE_PARTIAL_PATH', 'resources/views/blade/partials'),
                'error_path': env('VIEW_BLADE_ERROR_PATH', 'resources/views/blade/errors'),
                'mail_path': env('VIEW_BLADE_MAIL_PATH', 'resources/views/blade/mail'),
                'notification_path': env('VIEW_BLADE_NOTIFICATION_PATH', 'resources/views/blade/notifications'),
            },
            
            'twig': {
                'driver': 'twig',
                'cache': env('VIEW_TWIG_CACHE', False),
                'cache_path': env('VIEW_TWIG_CACHE_PATH', 'storage/framework/views/twig'),
                'compiled_path': env('VIEW_TWIG_COMPILED_PATH', 'storage/framework/views/twig/compiled'),
                'extension': env('VIEW_TWIG_EXTENSION', '.twig'),
                'namespace': env('VIEW_TWIG_NAMESPACE', 'App\\\\Views\\\\Twig'),
                'shared_path': env('VIEW_TWIG_SHARED_PATH', 'resources/views/twig/shared'),
                'layout_path': env('VIEW_TWIG_LAYOUT_PATH', 'resources/views/twig/layouts'),
                'component_path': env('VIEW_TWIG_COMPONENT_PATH', 'resources/views/twig/components'),
                'partial_path': env('VIEW_TWIG_PARTIAL_PATH', 'resources/views/twig/partials'),
                'error_path': env('VIEW_TWIG_ERROR_PATH', 'resources/views/twig/errors'),
                'mail_path': env('VIEW_TWIG_MAIL_PATH', 'resources/views/twig/mail'),
                'notification_path': env('VIEW_TWIG_NOTIFICATION_PATH', 'resources/views/twig/notifications'),
            },
            
            'jinja2': {
                'driver': 'jinja2',
                'cache': env('VIEW_JINJA2_CACHE', False),
                'cache_path': env('VIEW_JINJA2_CACHE_PATH', 'storage/framework/views/jinja2'),
                'compiled_path': env('VIEW_JINJA2_COMPILED_PATH', 'storage/framework/views/jinja2/compiled'),
                'extension': env('VIEW_JINJA2_EXTENSION', '.jinja2'),
                'namespace': env('VIEW_JINJA2_NAMESPACE', 'App\\\\Views\\\\Jinja2'),
                'shared_path': env('VIEW_JINJA2_SHARED_PATH', 'resources/views/jinja2/shared'),
                'layout_path': env('VIEW_JINJA2_LAYOUT_PATH', 'resources/views/jinja2/layouts'),
                'component_path': env('VIEW_JINJA2_COMPONENT_PATH', 'resources/views/jinja2/components'),
                'partial_path': env('VIEW_JINJA2_PARTIAL_PATH', 'resources/views/jinja2/partials'),
                'error_path': env('VIEW_JINJA2_ERROR_PATH', 'resources/views/jinja2/errors'),
                'mail_path': env('VIEW_JINJA2_MAIL_PATH', 'resources/views/jinja2/mail'),
                'notification_path': env('VIEW_JINJA2_NOTIFICATION_PATH', 'resources/views/jinja2/notifications'),
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
        """Test default view settings"""
        self.assertEqual(get('view.driver'), 'blade')
        self.assertEqual(get('view.path'), 'resources/views')
        self.assertTrue(get('view.cache'))
        self.assertEqual(get('view.cache_path'), 'storage/framework/views')
        self.assertEqual(get('view.compiled_path'), 'storage/framework/views/compiled')
        self.assertEqual(get('view.extension'), '.blade.php')
        self.assertEqual(get('view.namespace'), 'App\\Views')
        self.assertEqual(get('view.shared_path'), 'resources/views/shared')
        self.assertEqual(get('view.layout_path'), 'resources/views/layouts')
        self.assertEqual(get('view.component_path'), 'resources/views/components')
        self.assertEqual(get('view.partial_path'), 'resources/views/partials')
        self.assertEqual(get('view.error_path'), 'resources/views/errors')
        self.assertEqual(get('view.mail_path'), 'resources/views/mail')
        self.assertEqual(get('view.notification_path'), 'resources/views/notifications')
        
        print("✅ Default Settings")
        
    def test_engines(self):
        """Test view engines"""
        # Test Blade engine
        blade = get('view.engines.blade')
        self.assertEqual(blade['driver'], 'blade')
        self.assertTrue(blade['cache'])
        self.assertEqual(blade['cache_path'], 'storage/framework/views/blade')
        self.assertEqual(blade['compiled_path'], 'storage/framework/views/blade/compiled')
        self.assertEqual(blade['extension'], '.blade.php')
        self.assertEqual(blade['namespace'], 'App\\Views\\Blade')
        self.assertEqual(blade['shared_path'], 'resources/views/blade/shared')
        self.assertEqual(blade['layout_path'], 'resources/views/blade/layouts')
        self.assertEqual(blade['component_path'], 'resources/views/blade/components')
        self.assertEqual(blade['partial_path'], 'resources/views/blade/partials')
        self.assertEqual(blade['error_path'], 'resources/views/blade/errors')
        self.assertEqual(blade['mail_path'], 'resources/views/blade/mail')
        self.assertEqual(blade['notification_path'], 'resources/views/blade/notifications')
        
        # Test Twig engine
        twig = get('view.engines.twig')
        self.assertEqual(twig['driver'], 'twig')
        self.assertTrue(twig['cache'])
        self.assertEqual(twig['cache_path'], 'storage/framework/views/twig')
        self.assertEqual(twig['compiled_path'], 'storage/framework/views/twig/compiled')
        self.assertEqual(twig['extension'], '.twig')
        self.assertEqual(twig['namespace'], 'App\\Views\\Twig')
        self.assertEqual(twig['shared_path'], 'resources/views/twig/shared')
        self.assertEqual(twig['layout_path'], 'resources/views/twig/layouts')
        self.assertEqual(twig['component_path'], 'resources/views/twig/components')
        self.assertEqual(twig['partial_path'], 'resources/views/twig/partials')
        self.assertEqual(twig['error_path'], 'resources/views/twig/errors')
        self.assertEqual(twig['mail_path'], 'resources/views/twig/mail')
        self.assertEqual(twig['notification_path'], 'resources/views/twig/notifications')
        
        # Test Jinja2 engine
        jinja2 = get('view.engines.jinja2')
        self.assertEqual(jinja2['driver'], 'jinja2')
        self.assertTrue(jinja2['cache'])
        self.assertEqual(jinja2['cache_path'], 'storage/framework/views/jinja2')
        self.assertEqual(jinja2['compiled_path'], 'storage/framework/views/jinja2/compiled')
        self.assertEqual(jinja2['extension'], '.jinja2')
        self.assertEqual(jinja2['namespace'], 'App\\Views\\Jinja2')
        self.assertEqual(jinja2['shared_path'], 'resources/views/jinja2/shared')
        self.assertEqual(jinja2['layout_path'], 'resources/views/jinja2/layouts')
        self.assertEqual(jinja2['component_path'], 'resources/views/jinja2/components')
        self.assertEqual(jinja2['partial_path'], 'resources/views/jinja2/partials')
        self.assertEqual(jinja2['error_path'], 'resources/views/jinja2/errors')
        self.assertEqual(jinja2['mail_path'], 'resources/views/jinja2/mail')
        self.assertEqual(jinja2['notification_path'], 'resources/views/jinja2/notifications')
        
        print("✅ View Engines")
        
    def test_engine_override(self):
        """Test engine override"""
        # Set environment variables
        os.environ['VIEW_DRIVER'] = 'twig'
        os.environ['VIEW_TWIG_CACHE_PATH'] = 'storage/cache/twig'
        os.environ['VIEW_TWIG_EXTENSION'] = '.html.twig'
        
        # Reload configuration
        reload()
        
        # Test overridden values
        self.assertEqual(get('view.driver'), 'twig')
        self.assertEqual(get('view.engines.twig.cache_path'), 'storage/cache/twig')
        self.assertEqual(get('view.engines.twig.extension'), '.html.twig')
        
        print("✅ Engine Override")

if __name__ == '__main__':
    unittest.main() 