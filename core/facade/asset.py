from core.facade.facade import Facade
from core.facade.helpers import (
    asset as asset_helper,
    secure_asset as secure_asset_helper
)

class Asset(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'asset'
        
    @staticmethod
    def get(path: str):
        """Get the URL for the given asset."""
        return asset_helper(path)
        
    @staticmethod
    def secure(path: str):
        """Get the secure URL for the given asset."""
        return secure_asset_helper(path) 