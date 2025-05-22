from app.blueprints import role_required
from app.blueprints.role import bp
from app.blueprints.role.schemas import RoleRequestSchema, RoleResponseSchema, RoleSchema
from app.blueprints.role.service import RoleService
from apiflask import HTTPError
from app.extensions import auth


@bp.route('/')
def index():
    return 'This is The Role Blueprint'


@bp.post('/add')
@bp.input(RoleRequestSchema, location="json")
#@bp.auth_required(auth)
def role_add(json_data):
    success, response = RoleService.role_add(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)


@bp.put('/update')
@bp.input(RoleSchema, location="json")
@bp.output(RoleResponseSchema)
#@bp.auth_required(auth)
def role_update(json_data):
    success, response = RoleService.role_update(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
#@bp.auth_required(auth)
def role_delete(id):
    success, response = RoleService.role_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(RoleResponseSchema)
#@bp.auth_required(auth)
def role_get(id):
    success, response = RoleService.role_get(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all')
@bp.output(RoleSchema(many=True))
#@bp.auth_required(auth)
def role_list_all():
    success, response = RoleService.role_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/my_roles')
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["User"])
def list_user_roles():
    print(str(auth.current_user))
    success, response = RoleService.list_user_roles(auth.current_user.get("id"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
