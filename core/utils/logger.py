from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
import logging
import sys
import os
from datetime import datetime

class Logger:
    def __init__(self, name: str = 'app', level: int = logging.INFO):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        
        # Create logs directory if it doesn't exist
        os.makedirs('storage/logs', exist_ok=True)
        
        # Create file handler
        file_handler = logging.FileHandler(
            f'storage/logs/{datetime.now().strftime("%Y-%m-%d")}.log'
        )
        file_handler.setLevel(level)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
        
    def debug(self, message: str, *args, **kwargs):
        """Log a debug message"""
        self._logger.debug(message, *args, **kwargs)
        
    def info(self, message: str, *args, **kwargs):
        """Log an info message"""
        self._logger.info(message, *args, **kwargs)
        
    def warning(self, message: str, *args, **kwargs):
        """Log a warning message"""
        self._logger.warning(message, *args, **kwargs)
        
    def error(self, message: str, *args, **kwargs):
        """Log an error message"""
        self._logger.error(message, *args, **kwargs)
        
    def critical(self, message: str, *args, **kwargs):
        """Log a critical message"""
        self._logger.critical(message, *args, **kwargs)
        
    def exception(self, message: str, *args, **kwargs):
        """Log an exception message"""
        self._logger.exception(message, *args, **kwargs)
        
class LoggerServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('logger', Logger)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot logger bindings
        pass 