"""
Configuration loader
"""
import os
import importlib
import sys
from typing import Any, Dict, Optional, Union
from pathlib import Path
from dotenv import load_dotenv

def _convert_value(value: str, default: Any = None) -> Any:
    """
    Convert string value to appropriate type based on default value
    """
    if default is None:
        return value
        
    if isinstance(default, bool):
        return value.lower() in ('true', '1', 'yes', 'on')
    elif isinstance(default, int):
        try:
            # Check if it's an octal value
            if isinstance(value, str) and value.startswith('0o'):
                return int(value, 8)
            elif isinstance(value, str) and value.startswith('0'):
                return int(value, 8)
            return int(value)
        except (ValueError, TypeError):
            return default
    elif isinstance(default, float):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    elif isinstance(default, str):
        return str(value)
    else:
        return value

def env(key: str, default: Any = None) -> Any:
    """
    Get an environment variable with type conversion
    """
    value = os.getenv(key)
    if value is None:
        return default
    if value == '':
        # Special case for DB_ENGINE: empty string should be None
        if key == 'DB_ENGINE':
            return None
        # For empty strings, return empty string if default is string or None
        if default is None or isinstance(default, str):
            return ''
        return default
    return _convert_value(value, default)

class ConfigLoader:
    """
    Configuration loader that supports Laravel-style configuration
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if not self._initialized:
            self._config = {}
            self._cache = {}
            self._env_loaded = False
            self._config_path = None
            self._initialized = True
        
    def load_environment(self, env_file: Optional[str] = None) -> None:
        """
        Load environment variables from .env file
        """
        if env_file is None:
            env_file = '.env'
            
        # Clear existing environment variables that might interfere
        for key in list(os.environ.keys()):
            if key.startswith(('APP_', 'DB_', 'CACHE_', 'QUEUE_', 'MAIL_', 'SESSION_', 'LOG_')):
                del os.environ[key]
        
        # If the file is a specific environment file, load it directly
        if env_file.endswith(('.env.development', '.env.testing', '.env.production')):
            if os.path.exists(env_file):
                load_dotenv(env_file, override=True)
            return
        
        # Load base .env file first
        if os.path.exists(env_file):
            load_dotenv(env_file, override=True)
        
        # Get the current environment
        app_env = os.getenv('APP_ENV', 'development')
        
        # If APP_ENV was manually set in os.environ, use that value
        if 'APP_ENV' in os.environ:
            app_env = os.environ['APP_ENV']
        
        # Load environment-specific .env file
        env_specific = str(Path(env_file).parent / f'.env.{app_env}')
        if os.path.exists(env_specific):
            load_dotenv(env_specific, override=True)
        
        # Ensure APP_ENV is set correctly
        os.environ['APP_ENV'] = app_env
        
        self._env_loaded = True
        
    def load_config(self, config_path: str = 'config') -> None:
        """
        Load all configuration files from the config directory
        """
        self._config_path = config_path
        config_dir = Path(config_path)
        
        if not config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {config_path}")
            
        # Add config directory parent to Python path if it's not already there
        config_dir_str = str(config_dir.parent)
        if config_dir_str not in sys.path:
            sys.path.insert(0, config_dir_str)
            
        # Clear existing configuration
        self.clear()
        
        for config_file in config_dir.glob('*.py'):
            if config_file.stem == '__init__':
                continue
                
            try:
                # Read the config file content
                with open(config_file, 'r') as f:
                    code = compile(f.read(), config_file, 'exec')
                    
                # Create a new module namespace
                module_dict = {'env': env}
                
                # Execute the config file in the module namespace
                exec(code, module_dict)
                
                if 'config' in module_dict:
                    config = module_dict['config']()
                    self._config[config_file.stem] = config
            except Exception as e:
                print(f"Warning: Could not load {config_file}: {e}")
                continue
                
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation
        """
        if key in self._cache:
            return self._cache[key]
            
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        self._cache[key] = value
        return value
        
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        self._cache.clear()
        
    def has(self, key: str) -> bool:
        """
        Check if a configuration key exists
        """
        return self.get(key) is not None
        
    def all(self) -> Dict[str, Any]:
        """
        Get all configuration values
        """
        return self._config
        
    def clear(self) -> None:
        """
        Clear all configuration values
        """
        self._config.clear()
        self._cache.clear()
        
    def reload(self) -> None:
        """
        Reload all configuration values
        """
        self.clear()
        if self._config_path:
            self.load_config(self._config_path)

# Create a global config instance
config = ConfigLoader()

def get(key: str, default: Any = None) -> Any:
    """
    Get a configuration value
    """
    return config.get(key, default)

def set(key: str, value: Any) -> None:
    """
    Set a configuration value
    """
    config.set(key, value)

def has(key: str) -> bool:
    """
    Check if a configuration key exists
    """
    return config.has(key)

def all() -> Dict[str, Any]:
    """
    Get all configuration values
    """
    return config.all()

def clear() -> None:
    """
    Clear all configuration values
    """
    config.clear()

def reload() -> None:
    """
    Reload all configuration values
    """
    config.reload() 