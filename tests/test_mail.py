"""
Test mail functionality
"""
import os
import tempfile
import unittest
from pathlib import Path
from core.config.loader import ConfigLoader, env, get, set, has, all, clear, reload

class TestMail(unittest.TestCase):
    """Test mail functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.env_file = self.temp_dir / '.env'
        self.config_dir = self.temp_dir / 'config'
        self.config_dir.mkdir()
        
        # Create test environment file
        self.env_file.write_text("""
# Mail Settings
MAIL_MAILER=smtp
MAIL_FROM_ADDRESS=hello@example.com
MAIL_FROM_NAME="Example App"
MAIL_REPLY_TO_ADDRESS=reply@example.com
MAIL_REPLY_TO_NAME="Example Reply"

# SMTP Settings
MAIL_SMTP_HOST=smtp.mailtrap.io
MAIL_SMTP_PORT=2525
MAIL_SMTP_USERNAME=null
MAIL_SMTP_PASSWORD=null
MAIL_SMTP_ENCRYPTION=tls
MAIL_SMTP_TIMEOUT=30
MAIL_SMTP_AUTH_MODE=login
MAIL_SMTP_VERIFY_PEER=true

# Sendmail Settings
MAIL_SENDMAIL_PATH=/usr/sbin/sendmail
MAIL_SENDMAIL_MODE=bs

# Mailgun Settings
MAIL_MAILGUN_DOMAIN=mg.example.com
MAIL_MAILGUN_SECRET=your-mailgun-key
MAIL_MAILGUN_ENDPOINT=api.mailgun.net
MAIL_MAILGUN_SCHEME=https
MAIL_MAILGUN_API_VERSION=v3

# Amazon SES Settings
MAIL_SES_KEY=your-ses-key
MAIL_SES_SECRET=your-ses-secret
MAIL_SES_REGION=us-east-1
MAIL_SES_VERSION=2010-12-01

# Postmark Settings
MAIL_POSTMARK_TOKEN=your-postmark-token
MAIL_POSTMARK_MESSAGE_STREAM=outbound

# SparkPost Settings
MAIL_SPARKPOST_SECRET=your-sparkpost-key
MAIL_SPARKPOST_OPTIONS=null

# Log Settings
MAIL_LOG_CHANNEL=stack

# Queue Settings
MAIL_QUEUE_CONNECTION=sync
MAIL_QUEUE_NAME=default
MAIL_QUEUE_TRIES=3
MAIL_QUEUE_TIMEOUT=30
""")
        
        # Create mail configuration file
        (self.config_dir / 'mail.py').write_text("""
