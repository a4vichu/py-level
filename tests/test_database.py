"""
Test database functionality
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestDatabase(unittest.TestCase):
    """Test database functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file
        self.env_file.write_text("""
# Database Settings
DB_CONNECTION=sqlite
DB_DATABASE=:memory:
DB_PREFIX=test_

# MySQL Settings
DB_MYSQL_HOST=localhost
DB_MYSQL_PORT=3306
DB_MYSQL_DATABASE=pylevel
DB_MYSQL_USERNAME=root
DB_MYSQL_PASSWORD=secret
DB_MYSQL_CHARSET=utf8mb4
DB_MYSQL_COLLATION=utf8mb4_unicode_ci
DB_MYSQL_PREFIX=
DB_MYSQL_STRICT=true
DB_MYSQL_ENGINE=InnoDB

# PostgreSQL Settings
DB_PGSQL_HOST=localhost
DB_PGSQL_PORT=5432
DB_PGSQL_DATABASE=pylevel
DB_PGSQL_USERNAME=postgres
DB_PGSQL_PASSWORD=secret
DB_PGSQL_CHARSET=utf8
DB_PGSQL_PREFIX=
DB_PGSQL_SCHEMA=public
DB_PGSQL_SSL_MODE=prefer

# SQLite Settings
DB_SQLITE_DATABASE=:memory:
DB_SQLITE_PREFIX=test_

# Migration Settings
DB_MIGRATIONS_PATH=database/migrations
DB_MIGRATIONS_TABLE=migrations
DB_MIGRATIONS_NAMESPACE=Database\\Migrations

# Model Settings
DB_MODELS_PATH=app/Models
DB_MODELS_NAMESPACE=App\\Models

# Query Settings
DB_QUERY_CACHE=true
DB_QUERY_CACHE_TTL=3600
DB_QUERY_LOG=true
DB_QUERY_LOG_PATH=storage/logs/queries.log
""")
        
        # Create database configuration file
        (self.config_dir / 'database.py').write_text("""
def config():
    return {
        'default': env('DB_CONNECTION', 'sqlite'),
        'prefix': env('DB_PREFIX', ''),
        
        'connections': {
            'sqlite': {
                'driver': 'sqlite',
                'database': env('DB_SQLITE_DATABASE', ':memory:'),
                'prefix': env('DB_SQLITE_PREFIX', ''),
            },
            
            'mysql': {
                'driver': 'mysql',
                'host': env('DB_MYSQL_HOST', 'localhost'),
                'port': env('DB_MYSQL_PORT', 3306),
                'database': env('DB_MYSQL_DATABASE', 'pylevel'),
                'username': env('DB_MYSQL_USERNAME', 'root'),
                'password': env('DB_MYSQL_PASSWORD', ''),
                'charset': env('DB_MYSQL_CHARSET', 'utf8mb4'),
                'collation': env('DB_MYSQL_COLLATION', 'utf8mb4_unicode_ci'),
                'prefix': env('DB_MYSQL_PREFIX', ''),
                'strict': env('DB_MYSQL_STRICT', True),
                'engine': env('DB_MYSQL_ENGINE', 'InnoDB'),
            },
            
            'pgsql': {
                'driver': 'pgsql',
                'host': env('DB_PGSQL_HOST', 'localhost'),
                'port': env('DB_PGSQL_PORT', 5432),
                'database': env('DB_PGSQL_DATABASE', 'pylevel'),
                'username': env('DB_PGSQL_USERNAME', 'postgres'),
                'password': env('DB_PGSQL_PASSWORD', ''),
                'charset': env('DB_PGSQL_CHARSET', 'utf8'),
                'prefix': env('DB_PGSQL_PREFIX', ''),
                'schema': env('DB_PGSQL_SCHEMA', 'public'),
                'sslmode': env('DB_PGSQL_SSL_MODE', 'prefer'),
            },
        },
        
        'migrations': {
            'path': env('DB_MIGRATIONS_PATH', 'database/migrations'),
            'table': env('DB_MIGRATIONS_TABLE', 'migrations'),
            'namespace': env('DB_MIGRATIONS_NAMESPACE', 'Database\\\\Migrations'),
        },
        
        'models': {
            'path': env('DB_MODELS_PATH', 'app/Models'),
            'namespace': env('DB_MODELS_NAMESPACE', 'App\\\\Models'),
        },
        
        'query': {
            'cache': env('DB_QUERY_CACHE', False),
            'cache_ttl': env('DB_QUERY_CACHE_TTL', 3600),
            'log': env('DB_QUERY_LOG', False),
            'log_path': env('DB_QUERY_LOG_PATH', 'storage/logs/queries.log'),
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
        
    def test_default_connection(self):
        """Test default database connection"""
        self.assertEqual(get('database.default'), 'sqlite')
        self.assertEqual(get('database.prefix'), 'test_')
        
        print("✅ Default Connection")
        
    def test_connections(self):
        """Test database connections"""
        # Test SQLite connection
        sqlite = get('database.connections.sqlite')
        self.assertEqual(sqlite['driver'], 'sqlite')
        self.assertEqual(sqlite['database'], ':memory:')
        self.assertEqual(sqlite['prefix'], 'test_')
        
        # Test MySQL connection
        mysql = get('database.connections.mysql')
        self.assertEqual(mysql['driver'], 'mysql')
        self.assertEqual(mysql['host'], 'localhost')
        self.assertEqual(mysql['port'], 3306)
        self.assertEqual(mysql['database'], 'pylevel')
        self.assertEqual(mysql['username'], 'root')
        self.assertEqual(mysql['password'], 'secret')
        self.assertEqual(mysql['charset'], 'utf8mb4')
        self.assertEqual(mysql['collation'], 'utf8mb4_unicode_ci')
        self.assertEqual(mysql['prefix'], '')
        self.assertTrue(mysql['strict'])
        self.assertEqual(mysql['engine'], 'InnoDB')
        
        # Test PostgreSQL connection
        pgsql = get('database.connections.pgsql')
        self.assertEqual(pgsql['driver'], 'pgsql')
        self.assertEqual(pgsql['host'], 'localhost')
        self.assertEqual(pgsql['port'], 5432)
        self.assertEqual(pgsql['database'], 'pylevel')
        self.assertEqual(pgsql['username'], 'postgres')
        self.assertEqual(pgsql['password'], 'secret')
        self.assertEqual(pgsql['charset'], 'utf8')
        self.assertEqual(pgsql['prefix'], '')
        self.assertEqual(pgsql['schema'], 'public')
        self.assertEqual(pgsql['sslmode'], 'prefer')
        
        print("✅ Database Connections")
        
    def test_migrations(self):
        """Test migration settings"""
        migrations = get('database.migrations')
        self.assertEqual(migrations['path'], 'database/migrations')
        self.assertEqual(migrations['table'], 'migrations')
        self.assertEqual(migrations['namespace'], 'Database\\Migrations')
        
        print("✅ Migration Settings")
        
    def test_models(self):
        """Test model settings"""
        models = get('database.models')
        self.assertEqual(models['path'], 'app/Models')
        self.assertEqual(models['namespace'], 'App\\Models')
        
        print("✅ Model Settings")
        
    def test_query_settings(self):
        """Test query settings"""
        query = get('database.query')
        self.assertTrue(query['cache'])
        self.assertEqual(query['cache_ttl'], 3600)
        self.assertTrue(query['log'])
        self.assertEqual(query['log_path'], 'storage/logs/queries.log')
        
        print("✅ Query Settings")
        
    def test_connection_override(self):
        """Test connection override"""
        # Set environment variables
        os.environ['DB_CONNECTION'] = 'mysql'
        os.environ['DB_MYSQL_DATABASE'] = 'test_db'
        os.environ['DB_MYSQL_USERNAME'] = 'test_user'
        
        # Reload configuration
        reload()
        
        # Test overridden values
        self.assertEqual(get('database.default'), 'mysql')
        self.assertEqual(get('database.connections.mysql.database'), 'test_db')
        self.assertEqual(get('database.connections.mysql.username'), 'test_user')
        
        print("✅ Connection Override")

if __name__ == '__main__':
    unittest.main() 