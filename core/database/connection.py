import sqlite3
import mysql.connector
import psycopg2
from typing import List, Tuple, Any, Dict
from config.database import config

class Connection:
    _instances: Dict[str, 'Connection'] = {}
    
    @classmethod
    def get_instance(cls, connection_name: str = None) -> 'Connection':
        """Get a database connection instance"""
        if connection_name is None:
            db_config = config()
            connection_name = db_config.get('default', 'sqlite')
            
        if connection_name not in cls._instances:
            cls._instances[connection_name] = Connection()
            # Get connection config
            db_config = config()
            connection_config = db_config['connections'][connection_name]
            driver = connection_config.pop('driver')  # Remove driver from config
            # Connect using the configuration
            cls._instances[connection_name].connect(driver, **connection_config)
            
        return cls._instances[connection_name]
    
    def __init__(self):
        self.connection = None
        self.query_pointer = None
        self.driver = None
        
    def connect(self, driver: str, **kwargs):
        """Connect to the database"""
        self.driver = driver
        if driver == 'sqlite':
            database = kwargs.get('database', ':memory:')
            if database != ':memory:':
                import os
                # Create database directory if it doesn't exist
                db_dir = os.path.dirname(os.path.abspath(database))
                if not os.path.exists(db_dir):
                    os.makedirs(db_dir)
            self.connection = sqlite3.connect(database)
            # Enable foreign key support
            self.connection.execute("PRAGMA foreign_keys = ON")
            # Use Row factory for better result handling
            self.connection.row_factory = sqlite3.Row
        elif driver == 'mysql':
            self.connection = mysql.connector.connect(
                host=kwargs.get('host', '127.0.0.1'),
                port=kwargs.get('port', 3306),
                database=kwargs.get('database', 'pylevel'),
                user=kwargs.get('username', 'root'),
                password=kwargs.get('password', ''),
                charset=kwargs.get('charset', 'utf8mb4')
            )
        elif driver == 'pgsql':
            self.connection = psycopg2.connect(
                host=kwargs.get('host', '127.0.0.1'),
                port=kwargs.get('port', 5432),  # Use PostgreSQL default port
                dbname=kwargs.get('database', 'pylevel'),
                user=kwargs.get('username', 'postgres'),  # Use PostgreSQL default user
                password=kwargs.get('password', ''),
                options=f"-c search_path={kwargs.get('schema', 'public')}"
            )
            
    def execute(self, query: str, params: tuple = None) -> List[Tuple[Any, ...]]:
        """Execute a query and return results"""
        if not self.connection:
            raise Exception("Database connection not set")
            
        query_pointer = self.connection.cursor()
        try:
            if params:
                query_pointer.execute(query, params)
            else:
                query_pointer.execute(query)
                
            if query.strip().upper().startswith(('SELECT', 'PRAGMA', 'SHOW')):
                try:
                    results = query_pointer.fetchall()
                except (sqlite3.Error, mysql.connector.Error, psycopg2.Error):
                    results = []
            else:
                results = []
                
            self.connection.commit()
            return results
        finally:
            query_pointer.close()
        
    def close(self):
        """Close the connection"""
        if self.query_pointer:
            self.query_pointer.close()
            self.query_pointer = None
            
        if self.connection:
            self.connection.close()
            self.connection = None
            
    def get_driver(self) -> str:
        """Get the current database driver"""
        return self.driver 