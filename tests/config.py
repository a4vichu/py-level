"""
Test configuration
"""
import os
import tempfile
from pathlib import Path

# Test environment
TEST_ENV = 'testing'

# Test directories
TEST_DIR = Path(__file__).parent
TEMP_DIR = Path(tempfile.gettempdir()) / 'pylevel_tests'

# Test database
TEST_DB = {
    'driver': 'sqlite',
    'database': ':memory:',
    'prefix': 'test_',
}

# Test cache
TEST_CACHE = {
    'driver': 'file',
    'path': str(TEMP_DIR / 'cache'),
    'prefix': 'test_',
}

# Test queue
TEST_QUEUE = {
    'driver': 'sync',
    'table': 'test_jobs',
    'failed_table': 'test_failed_jobs',
}

# Test mail
TEST_MAIL = {
    'driver': 'array',
    'from_address': 'test@example.com',
    'from_name': 'Test',
}

# Test session
TEST_SESSION = {
    'driver': 'file',
    'path': str(TEMP_DIR / 'sessions'),
    'lifetime': 120,
}

# Test logging
TEST_LOGGING = {
    'channel': 'stack',
    'level': 'debug',
    'file': str(TEMP_DIR / 'logs' / 'test.log'),
}

# Test filesystem
TEST_FILESYSTEM = {
    'driver': 'local',
    'root': str(TEMP_DIR / 'storage'),
}

# Test encryption
TEST_ENCRYPTION = {
    'key': 'base64:test_key_32_bytes_long_for_testing',
    'cipher': 'AES-256-CBC',
}

# Test validation
TEST_VALIDATION = {
    'locale': 'en',
    'fallback_locale': 'en',
}

# Test translation
TEST_TRANSLATION = {
    'locale': 'en',
    'fallback_locale': 'en',
    'path': str(TEST_DIR / 'lang'),
}

# Test view
TEST_VIEW = {
    'path': str(TEST_DIR / 'views'),
    'cache': False,
}

# Test route
TEST_ROUTE = {
    'prefix': 'test',
    'middleware': ['test'],
}

# Test event
TEST_EVENT = {
    'listeners': {},
    'subscribers': {},
}

# Test console
TEST_CONSOLE = {
    'commands': {},
}

# Test provider
TEST_PROVIDER = {
    'providers': [],
    'aliases': {},
}

# Test middleware
TEST_MIDDLEWARE = {
    'global': [],
    'groups': {},
    'route': {},
}

# Test service
TEST_SERVICE = {
    'auto_discover': False,
    'auto_discover_path': str(TEST_DIR / 'providers'),
}

# Test application
TEST_APP = {
    'name': 'PyLevel Test',
    'env': TEST_ENV,
    'debug': True,
    'url': 'http://localhost:8000',
    'key': TEST_ENCRYPTION['key'],
    'timezone': 'UTC',
    'locale': 'en',
    'fallback_locale': 'en',
    'faker_locale': 'en_US',
    'cipher': TEST_ENCRYPTION['cipher'],
}

# Create test directories
def create_test_dirs():
    """Create test directories"""
    dirs = [
        TEMP_DIR,
        TEMP_DIR / 'cache',
        TEMP_DIR / 'sessions',
        TEMP_DIR / 'logs',
        TEMP_DIR / 'storage',
        TEST_DIR / 'views',
        TEST_DIR / 'lang',
        TEST_DIR / 'providers',
    ]
    
    for dir in dirs:
        dir.mkdir(parents=True, exist_ok=True)

# Clean test directories
def clean_test_dirs():
    """Clean test directories"""
    import shutil
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR) 