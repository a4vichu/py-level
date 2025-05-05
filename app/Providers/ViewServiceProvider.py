from core.foundation.service_provider import ServiceProvider
from slave.view import View
from pathlib import Path

class ViewServiceProvider(ServiceProvider):
    """Service provider for view system"""
    
    def _register(self):
        """Register view paths and shared data"""
        # Add default view path
        View.add_path(str(Path(__file__).parent.parent.parent / 'resources' / 'views'))
        
        # Share common data with all views
        View.share('app_name', 'PY Level')
        View.share('app_version', '1.0.0')
        
        # Register view in container
        self.app.singleton('view', View)
        
    def _boot(self):
        """Boot the view system"""
        # Additional view configuration can go here
        pass 