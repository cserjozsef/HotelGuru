from app.blueprints import role_required
from app.blueprints.booking import bp
from app.blueprints.booking.schemas import BookingUpdateSchema, BookingRequestSchema, BookingSchema
from app.blueprints.booking.service import BookingService
from apiflask import HTTPError
from app.extensions import auth


@bp.route('/')
def index():
    return 'This is The Booking Blueprint'


@bp.post('/add')
@bp.input(BookingRequestSchema, location="json")
@bp.auth_required(auth)
@role_required(["User"])
def address_add(json_data):
    success, response = BookingService.booking_add(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)


@bp.put('/update')
@bp.input(BookingUpdateSchema, location="json")
@bp.output(BookingSchema)
@bp.auth_required(auth)
def booking_update(json_data):
    success, response = BookingService.booking_update(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)


@bp.delete('/delete/<int:id>')
@bp.auth_required(auth)
@role_required(["Receptionist", "Administrator", "User"])
def booking_delete(id):
    success, response = BookingService.booking_delete(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/get/<int:id>')
@bp.output(BookingSchema)
#@bp.auth_required(auth)
def booking_get(id):
    success, response = BookingService.booking_get(id)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/list_all')
@bp.output(BookingSchema(many=True))
#@bp.auth_required(auth)
def booking_list_all():
    success, response = BookingService.booking_list_all()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
