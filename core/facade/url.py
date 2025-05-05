from core.facade.facade import Facade
from core.facade.helpers import (
    url as url_helper,
    secure_url as secure_url_helper,
    route as route_helper,
    secure_asset as secure_asset_helper
)

class Url(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'url'
        
    @staticmethod
    def to(path: str, parameters: dict = None):
        """Generate a URL for the given path."""
        return url_helper(path, parameters)
        
    @staticmethod
    def secure(path: str, parameters: dict = None):
        """Generate a secure URL for the given path."""
        return secure_url_helper(path, parameters)
        
    @staticmethod
    def route(name: str, parameters: dict = None):
        """Generate a URL for the given route."""
        return route_helper(name, parameters)
        
    @staticmethod
    def asset(path: str):
        """Generate a URL for the given asset."""
        return secure_asset_helper(path)
        
    @staticmethod
    def secure_asset(path: str):
        """Generate a secure URL for the given asset."""
        return secure_asset_helper(path) 