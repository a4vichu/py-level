"""
Mail configuration
"""
from core.config.loader import env

def config():
    return {
        'default': env('MAIL_MAILER', 'smtp'),
        
        'mailers': {
            'smtp': {
                'transport': 'smtp',
                'host': env('MAIL_HOST', 'smtp.mailtrap.io'),
                'port': env('MAIL_PORT', 2525),
                'encryption': env('MAIL_ENCRYPTION', 'tls'),
                'username': env('MAIL_USERNAME'),
                'password': env('MAIL_PASSWORD'),
                'timeout': env('MAIL_TIMEOUT'),
                'local_domain': env('MAIL_LOCAL_DOMAIN'),
                'auth_mode': env('MAIL_AUTH_MODE'),
            },
            
            'ses': {
                'transport': 'ses',
                'key': env('AWS_ACCESS_KEY_ID'),
                'secret': env('AWS_SECRET_ACCESS_KEY'),
                'region': env('AWS_DEFAULT_REGION', 'us-east-1'),
                'options': {
                    'ConfigurationSetName': env('MAIL_SES_CONFIGURATION_SET'),
                    'TrackingOptions': {
                        'ClickTracking': env('MAIL_SES_CLICK_TRACKING', True),
                        'OpenTracking': env('MAIL_SES_OPEN_TRACKING', True),
                    },
                },
            },
            
            'mailgun': {
                'transport': 'mailgun',
                'domain': env('MAILGUN_DOMAIN'),
                'secret': env('MAILGUN_SECRET'),
                'endpoint': env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
                'scheme': env('MAILGUN_SCHEME', 'https'),
            },
            
            'postmark': {
                'transport': 'postmark',
                'token': env('POSTMARK_TOKEN'),
                'message_stream_id': env('POSTMARK_MESSAGE_STREAM_ID'),
            },
            
            'sendmail': {
                'transport': 'sendmail',
                'path': env('MAIL_SENDMAIL_PATH', '/usr/sbin/sendmail -bs -i'),
            },
            
            'log': {
                'transport': 'log',
                'channel': env('MAIL_LOG_CHANNEL'),
            },
            
            'array': {
                'transport': 'array',
            },
        },
        
        'from': {
            'address': env('MAIL_FROM_ADDRESS', 'hello@example.com'),
            'name': env('MAIL_FROM_NAME', 'Example'),
        },
        
        'markdown': {
            'theme': env('MAIL_MARKDOWN_THEME', 'default'),
            'paths': [
                'resources/views/vendor/mail',
            ],
        },
    } 