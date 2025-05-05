from core.facade.facade import Facade
from typing import Dict, Any, Optional

class Template(Facade):
    @staticmethod
    def get_facade_accessor():
        """Get the facade accessor name."""
        return 'template'
        
    @staticmethod
    def render(template: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Render a template with the given context."""
        return Template.get_facade_root().render(template, context or {})
        
    @staticmethod
    def make(template: str) -> 'Template':
        """Create a new template instance."""
        from core.services.template_engine import Template as TemplateInstance
        return TemplateInstance(template) 