def config():
    return {
        'default': env('MAIL_MAILER', 'smtp'),
        'from': {
            'address': env('MAIL_FROM_ADDRESS', 'hello@example.com'),
            'name': env('MAIL_FROM_NAME', 'Example App'),
        },
        'reply_to': {
            'address': env('MAIL_REPLY_TO_ADDRESS', 'reply@example.com'),
            'name': env('MAIL_REPLY_TO_NAME', 'Example Reply'),
        },
        
        'mailers': {
            'smtp': {
                'transport': 'smtp',
                'host': env('MAIL_SMTP_HOST', 'smtp.mailtrap.io'),
                'port': env('MAIL_SMTP_PORT', 2525),
                'username': env('MAIL_SMTP_USERNAME'),
                'password': env('MAIL_SMTP_PASSWORD'),
                'encryption': env('MAIL_SMTP_ENCRYPTION', 'tls'),
                'timeout': env('MAIL_SMTP_TIMEOUT', 30),
                'auth_mode': env('MAIL_SMTP_AUTH_MODE', 'login'),
                'verify_peer': env('MAIL_SMTP_VERIFY_PEER', True),
            },
            
            'sendmail': {
                'transport': 'sendmail',
                'path': env('MAIL_SENDMAIL_PATH', '/usr/sbin/sendmail'),
                'mode': env('MAIL_SENDMAIL_MODE', 'bs'),
            },
            
            'mailgun': {
                'transport': 'mailgun',
                'domain': env('MAIL_MAILGUN_DOMAIN'),
                'secret': env('MAIL_MAILGUN_SECRET'),
                'endpoint': env('MAIL_MAILGUN_ENDPOINT', 'api.mailgun.net'),
                'scheme': env('MAIL_MAILGUN_SCHEME', 'https'),
                'api_version': env('MAIL_MAILGUN_API_VERSION', 'v3'),
            },
            
            'ses': {
                'transport': 'ses',
                'key': env('MAIL_SES_KEY'),
                'secret': env('MAIL_SES_SECRET'),
                'region': env('MAIL_SES_REGION', 'us-east-1'),
                'version': env('MAIL_SES_VERSION', '2010-12-01'),
            },
            
            'postmark': {
                'transport': 'postmark',
                'token': env('MAIL_POSTMARK_TOKEN'),
                'message_stream': env('MAIL_POSTMARK_MESSAGE_STREAM', 'outbound'),
            },
            
            'sparkpost': {
                'transport': 'sparkpost',
                'secret': env('MAIL_SPARKPOST_SECRET'),
                'options': env('MAIL_SPARKPOST_OPTIONS'),
            },
            
            'log': {
                'transport': 'log',
                'channel': env('MAIL_LOG_CHANNEL', 'stack'),
            },
        },
        
        'queue': {
            'connection': env('MAIL_QUEUE_CONNECTION', 'sync'),
            'name': env('MAIL_QUEUE_NAME', 'default'),
            'tries': env('MAIL_QUEUE_TRIES', 3),
            'timeout': env('MAIL_QUEUE_TIMEOUT', 30),
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
        """Test default mail settings"""
        self.assertEqual(get('mail.default'), 'smtp')
        self.assertEqual(get('mail.from.address'), 'hello@example.com')
        self.assertEqual(get('mail.from.name'), 'Example App')
        self.assertEqual(get('mail.reply_to.address'), 'reply@example.com')
        self.assertEqual(get('mail.reply_to.name'), 'Example Reply')
        
        print("✅ Default Settings")
        
    def test_mailers(self):
        """Test mail mailers"""
        # Test SMTP mailer
        smtp = get('mail.mailers.smtp')
        self.assertEqual(smtp['transport'], 'smtp')
        self.assertEqual(smtp['host'], 'smtp.mailtrap.io')
        self.assertEqual(smtp['port'], 2525)
        self.assertEqual(smtp['username'], 'null')
        self.assertEqual(smtp['password'], 'null')
        self.assertEqual(smtp['encryption'], 'tls')
        self.assertEqual(smtp['timeout'], 30)
        self.assertEqual(smtp['auth_mode'], 'login')
        self.assertTrue(smtp['verify_peer'])
        
        # Test Sendmail mailer
        sendmail = get('mail.mailers.sendmail')
        self.assertEqual(sendmail['transport'], 'sendmail')
        self.assertEqual(sendmail['path'], '/usr/sbin/sendmail')
        self.assertEqual(sendmail['mode'], 'bs')
        
        # Test Mailgun mailer
        mailgun = get('mail.mailers.mailgun')
        self.assertEqual(mailgun['transport'], 'mailgun')
        self.assertEqual(mailgun['domain'], 'mg.example.com')
        self.assertEqual(mailgun['secret'], 'your-mailgun-key')
        self.assertEqual(mailgun['endpoint'], 'api.mailgun.net')
        self.assertEqual(mailgun['scheme'], 'https')
        self.assertEqual(mailgun['api_version'], 'v3')
        
        # Test Amazon SES mailer
        ses = get('mail.mailers.ses')
        self.assertEqual(ses['transport'], 'ses')
        self.assertEqual(ses['key'], 'your-ses-key')
        self.assertEqual(ses['secret'], 'your-ses-secret')
        self.assertEqual(ses['region'], 'us-east-1')
        self.assertEqual(ses['version'], '2010-12-01')
        
        # Test Postmark mailer
        postmark = get('mail.mailers.postmark')
        self.assertEqual(postmark['transport'], 'postmark')
        self.assertEqual(postmark['token'], 'your-postmark-token')
        self.assertEqual(postmark['message_stream'], 'outbound')
        
        # Test SparkPost mailer
        sparkpost = get('mail.mailers.sparkpost')
        self.assertEqual(sparkpost['transport'], 'sparkpost')
        self.assertEqual(sparkpost['secret'], 'your-sparkpost-key')
        self.assertEqual(sparkpost['options'], 'null')
        
        # Test Log mailer
        log = get('mail.mailers.log')
        self.assertEqual(log['transport'], 'log')
        self.assertEqual(log['channel'], 'stack')
        
        print("✅ Mail Mailers")
        
    def test_queue_settings(self):
        """Test mail queue settings"""
        queue = get('mail.queue')
        self.assertEqual(queue['connection'], 'sync')
        self.assertEqual(queue['name'], 'default')
        self.assertEqual(queue['tries'], 3)
        self.assertEqual(queue['timeout'], 30)
        
        print("✅ Queue Settings")
        
    def test_mailer_override(self):
        """Test mailer override"""
        # Set environment variables
        os.environ['MAIL_MAILER'] = 'mailgun'
        os.environ['MAIL_MAILGUN_DOMAIN'] = 'custom.example.com'
        os.environ['MAIL_MAILGUN_SECRET'] = 'custom-mailgun-key'
        
        # Reload configuration
        reload()
        
        # Test overridden values
        self.assertEqual(get('mail.default'), 'mailgun')
        self.assertEqual(get('mail.mailers.mailgun.domain'), 'custom.example.com')
        self.assertEqual(get('mail.mailers.mailgun.secret'), 'custom-mailgun-key')
        
        print("✅ Mailer Override")

if __name__ == '__main__':
    unittest.main() 