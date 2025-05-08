from core.database.migrations import Migration
from core.database.schema import Column, Integer, String, DateTime

class CreateMigrationsTable(Migration):
    """
    Migration to create the migrations table
    """
    def up(self):
        """Create the migrations table"""
        self.create_table('migrations', [
            Column('id', Integer, primary_key=True, auto_increment=True),
            Column('migration', String, nullable=False),
            Column('batch', Integer, nullable=False),
            Column('created_at', DateTime)
        ])
    
    def down(self):
        """Drop the migrations table"""
        self.drop_table('migrations') 