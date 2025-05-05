from core.http.controllers.controller import Controller
from core.routing.router import Router
from core.http.middleware.middleware import (
    EncryptCookies,
    StartSession,
    VerifyCsrfToken,
    ShareErrorsFromSession
)
from app.Http.Controllers.welcome_controller import WelcomeController

def register_web_routes(router: Router):
    """Register web routes"""
    # Home page
    router.get('/', WelcomeController().index)

    return router 