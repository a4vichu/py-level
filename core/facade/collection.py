from core.facade.facade import Facade
from core.facade.helpers import (
    collect as collect_helper,
    data_get as data_get_helper,
    data_set as data_set_helper,
    head as head_helper,
    last as last_helper,
    value as value_helper,
    with_value as with_value_helper
)

class Collection(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'collection'
        
    @staticmethod
    def make(items):
        """Create a new collection."""
        return collect_helper(items)
        
    @staticmethod
    def get(data, key: str, default=None):
        """Get a value from the data using dot notation."""
        return data_get_helper(data, key, default)
        
    @staticmethod
    def set(data, key: str, value):
        """Set a value in the data using dot notation."""
        return data_set_helper(data, key, value)
        
    @staticmethod
    def head(items):
        """Get the first item from the collection."""
        return head_helper(items)
        
    @staticmethod
    def last(items):
        """Get the last item from the collection."""
        return last_helper(items)
        
    @staticmethod
    def value(value, default=None):
        """Get the value or return the default."""
        return value_helper(value, default)
        
    @staticmethod
    def with_value(value, callback):
        """Execute the callback if the value is not null."""
        return with_value_helper(value, callback) 