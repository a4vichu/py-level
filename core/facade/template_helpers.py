from core.facade.facade import Facade
from core.facade.helpers import (
    config as config_helper,
    env as env_helper,
    app as app_helper,
    base_path as base_path_helper,
    app_path as app_path_helper,
    config_path as config_path_helper,
    database_path as database_path_helper,
    resource_path as resource_path_helper,
    storage_path as storage_path_helper,
    log as log_helper,
    url as url_helper,
    secure_asset as secure_asset_helper,
    secure_url as secure_url_helper,
    route as route_helper,
    redirect as redirect_helper,
    back as back_helper,
    abort as abort_helper,
    abort_if as abort_if_helper,
    abort_unless as abort_unless_helper,
    request as request_helper,
    old as old_helper,
    session as session_helper,
    __ as __helper,
    trans as trans_helper,
    trans_choice as trans_choice_helper,
    collect as collect_helper,
    data_get as data_get_helper,
    data_set as data_set_helper,
    head as head_helper,
    last as last_helper,
    value as value_helper,
    with_value as with_value_helper,
    bcrypt_hash as bcrypt_hash_helper,
    bcrypt_check as bcrypt_check_helper,
    event as event_helper,
    dispatch as dispatch_helper
)

class Config(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'config'
        
    @staticmethod
    def get(key: str, default=None):
        """Get a configuration value."""
        return config_helper(key, default)

class Env(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'env'
        
    @staticmethod
    def get(key: str, default=None):
        """Get an environment variable."""
        return env_helper(key, default)

class App(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'app'
        
    @staticmethod
    def get(key: str, default=None):
        """Get an application value."""
        return app_helper(key, default)

class Path(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'path'
        
    @staticmethod
    def base():
        """Get the base path."""
        return base_path_helper()
        
    @staticmethod
    def app():
        """Get the application path."""
        return app_path_helper()
        
    @staticmethod
    def config():
        """Get the configuration path."""
        return config_path_helper()
        
    @staticmethod
    def database():
        """Get the database path."""
        return database_path_helper()
        
    @staticmethod
    def resource():
        """Get the resource path."""
        return resource_path_helper()
        
    @staticmethod
    def storage():
        """Get the storage path."""
        return storage_path_helper()

class Log(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'log'
        
    @staticmethod
    def info(message: str, *args):
        """Log an info message."""
        return log_helper('info', message, *args)
        
    @staticmethod
    def error(message: str, *args):
        """Log an error message."""
        return log_helper('error', message, *args)
        
    @staticmethod
    def warning(message: str, *args):
        """Log a warning message."""
        return log_helper('warning', message, *args)
        
    @staticmethod
    def debug(message: str, *args):
        """Log a debug message."""
        return log_helper('debug', message, *args)

class Url(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'url'
        
    @staticmethod
    def to(path: str, parameters: dict = None):
        """Generate a URL for the given path."""
        return url_helper(path, parameters)
        
    @staticmethod
    def secure(path: str, parameters: dict = None):
        """Generate a secure URL for the given path."""
        return secure_url_helper(path, parameters)
        
    @staticmethod
    def route(name: str, parameters: dict = None):
        """Generate a URL for the given route."""
        return route_helper(name, parameters)
        
    @staticmethod
    def asset(path: str):
        """Generate a URL for the given asset."""
        return secure_asset_helper(path)
        
    @staticmethod
    def secure_asset(path: str):
        """Generate a secure URL for the given asset."""
        return secure_asset_helper(path)

class Redirect(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'redirect'
        
    @staticmethod
    def to(path: str, parameters: dict = None):
        """Redirect to the given path."""
        return redirect_helper(path, parameters)
        
    @staticmethod
    def back():
        """Redirect back to the previous page."""
        return back_helper()

class Request(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'request'
        
    @staticmethod
    def get(key: str = None, default=None):
        """Get a request value."""
        return request_helper(key, default)
        
    @staticmethod
    def old(key: str = None, default=None):
        """Get an old input value."""
        return old_helper(key, default)
        
    @staticmethod
    def session(key: str = None, default=None):
        """Get a session value."""
        return session_helper(key, default)

class Translation(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'trans'
        
    @staticmethod
    def get(key: str, parameters: dict = None):
        """Get a translation string."""
        return __helper(key, parameters)
        
    @staticmethod
    def choice(key: str, number: int, parameters: dict = None):
        """Get a translation string with pluralization."""
        return trans_choice_helper(key, number, parameters)

class Collection(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'collection'
        
    @staticmethod
    def make(items):
        """Create a new collection."""
        return collect_helper(items)
        
    @staticmethod
    def get(data, key: str, default=None):
        """Get a value from the data using dot notation."""
        return data_get_helper(data, key, default)
        
    @staticmethod
    def set(data, key: str, value):
        """Set a value in the data using dot notation."""
        return data_set_helper(data, key, value)
        
    @staticmethod
    def head(items):
        """Get the first item from the collection."""
        return head_helper(items)
        
    @staticmethod
    def last(items):
        """Get the last item from the collection."""
        return last_helper(items)
        
    @staticmethod
    def value(value, default=None):
        """Get the value or return the default."""
        return value_helper(value, default)
        
    @staticmethod
    def with_value(value, callback):
        """Execute the callback if the value is not null."""
        return with_value_helper(value, callback)

class Security(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'security'
        
    @staticmethod
    def hash(value: str):
        """Hash the given value."""
        return bcrypt_hash_helper(value)
        
    @staticmethod
    def check(value: str, hashed: str):
        """Check if the value matches the hash."""
        return bcrypt_check_helper(value, hashed)

class Event(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'event'
        
    @staticmethod
    def listen(event: str, listener):
        """Register an event listener."""
        return event_helper(event, listener)
        
    @staticmethod
    def dispatch(event: str, *args):
        """Dispatch an event."""
        return dispatch_helper(event, *args) 