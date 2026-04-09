"""Flask application factory."""

from flask import Flask

from app.routes.library_routes import library_blueprint


def create_app() -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "digital-book-library-secret-key"
    app.register_blueprint(library_blueprint)
    return app
