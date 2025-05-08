from core.http.request import Request

class UserregistrationRequest(Request):
    """
    Form request for UserRegistration
    """
    def rules(self):
        return {
            # Define your validation rules here
            # Example:
            # 'email': ['required', 'email'],
            # 'password': ['required', 'string', 'min:8'],
        }

    def messages(self):
        return {
            # Define your custom error messages here
            # Example:
            # 'email.required': 'Please provide your email address',
            # 'password.min': 'Password must be at least 8 characters',
        }

    def authorize(self):
        return True
