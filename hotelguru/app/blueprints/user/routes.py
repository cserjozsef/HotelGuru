from . import bp
from app.blueprints.user.schemas import UserResponseSchema, UserRequestSchema, UserLoginSchema, RoleSchema
from app.blueprints.user.service import UserService
from app.extensions import auth
from apiflask import HTTPError
from app.auth import role_required

@bp.route('/')
def index():
    return 'This is The User Blueprint'

@bp.post('/registrate')
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def user_registrate(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.post('/login')
@bp.input(UserLoginSchema, location="json")
@bp.output(UserResponseSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/roles')
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["Administrator", "Receptionist", "Guest"])
def user_list_roles():
    success, response = UserService.user_list_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/myroles')
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
def user_list_user_roles():
    user_id = auth.current_user.get("user_id")
    success, response = UserService.list_user_roles(user_id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
