from app.blueprints import role_required
from app.blueprints.user import bp
from app.blueprints.user.schemas import UserResponseSchema, UserRequestSchema, UserLoginSchema, UserUpdateSchema, UserSchema
from app.blueprints.user.service import UserService
from apiflask import HTTPError
from app.extensions import auth


@bp.route('/')
def index():
    return 'This is The User Blueprint'


@bp.post('/register')
@bp.doc(tags=["user"])
@bp.input(UserRequestSchema, location="json")
@bp.output(UserResponseSchema)
def user_register(json_data):
    success, response = UserService.user_register(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.post('/login')
@bp.doc(tags=["user"])
@bp.input(UserLoginSchema, location="json")
@bp.output(UserResponseSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.post('/update')
@bp.doc(tags=["user"])
@bp.input(UserUpdateSchema, location="json")
@bp.output(UserResponseSchema)
@bp.auth_required(auth)
@role_required(["User"])
def user_update(json_data):
    success, response = UserService.user_update(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.delete('/delete/<int:id>')
#@bp.auth_required(auth)
def role_delete(id):
    success, response = UserService.user_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(UserResponseSchema)
#@bp.auth_required(auth)
def user_get(id):
    success, response = UserService.user_get(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all')
@bp.doc(tags=["user"])
@bp.output(UserSchema(many=True))
#@bp.auth_required(auth)
#@role_required(["Administrator"])
def user_list_all():
    success, response = UserService.user_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
