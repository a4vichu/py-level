from typing import Dict, Any, List, Optional
from core.foundation.application import Application
from core.exceptions.validation import ValidationException

class Request:
    """
    Base request class for handling form requests and validation
    """
    _current_request = None
    
    def __init__(self, app: Application, method: str, path: str, headers: Dict[str, str], body: Optional[str] = None):
        self.app = app
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self._previous = None
        self._validated_data = {}
        self._errors = {}
        self._authorized = True
        
    @classmethod
    def current(cls) -> 'Request':
        """Get the current request instance"""
        return cls._current_request
        
    def set_current(self):
        """Set this request as the current request"""
        self._previous = self._current_request
        self.__class__._current_request = self
        
    def clear_current(self):
        """Clear the current request"""
        self.__class__._current_request = self._previous 

    def rules(self) -> Dict[str, List[str]]:
        """
        Define validation rules for the request
        Returns a dictionary of field names and their validation rules
        """
        return {}

    def messages(self) -> Dict[str, Dict[str, str]]:
        """
        Define custom validation messages
        Returns a dictionary of field names and their custom error messages
        """
        return {}

    def authorize(self) -> bool:
        """
        Determine if the user is authorized to make this request
        """
        return True

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the request data against the defined rules
        """
        # Check authorization first
        self._authorized = self.authorize()
        if not self._authorized:
            return {}

        rules = self.rules()
        messages = self.messages()
        self._errors = {}

        for field, field_rules in rules.items():
            value = data.get(field)
            field_messages = messages.get(field, {})
            
            for rule in field_rules:
                if not self._validate_rule(rule, value, field, field_messages):
                    break

        if self._errors:
            raise ValidationException(self._errors)

        self._validated_data = data
        return data

    def _validate_rule(self, rule: str, value: Any, field: str, messages: Dict[str, str]) -> bool:
        """
        Validate a single rule against a value
        """
        if rule == 'required' and (value is None or value == ''):
            self._errors[field] = messages.get('required', f'The {field} field is required.')
            return False
        elif rule == 'string' and not isinstance(value, str):
            self._errors[field] = messages.get('string', f'The {field} must be a string.')
            return False
        elif rule == 'numeric' and not isinstance(value, (int, float)):
            self._errors[field] = messages.get('numeric', f'The {field} must be a number.')
            return False
        elif rule == 'email' and not self._is_valid_email(value):
            self._errors[field] = messages.get('email', f'The {field} must be a valid email address.')
            return False
        return True

    def _is_valid_email(self, email: str) -> bool:
        """
        Basic email validation
        """
        if not isinstance(email, str):
            return False
        return '@' in email and '.' in email

    @property
    def validated_data(self) -> Dict[str, Any]:
        """
        Get the validated data
        """
        return self._validated_data

    @property
    def errors(self) -> Dict[str, str]:
        """
        Get validation errors
        """
        return self._errors

    @property
    def is_authorized(self) -> bool:
        """
        Check if the request is authorized
        """
        return self._authorized 