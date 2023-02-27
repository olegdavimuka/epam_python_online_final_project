# Entry point for the application.
from . import app  # For application discovery by the 'flask' command.
from .rest import purses, transactions, users # For import side-effects of setting up routes.
from .views import home, purses, transactions, users  # For import side-effects of setting up routes.
