from flask import Flask
from config import Config
from app.extensions import db
import app.models.user
import app.models.role
import app.models.room
import app.models.booking
import app.models.invoice
import app.models.service


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app