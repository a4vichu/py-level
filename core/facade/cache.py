from core.facade.facade import Facade
from core.facade.helpers import (
    cache as cache_helper,
    cache_remember as cache_remember_helper
)

class Cache(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'cache'
        
    @staticmethod
    def get(key: str, default=None):
        """Get a cache value."""
        return cache_helper(key, default)
        
    @staticmethod
    def put(key: str, value: Any, ttl: int = None):
        """Store a value in the cache."""
        return cache_helper(key, value, ttl)
        
    @staticmethod
    def remember(key: str, ttl: int, callback):
        """Get a cache value or store the result of the callback."""
        return cache_remember_helper(key, ttl, callback)
        
    @staticmethod
    def forget(key: str):
        """Remove a value from the cache."""
        from core.cache import cache as cache_manager
        return cache_manager.forget(key)
        
    @staticmethod
    def flush():
        """Remove all items from the cache."""
        from core.cache import cache as cache_manager
        return cache_manager.flush() 