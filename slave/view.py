import os
from typing import Dict, Any, Optional
from pathlib import Path

class View:
    """View class for handling template rendering"""
    
    _view_paths = []
    _shared_data = {}
    
    @classmethod
    def add_path(cls, path: str):
        """Add a view path to search for templates"""
        cls._view_paths.append(path)
        
    @classmethod
    def share(cls, key: str, value: Any):
        """Share data across all views"""
        cls._shared_data[key] = value
        
    @classmethod
    def make(cls, view_name: str, data: Optional[Dict[str, Any]] = None) -> str:
        """
        Render a view template with the given data
        
        Args:
            view_name: The name of the view file (without extension)
            data: Dictionary of data to pass to the view
            
        Returns:
            str: Rendered HTML content
        """
        # Convert view name to file path
        view_path = cls._get_view_path(view_name)
        
        # Read template
        with open(view_path, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # Merge shared data with view data
        merged_data = {**cls._shared_data, **(data or {})}
            
        # Replace template variables
        for key, value in merged_data.items():
            template = template.replace(f'{{{{ {key} }}}}', str(value))
                
        return template
        
    @classmethod
    def _get_view_path(cls, view_name: str) -> str:
        """
        Get the full path to a view file
        
        Args:
            view_name: The name of the view file (without extension)
            
        Returns:
            str: Full path to the view file
        """
        # Convert dots to directory separators
        view_path = view_name.replace('.', '/')
        
        # Add .html extension
        view_path = f"{view_path}.html"
        
        # Search in all view paths
        for base_path in cls._view_paths:
            full_path = os.path.join(base_path, view_path)
            if os.path.exists(full_path):
                return full_path
                
        raise FileNotFoundError("View [{}] not found.".format(view_name))
        
    @classmethod
    def exists(cls, view_name: str) -> bool:
        """
        Check if a view exists
        
        Args:
            view_name: The name of the view file (without extension)
            
        Returns:
            bool: True if view exists, False otherwise
        """
        try:
            cls._get_view_path(view_name)
            return True
        except FileNotFoundError:
            return False 