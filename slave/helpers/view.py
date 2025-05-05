from core.facade.template import Template
import os

def view(template: str, context: dict = None) -> str:
    """
    Render a view template with the given context.
    
    Args:
        template: The template name (without extension)
        context: The context data to pass to the template
        
    Returns:
        The rendered template as a string
    """
    # Get the template path
    template_path = os.path.join('resources', 'views', f'{template}.html')
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Render the template
    return Template.render(template_content, context or {}) 