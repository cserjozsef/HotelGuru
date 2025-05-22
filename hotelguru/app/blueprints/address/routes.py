from app.blueprints import role_required
from app.blueprints.address import bp
from app.blueprints.address.schemas import AddressSchema, AddressUpdateSchema
from app.blueprints.address.service import AddressService
from apiflask import HTTPError
from app.extensions import auth


@bp.route('/')
def index():
    return 'This is The Address Blueprint'


@bp.post('/add')
@bp.input(AddressSchema, location="json")
#@bp.auth_required(auth)
def address_add(json_data):
    success, response = AddressService.address_add(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)


@bp.put('/update')
@bp.input(AddressUpdateSchema, location="json")
@bp.output(AddressSchema)
#@bp.auth_required(auth)
def address_update(json_data):
    success, response = AddressService.address_update(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
#@bp.auth_required(auth)
def address_delete(id):
    success, response = AddressService.address_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(AddressSchema)
#@bp.auth_required(auth)
def address_get(id):
    success, response = AddressService.address_get(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all')
@bp.output(AddressSchema(many=True))
#@bp.auth_required(auth)
def address_list_all():
    success, response = AddressService.address_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
