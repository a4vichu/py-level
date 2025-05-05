from app.Http.Controllers.welcome_controller import WelcomeController

def web_routes(router):
    """Define web routes"""
    router.get('/', WelcomeController.index)
    router.get('/home', WelcomeController.home) 