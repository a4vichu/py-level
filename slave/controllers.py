import os
import re
from typing import List, Optional
from pathlib import Path
from jinja2 import Template

# Controller template
CONTROLLER_TEMPLATE = '''from typing import Dict, Any
from .base_controller import BaseController

class {{ name }}:
    """{{ name }} controller"""
    
    {% for method in methods %}
    async def {{ method }}(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle {{ method.upper() }} request"""
        return {
            'message': '{{ name }} {{ method.upper() }} endpoint'
        }
    
    {% endfor %}
'''

def create_controller(name: str, methods: List[str]) -> None:
    """Create a new controller"""
    # Validate controller name
    if not re.match(r'^[A-Za-z][A-Za-z0-9]*Controller$', name):
        raise ValueError(
            "Invalid controller name. Must end with 'Controller' and start with a letter."
        )
    
    # Get controllers directory
    controllers_dir = _get_controllers_dir()
    
    # Create controller file path
    controller_file = controllers_dir / f"{_to_snake_case(name)}.py"
    
    # Check if controller already exists
    if controller_file.exists():
        raise ValueError(f"Controller {name} already exists")
    
    # Create controllers directory if it doesn't exist
    controllers_dir.mkdir(parents=True, exist_ok=True)
    
    # Create controller file
    template = Template(CONTROLLER_TEMPLATE)
    content = template.render(name=name, methods=methods)
    
    with open(controller_file, 'w') as f:
        f.write(content)
        
def list_controllers() -> List[str]:
    """List all controllers"""
    controllers = []
    controllers_dir = _get_controllers_dir()
    
    if controllers_dir.exists():
        for file in controllers_dir.glob('*_controller.py'):
            controller_name = _to_class_name(file.stem)
            controllers.append(controller_name)
            
    return sorted(controllers)
    
def remove_controller(name: str) -> None:
    """Remove a controller"""
    # Validate controller name
    if not name.endswith('Controller'):
        name = f"{name}Controller"
        
    # Get controller file path
    controllers_dir = _get_controllers_dir()
    controller_file = controllers_dir / f"{_to_snake_case(name)}.py"
    
    # Check if controller exists
    if not controller_file.exists():
        raise ValueError(f"Controller {name} does not exist")
        
    # Remove controller file
    controller_file.unlink()
    
def _get_controllers_dir() -> Path:
    """Get the controllers directory path"""
    return Path(os.path.dirname(__file__)) / 'app' / 'controllers'
    
def _to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case"""
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()
    
def _to_class_name(snake_str: str) -> str:
    """Convert snake_case to CamelCase"""
    return ''.join(x.capitalize() for x in snake_str.split('_')) 