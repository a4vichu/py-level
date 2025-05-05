from core.facade.facade import Facade
from core.facade.helpers import app as app_helper

class App(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'app'
        
    @staticmethod
    def get(key: str, default=None):
        """Get an application value."""
        return app_helper(key, default) 