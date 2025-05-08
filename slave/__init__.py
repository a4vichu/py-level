"""
Slave Server - A Python-based command-line server with model, controller, and migration management
"""

__version__ = '1.0.0'
__author__ = 'Your Name'

from .cli import cli
from .config import Config
from .process import SlaveProcess
from .controllers import create_controller, list_controllers, remove_controller
from .models import create_model
from .migrations import create_migration
from .helpers import view, dump

__all__ = [
    'cli',
    'Config',
    'SlaveProcess',
    'create_controller',
    'list_controllers',
    'remove_controller',
    'create_model',
    'create_migration',
    'view',
    'dump'
] 