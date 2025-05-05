from core.facade.facade import Facade
from core.facade.helpers import (
    db as db_helper,
    db_table as db_table_helper
)

class DB(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'db'
        
    @staticmethod
    def query(query: str, bindings: List = None):
        """Execute a database query."""
        return db_helper(query, bindings)
        
    @staticmethod
    def table(table: str):
        """Get a database table instance."""
        return db_table_helper(table)
        
    @staticmethod
    def select(query: str, bindings: List = None):
        """Execute a select query."""
        from core.database import db as db_manager
        return db_manager.select(query, bindings)
        
    @staticmethod
    def insert(query: str, bindings: List = None):
        """Execute an insert query."""
        from core.database import db as db_manager
        return db_manager.insert(query, bindings)
        
    @staticmethod
    def update(query: str, bindings: List = None):
        """Execute an update query."""
        from core.database import db as db_manager
        return db_manager.update(query, bindings)
        
    @staticmethod
    def delete(query: str, bindings: List = None):
        """Execute a delete query."""
        from core.database import db as db_manager
        return db_manager.delete(query, bindings) 