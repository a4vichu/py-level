from core.database.migrations import Migration
from core.database.schema import Column, Integer, String, DateTime

class CreateUsersTable(Migration):
    """
    Migration to create the users table
    """
    def up(self):
        """Create the table"""
        self.create_table('users', [
            Column('id', Integer, primary_key=True),
            Column('created_at', DateTime),
            Column('updated_at', DateTime)
        ])
    
    def down(self):
        """Drop the table"""
        self.drop_table('users')
