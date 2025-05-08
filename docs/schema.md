# Database Schema Documentation

The schema system provides a fluent interface for defining database tables and their columns. It supports various data types and column modifiers, similar to Laravel's schema builder.

## Column Types

### Numeric Types
- `Integer`: Standard integer type
- `BigInteger`: Large integer type
- `SmallInteger`: Small integer type
- `Float`: Floating-point number
- `Decimal`: Decimal number with precision
- `Numeric`: Numeric value with precision

### String Types
- `String`: VARCHAR(255) by default
- `Text`: TEXT type
- `Char`: Fixed-length character string
- `Varchar`: Variable-length character string
- `LongText`: LONGTEXT (MySQL) or TEXT (SQLite/PostgreSQL)
- `MediumText`: MEDIUMTEXT (MySQL) or TEXT (SQLite/PostgreSQL)
- `TinyText`: TINYTEXT (MySQL) or TEXT (SQLite/PostgreSQL)

### Date/Time Types
- `DateTime`: TIMESTAMP type
- `Date`: DATE type
- `Time`: TIME type
- `Timestamp`: TIMESTAMP type
- `Year`: YEAR (MySQL) or INTEGER (SQLite/PostgreSQL)

### Binary Types
- `Binary`: BINARY type
- `Blob`: BLOB type
- `LongBlob`: LONGBLOB (MySQL) or BLOB (SQLite/PostgreSQL)
- `MediumBlob`: MEDIUMBLOB (MySQL) or BLOB (SQLite/PostgreSQL)
- `TinyBlob`: TINYBLOB (MySQL) or BLOB (SQLite/PostgreSQL)

### Other Types
- `Boolean`: BOOLEAN type
- `JSON`: JSON (MySQL) or TEXT (SQLite/PostgreSQL)
- `Enum`: ENUM type
- `UUID`: CHAR(36) type

## Column Modifiers

The `Column` class accepts the following parameters:

```python
Column(
    name,           # Column name
    type,           # Column type (e.g., Integer, String)
    primary_key=False,  # Whether this is a primary key
    nullable=True,      # Whether NULL values are allowed
    default=None,       # Default value
    unique=False,       # Whether this column should be unique
    index=False,        # Whether this column should be indexed
    auto_increment=False  # Whether this column should auto-increment
)
```

## Foreign Keys

The `ForeignKey` class is used to define foreign key constraints:

```python
ForeignKey(
    column,         # Column name
    references,     # Referenced table and column (e.g., 'users.id')
    on_delete='CASCADE',  # Action on delete
    on_update='CASCADE'   # Action on update
)
```

## Example Usage

```python
from core.database.migrations import Migration
from core.database.schema import (
    Column, ForeignKey, Integer, String, DateTime, Boolean
)

class CreateUsersTable(Migration):
    def up(self):
        self.create_table('users', [
            Column('id', Integer, primary_key=True, auto_increment=True),
            Column('name', String, nullable=False),
            Column('email', String, nullable=False, unique=True),
            Column('is_active', Boolean, default=True),
            Column('created_at', DateTime),
            Column('updated_at', DateTime)
        ])

class CreatePostsTable(Migration):
    def up(self):
        self.create_table('posts', [
            Column('id', Integer, primary_key=True, auto_increment=True),
            Column('title', String, nullable=False),
            Column('content', Text),
            Column('user_id', Integer),
            ForeignKey('user_id', 'users.id', on_delete='CASCADE'),
            Column('created_at', DateTime),
            Column('updated_at', DateTime)
        ])
```

## Database Support

The schema system supports multiple database types:

### MySQL
- Uses MySQL-specific types (e.g., LONGTEXT, YEAR)
- Supports AUTO_INCREMENT for primary keys
- Uses JSON type for JSON columns

### SQLite
- Uses simplified types (e.g., TEXT instead of LONGTEXT)
- Supports AUTOINCREMENT for primary keys
- Uses TEXT type for JSON columns

### PostgreSQL
- Uses PostgreSQL-specific types (e.g., BYTEA for binary)
- Uses UUID type for UUID columns
- Uses JSONB type for JSON columns

## Best Practices

1. Always include `id`, `created_at`, and `updated_at` columns in your tables
2. Use appropriate column types for your data
3. Set `nullable=False` for required fields
4. Use `unique=True` for columns that should be unique
5. Use `index=True` for columns that will be frequently queried
6. Use foreign keys to maintain referential integrity
7. Use appropriate `on_delete` and `on_update` actions for foreign keys 