from core.foundation.service_provider import ServiceProvider
from core.routing.router import Router
from routes.web import register_web_routes
from routes.api import register_api_routes

class RouteServiceProvider(ServiceProvider):
    def _register(self):
        """Register the router service."""
        self.app.singleton('router', Router())
        
    def _boot(self):
        """Boot the router service."""
        router = self.app.make('router')
        register_web_routes(router)
        register_api_routes(router) 