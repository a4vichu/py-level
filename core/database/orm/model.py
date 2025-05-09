from typing import Any, Dict, List, Optional, Type, TypeVar
from datetime import datetime
import json
from core.database.connection import Connection

T = TypeVar('T', bound='Model')

class Model:
    # Default values that can be overridden by @model decorator
    _table: str = ''
    _primary_key: str = 'id'
    _fillable: List[str] = []
    _hidden: List[str] = []
    _casts: Dict[str, str] = {}
    
    def __init__(self, **kwargs):
        self._attributes: Dict[str, Any] = {}
        self._original: Dict[str, Any] = {}
        self._exists: bool = False
        
        # Set timestamps if enabled
        if 'created_at' in self._casts and 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.utcnow()
        if 'updated_at' in self._casts and 'updated_at' not in kwargs:
            kwargs['updated_at'] = datetime.utcnow()
        
        # Only set fillable attributes if specified
        for key, value in kwargs.items():
            if not self._fillable or key in self._fillable:
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
                return int(value) if value is not None else None
            elif cast_type == 'float':
                return float(value) if value is not None else None
            elif cast_type == 'bool':
                return bool(value) if value is not None else None
            elif cast_type == 'datetime':
                return datetime.fromisoformat(value) if isinstance(value, str) else value
            elif cast_type == 'json':
                return json.loads(value) if isinstance(value, str) else value
        return value

    @classmethod
    def _get_connection(cls) -> Connection:
        """Get database connection instance"""
        return Connection.get_instance()

    @classmethod
    def _execute_query(cls, query: str, params: tuple = None) -> List[tuple]:
        """Execute a database query"""
        connection = cls._get_connection()
        return connection.execute(query, params)

    @classmethod
    def _build_select_query(cls, conditions: str = None, params: tuple = None) -> tuple:
        """Build a SELECT query"""
        query = f"SELECT * FROM {cls._table}"
        if conditions:
            query += f" WHERE {conditions}"
        return query, params

    @classmethod
    def _create_instance(cls, row: tuple) -> 'Model':
        """Create a model instance from a database row"""
        instance = cls()
        instance._exists = True
        for key, value in zip(row.keys(), row):
            setattr(instance, key, value)
        return instance

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        """Get all records from the table"""
        query, params = cls._build_select_query()
        results = cls._execute_query(query, params)
        return [cls._create_instance(row) for row in results]
        
    @classmethod
    def find(cls: Type[T], id: Any) -> Optional[T]:
        """Find a model by its primary key"""
        query, params = cls._build_select_query(
            f"{cls._primary_key} = %s",
            (id,)
        )
        results = cls._execute_query(query, params)
        return cls._create_instance(results[0]) if results else None
        
    @classmethod
    def where(cls: Type[T], column: str, operator: str, value: Any) -> List[T]:
        """Query the database with conditions"""
        query, params = cls._build_select_query(
            f"{column} {operator} %s",
            (value,)
        )
        results = cls._execute_query(query, params)
        return [cls._create_instance(row) for row in results]
        
    def save(self) -> bool:
        """Save the model to the database"""
        # Update timestamps if enabled
        if 'updated_at' in self._casts:
            self.updated_at = datetime.utcnow()
            
        if self._exists:
            return self._update()
        
        if 'created_at' in self._casts:
            self.created_at = datetime.utcnow()
        return self._insert()
        
    def _insert(self) -> bool:
        """Insert the model into the database"""
        columns = []
        values = []
        params = []
        
        for key, value in self._attributes.items():
            if not self._fillable or key in self._fillable:
                columns.append(key)
                values.append('%s')
                params.append(value)
        
        query = f"INSERT INTO {self._table} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        self._execute_query(query, tuple(params))
        self._exists = True
        return True
        
    def _update(self) -> bool:
        """Update the model in the database"""
        sets = []
        params = []
        
        for key, value in self._attributes.items():
            if not self._fillable or key in self._fillable:
                sets.append(f"{key} = %s")
                params.append(value)
        
        params.append(getattr(self, self._primary_key))
        query = f"UPDATE {self._table} SET {', '.join(sets)} WHERE {self._primary_key} = %s"
        self._execute_query(query, tuple(params))
        return True
        
    def delete(self) -> bool:
        """Delete the model from the database"""
        query = f"DELETE FROM {self._table} WHERE {self._primary_key} = %s"
        self._execute_query(query, (getattr(self, self._primary_key),))
        self._exists = False
        return True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary"""
        attributes = {}
        for key, value in self._attributes.items():
            if key not in self._hidden:
                attributes[key] = self._cast_attribute(key, value)
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