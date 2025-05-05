"""
Slave Server - A Python-based command-line server with controller management
"""

__version__ = '1.0.0'
__author__ = 'Your Name'

from .cli import cli
from .config import Config
from .process import SlaveProcess
from .controllers import create_controller, list_controllers, remove_controller
from .helpers import view

__all__ = [
    'cli',
    'Config',
    'SlaveProcess',
    'create_controller',
    'list_controllers',
    'remove_controller',
    'view'
] 