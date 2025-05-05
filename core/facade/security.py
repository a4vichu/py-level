from core.facade.facade import Facade
from core.facade.helpers import (
    bcrypt_hash as bcrypt_hash_helper,
    bcrypt_check as bcrypt_check_helper
)

class Security(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'security'
        
    @staticmethod
    def hash(value: str):
        """Hash the given value."""
        return bcrypt_hash_helper(value)
        
    @staticmethod
    def check(value: str, hashed: str):
        """Check if the value matches the hash."""
        return bcrypt_check_helper(value, hashed) 