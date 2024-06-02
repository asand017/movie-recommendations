from flask import Flask
from flask_cors import CORS # type: ignore
from .config import Config
from .base_model import db
 
def create_app():
    app = Flask(__name__)
    # CORS(app)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from . import routes, models
        app.register_blueprint(routes.api)
        db.create_all()

    return app
