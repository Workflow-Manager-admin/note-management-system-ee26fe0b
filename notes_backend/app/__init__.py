from flask import Flask
from flask_cors import CORS
from .routes.health import blp as health_blp
from flask_smorest import Api
from .config import Config
from .models import db
from .routes.notes import blp as notes_blp

def create_app():
    """Factory to create app with database and blueprints."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    api = Api(app)
    api.register_blueprint(health_blp)
    api.register_blueprint(notes_blp)

    # Create tables if not exist at startup
    @app.before_first_request
    def create_tables():
        db.create_all()
    return app

# For use by run.py
app = create_app()
