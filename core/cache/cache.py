from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
import time
import json
import uuid

class Cache(ABC):
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get an item from the cache"""
        if key in self._store:
            item = self._store[key]
            if item['expires'] is None or item['expires'] > time.time():
                return item['value']
            self.forget(key)
        return default
        
    def put(self, key: str, value: Any, ttl: Optional[int] = None):
        """Store an item in the cache"""
        self._store[key] = {
            'value': value,
            'expires': time.time() + ttl if ttl is not None else None
        }
        
    def add(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Store an item in the cache if it doesn't exist"""
        if key not in self._store:
            self.put(key, value, ttl)
            return True
        return False
        
    def forever(self, key: str, value: Any):
        """Store an item in the cache indefinitely"""
        self.put(key, value)
        
    def remember(self, key: str, ttl: Optional[int], callback: Callable) -> Any:
        """Get an item from the cache, or store the default value"""
        value = self.get(key)
        if value is not None:
            return value
            
        value = callback()
        self.put(key, value, ttl)
        return value
        
    def forget(self, key: str) -> bool:
        """Remove an item from the cache"""
        if key in self._store:
            del self._store[key]
            return True
        return False
        
    def flush(self):
        """Remove all items from the cache"""
        self._store.clear()
        
    def has(self, key: str) -> bool:
        """Determine if an item exists in the cache"""
        return key in self._store and (
            self._store[key]['expires'] is None or
            self._store[key]['expires'] > time.time()
        )
        
class CacheServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('cache', Cache)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot cache bindings
        pass
        
class CacheManager:
    def __init__(self):
        self._stores: Dict[str, Cache] = {}
        
    def register(self, name: str, store: Cache):
        """Register a cache store"""
        self._stores[name] = store
        
    def get(self, name: str) -> Optional[Cache]:
        """Get a cache store"""
        return self._stores.get(name)
        
    def has(self, name: str) -> bool:
        """Determine if a cache store exists"""
        return name in self._stores
        
    def all(self) -> Dict[str, Cache]:
        """Get all cache stores"""
        return self._stores
        
    def remove(self, name: str) -> bool:
        """Remove a cache store"""
        if name in self._stores:
            del self._stores[name]
            return True
        return False
        
    def clear(self):
        """Clear all cache stores"""
        self._stores.clear()
        
class CacheManagerServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('cache_manager', CacheManager)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot cache manager bindings
        pass 