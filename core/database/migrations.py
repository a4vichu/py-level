from core.database.schema import (
    Column, ForeignKey, Integer, BigInteger, SmallInteger, Float, Decimal, Numeric,
    String, Text, Char, Varchar, LongText, MediumText, TinyText,
    DateTime, Date, Time, Timestamp, Year,
    Binary, Blob, LongBlob, MediumBlob, TinyBlob,
    Boolean, JSON, Enum, UUID
)
from core.database.connection import Connection
import logging
import os
from datetime import datetime

logger = logging.getLogger('slave.migrations')

class Migration:
    def __init__(self, connection_name: str = None):
        # Get database connection
        self.connection = Connection.get_instance(connection_name)
        self.dialect = self.connection.get_driver()
        
    def create_table(self, table_name, columns, schema='public'):
        """Create a new table with schema support"""
        if not self.connection:
            raise Exception("Database connection not set")
            
        # Build column definitions
        column_defs = []
        foreign_keys = []
        
        for col in columns:
            if isinstance(col, Column):
                col_def = f"{col.name} {self._get_type(col.type)}"
                if col.primary_key:
                    col_def += " PRIMARY KEY"
                    if getattr(col, 'auto_increment', False):
                        if self.dialect == 'mysql':
                            col_def += " AUTO_INCREMENT"
                        elif self.dialect == 'sqlite':
                            col_def += " AUTOINCREMENT"
                if not col.nullable:
                    col_def += " NOT NULL"
                if col.default is not None:
                    col_def += f" DEFAULT {self._format_default(col.default)}"
                if col.unique:
                    col_def += " UNIQUE"
                if col.index:
                    col_def += " INDEX"
                column_defs.append(col_def)
            elif isinstance(col, ForeignKey):
                foreign_keys.append(
                    f"FOREIGN KEY ({col.column}) REFERENCES {col.references} "
                    f"ON DELETE {col.on_delete} ON UPDATE {col.on_update}"
                )
        
        # Combine all definitions
        all_defs = column_defs + foreign_keys
        
        # Create table with schema
        if self.dialect == 'pgsql':
            query = f"CREATE TABLE {schema}.{table_name} ({', '.join(all_defs)})"
        else:
            query = f"CREATE TABLE {table_name} ({', '.join(all_defs)})"
            
        logger.info(f"Executing query: {query}")
        self.connection.execute(query)
        
    def drop_table(self, table_name, schema='public'):
        """Drop an existing table with schema support"""
        if self.dialect == 'pgsql':
            query = f"DROP TABLE IF EXISTS {schema}.{table_name} CASCADE"
        else:
            query = f"DROP TABLE IF EXISTS {table_name}"
        logger.info(f"Executing query: {query}")
        self.connection.execute(query)
        
    def _get_type(self, type_class):
        """Convert Python type to database type"""
        if isinstance(type_class, Enum):
            return str(type_class)
            
        type_map = {
            # Numeric Types
            'Integer': 'INTEGER',
            'BigInteger': 'BIGINT',
            'SmallInteger': 'SMALLINT',
            'Float': 'FLOAT',
            'Decimal': 'DECIMAL',
            'Numeric': 'NUMERIC',
            
            # String Types
            'String': 'VARCHAR(255)',
            'Text': 'TEXT',
            'Char': 'CHAR',
            'Varchar': 'VARCHAR',
            'LongText': 'LONGTEXT' if self.dialect == 'mysql' else 'TEXT',
            'MediumText': 'MEDIUMTEXT' if self.dialect == 'mysql' else 'TEXT',
            'TinyText': 'TINYTEXT' if self.dialect == 'mysql' else 'TEXT',
            
            # Date/Time Types
            'DateTime': 'TIMESTAMP',
            'Date': 'DATE',
            'Time': 'TIME',
            'Timestamp': 'TIMESTAMP',
            'Year': 'YEAR' if self.dialect == 'mysql' else 'INTEGER',
            
            # Binary Types
            'Binary': 'BINARY',
            'Blob': 'BLOB',
            'LongBlob': 'LONGBLOB' if self.dialect == 'mysql' else 'BLOB',
            'MediumBlob': 'MEDIUMBLOB' if self.dialect == 'mysql' else 'BLOB',
            'TinyBlob': 'TINYBLOB' if self.dialect == 'mysql' else 'BLOB',
            
            # Other Types
            'Boolean': 'BOOLEAN',
            'JSON': 'JSON' if self.dialect in ('mysql', 'pgsql') else 'TEXT',
            'Enum': 'ENUM',
            'UUID': 'UUID' if self.dialect == 'pgsql' else 'CHAR(36)'
        }
        return type_map.get(type_class.__name__, 'TEXT')
        
    def _format_default(self, default):
        """Format default value based on type"""
        if isinstance(default, str):
            return f"'{default}'"
        elif isinstance(default, bool):
            return '1' if default else '0'
        elif default is None:
            return 'NULL'
        return str(default)

    def _ensure_migrations_table(self):
        """Ensure the migrations table exists"""
        if not self.connection:
            raise Exception("Database connection not set")
            
        # Check if migrations table exists
        if self.dialect == 'pgsql':
            query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'migrations'
                )
            """
        elif self.dialect == 'mysql':
            query = "SHOW TABLES LIKE 'migrations'"
        else:  # sqlite
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name='migrations'"
            
        result = self.connection.execute(query)
        table_exists = bool(result)
        
        if not table_exists:
            # Create migrations table
            self.create_table('migrations', [
                Column('id', Integer, primary_key=True, auto_increment=True),
                Column('migration', String, nullable=False),
                Column('batch', Integer, nullable=False),
                Column('created_at', DateTime)
            ])
            
    def _record_migration(self, migration_name: str, batch: int):
        """Record a migration in the migrations table"""
        if not self.connection:
            raise Exception("Database connection not set")
            
        # Ensure migrations table exists
        self._ensure_migrations_table()
            
        # Get current timestamp
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert migration record
        query = """
            INSERT INTO migrations (migration, batch, created_at)
            VALUES (%s, %s, %s)
        """
        self.connection.execute(query, (migration_name, batch, now))
        
    def _get_last_batch(self) -> int:
        """Get the last batch number from migrations table"""
        if not self.connection:
            raise Exception("Database connection not set")
            
        # Ensure migrations table exists
        self._ensure_migrations_table()
            
        query = "SELECT MAX(batch) as last_batch FROM migrations"
        result = self.connection.execute(query)
        if result and result[0][0] is not None:
            return result[0][0]
        return 0
        
    def _get_migrations(self):
        """Get all migration files in order"""
        import importlib.util
        from pathlib import Path
        
        migrations_dir = Path('database/migrations')
        if not migrations_dir.exists():
            return []
            
        migrations = []
        for file in sorted(migrations_dir.glob('*.py')):
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find the migration class in the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Migration) and attr != Migration:
                    # Store both the migration instance and its filename
                    migration_instance = attr()
                    migration_instance.filename = file.stem  # Add filename to instance
                    migrations.append(migration_instance)
                    
        return migrations

    def up(self):
        """Run all pending migrations"""
        migrations = self._get_migrations()
        if not migrations:
            logger.info("No migrations to run")
            return
            
        # Get the next batch number
        batch = self._get_last_batch() + 1
        
        # Get already run migrations
        query = "SELECT migration FROM migrations"
        results = self.connection.execute(query)
        run_migrations = {row[0] for row in results} if results else set()
        
        # Run only pending migrations
        for migration in migrations:
            migration_name = migration.filename  # Use filename instead of class name
            if migration_name.endswith('create_migrations_table'):
                # Skip migrations table creation if it already exists
                continue
                
            if migration_name not in run_migrations:
                logger.info(f"Running migration: {migration_name}")
                migration.connection = self.connection
                migration.dialect = self.dialect
                migration.up()
                self._record_migration(migration_name, batch)
                logger.info(f"✅ Migration completed: {migration_name}")
            else:
                logger.info(f"Migration already run: {migration_name}")
                
        logger.info("✅ Migrations completed successfully")

    def down(self):
        """Reverse all migrations"""
        migrations = reversed(self._get_migrations())
        for migration in migrations:
            logger.info(f"Reversing migration: {migration.__class__.__name__}")
            migration.connection = self.connection
            migration.dialect = self.dialect
            migration.down()
            logger.info(f"✅ Migration reversed: {migration.__class__.__name__}")

    def refresh(self):
        """Rollback all migrations and then run them again"""
        self.rollback(0)  # 0 means rollback all
        self.up()

    def rollback(self, steps: int = 1):
        """Rollback the last N migrations or the last batch
        
        Args:
            steps: Number of migrations to rollback (0 means all)
        """
        if not self.connection:
            raise Exception("Database connection not set")
            
        # Get the last batch number
        last_batch = self._get_last_batch()
        if last_batch == 0:
            logger.info("No migrations to rollback")
            return
            
        # Get migrations from the last batch
        query = "SELECT migration FROM migrations WHERE batch = %s ORDER BY id DESC"
        results = self.connection.execute(query, (last_batch,))
        if not results:
            logger.info(f"No migrations found in batch {last_batch}")
            return
            
        # Get all migration files
        migrations = self._get_migrations()
        if not migrations:
            logger.info("No migration files found")
            return
            
        # Create a mapping of migration filenames to instances
        migration_map = {m.filename: m for m in migrations}
        
        # Rollback each migration in the last batch
        for migration_name in [row[0] for row in results]:
            if migration_name in migration_map:
                migration = migration_map[migration_name]
                logger.info(f"Rolling back migration: {migration_name}")
                migration.connection = self.connection
                migration.dialect = self.dialect
                migration.down()
                
                # Remove the migration record
                delete_query = "DELETE FROM migrations WHERE migration = %s"
                self.connection.execute(delete_query, (migration_name,))
                logger.info(f"✅ Migration rolled back: {migration_name}")
            else:
                logger.warning(f"🚫 Migration file not found: {migration_name}")
                
        logger.info(f"✅ Rolled back batch {last_batch} successfully")

    def fresh(self):
        """Drop all tables and re-run all migrations"""
        if not self.connection:
            raise Exception("❓ Database connection not set")
            
        # Get all tables
        if self.dialect == 'pgsql':
            query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """
        elif self.dialect == 'mysql':
            query = "SHOW TABLES"
        else:  # sqlite
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            
        results = self.connection.execute(query)
        tables = [row[0] for row in results] if results else []
        
        # Drop all tables
        for table in tables:
            logger.info(f"Dropping table: {table}")
            self.drop_table(table)
            
        # Create migrations table first
        logger.info("Creating migrations table")
        self.create_table('migrations', [
            Column('id', Integer, primary_key=True, auto_increment=True),
            Column('migration', String, nullable=False),
            Column('batch', Integer, nullable=False),
            Column('created_at', DateTime)
        ])
            
        # Run all migrations except migrations table creation
        migrations = self._get_migrations()
        if not migrations:
            logger.info("🤔 No migrations to run")
            return
            
        batch = 1  # First batch
        
        for migration in migrations:
            migration_name = migration.filename  # Use filename instead of class name
            if not migration_name.endswith('create_migrations_table'):  # Skip migrations table creation
                logger.info(f"Running migration: {migration_name}")
                migration.connection = self.connection
                migration.dialect = self.dialect
                migration.up()
                self._record_migration(migration_name, batch)
                logger.info(f"✅ Migration completed: {migration_name}")
                
        logger.info("✅ Database refreshed successfully") 