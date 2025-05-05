from typing import Any, Dict, List, Optional, Type, TypeVar
from datetime import datetime
import json

T = TypeVar('T', bound='Model')

class Model:
    _table: str = ''
    _primary_key: str = 'id'
    _fillable: List[str] = []
    _hidden: List[str] = []
    _casts: Dict[str, str] = {}
    
    def __init__(self, **kwargs):
        self._attributes: Dict[str, Any] = {}
        self._original: Dict[str, Any] = {}
        self._exists: bool = False
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __getattr__(self, name: str) -> Any:
        if name in self._attributes:
            return self._cast_attribute(name, self._attributes[name])
        return None
        
    def __setattr__(self, name: str, value: Any):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._attributes[name] = value
            
    def _cast_attribute(self, name: str, value: Any) -> Any:
        if name in self._casts:
            cast_type = self._casts[name]
            if cast_type == 'int':
                return int(value)
            elif cast_type == 'float':
                return float(value)
            elif cast_type == 'bool':
                return bool(value)
            elif cast_type == 'datetime':
                return datetime.fromisoformat(value) if isinstance(value, str) else value
            elif cast_type == 'json':
                return json.loads(value) if isinstance(value, str) else value
        return value
        
    @classmethod
    def find(cls: Type[T], id: Any) -> Optional[T]:
        """Find a model by its primary key"""
        # Implement database query
        pass
        
    @classmethod
    def where(cls: Type[T], column: str, operator: str, value: Any) -> List[T]:
        """Query the database"""
        # Implement database query
        pass
        
    def save(self) -> bool:
        """Save the model to the database"""
        if self._exists:
            return self._update()
        return self._insert()
        
    def _insert(self) -> bool:
        """Insert the model into the database"""
        # Implement database insert
        self._exists = True
        return True
        
    def _update(self) -> bool:
        """Update the model in the database"""
        # Implement database update
        return True
        
    def delete(self) -> bool:
        """Delete the model from the database"""
        # Implement database delete
        self._exists = False
        return True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary"""
        attributes = {}
        for key, value in self._attributes.items():
            if key not in self._hidden:
                attributes[key] = value
        return attributes
        
    def to_json(self) -> str:
        """Convert the model to JSON"""
        return json.dumps(self.to_dict())
        
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create a model from a dictionary"""
        return cls(**data)
        
    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """Create a model from JSON"""
        return cls.from_dict(json.loads(json_str)) 