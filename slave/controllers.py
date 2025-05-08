import os
import re
from typing import List, Optional
from pathlib import Path
from jinja2 import Template
from .exceptions import SlaveProcessError

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
    """
    Create a new controller file
    
    Args:
        name: The name of the controller
        methods: List of HTTP methods to implement
    """
    # Convert name to snake case
    controller_name = ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
    
    # Add 'controller' suffix if not present
    if not controller_name.endswith('_controller'):
        controller_name += '_controller'
    
    # Define the controller directory and file path
    controller_dir = Path('app/Http/Controllers')
    controller_file = controller_dir / f"{controller_name}.py"
    
    # Create the controllers directory if it doesn't exist
    controller_dir.mkdir(parents=True, exist_ok=True)
    
    # Method templates
    method_templates = {
        'get': '''    def get(self, request):
        """Handle GET request"""
        return {'message': 'GET method not implemented'}
''',
        'post': '''    def post(self, request):
        """Handle POST request"""
        return {'message': 'POST method not implemented'}
''',
        'put': '''    def put(self, request):
        """Handle PUT request"""
        return {'message': 'PUT method not implemented'}
''',
        'delete': '''    def delete(self, request):
        """Handle DELETE request"""
        return {'message': 'DELETE method not implemented'}
'''
    }
    
    # Build methods string
    methods_str = ''
    for method in methods:
        if method.lower() in method_templates:
            methods_str += method_templates[method.lower()]
    
    # Convert to PascalCase for class name
    class_name = ''.join(word.title() for word in controller_name.split('_'))
    
    # Controller template
    controller_template = f'''from core.http.controllers.controller import Controller
from core.http import Request, Response

class {class_name}(Controller):
    """
    {class_name} controller
    """
{methods_str}
'''
    
    # Write the controller file
    if controller_file.exists():
        raise SlaveProcessError(f"Controller {controller_name} already exists")
        
    with open(controller_file, 'w') as f:
        f.write(controller_template)

def list_controllers() -> List[str]:
    """List all available controllers"""
    controller_dir = Path('app/controllers')
    if not controller_dir.exists():
        return []
    
    controllers = []
    for file in controller_dir.glob('*.py'):
        if file.stem != '__init__':
            controllers.append(file.stem)
    return controllers

def remove_controller(name: str) -> None:
    """Remove a controller"""
    controller_name = name[0].upper() + name[1:] if name else ''
    if not controller_name.endswith('Controller'):
        controller_name += 'Controller'
    
    controller_file = Path('app/controllers') / f"{controller_name.lower()}.py"
    if not controller_file.exists():
        raise SlaveProcessError(f"Controller {controller_name} does not exist")
    
    os.remove(controller_file)
    
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