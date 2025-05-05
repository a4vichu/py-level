class SlaveProcessError(Exception):
    """Base exception for all slave process errors"""
    pass

class ValidationError(SlaveProcessError):
    """Raised when command validation fails"""
    pass

class CommandError(SlaveProcessError):
    """Raised when command execution fails"""
    pass

class CommandTimeoutError(SlaveProcessError):
    """Raised when command execution times out"""
    pass

class InvalidStateError(SlaveProcessError):
    """Raised when operation is invalid in current state"""
    pass

class ConfigurationError(SlaveProcessError):
    """Raised when configuration is invalid"""
    pass

class SecurityError(SlaveProcessError):
    """Raised when a security violation is detected"""
    pass

class AuthenticationError(SlaveProcessError):
    """Raised when authentication fails"""
    pass

class CommunicationError(SlaveProcessError):
    """Raised when there is a communication error"""
    pass 