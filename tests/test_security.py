"""
Test security features
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestSecurity(unittest.TestCase):
    """Test security features"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file with security settings
        self.env_file.write_text("""
# Application Security
APP_KEY=base64:test_key_32_bytes_long_for_testing
APP_CIPHER=AES-256-CBC
APP_DEBUG=false
APP_ENV=production

# Session Security
SESSION_DRIVER=file
SESSION_LIFETIME=120
SESSION_SECURE=true
SESSION_HTTP_ONLY=true
SESSION_SAME_SITE=strict

# Cookie Security
COOKIE_SECURE=true
COOKIE_HTTP_ONLY=true
COOKIE_SAME_SITE=strict

# CSRF Protection
CSRF_ENABLED=true
CSRF_TOKEN_LENGTH=32
CSRF_TOKEN_NAME=_csrf_token

# XSS Protection
XSS_PROTECTION=true
CONTENT_SECURITY_POLICY=true
X_FRAME_OPTIONS=SAMEORIGIN
X_CONTENT_TYPE_OPTIONS=nosniff
X_XSS_PROTECTION=1; mode=block

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_ATTEMPTS=60
RATE_LIMIT_DECAY_MINUTES=1

# Password Hashing
PASSWORD_HASH_ALGO=bcrypt
PASSWORD_HASH_ROUNDS=12

# SSL/TLS
FORCE_HTTPS=true
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem

# Database Security
DB_SSL_MODE=require
DB_SSL_VERIFY=true
""")
        
        # Create security configuration file
        (self.config_dir / 'security.py').write_text("""
def config():
    return {
        'app': {
            'key': env('APP_KEY'),
            'cipher': env('APP_CIPHER', 'AES-256-CBC'),
            'debug': env('APP_DEBUG', False),
            'env': env('APP_ENV', 'production'),
        },
        
        'session': {
            'driver': env('SESSION_DRIVER', 'file'),
            'lifetime': env('SESSION_LIFETIME', 120),
            'secure': env('SESSION_SECURE', True),
            'http_only': env('SESSION_HTTP_ONLY', True),
            'same_site': env('SESSION_SAME_SITE', 'strict'),
        },
        
        'cookie': {
            'secure': env('COOKIE_SECURE', True),
            'http_only': env('COOKIE_HTTP_ONLY', True),
            'same_site': env('COOKIE_SAME_SITE', 'strict'),
        },
        
        'csrf': {
            'enabled': env('CSRF_ENABLED', True),
            'token_length': env('CSRF_TOKEN_LENGTH', 32),
            'token_name': env('CSRF_TOKEN_NAME', '_csrf_token'),
        },
        
        'xss': {
            'protection': env('XSS_PROTECTION', True),
            'content_security_policy': env('CONTENT_SECURITY_POLICY', True),
            'x_frame_options': env('X_FRAME_OPTIONS', 'SAMEORIGIN'),
            'x_content_type_options': env('X_CONTENT_TYPE_OPTIONS', 'nosniff'),
            'x_xss_protection': env('X_XSS_PROTECTION', '1; mode=block'),
        },
        
        'rate_limit': {
            'enabled': env('RATE_LIMIT_ENABLED', True),
            'attempts': env('RATE_LIMIT_ATTEMPTS', 60),
            'decay_minutes': env('RATE_LIMIT_DECAY_MINUTES', 1),
        },
        
        'password': {
            'hash_algo': env('PASSWORD_HASH_ALGO', 'bcrypt'),
            'hash_rounds': env('PASSWORD_HASH_ROUNDS', 12),
        },
        
        'ssl': {
            'force_https': env('FORCE_HTTPS', True),
            'cert_path': env('SSL_CERT_PATH'),
            'key_path': env('SSL_KEY_PATH'),
        },
        
        'database': {
            'ssl_mode': env('DB_SSL_MODE', 'require'),
            'ssl_verify': env('DB_SSL_VERIFY', True),
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
        
    def test_app_security(self):
        """Test application security settings"""
        # Test app key
        app_key = get('security.app.key')
        self.assertTrue(app_key)
        self.assertTrue(app_key.startswith('base64:'))
        self.assertTrue(len(app_key.split(':')[1]) >= 32)  # At least 32 bytes
        
        # Test cipher
        self.assertEqual(get('security.app.cipher'), 'AES-256-CBC')
        
        # Test debug mode
        self.assertFalse(get('security.app.debug'))
        
        # Test environment
        self.assertEqual(get('security.app.env'), 'production')
        
        print("✅ Application Security Settings")
        
    def test_session_security(self):
        """Test session security settings"""
        # Test session driver
        self.assertEqual(get('security.session.driver'), 'file')
        
        # Test session lifetime
        self.assertEqual(get('security.session.lifetime'), 120)
        
        # Test session security flags
        self.assertTrue(get('security.session.secure'))
        self.assertTrue(get('security.session.http_only'))
        self.assertEqual(get('security.session.same_site'), 'strict')
        
        print("✅ Session Security Settings")
        
    def test_cookie_security(self):
        """Test cookie security settings"""
        # Test cookie security flags
        self.assertTrue(get('security.cookie.secure'))
        self.assertTrue(get('security.cookie.http_only'))
        self.assertEqual(get('security.cookie.same_site'), 'strict')
        
        print("✅ Cookie Security Settings")
        
    def test_csrf_protection(self):
        """Test CSRF protection settings"""
        # Test CSRF enabled
        self.assertTrue(get('security.csrf.enabled'))
        
        # Test CSRF token settings
        self.assertEqual(get('security.csrf.token_length'), 32)
        self.assertEqual(get('security.csrf.token_name'), '_csrf_token')
        
        print("✅ CSRF Protection Settings")
        
    def test_xss_protection(self):
        """Test XSS protection settings"""
        # Test XSS protection enabled
        self.assertTrue(get('security.xss.protection'))
        self.assertTrue(get('security.xss.content_security_policy'))
        
        # Test security headers
        self.assertEqual(get('security.xss.x_frame_options'), 'SAMEORIGIN')
        self.assertEqual(get('security.xss.x_content_type_options'), 'nosniff')
        self.assertEqual(get('security.xss.x_xss_protection'), '1; mode=block')
        
        print("✅ XSS Protection Settings")
        
    def test_rate_limiting(self):
        """Test rate limiting settings"""
        # Test rate limiting enabled
        self.assertTrue(get('security.rate_limit.enabled'))
        
        # Test rate limit settings
        self.assertEqual(get('security.rate_limit.attempts'), 60)
        self.assertEqual(get('security.rate_limit.decay_minutes'), 1)
        
        print("✅ Rate Limiting Settings")
        
    def test_password_security(self):
        """Test password security settings"""
        # Test password hashing algorithm
        self.assertEqual(get('security.password.hash_algo'), 'bcrypt')
        
        # Test password hash rounds
        self.assertEqual(get('security.password.hash_rounds'), 12)
        
        print("✅ Password Security Settings")
        
    def test_ssl_security(self):
        """Test SSL/TLS security settings"""
        # Test HTTPS enforcement
        self.assertTrue(get('security.ssl.force_https'))
        
        # Test SSL certificate paths
        self.assertEqual(get('security.ssl.cert_path'), '/path/to/cert.pem')
        self.assertEqual(get('security.ssl.key_path'), '/path/to/key.pem')
        
        print("✅ SSL/TLS Security Settings")
        
    def test_database_security(self):
        """Test database security settings"""
        # Test SSL mode
        self.assertEqual(get('security.database.ssl_mode'), 'require')
        
        # Test SSL verification
        self.assertTrue(get('security.database.ssl_verify'))
        
        print("✅ Database Security Settings")
        
    def test_environment_security(self):
        """Test environment security settings"""
        # Test production environment
        self.assertEqual(os.getenv('APP_ENV'), 'production')
        
        # Test debug mode disabled
        self.assertEqual(os.getenv('APP_DEBUG'), 'false')
        
        # Test secure session
        self.assertEqual(os.getenv('SESSION_SECURE'), 'true')
        
        print("✅ Environment Security Settings")
        
    def test_security_headers(self):
        """Test security headers"""
        headers = {
            'X-Frame-Options': get('security.xss.x_frame_options'),
            'X-Content-Type-Options': get('security.xss.x_content_type_options'),
            'X-XSS-Protection': get('security.xss.x_xss_protection'),
            'Content-Security-Policy': 'default-src \'self\'' if get('security.xss.content_security_policy') else None,
        }
        
        # Test all security headers are set
        for header, value in headers.items():
            self.assertIsNotNone(value, f"Security header {header} is not set")
            
        print("✅ Security Headers")
        
    def test_security_middleware(self):
        """Test security middleware settings"""
        # Test HTTPS redirect
        self.assertTrue(get('security.ssl.force_https'))
        
        # Test secure cookies
        self.assertTrue(get('security.cookie.secure'))
        
        # Test CSRF protection
        self.assertTrue(get('security.csrf.enabled'))
        
        print("✅ Security Middleware Settings")

if __name__ == '__main__':
    unittest.main() 