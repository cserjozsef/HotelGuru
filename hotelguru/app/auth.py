from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
)
from functools import wraps
from apiflask import HTTPError
import datetime

jwt = JWTManager()

def init_jwt(app):
    app.config["JWT_SECRET_KEY"] = app.config.get("SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
    jwt.init_app(app)

def roles_required(*required_roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            user_roles = claims.get("roles", [])
            if not any(role in user_roles for role in required_roles):
                raise HTTPError(message="Permission denied", status_code=403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def generate_token(user):
    roles = [role.name for role in user.role]
    additional_claims = {"roles": roles}
    return create_access_token(identity=user.id, additional_claims=additional_claims)
