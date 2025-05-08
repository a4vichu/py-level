"""
Queue configuration
"""
from core.config.loader import env

def config():
    return {
        'default': env('QUEUE_CONNECTION', 'sync'),
        
        'connections': {
            'sync': {
                'driver': 'sync',
            },
            
            'database': {
                'driver': 'database',
                'table': env('QUEUE_DATABASE_TABLE', 'jobs'),
                'queue': env('QUEUE_DATABASE_QUEUE', 'default'),
                'retry_after': env('QUEUE_DATABASE_RETRY_AFTER', 90),
                'after_commit': env('QUEUE_DATABASE_AFTER_COMMIT', False),
            },
            
            'redis': {
                'driver': 'redis',
                'connection': env('QUEUE_REDIS_CONNECTION', 'default'),
                'queue': env('QUEUE_REDIS_QUEUE', 'default'),
                'retry_after': env('QUEUE_REDIS_RETRY_AFTER', 90),
                'block_for': env('QUEUE_REDIS_BLOCK_FOR'),
                'after_commit': env('QUEUE_REDIS_AFTER_COMMIT', False),
            },
            
            'beanstalkd': {
                'driver': 'beanstalkd',
                'host': env('QUEUE_BEANSTALKD_HOST', '127.0.0.1'),
                'queue': env('QUEUE_BEANSTALKD_QUEUE', 'default'),
                'retry_after': env('QUEUE_BEANSTALKD_RETRY_AFTER', 90),
                'block_for': env('QUEUE_BEANSTALKD_BLOCK_FOR'),
                'after_commit': env('QUEUE_BEANSTALKD_AFTER_COMMIT', False),
            },
            
            'sqs': {
                'driver': 'sqs',
                'key': env('AWS_ACCESS_KEY_ID'),
                'secret': env('AWS_SECRET_ACCESS_KEY'),
                'prefix': env('QUEUE_SQS_PREFIX', 'https://sqs.us-east-1.amazonaws.com/your-account-id'),
                'queue': env('QUEUE_SQS_QUEUE', 'default'),
                'suffix': env('QUEUE_SQS_SUFFIX'),
                'region': env('AWS_DEFAULT_REGION', 'us-east-1'),
                'after_commit': env('QUEUE_SQS_AFTER_COMMIT', False),
            },
        },
        
        'failed': {
            'driver': env('QUEUE_FAILED_DRIVER', 'database'),
            'database': env('QUEUE_FAILED_DATABASE', 'default'),
            'table': env('QUEUE_FAILED_TABLE', 'failed_jobs'),
        },
    } 