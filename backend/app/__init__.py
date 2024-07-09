from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_cors import CORS # type: ignore
from .config import Config
import logging
from flask_migrate import Migrate # type: ignore
# from sqlalchemy.orm import scoped_session, sessionmaker # type: ignore

from flask_jwt_extended import JWTManager # type: ignore

logging.basicConfig(level=logging.DEBUG) # TODO: instrument logger

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    jwt.init_app(app)
    db.init_app(app)
    
    migrate = Migrate(app, db)

    with app.app_context():
        from . import routes, models
        app.register_blueprint(routes.api, url_prefix='/api')
        db.create_all()
        
        # db.session = scoped_session(sessionmaker(bind=db.engine))

    return app
