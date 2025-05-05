from typing import Any, Dict, List, Optional, Union
import os
import logging
import bcrypt
from datetime import datetime
import json
import hashlib
import uuid
import random
import string

# Configuration helpers
def config(key: str, default=None) -> Any:
    """Get a configuration value."""
    from core.config import config as config_manager
    return config_manager.get(key, default)

def env(key: str, default=None) -> Any:
    """Get an environment variable."""
    return os.environ.get(key, default)

def app(key: str, default=None) -> Any:
    """Get an application value."""
    from core.app import app as app_manager
    return app_manager.get(key, default)

# Path helpers
def base_path() -> str:
    """Get the base path."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def app_path() -> str:
    """Get the application path."""
    return os.path.join(base_path(), 'app')

def config_path() -> str:
    """Get the configuration path."""
    return os.path.join(base_path(), 'config')

def database_path() -> str:
    """Get the database path."""
    return os.path.join(base_path(), 'database')

def resource_path() -> str:
    """Get the resource path."""
    return os.path.join(base_path(), 'resources')

def storage_path() -> str:
    """Get the storage path."""
    return os.path.join(base_path(), 'storage')

# Logging helpers
def log(level: str, message: str, *args) -> None:
    """Log a message."""
    logger = logging.getLogger('app')
    getattr(logger, level)(message, *args)

# URL helpers
def url(path: str, parameters: Dict[str, Any] = None) -> str:
    """Generate a URL for the given path."""
    from core.routing import url as url_generator
    return url_generator(path, parameters)

def secure_url(path: str, parameters: Dict[str, Any] = None) -> str:
    """Generate a secure URL for the given path."""
    from core.routing import secure_url as secure_url_generator
    return secure_url_generator(path, parameters)

def route(name: str, parameters: Dict[str, Any] = None) -> str:
    """Generate a URL for the given route."""
    from core.routing import route as route_generator
    return route_generator(name, parameters)

def secure_asset(path: str) -> str:
    """Generate a secure URL for the given asset."""
    from core.routing import secure_asset as secure_asset_generator
    return secure_asset_generator(path)

# Redirect helpers
def redirect(path: str, parameters: Dict[str, Any] = None) -> None:
    """Redirect to the given path."""
    from core.routing import redirect as redirect_handler
    return redirect_handler(path, parameters)

def back() -> None:
    """Redirect back to the previous page."""
    from core.routing import back as back_handler
    return back_handler()

# Request helpers
def request(key: str = None, default=None) -> Any:
    """Get a request value."""
    from core.http import request as request_handler
    return request_handler.get(key, default)

def old(key: str = None, default=None) -> Any:
    """Get an old input value."""
    from core.http import old as old_handler
    return old_handler.get(key, default)

def session(key: str = None, default=None) -> Any:
    """Get a session value."""
    from core.http import session as session_handler
    return session_handler.get(key, default)

# Translation helpers
def __(key: str, parameters: Dict[str, Any] = None) -> str:
    """Get a translation string."""
    from core.translation import translate as translation_handler
    return translation_handler.get(key, parameters)

def trans(key: str, parameters: Dict[str, Any] = None) -> str:
    """Get a translation string."""
    return __(key, parameters)

def trans_choice(key: str, number: int, parameters: Dict[str, Any] = None) -> str:
    """Get a translation string with pluralization."""
    from core.translation import trans_choice as trans_choice_handler
    return trans_choice_handler(key, number, parameters)

# Collection helpers
def collect(items) -> List[Any]:
    """Create a new collection."""
    from core.collection import Collection
    return Collection(items)

def data_get(data: Union[Dict, List], key: str, default=None) -> Any:
    """Get a value from the data using dot notation."""
    from core.collection import data_get as data_get_handler
    return data_get_handler(data, key, default)

def data_set(data: Union[Dict, List], key: str, value: Any) -> Union[Dict, List]:
    """Set a value in the data using dot notation."""
    from core.collection import data_set as data_set_handler
    return data_set_handler(data, key, value)

def head(items: List[Any]) -> Any:
    """Get the first item from the collection."""
    return items[0] if items else None

def last(items: List[Any]) -> Any:
    """Get the last item from the collection."""
    return items[-1] if items else None

def value(value: Any, default=None) -> Any:
    """Get the value or return the default."""
    return value if value is not None else default

def with_value(value: Any, callback) -> Any:
    """Execute the callback if the value is not null."""
    return callback(value) if value is not None else None

# Security helpers
def bcrypt_hash(value: str) -> str:
    """Hash the given value."""
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()

def bcrypt_check(value: str, hashed: str) -> bool:
    """Check if the value matches the hash."""
    return bcrypt.checkpw(value.encode(), hashed.encode())

# Event helpers
def event(event: str, listener) -> None:
    """Register an event listener."""
    from core.events import event as event_handler
    return event_handler(event, listener)

def dispatch(event: str, *args) -> None:
    """Dispatch an event."""
    from core.events import dispatch as dispatch_handler
    return dispatch_handler(event, *args)

# Cache helpers
def cache(key: str = None, value: Any = None, ttl: int = None) -> Any:
    """Get or set a cache value."""
    from core.cache import cache as cache_manager
    if value is None:
        return cache_manager.get(key)
    return cache_manager.put(key, value, ttl)

def cache_remember(key: str, ttl: int, callback) -> Any:
    """Get a cache value or store the result of the callback."""
    from core.cache import cache as cache_manager
    return cache_manager.remember(key, ttl, callback)

# Database helpers
def db(query: str = None, bindings: List = None) -> Any:
    """Execute a database query."""
    from core.database import db as db_manager
    if query is None:
        return db_manager
    return db_manager.query(query, bindings)

def db_table(table: str) -> Any:
    """Get a database table instance."""
    from core.database import db as db_manager
    return db_manager.table(table)

# File helpers
def file(path: str) -> Any:
    """Get a file instance."""
    from core.filesystem import file as file_manager
    return file_manager.get(path)

def file_exists(path: str) -> bool:
    """Check if a file exists."""
    from core.filesystem import file as file_manager
    return file_manager.exists(path)

def file_get(path: str) -> str:
    """Get the contents of a file."""
    from core.filesystem import file as file_manager
    return file_manager.get_contents(path)

def file_put(path: str, contents: str) -> bool:
    """Write contents to a file."""
    from core.filesystem import file as file_manager
    return file_manager.put_contents(path, contents)

# Hash helpers
def hash_make(value: str) -> str:
    """Hash the given value."""
    return hashlib.sha256(value.encode()).hexdigest()

def hash_check(value: str, hashed: str) -> bool:
    """Check if the value matches the hash."""
    return hashlib.sha256(value.encode()).hexdigest() == hashed

# Mail helpers
def mail(to: str, subject: str, message: str, from_email: str = None) -> bool:
    """Send an email."""
    from core.mail import mail as mail_manager
    return mail_manager.send(to, subject, message, from_email)

# Queue helpers
def queue(job, queue: str = 'default') -> bool:
    """Queue a job."""
    from core.queue import queue as queue_manager
    return queue_manager.push(job, queue)

# Session helpers
def session_put(key: str, value: Any) -> None:
    """Put a value in the session."""
    from core.http import session as session_manager
    return session_manager.put(key, value)

def session_get(key: str = None, default=None) -> Any:
    """Get a value from the session."""
    from core.http import session as session_manager
    return session_manager.get(key, default)

def session_forget(key: str) -> None:
    """Remove a value from the session."""
    from core.http import session as session_manager
    return session_manager.forget(key)

# Storage helpers
def storage_disk(disk: str = None) -> Any:
    """Get a storage disk instance."""
    from core.filesystem import storage as storage_manager
    return storage_manager.disk(disk)

def storage_put(path: str, contents: str, disk: str = None) -> bool:
    """Store a file on the disk."""
    from core.filesystem import storage as storage_manager
    return storage_manager.disk(disk).put(path, contents)

def storage_get(path: str, disk: str = None) -> str:
    """Get the contents of a file from the disk."""
    from core.filesystem import storage as storage_manager
    return storage_manager.disk(disk).get(path)

# Validation helpers
def validate(data: Dict, rules: Dict) -> bool:
    """Validate data against rules."""
    from core.validation import validate as validate_manager
    return validate_manager(data, rules)

def validator(data: Dict, rules: Dict) -> Any:
    """Get a validator instance."""
    from core.validation import validator as validator_manager
    return validator_manager(data, rules)

# View helpers
def view(name: str, data: Dict = None) -> str:
    """Render a view."""
    from core.view import view as view_manager
    return view_manager.render(name, data)

def view_exists(name: str) -> bool:
    """Check if a view exists."""
    from core.view import view as view_manager
    return view_manager.exists(name)

# Asset helpers
def asset(path: str) -> str:
    """Get the URL for an asset."""
    from core.filesystem import asset as asset_manager
    return asset_manager.url(path)

def secure_asset(path: str) -> str:
    """Get the secure URL for an asset."""
    from core.filesystem import asset as asset_manager
    return asset_manager.secure_url(path) 