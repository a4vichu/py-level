"""
Services configuration
"""
from core.config.loader import env

def config():
    return {
        'providers': [
            'core.providers.DatabaseServiceProvider',
            'core.providers.CacheServiceProvider',
            'core.providers.QueueServiceProvider',
            'core.providers.MailServiceProvider',
            'core.providers.RouteServiceProvider',
            'core.providers.ViewServiceProvider',
            'core.providers.EventServiceProvider',
            'core.providers.ValidationServiceProvider',
            'core.providers.TranslationServiceProvider',
            'core.providers.ConsoleServiceProvider',
            'core.providers.HashServiceProvider',
            'core.providers.CookieServiceProvider',
            'core.providers.SessionServiceProvider',
            'core.providers.EncryptionServiceProvider',
            'core.providers.FilesystemServiceProvider',
            'core.providers.TemplateServiceProvider',
        ],
        
        'aliases': {
            'app': 'core.app.Application',
            'auth': 'core.auth.Auth',
            'blade': 'core.view.Blade',
            'cache': 'core.cache.Cache',
            'config': 'core.config.Config',
            'cookie': 'core.cookie.Cookie',
            'crypt': 'core.encryption.Encrypter',
            'db': 'core.database.Database',
            'event': 'core.events.Dispatcher',
            'file': 'core.filesystem.File',
            'hash': 'core.hashing.Hash',
            'log': 'core.logging.Log',
            'mail': 'core.mail.Mail',
            'queue': 'core.queue.Queue',
            'redirect': 'core.routing.Redirector',
            'request': 'core.http.Request',
            'response': 'core.http.Response',
            'route': 'core.routing.Router',
            'schema': 'core.database.Schema',
            'session': 'core.session.Session',
            'storage': 'core.filesystem.Storage',
            'url': 'core.routing.UrlGenerator',
            'validator': 'core.validation.Validator',
            'view': 'core.view.View',
        },
        
        'auto_discover': env('SERVICE_AUTO_DISCOVER', True),
        'auto_discover_path': env('SERVICE_AUTO_DISCOVER_PATH', 'app/providers'),
        'auto_discover_namespace': env('SERVICE_AUTO_DISCOVER_NAMESPACE', 'App\\Providers'),
    } 