"""
Database module with Model base class and schema components
"""

class Model:
    """Base model class for all database models"""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}>" 