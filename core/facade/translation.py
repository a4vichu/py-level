from core.facade.facade import Facade
from core.facade.helpers import (
    __ as __helper,
    trans as trans_helper,
    trans_choice as trans_choice_helper
)

class Translation(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'trans'
        
    @staticmethod
    def get(key: str, parameters: dict = None):
        """Get a translation string."""
        return __helper(key, parameters)
        
    @staticmethod
    def choice(key: str, number: int, parameters: dict = None):
        """Get a translation string with pluralization."""
        return trans_choice_helper(key, number, parameters) 