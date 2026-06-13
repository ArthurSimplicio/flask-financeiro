from flask import Flask
from app.extensions import (db, jwt, migrate)
from app.config import Config
import app.models

def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(class_config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth_route import auth_bp
    from app.routes.categoria_route import categoria_bp
    from app.routes.transacao_route import transacao_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(transacao_bp)

    return app