from core.facade.facade import Facade
from core.facade.helpers import (
    file as file_helper,
    file_exists as file_exists_helper,
    file_get as file_get_helper,
    file_put as file_put_helper
)

class File(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'file'
        
    @staticmethod
    def exists(path: str):
        """Check if a file exists."""
        return file_exists_helper(path)
        
    @staticmethod
    def get(path: str):
        """Get the contents of a file."""
        return file_get_helper(path)
        
    @staticmethod
    def put(path: str, contents: str):
        """Write contents to a file."""
        return file_put_helper(path, contents)
        
    @staticmethod
    def delete(path: str):
        """Delete a file."""
        from core.filesystem import filesystem
        return filesystem.delete(path)
        
    @staticmethod
    def copy(source: str, destination: str):
        """Copy a file."""
        from core.filesystem import filesystem
        return filesystem.copy(source, destination)
        
    @staticmethod
    def move(source: str, destination: str):
        """Move a file."""
        from core.filesystem import filesystem
        return filesystem.move(source, destination)
        
    @staticmethod
    def size(path: str):
        """Get the size of a file."""
        from core.filesystem import filesystem
        return filesystem.size(path)
        
    @staticmethod
    def last_modified(path: str):
        """Get the last modified time of a file."""
        from core.filesystem import filesystem
        return filesystem.last_modified(path) 