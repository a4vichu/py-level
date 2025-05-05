from core.facade.facade import Facade
from core.facade.helpers import log as log_helper

class Log(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'log'
        
    @staticmethod
    def info(message: str, *args):
        """Log an info message."""
        return log_helper('info', message, *args)
        
    @staticmethod
    def error(message: str, *args):
        """Log an error message."""
        return log_helper('error', message, *args)
        
    @staticmethod
    def warning(message: str, *args):
        """Log a warning message."""
        return log_helper('warning', message, *args)
        
    @staticmethod
    def debug(message: str, *args):
        """Log a debug message."""
        return log_helper('debug', message, *args) 