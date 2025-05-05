from core.facade.facade import Facade
from core.facade.helpers import env as env_helper

class Env(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'env'
        
    @staticmethod
    def get(key: str, default=None):
        """Get an environment variable."""
        return env_helper(key, default) 