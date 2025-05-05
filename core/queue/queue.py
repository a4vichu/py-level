from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
import asyncio
import json
import time
import uuid

class Job:
    def __init__(self, job_id: str, queue: str, payload: Dict[str, Any], attempts: int = 0):
        self.job_id = job_id
        self.queue = queue
        self.payload = payload
        self.attempts = attempts
        self.created_at = time.time()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the job to a dictionary"""
        return {
            'id': self.job_id,
            'queue': self.queue,
            'payload': self.payload,
            'attempts': self.attempts,
            'created_at': self.created_at
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Job':
        """Create a job from a dictionary"""
        return cls(
            job_id=data['id'],
            queue=data['queue'],
            payload=data['payload'],
            attempts=data['attempts']
        )
        
class Queue(ABC):
    def __init__(self):
        self._queues: Dict[str, List[Job]] = {}
        
    def push(self, queue: str, job: Job):
        """Push a job onto the queue"""
        if queue not in self._queues:
            self._queues[queue] = []
        self._queues[queue].append(job)
        
    def pop(self, queue: str) -> Optional[Job]:
        """Pop a job from the queue"""
        if queue in self._queues and self._queues[queue]:
            return self._queues[queue].pop(0)
        return None
        
    def size(self, queue: str) -> int:
        """Get the size of the queue"""
        return len(self._queues.get(queue, []))
        
    def clear(self, queue: str):
        """Clear the queue"""
        if queue in self._queues:
            self._queues[queue].clear()
            
    def clear_all(self):
        """Clear all queues"""
        self._queues.clear()
        
class QueueServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('queue', Queue)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot queue bindings
        pass
        
class QueueManager:
    def __init__(self):
        self._queues: Dict[str, Queue] = {}
        
    def register(self, name: str, queue: Queue):
        """Register a queue"""
        self._queues[name] = queue
        
    def get(self, name: str) -> Optional[Queue]:
        """Get a queue"""
        return self._queues.get(name)
        
    def has(self, name: str) -> bool:
        """Determine if a queue exists"""
        return name in self._queues
        
    def all(self) -> Dict[str, Queue]:
        """Get all queues"""
        return self._queues
        
    def remove(self, name: str) -> bool:
        """Remove a queue"""
        if name in self._queues:
            del self._queues[name]
            return True
        return False
        
    def clear(self):
        """Clear all queues"""
        self._queues.clear()
        
class QueueManagerServiceProvider(ServiceProvider):
    def _register(self):
        """Register bindings in the container"""
        self.app.singleton('queue_manager', QueueManager)
        
    def _boot(self):
        """Boot the service provider"""
        # Boot queue manager bindings
        pass 