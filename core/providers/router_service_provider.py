from core.foundation.service_provider import ServiceProvider
from core.routing.router import Router

class RouterServiceProvider(ServiceProvider):
    def _register(self):
        """Register the router service."""
        self.app.singleton('router', lambda app: Router())
        
    def _boot(self):
        """Boot the router service."""
        pass 