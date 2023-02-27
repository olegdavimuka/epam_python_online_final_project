# Entry point for the application.
from . import app  # noqa: F401
from .rest import purses, transactions, users  # noqa: F401
from .views import home, purses, transactions, users  # noqa: F401, F811
