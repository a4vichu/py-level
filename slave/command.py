import json
from typing import Dict, Any, Set
from datetime import datetime
from .exceptions import ValidationError
from dataclasses import dataclass
from functools import wraps

def command(func):
    """Decorator to register a command function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@dataclass
class Command:
    """Represents a command to be executed"""
    
    command_id: str
    command_type: str
    parameters: Dict[str, Any]
    timestamp: datetime = datetime.now()

class CommandValidator:
    """Validates command structure and content"""
    
    def __init__(self):
        self.valid_command_types: Set[str] = set()
        
    def register_command_type(self, command_type: str):
        """Register a valid command type"""
        self.valid_command_types.add(command_type)
        
    def validate(self, command_data: Dict[str, Any]) -> Command:
        """Validate command data"""
        if not isinstance(command_data, dict):
            raise ValueError("Command must be a dictionary")
            
        if 'command_id' not in command_data:
            raise ValueError("Command must have a command_id")
            
        if 'command_type' not in command_data:
            raise ValueError("Command must have a command_type")
            
        if 'parameters' not in command_data:
            command_data['parameters'] = {}
            
        return Command(
            command_id=command_data['command_id'],
            command_type=command_data['command_type'],
            parameters=command_data['parameters']
        )
        
    def validate_command_str(self, command_str: str) -> Command:
        """Validate command string and create Command object"""
        try:
            # Parse JSON
            data = json.loads(command_str)
            
            # Create command
            command = self.validate(data)
            
            # Validate command type
            if command.command_type not in self.valid_command_types:
                raise ValidationError(f"Invalid command type: {command.command_type}")
                
            return command
            
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON: {str(e)}")
        except Exception as e:
            if not isinstance(e, ValidationError):
                raise ValidationError(f"Invalid command format: {str(e)}")
            raise 

@command
def migrate_refresh():
    """Refresh all migrations by rolling back and re-running them"""
    from .migrations import refresh_migrations
    refresh_migrations()
    print("✓ Migrations refreshed successfully")

@command
def migrate_rollback(steps: int = 1):
    """Rollback the last N migrations
    
    Args:
        steps: Number of migrations to rollback (default: 1)
    """
    from .migrations import rollback_migrations
    rollback_migrations(steps)
    print(f"✓ Rolled back {steps} migration(s) successfully")

@command
def migrate_fresh():
    """Drop all tables and re-run all migrations"""
    from .migrations import fresh_migrations
    fresh_migrations()
    print("✓ Database refreshed successfully") 