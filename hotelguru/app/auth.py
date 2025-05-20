import datetime
from flask import current_app, g, jsonify
from authlib.jose import jwt, JoseError
from flask_httpauth import HTTPTokenAuth
from functools import wraps
from app.models.user import User  

auth = HTTPTokenAuth(scheme='Bearer')

def generate_token(user_id):
    header = {'alg': 'HS256'}
    payload = {
        'sub': user_id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(header, payload, current_app.config['SECRET_KEY']) 
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        data.validate_exp()
        user_id = data['sub']
        g.current_user_id = user_id
 
        user = User.query.get(user_id)
        if user:
            g.current_user_roles = [role.name for role in user.roles]
        else:
            g.current_user_roles = []
        return True
    except JoseError:
        return False

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            roles = getattr(g, 'current_user_roles', [])
            if role_name not in roles:
                return jsonify({"message": "Access denied: insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def init_jwt(app): 
    pass
