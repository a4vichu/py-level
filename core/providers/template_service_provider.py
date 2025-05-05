from core.providers.provider import ServiceProvider
from core.services.template_engine import TemplateEngine

class TemplateServiceProvider(ServiceProvider):
    def _register(self):
        """Register the template engine service."""
        self.app.singleton('template', TemplateEngine())
        
    def _boot(self):
        """Boot the template engine service."""
        pass 