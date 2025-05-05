from core.http.controllers.controller import Controller
from slave import view

class WelcomeController(Controller):
    def index(self):
        """Display the welcome page"""
        data = {
            'title': 'Welcome to PY Level Framework',
            'welcome_message': 'Welcome to PY Level Framework !',
            'status': 'running',
            'links': [
                {'url': '/home', 'text': 'Home'},
                {'url': '/docs', 'text': 'Documentation'},
                {'url': '/github', 'text': 'GitHub'}
            ]
        }
        
        return view('welcome', data)