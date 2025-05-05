from abc import ABC, abstractmethod
from core.foundation.application import Application

class ServiceProvider(ABC):
    """Base class for service providers"""
    
    def __init__(self):
        self.app = None
        
    def register(self, app: Application):
        """Register the service provider"""
        self.app = app
        self._register()
        
    def boot(self, app: Application):
        """Boot the service provider"""
        self.app = app
        self._boot()
        
    @abstractmethod
    def _register(self):
        """Register services"""
        pass
        
    def _boot(self):
        """Boot services"""
        pass 