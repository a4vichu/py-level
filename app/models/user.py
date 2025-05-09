from core.database.orm.model import Model
from core.database.orm.decorators import model
from core.database.schema import Column, Integer, String, DateTime
from datetime import datetime

@model(
    table='users',
    fillable=['name', 'email'],  # Add your fillable fields here
    hidden=['password'],  # Add fields to hide from JSON/array output
    casts={
        'id': 'int',
        'created_at': 'datetime',
        'updated_at': 'datetime'
    }
)
class User(Model):
    """
    User model
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __repr__(self):
        return f'<User {self.id}>'
