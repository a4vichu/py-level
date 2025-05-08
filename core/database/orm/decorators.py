from typing import List, Dict, Any, Type, TypeVar, Optional, Callable
from functools import wraps

T = TypeVar('T')

def model(table: Optional[str] = None,
          primary_key: str = 'id',
          fillable: Optional[List[str]] = None,
          hidden: Optional[List[str]] = None,
          casts: Optional[Dict[str, str]] = None,
          timestamps: bool = True) -> Callable[[Type[T]], Type[T]]:
    """
    Model decorator for configuring model attributes
    
    Args:
        table: The table name (if None, will be derived from class name)
        primary_key: The primary key field name
        fillable: List of fields that can be mass-assigned
        hidden: List of fields that should be hidden from array/JSON output
        casts: Dictionary of field type casts
        timestamps: Whether to include created_at and updated_at timestamps
    """
    def decorator(cls: Type[T]) -> Type[T]:
        # Set table name if not provided
        if not hasattr(cls, '_table') or not cls._table:
            cls._table = table or cls.__name__.lower() + 's'
        
        # Set primary key
        cls._primary_key = primary_key
        
        # Set fillable fields
        cls._fillable = fillable or []
        
        # Set hidden fields
        cls._hidden = hidden or []
        
        # Set field casts
        cls._casts = casts or {}
        
        # Add timestamp fields if enabled
        if timestamps:
            if 'created_at' not in cls._casts:
                cls._casts['created_at'] = 'datetime'
            if 'updated_at' not in cls._casts:
                cls._casts['updated_at'] = 'datetime'
        
        return cls
    
    return decorator 