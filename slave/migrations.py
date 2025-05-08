import os
from pathlib import Path
from datetime import datetime
from .exceptions import SlaveProcessError

def create_migration(model_name: str) -> None:
    """
    Create a new migration file for the model
    
    Args:
        model_name: The name of the model
    """
    # Ensure the name is properly formatted
    model_name = model_name[0].upper() + model_name[1:] if model_name else ''
    if not model_name:
        raise SlaveProcessError("Model name cannot be empty")
    
    # Define the migrations directory and file path
    migrations_dir = Path('database/migrations')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    migration_file = migrations_dir / f"{timestamp}_create_{model_name.lower()}s_table.py"
    
    # Create the migrations directory if it doesn't exist
    migrations_dir.mkdir(parents=True, exist_ok=True)
    
    # Migration template
    migration_template = f'''from core.database.migrations import Migration
from core.database.schema import Column, Integer, String, DateTime

class Create{model_name}sTable(Migration):
    """
    Migration to create the {model_name.lower()}s table
    """
    def up(self):
        """Create the table"""
        self.create_table('{model_name.lower()}s', [
            Column('id', Integer, primary_key=True),
            Column('created_at', DateTime),
            Column('updated_at', DateTime)
        ])
    
    def down(self):
        """Drop the table"""
        self.drop_table('{model_name.lower()}s')
'''
    
    # Write the migration file
    with open(migration_file, 'w') as f:
        f.write(migration_template)

def refresh_migrations() -> None:
    """
    Rollback all migrations and then run them again
    """
    from core.database.migrations import Migration
    migration = Migration()
    migration.refresh()

def rollback_migrations(steps: int = 1) -> None:
    """
    Rollback the last N migrations
    
    Args:
        steps: Number of migrations to rollback (default: 1)
    """
    from core.database.migrations import Migration
    migration = Migration()
    migration.rollback(steps)

def fresh_migrations() -> None:
    """
    Drop all tables and re-run all migrations
    """
    from core.database.migrations import Migration
    migration = Migration()
    migration.fresh() 