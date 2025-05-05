from typing import Dict, Any, Optional
from pathlib import Path
from core.foundation.application import Application
from core.http.request import Request

def view(view_name: str, data: Optional[Dict[str, Any]] = None) -> str:
    """Render a view template"""
    request = Request.current()
    template = request.app.make('template')
    
    # Get the template file path
    template_path = Path(__file__).parent.parent / 'resources' / 'views' / f"{view_name}.html"
    
    # Load and render the template
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            return template.render(template_content, data or {})
    except FileNotFoundError:
        return f"Template '{view_name}' not found." 