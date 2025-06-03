from app.blueprints import role_required
from app.blueprints.room import bp
from app.blueprints.room.schemas import RoomSchema, RoomUpdateSchema, RoomRequestSchema, RoomUpdateStatusSchema
from app.blueprints.room.service import RoomService
from apiflask import HTTPError
from app.extensions import auth


@bp.route('/')
def index():
    return 'This is The Room Blueprint'


@bp.post('/add')
@bp.input(RoomRequestSchema, location="json")
#@bp.auth_required(auth)
def room_add(json_data):
    success, response = RoomService.room_add(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)


@bp.put('/update')
@bp.input(RoomUpdateSchema, location="json")
@bp.output(RoomSchema)
#@bp.auth_required(auth)
def room_update(json_data):
    success, response = RoomService.room_update(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.put("/update_status")
@bp.input(RoomUpdateStatusSchema, location="json")
@bp.output(RoomSchema)
@bp.auth_required(auth)
@role_required(["User", "Receptionist"])
def room_update_status(json_data):
    success, response = RoomService.room_update_status(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
#@bp.auth_required(auth)
def room_delete(id):
    success, response = RoomService.room_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(RoomSchema)
#@bp.auth_required(auth)
def room_get(id):
    success, response = RoomService.room_get(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all')
@bp.output(RoomSchema(many=True))
#@bp.auth_required(auth)
def room_list_all():
    success, response = RoomService.room_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
