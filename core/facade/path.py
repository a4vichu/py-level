from core.facade.facade import Facade
from core.facade.helpers import (
    base_path as base_path_helper,
    app_path as app_path_helper,
    config_path as config_path_helper,
    database_path as database_path_helper,
    resource_path as resource_path_helper,
    storage_path as storage_path_helper
)

class Path(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'path'
        
    @staticmethod
    def base():
        """Get the base path."""
        return base_path_helper()
        
    @staticmethod
    def app():
        """Get the application path."""
        return app_path_helper()
        
    @staticmethod
    def config():
        """Get the configuration path."""
        return config_path_helper()
        
    @staticmethod
    def database():
        """Get the database path."""
        return database_path_helper()
        
    @staticmethod
    def resource():
        """Get the resource path."""
        return resource_path_helper()
        
    @staticmethod
    def storage():
        """Get the storage path."""
        return storage_path_helper() 