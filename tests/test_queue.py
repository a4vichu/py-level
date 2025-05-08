"""
Test queue functionality
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestQueue(unittest.TestCase):
    """Test queue functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file
        self.env_file.write_text("""
# Queue Settings
QUEUE_CONNECTION=sync
QUEUE_DRIVER=sync
QUEUE_DEFAULT=default
QUEUE_FAILED_DRIVER=database
QUEUE_FAILED_TABLE=failed_jobs
QUEUE_FAILED_DATABASE=mysql
QUEUE_FAILED_AFTER=60
QUEUE_FAILED_ATTEMPTS=3
QUEUE_FAILED_TIMEOUT=90

# Sync Queue Settings
QUEUE_SYNC_DRIVER=sync
QUEUE_SYNC_QUEUE=default
QUEUE_SYNC_DELAY=0
QUEUE_SYNC_MEMORY=128
QUEUE_SYNC_TIMEOUT=60
QUEUE_SYNC_SLEEP=3
QUEUE_SYNC_TRIES=3
QUEUE_SYNC_RETRY_AFTER=60

# Database Queue Settings
QUEUE_DATABASE_DRIVER=database
QUEUE_DATABASE_TABLE=jobs
QUEUE_DATABASE_QUEUE=default
QUEUE_DATABASE_DELAY=0
QUEUE_DATABASE_MEMORY=128
QUEUE_DATABASE_TIMEOUT=60
QUEUE_DATABASE_SLEEP=3
QUEUE_DATABASE_TRIES=3
QUEUE_DATABASE_RETRY_AFTER=60
QUEUE_DATABASE_CONNECTION=mysql

# Redis Queue Settings
QUEUE_REDIS_DRIVER=redis
QUEUE_REDIS_CONNECTION=default
QUEUE_REDIS_QUEUE=default
QUEUE_REDIS_DELAY=0
QUEUE_REDIS_MEMORY=128
QUEUE_REDIS_TIMEOUT=60
QUEUE_REDIS_SLEEP=3
QUEUE_REDIS_TRIES=3
QUEUE_REDIS_RETRY_AFTER=60
QUEUE_REDIS_BLOCK_FOR=null

# Beanstalkd Queue Settings
QUEUE_BEANSTALKD_DRIVER=beanstalkd
QUEUE_BEANSTALKD_HOST=localhost
QUEUE_BEANSTALKD_PORT=11300
QUEUE_BEANSTALKD_QUEUE=default
QUEUE_BEANSTALKD_DELAY=0
QUEUE_BEANSTALKD_MEMORY=128
QUEUE_BEANSTALKD_TIMEOUT=60
QUEUE_BEANSTALKD_SLEEP=3
QUEUE_BEANSTALKD_TRIES=3
QUEUE_BEANSTALKD_RETRY_AFTER=60
QUEUE_BEANSTALKD_RESERVE_TIMEOUT=5

# Amazon SQS Queue Settings
QUEUE_SQS_DRIVER=sqs
QUEUE_SQS_KEY=your-key
QUEUE_SQS_SECRET=your-secret
QUEUE_SQS_PREFIX=https://sqs.us-east-1.amazonaws.com/your-account-id
QUEUE_SQS_QUEUE=default
QUEUE_SQS_REGION=us-east-1
QUEUE_SQS_DELAY=0
QUEUE_SQS_MEMORY=128
QUEUE_SQS_TIMEOUT=60
QUEUE_SQS_SLEEP=3
QUEUE_SQS_TRIES=3
QUEUE_SQS_RETRY_AFTER=60

# Batch Settings
QUEUE_BATCH_SIZE=1000
QUEUE_BATCH_TIMEOUT=3600
QUEUE_BATCH_SLEEP=1
""")
        
        # Create queue configuration file
        (self.config_dir / 'queue.py').write_text("""
def config():
    return {
        'default': env('QUEUE_CONNECTION', 'sync'),
        'driver': env('QUEUE_DRIVER', 'sync'),
        'queue': env('QUEUE_DEFAULT', 'default'),
        
        'failed': {
            'driver': env('QUEUE_FAILED_DRIVER', 'database'),
            'table': env('QUEUE_FAILED_TABLE', 'failed_jobs'),
            'database': env('QUEUE_FAILED_DATABASE', 'mysql'),
            'after': env('QUEUE_FAILED_AFTER', 60),
            'attempts': env('QUEUE_FAILED_ATTEMPTS', 3),
            'timeout': env('QUEUE_FAILED_TIMEOUT', 90),
        },
        
        'connections': {
            'sync': {
                'driver': env('QUEUE_SYNC_DRIVER', 'sync'),
                'queue': env('QUEUE_SYNC_QUEUE', 'default'),
                'delay': env('QUEUE_SYNC_DELAY', 0),
                'memory': env('QUEUE_SYNC_MEMORY', 128),
                'timeout': env('QUEUE_SYNC_TIMEOUT', 60),
                'sleep': env('QUEUE_SYNC_SLEEP', 3),
                'tries': env('QUEUE_SYNC_TRIES', 3),
                'retry_after': env('QUEUE_SYNC_RETRY_AFTER', 60),
            },
            
            'database': {
                'driver': env('QUEUE_DATABASE_DRIVER', 'database'),
                'table': env('QUEUE_DATABASE_TABLE', 'jobs'),
                'queue': env('QUEUE_DATABASE_QUEUE', 'default'),
                'delay': env('QUEUE_DATABASE_DELAY', 0),
                'memory': env('QUEUE_DATABASE_MEMORY', 128),
                'timeout': env('QUEUE_DATABASE_TIMEOUT', 60),
                'sleep': env('QUEUE_DATABASE_SLEEP', 3),
                'tries': env('QUEUE_DATABASE_TRIES', 3),
                'retry_after': env('QUEUE_DATABASE_RETRY_AFTER', 60),
                'connection': env('QUEUE_DATABASE_CONNECTION', 'mysql'),
            },
            
            'redis': {
                'driver': env('QUEUE_REDIS_DRIVER', 'redis'),
                'connection': env('QUEUE_REDIS_CONNECTION', 'default'),
                'queue': env('QUEUE_REDIS_QUEUE', 'default'),
                'delay': env('QUEUE_REDIS_DELAY', 0),
                'memory': env('QUEUE_REDIS_MEMORY', 128),
                'timeout': env('QUEUE_REDIS_TIMEOUT', 60),
                'sleep': env('QUEUE_REDIS_SLEEP', 3),
                'tries': env('QUEUE_REDIS_TRIES', 3),
                'retry_after': env('QUEUE_REDIS_RETRY_AFTER', 60),
                'block_for': env('QUEUE_REDIS_BLOCK_FOR'),
            },
            
            'beanstalkd': {
                'driver': env('QUEUE_BEANSTALKD_DRIVER', 'beanstalkd'),
                'host': env('QUEUE_BEANSTALKD_HOST', 'localhost'),
                'port': env('QUEUE_BEANSTALKD_PORT', 11300),
                'queue': env('QUEUE_BEANSTALKD_QUEUE', 'default'),
                'delay': env('QUEUE_BEANSTALKD_DELAY', 0),
                'memory': env('QUEUE_BEANSTALKD_MEMORY', 128),
                'timeout': env('QUEUE_BEANSTALKD_TIMEOUT', 60),
                'sleep': env('QUEUE_BEANSTALKD_SLEEP', 3),
                'tries': env('QUEUE_BEANSTALKD_TRIES', 3),
                'retry_after': env('QUEUE_BEANSTALKD_RETRY_AFTER', 60),
                'reserve_timeout': env('QUEUE_BEANSTALKD_RESERVE_TIMEOUT', 5),
            },
            
            'sqs': {
                'driver': env('QUEUE_SQS_DRIVER', 'sqs'),
                'key': env('QUEUE_SQS_KEY'),
                'secret': env('QUEUE_SQS_SECRET'),
                'prefix': env('QUEUE_SQS_PREFIX'),
                'queue': env('QUEUE_SQS_QUEUE', 'default'),
                'region': env('QUEUE_SQS_REGION', 'us-east-1'),
                'delay': env('QUEUE_SQS_DELAY', 0),
                'memory': env('QUEUE_SQS_MEMORY', 128),
                'timeout': env('QUEUE_SQS_TIMEOUT', 60),
                'sleep': env('QUEUE_SQS_SLEEP', 3),
                'tries': env('QUEUE_SQS_TRIES', 3),
                'retry_after': env('QUEUE_SQS_RETRY_AFTER', 60),
            },
        },
        
        'batch': {
            'size': env('QUEUE_BATCH_SIZE', 1000),
            'timeout': env('QUEUE_BATCH_TIMEOUT', 3600),
            'sleep': env('QUEUE_BATCH_SLEEP', 1),
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
        """Test default queue settings"""
        self.assertEqual(get('queue.default'), 'sync')
        self.assertEqual(get('queue.driver'), 'sync')
        self.assertEqual(get('queue.queue'), 'default')
        
        print("✅ Default Settings")
        
    def test_failed_jobs(self):
        """Test failed jobs settings"""
        failed = get('queue.failed')
        self.assertEqual(failed['driver'], 'database')
        self.assertEqual(failed['table'], 'failed_jobs')
        self.assertEqual(failed['database'], 'mysql')
        self.assertEqual(failed['after'], 60)
        self.assertEqual(failed['attempts'], 3)
        self.assertEqual(failed['timeout'], 90)
        
        print("✅ Failed Jobs")
        
    def test_connections(self):
        """Test queue connections"""
        # Test sync connection
        sync = get('queue.connections.sync')
        self.assertEqual(sync['driver'], 'sync')
        self.assertEqual(sync['queue'], 'default')
        self.assertEqual(sync['delay'], 0)
        self.assertEqual(sync['memory'], 128)
        self.assertEqual(sync['timeout'], 60)
        self.assertEqual(sync['sleep'], 3)
        self.assertEqual(sync['tries'], 3)
        self.assertEqual(sync['retry_after'], 60)
        
        # Test database connection
        database = get('queue.connections.database')
        self.assertEqual(database['driver'], 'database')
        self.assertEqual(database['table'], 'jobs')
        self.assertEqual(database['queue'], 'default')
        self.assertEqual(database['delay'], 0)
        self.assertEqual(database['memory'], 128)
        self.assertEqual(database['timeout'], 60)
        self.assertEqual(database['sleep'], 3)
        self.assertEqual(database['tries'], 3)
        self.assertEqual(database['retry_after'], 60)
        self.assertEqual(database['connection'], 'mysql')
        
        # Test Redis connection
        redis = get('queue.connections.redis')
        self.assertEqual(redis['driver'], 'redis')
        self.assertEqual(redis['connection'], 'default')
        self.assertEqual(redis['queue'], 'default')
        self.assertEqual(redis['delay'], 0)
        self.assertEqual(redis['memory'], 128)
        self.assertEqual(redis['timeout'], 60)
        self.assertEqual(redis['sleep'], 3)
        self.assertEqual(redis['tries'], 3)
        self.assertEqual(redis['retry_after'], 60)
        self.assertEqual(redis['block_for'], 'null')
        
        # Test Beanstalkd connection
        beanstalkd = get('queue.connections.beanstalkd')
        self.assertEqual(beanstalkd['driver'], 'beanstalkd')
        self.assertEqual(beanstalkd['host'], 'localhost')
        self.assertEqual(beanstalkd['port'], 11300)
        self.assertEqual(beanstalkd['queue'], 'default')
        self.assertEqual(beanstalkd['delay'], 0)
        self.assertEqual(beanstalkd['memory'], 128)
        self.assertEqual(beanstalkd['timeout'], 60)
        self.assertEqual(beanstalkd['sleep'], 3)
        self.assertEqual(beanstalkd['tries'], 3)
        self.assertEqual(beanstalkd['retry_after'], 60)
        self.assertEqual(beanstalkd['reserve_timeout'], 5)
        
        # Test SQS connection
        sqs = get('queue.connections.sqs')
        self.assertEqual(sqs['driver'], 'sqs')
        self.assertEqual(sqs['key'], 'your-key')
        self.assertEqual(sqs['secret'], 'your-secret')
        self.assertEqual(sqs['prefix'], 'https://sqs.us-east-1.amazonaws.com/your-account-id')
        self.assertEqual(sqs['queue'], 'default')
        self.assertEqual(sqs['region'], 'us-east-1')
        self.assertEqual(sqs['delay'], 0)
        self.assertEqual(sqs['memory'], 128)
        self.assertEqual(sqs['timeout'], 60)
        self.assertEqual(sqs['sleep'], 3)
        self.assertEqual(sqs['tries'], 3)
        self.assertEqual(sqs['retry_after'], 60)
        
        print("✅ Queue Connections")
        
    def test_batch_settings(self):
        """Test batch settings"""
        batch = get('queue.batch')
        self.assertEqual(batch['size'], 1000)
        self.assertEqual(batch['timeout'], 3600)
        self.assertEqual(batch['sleep'], 1)
        
        print("✅ Batch Settings")
        
    def test_connection_override(self):
        """Test connection override"""
        # Set environment variables
        os.environ['QUEUE_CONNECTION'] = 'redis'
        os.environ['QUEUE_REDIS_CONNECTION'] = 'cache'
        os.environ['QUEUE_REDIS_QUEUE'] = 'high'
        
        # Reload configuration
        reload()
        
        # Test overridden values
        self.assertEqual(get('queue.default'), 'redis')
        self.assertEqual(get('queue.connections.redis.connection'), 'cache')
        self.assertEqual(get('queue.connections.redis.queue'), 'high')
        
        print("✅ Connection Override")

if __name__ == '__main__':
    unittest.main() 