from core.facade.facade import Facade
from core.facade.helpers import (
    event as event_helper,
    dispatch as dispatch_helper
)

class Event(Facade):
    @staticmethod
    def get_facade_accessor():
        return 'event'
        
    @staticmethod
    def listen(event: str, listener):
        """Register an event listener."""
        return event_helper(event, listener)
        
    @staticmethod
    def dispatch(event: str, *args):
        """Dispatch an event."""
        return dispatch_helper(event, *args) 