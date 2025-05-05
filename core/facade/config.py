from core.facade.facade import Facade
from core.facade.helpers import config as config_helper

class Config(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'config'
        
    @staticmethod
    def get(key: str, default=None):
        """Get a configuration value."""
        return config_helper(key, default) 