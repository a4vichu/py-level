import json
from datetime import datetime
from typing import Dict, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass

class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"
    COMPLETED = "completed"

@dataclass
class Response:
    """Represents a response from the slave process"""
    
    command_id: str
    status: str
    data: Dict[str, Any]
    timestamp: datetime = datetime.now()
    error: Optional[str] = None

    @classmethod
    def success(cls, command_id: str, data: Dict[str, Any]) -> 'Response':
        return cls(command_id=command_id, status='success', data=data)

    @classmethod
    def error(cls, command_id: str, error_message: str) -> 'Response':
        return cls(command_id=command_id, status='error', data={}, error=error_message)

    @classmethod
    def pending(cls, command_id: str, data: Optional[Dict[str, Any]] = None) -> 'Response':
        return cls(command_id=command_id, status='pending', data=data or {})

    def to_dict(self) -> Dict[str, Any]:
        """Convert the response to a dictionary"""
        response_dict = {
            'command_id': self.command_id,
            'status': self.status,
            'timestamp': self.timestamp.isoformat()
        }
        
        if self.data:
            response_dict['data'] = self.data
        if self.error:
            response_dict['error'] = self.error
            
        return response_dict
        
    def to_json(self) -> str:
        """Convert the response to a JSON string"""
        return json.dumps(self.to_dict())

class ResponseValidator:
    @staticmethod
    def validate(data: Dict[str, Any]) -> Response:
        if not isinstance(data, dict):
            raise ValueError("Response data must be a dictionary")
        
        required_fields = ['command_id', 'status']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        return Response(
            command_id=data['command_id'],
            status=data['status'],
            data=data.get('data', {})
        )

class ResponseFormatter:
    """Formats responses for output"""
    
    @staticmethod
    def format_success(command_id: str, data: Dict[str, Any]) -> str:
        """Format a success response"""
        response = Response(command_id, ResponseStatus.SUCCESS.value, data=data)
        return response.to_json()
        
    @staticmethod
    def format_error(command_id: str, error_message: str) -> str:
        """Format an error response"""
        response = Response(command_id, ResponseStatus.ERROR.value, data={}, error=error_message)
        return response.to_json()
        
    @staticmethod
    def format_pending(command_id: str, data: Optional[Dict[str, Any]] = None) -> str:
        """Format a pending response"""
        response = Response(command_id, ResponseStatus.PENDING.value, data=data or {})
        return response.to_json()
        
    @staticmethod
    def format_completed(command_id: str, data: Dict[str, Any]) -> str:
        """Format a completed response"""
        response = Response(command_id, ResponseStatus.COMPLETED.value, data=data)
        return response.to_json()
        
    @staticmethod
    def format_progress(
        command_id: str,
        progress: float,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format a progress update response"""
        data = {
            'progress': progress,
            'status': status
        }
        if details:
            data.update(details)
            
        response = Response(command_id, ResponseStatus.PENDING.value, data=data)
        return response.to_json()
        
    @staticmethod
    def format_metrics(
        command_id: str,
        metrics: Dict[str, Any],
        timestamp: Optional[datetime] = None
    ) -> str:
        """Format a metrics response"""
        data = {
            'metrics': metrics,
            'collected_at': (timestamp or datetime.utcnow()).isoformat()
        }
        response = Response(command_id, ResponseStatus.SUCCESS.value, data=data)
        return response.to_json() 