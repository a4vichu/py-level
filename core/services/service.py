from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

class Service(ABC):
    def __init__(self):
        self._app = None
        
    @property
    def app(self) -> Any:
        """Get the application instance"""
        return self._app
        
    def set_app(self, app: Any):
        """Set the application instance"""
        self._app = app
        
    @abstractmethod
    def handle(self, *args, **kwargs) -> Any:
        """Handle the service"""
        pass
        
class ServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('service', Service)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot service bindings
        pass
        
class ServiceContainer:
    def __init__(self):
        self._services: Dict[str, Service] = {}
        
    def register(self, name: str, service: Service):
        """Register a service"""
        self._services[name] = service
        
    def get(self, name: str) -> Optional[Service]:
        """Get a service"""
        return self._services.get(name)
        
    def has(self, name: str) -> bool:
        """Determine if a service exists"""
        return name in self._services
        
    def all(self) -> Dict[str, Service]:
        """Get all services"""
        return self._services
        
    def remove(self, name: str) -> bool:
        """Remove a service"""
        if name in self._services:
            del self._services[name]
            return True
        return False
        
    def clear(self):
        """Clear all services"""
        self._services.clear()
        
class ServiceContainerServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('service_container', ServiceContainer)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot service container bindings
        pass 