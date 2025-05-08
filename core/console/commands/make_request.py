import os
from core.console.command import Command

class MakeRequestCommand(Command):
    """
    Create a new form request class
    """
    name = "make:request"
    description = "Create a new form request class"

    def handle(self):
        name = self.argument('name')
        if not name:
            self.error("Please provide a name for the request class")
            return

        # Convert name to proper format
        name = name.replace('-', '_').replace(' ', '_')
        class_name = ''.join(word.capitalize() for word in name.split('_'))
        if not class_name.endswith('Request'):
            class_name += 'Request'

        # Create the request file
        request_path = os.path.join('app', 'requests', f"{name}.py")
        os.makedirs(os.path.dirname(request_path), exist_ok=True)

        template = f'''from core.http.request import Request

class {class_name}(Request):
    """
    Form request for {name}
    """
    def rules(self):
        return {{
            # Define your validation rules here
            # Example:
            # 'email': ['required', 'email'],
            # 'password': ['required', 'string', 'min:8'],
        }}

    def messages(self):
        return {{
            # Define your custom error messages here
            # Example:
            # 'email.required': 'Please provide your email address',
            # 'password.min': 'Password must be at least 8 characters',
        }}

    def authorize(self):
        return True
'''

        with open(request_path, 'w') as f:
            f.write(template)

        self.info(f"Request class created successfully: {request_path}") 