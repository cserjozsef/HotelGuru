from app.blueprints import role_required
from app.blueprints.amenity import bp
from app.blueprints.amenity.schemas import AmenitySchema, AmenityUpdateSchema
from app.blueprints.amenity.service import AmenityService
from apiflask import HTTPError
from app.extensions import auth


@bp.route('/')
def index():
    return 'This is The Amenity Blueprint'


@bp.post('/add')
@bp.input(AmenitySchema, location="json")
#@bp.auth_required(auth)
def amenity_add(json_data):
    success, response = AmenityService.amenity_add(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)


@bp.put('/update')
@bp.input(AmenityUpdateSchema, location="json")
@bp.output(AmenitySchema)
#@bp.auth_required(auth)
def amenity_update(json_data):
    success, response = AmenityService.amenity_update(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
#@bp.auth_required(auth)
def amenity_delete(id):
    success, response = AmenityService.amenity_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(AmenitySchema)
#@bp.auth_required(auth)
def amenity_get(id):
    success, response = AmenityService.amenity_get(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all')
@bp.output(AmenitySchema(many=True))
#@bp.auth_required(auth)
def amenity_list_all():
    success, response = AmenityService.amenity_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
