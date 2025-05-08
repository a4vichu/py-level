class ValidationException(Exception):
    """
    Exception raised when request validation fails
    """
    def __init__(self, errors: dict):
        self.errors = errors
        super().__init__("Validation failed") 