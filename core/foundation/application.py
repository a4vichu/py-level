from pathlib import Path
from typing import Dict, Any, Optional
import os
import sys

class Application:
    """Application container"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.config_path = self.base_path / 'config'
        self.routes_path = self.base_path / 'routes'
        self.app_path = self.base_path / 'app'
        self.database_path = self.base_path / 'database'
        self.resources_path = self.base_path / 'resources'
        self.storage_path = self.base_path / 'storage'
        self.public_path = self.base_path / 'public'
        
        self._config: Dict[str, Any] = {}
        self._services: Dict[str, Any] = {}
        self.providers = []
        
        self._load_environment()
        self._load_config()
        self._register_providers()
        self._boot_providers()
        
    def _load_environment(self):
        """Load environment variables from .env file"""
        from dotenv import load_dotenv
        load_dotenv(self.base_path / '.env')
        
    def _load_config(self):
        """Load configuration files"""
        config_files = [
            'app.py',
            'database.py',
            'cache.py',
            'queue.py',
            'mail.py',
            'services.py'
        ]
        
        for config_file in config_files:
            config_path = self.config_path / config_file
            if config_path.exists():
                # Load config file
                pass
                
    def _register_providers(self):
        """Register core service providers"""
        from core.providers import providers as core_providers
        for provider in core_providers:
            self._register_provider(provider)
            
    def _register_provider(self, provider):
        """Register a service provider"""
        provider_instance = provider()
        self.providers.append(provider_instance)
        provider_instance.register(self)
        
    def _boot_providers(self):
        """Boot all registered service providers"""
        for provider in self.providers:
            provider.boot(self)
            
    def make(self, abstract, parameters=None):
        """Resolve a service from the container"""
        if abstract in self._services:
            return self._services[abstract]
        return None
        
    def singleton(self, abstract, concrete=None):
        """Register a shared binding in the container"""
        if concrete is None:
            concrete = abstract
        self._services[abstract] = concrete
        
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        keys = key.split('.')
        config = self._config
        
        for k in keys:
            if isinstance(config, dict) and k in config:
                config = config[k]
            else:
                return default
                
        return config
        
    def environment(self) -> str:
        """Get the current application environment"""
        return os.getenv('APP_ENV', 'production')
        
    def is_development(self) -> bool:
        """Determine if the application is in development mode"""
        return self.environment() == 'development'
        
    def is_production(self) -> bool:
        """Determine if the application is in production mode"""
        return self.environment() == 'production' 