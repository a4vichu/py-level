class Column:
    def __init__(self, name, type, primary_key=False, nullable=True, default=None, unique=False, index=False, auto_increment=False):
        self.name = name
        self.type = type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.unique = unique
        self.index = index
        self.auto_increment = auto_increment

class ForeignKey:
    def __init__(self, column, references, on_delete='CASCADE', on_update='CASCADE'):
        self.column = column
        self.references = references
        self.on_delete = on_delete
        self.on_update = on_update

# Numeric Types
class Integer: pass
class BigInteger: pass
class SmallInteger: pass
class Float: pass
class Decimal: pass
class Numeric: pass

# String Types
class String: pass
class Text: pass
class Char: pass
class Varchar: pass
class LongText: pass
class MediumText: pass
class TinyText: pass

# Date/Time Types
class DateTime: pass
class Date: pass
class Time: pass
class Timestamp: pass
class Year: pass

# Binary Types
class Binary: pass
class Blob: pass
class LongBlob: pass
class MediumBlob: pass
class TinyBlob: pass

# Boolean Type
class Boolean: pass

# JSON Type
class JSON: pass

# Enum Type
class Enum: pass

# UUID Type
class UUID: pass 