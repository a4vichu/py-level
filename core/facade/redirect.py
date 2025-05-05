from core.facade.facade import Facade
from core.facade.helpers import (
    redirect as redirect_helper,
    back as back_helper
)

class Redirect(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'redirect'
        
    @staticmethod
    def to(path: str, parameters: dict = None):
        """Redirect to the given path."""
        return redirect_helper(path, parameters)
        
    @staticmethod
    def back():
        """Redirect back to the previous page."""
        return back_helper() 