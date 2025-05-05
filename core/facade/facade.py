from core.foundation.application import Application

class Facade:
    """Base facade class that all other facades inherit from."""
    
    _app = None
    
    @staticmethod
    def get_facade_accessor():
        """Get the facade accessor name."""
        raise NotImplementedError("Facade must implement get_facade_accessor()")
        
    @classmethod
    def get_facade_root(cls):
        """Get the facade root instance."""
        if not cls._app:
            cls._app = Application()
        return cls._app.make(cls.get_facade_accessor()) 