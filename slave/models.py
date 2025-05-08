import os
from pathlib import Path
from typing import List
from .exceptions import SlaveProcessError

def create_model(name: str) -> None:
    """
    Create a new model class file
    
    Args:
        name: The name of the model class
    """
    # Ensure the name is properly formatted
    model_name = name[0].upper() + name[1:] if name else ''
    if not model_name:
        raise SlaveProcessError("Model name cannot be empty")
    
    # Define the model directory and file path
    model_dir = Path('app/models')
    model_file = model_dir / f"{model_name.lower()}.py"
    
    # Create the models directory if it doesn't exist
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Model template with proper string formatting and @model decorator
    model_template = f"""from core.database import Model
from core.database.orm.decorators import model
from datetime import datetime

@model(
    table='{model_name.lower()}s',
    fillable=['name', 'email'],  # Add your fillable fields here
    hidden=['password'],  # Add fields to hide from JSON/array output
    casts={{
        'id': 'int',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }}
)
class {model_name}(Model):
    \"\"\"
    {model_name} model
    \"\"\"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __repr__(self):
        return f'<{model_name} {{self.id}}>'
"""
    
    # Write the model file
    if model_file.exists():
        raise SlaveProcessError(f"Model {model_name} already exists")
        
    with open(model_file, 'w') as f:
        f.write(model_template) 