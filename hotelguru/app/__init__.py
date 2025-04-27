from flask import Flask
from apiflask import APIFlask
from config import Config
from .extensions import db
from .auth import init_jwt
import app.models.user
import app.models.role
import app.models.room
import app.models.booking
import app.models.invoice
import app.models.service
import app.models.address


def create_app(config_class=Config):

    app = APIFlask(__name__, json_errors=True,
                   title="HotelGuru API",
                   docs_path="/swagger")
    app.config.from_object(config_class)
    init_jwt(app)

    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    from app.blueprints import bp as bp_default
    app.register_blueprint(bp_default, url_prefix='/api')

    from app.routes.user import user_bp
    from app.routes.reception import reception_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(reception_bp, url_prefix='/api/reception')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    return app
