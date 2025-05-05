import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class Config:
    """Configuration manager for the slave server"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or os.path.join(
            os.path.dirname(__file__),
            'config.json'
        )
        self._config: Dict[str, Any] = {}
        self._load()
        
    def _load(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self._config = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load config file: {str(e)}")
            self._config = {}
            
    def _save(self):
        """Save configuration to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save config file: {str(e)}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        # Check environment variable first
        env_key = f"SLAVE_{key.upper()}"
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
            
        # Then check config file
        return self._config.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set a configuration value"""
        self._config[key] = value
        self._save()
        
    def delete(self, key: str):
        """Delete a configuration value"""
        if key in self._config:
            del self._config[key]
            self._save()
            
    def list_all(self) -> Dict[str, Any]:
        """List all configurations"""
        # Combine file config with environment variables
        config = self._config.copy()
        
        # Add environment variables
        for key in os.environ:
            if key.startswith('SLAVE_'):
                config_key = key[6:].lower()  # Remove SLAVE_ prefix and convert to lowercase
                config[config_key] = os.environ[key]
                
        return config
        
    def clear(self):
        """Clear all configurations"""
        self._config.clear()
        self._save()
        
    def merge(self, config: Dict[str, Any]):
        """Merge configuration dictionary"""
        self._config.update(config)
        self._save()
        
    def get_int(self, key: str, default: Optional[int] = None) -> Optional[int]:
        """Get a configuration value as integer"""
        value = self.get(key, default)
        try:
            return int(value) if value is not None else None
        except (ValueError, TypeError):
            return default
            
    def get_bool(self, key: str, default: Optional[bool] = None) -> Optional[bool]:
        """Get a configuration value as boolean"""
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return default
        
    def get_list(self, key: str, default: Optional[list] = None) -> Optional[list]:
        """Get a configuration value as list"""
        value = self.get(key, default)
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(',')]
        return default 