from core.foundation.service_provider import ServiceProvider
from app.routes.web import web_routes

class RouteServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        pass

    def _boot(self):
        """Boot the service provider"""
        router = self.app.make('router')
        web_routes(router) 