"""
This module is the main entry point for running the Flask application.
It creates the Flask app instance by calling create_app() from the app module,
and then runs the app using app.run() if the script is executed directly.

Dependencies:
    - app.create_app() (function)

Exported Variables:
    - app: The Flask app instance.

"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()  # pragma: no cover
