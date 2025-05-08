from abc import ABC, abstractmethod

class Command(ABC):
    @property
    @abstractmethod
    def signature(self) -> str:
        """The command signature"""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """The command description"""
        pass
        
    @abstractmethod
    def handle(self, *args, **kwargs):
        """Execute the command"""
        pass

__all__ = ['Command'] 