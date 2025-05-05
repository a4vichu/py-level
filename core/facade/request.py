from core.facade.facade import Facade
from core.facade.helpers import (
    request as request_helper,
    old as old_helper,
    session as session_helper
)

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