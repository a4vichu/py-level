from typing import Dict, Any, Optional
from pathlib import Path
from core.foundation.application import Application
from core.http.request import Request
import json
from datetime import datetime

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

def dump(data: Any) -> str:
    """
    Dump data in a readable format, similar to Laravel's dump(), wrapped in <pre> tags for browser formatting.
    
    Args:
        data: The data to dump
        
    Returns:
        str: Formatted string representation of the data
    """
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)
    
    try:
        return f"<pre>{json.dumps(data, default=json_serial, indent=2)}</pre>"
    except Exception as e:
        return f"<pre>Error dumping data: {str(e)}\nData: {str(data)}</pre>" 