from app.blueprints import role_required
from app.blueprints.service import bp
from app.blueprints.service.schemas import ServiceSchema, ServiceUpdateSchema
from app.blueprints.service.service import ServiceService
from apiflask import HTTPError
from app.extensions import auth


@bp.route('/')
def index():
    return 'This is The Service Blueprint'


@bp.post('/add')
@bp.input(ServiceSchema, location="json")
#@bp.auth_required(auth)
def service_add(json_data):
    success, response = ServiceService.service_add(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)


@bp.put('/update')
@bp.input(ServiceUpdateSchema, location="json")
@bp.output(ServiceSchema)
#@bp.auth_required(auth)
def service_update(json_data):
    success, response = ServiceService.service_update(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
#@bp.auth_required(auth)
def service_delete(id):
    success, response = ServiceService.service_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(ServiceSchema)
#@bp.auth_required(auth)
def service_get(id):
    success, response = ServiceService.service_get(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all')
@bp.output(ServiceSchema(many=True))
#@bp.auth_required(auth)
def service_list_all():
    success, response = ServiceService.service_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
