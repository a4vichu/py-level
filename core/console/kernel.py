from typing import Dict, Type, List
from abc import ABC, abstractmethod
import sys
from core.console.commands.make_request import MakeRequestCommand

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

class ConsoleKernel:
    def __init__(self):
        self._commands: Dict[str, Type[Command]] = {}
        self._register_default_commands()
        
    def _register_default_commands(self):
        """Register default commands"""
        self.register(MakeRequestCommand)
        
    def register(self, command_class: Type[Command]):
        """Register a command"""
        command = command_class()
        self._commands[command.signature] = command_class
        
    def run(self, args: List[str]):
        """Run the command"""
        if not args:
            self._show_help()
            return
            
        command_name = args[0]
        if command_name not in self._commands:
            print(f"Command '{command_name}' not found.")
            self._show_help()
            return
            
        command_class = self._commands[command_name]
        command = command_class()
        
        try:
            command.handle(*args[1:])
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
            
    def _show_help(self):
        """Show available commands"""
        print("Available commands:")
        for signature, command_class in self._commands.items():
            command = command_class()
            print(f"  {signature:<30} {command.description}")
            
    def get_commands(self) -> Dict[str, Type[Command]]:
        """Get all registered commands"""
        return self._commands 