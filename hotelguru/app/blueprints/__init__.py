from functools import wraps
from apiflask import APIBlueprint
from app.extensions import auth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError

bp = APIBlueprint('main', __name__, tag="main")


@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'],
        )
        if data["exp"] < int(datetime.now().timestamp()):
            return None
        return data
    except:
        return None

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            user_roles = [item["name"] for item in auth.current_user.get("roles")]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)
            raise HTTPError(message="Access denied", status_code=403)
        return decorated_function
    return wrapper


from app.blueprints.user import bp as bp_user
bp.register_blueprint(bp_user, url_prefix="/user")

from app.blueprints.role import bp as bp_role
bp.register_blueprint(bp_role, url_prefix="/role")

from app.blueprints.address import bp as bp_address
bp.register_blueprint(bp_address, url_prefix="/address")

from app.blueprints.room import bp as bp_room
bp.register_blueprint(bp_room, url_prefix="/room")

from app.blueprints.amenity import bp as bp_amenity
bp.register_blueprint(bp_amenity, url_prefix="/amenity")

from app.blueprints.service import bp as bp_service
bp.register_blueprint(bp_service, url_prefix="/service")

from app.blueprints.booking import bp as bp_booking
bp.register_blueprint(bp_booking, url_prefix="/booking")

from app.blueprints.invoice import bp as bp_invoice
bp.register_blueprint(bp_invoice, url_prefix="/invoice")

from app.models import *