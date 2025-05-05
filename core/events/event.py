from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
import asyncio
import uuid

class Event(ABC):
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        
    def listen(self, event: str, listener: Callable):
        """Register an event listener"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(listener)
        
    def dispatch(self, event: str, *args, **kwargs):
        """Dispatch an event"""
        if event in self._listeners:
            for listener in self._listeners[event]:
                listener(*args, **kwargs)
                
    async def dispatch_async(self, event: str, *args, **kwargs):
        """Dispatch an event asynchronously"""
        if event in self._listeners:
            tasks = []
            for listener in self._listeners[event]:
                if asyncio.iscoroutinefunction(listener):
                    tasks.append(listener(*args, **kwargs))
                else:
                    tasks.append(asyncio.to_thread(listener, *args, **kwargs))
            await asyncio.gather(*tasks)
            
    def forget(self, event: str, listener: Optional[Callable] = None):
        """Remove an event listener"""
        if event in self._listeners:
            if listener is None:
                del self._listeners[event]
            else:
                self._listeners[event].remove(listener)
                
    def flush(self):
        """Remove all event listeners"""
        self._listeners.clear()
        
class EventServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('events', Event)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot event bindings
        pass
        
class EventDispatcher:
    def __init__(self):
        self._events: Dict[str, List[Callable]] = {}
        
    def listen(self, event: str, listener: Callable):
        """Register an event listener"""
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(listener)
        
    def dispatch(self, event: str, *args, **kwargs):
        """Dispatch an event"""
        if event in self._events:
            for listener in self._events[event]:
                listener(*args, **kwargs)
                
    async def dispatch_async(self, event: str, *args, **kwargs):
        """Dispatch an event asynchronously"""
        if event in self._events:
            tasks = []
            for listener in self._events[event]:
                if asyncio.iscoroutinefunction(listener):
                    tasks.append(listener(*args, **kwargs))
                else:
                    tasks.append(asyncio.to_thread(listener, *args, **kwargs))
            await asyncio.gather(*tasks)
            
    def forget(self, event: str, listener: Optional[Callable] = None):
        """Remove an event listener"""
        if event in self._events:
            if listener is None:
                del self._events[event]
            else:
                self._events[event].remove(listener)
                
    def flush(self):
        """Remove all event listeners"""
        self._events.clear()
        
class EventDispatcherServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('event_dispatcher', EventDispatcher)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot event dispatcher bindings
        pass 