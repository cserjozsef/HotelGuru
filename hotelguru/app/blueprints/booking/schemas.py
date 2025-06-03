from marshmallow import Schema, fields
from app.blueprints.user.schemas import UserSchema
from app.blueprints.room.schemas import RoomSchema
from app.blueprints.invoice.schemas import InvoiceSchema


class BookingRequestSchema(Schema):
    check_in = fields.Date(format='%Y-%m-%d')
    check_out = fields.Date(format='%Y-%m-%d')
    comment = fields.String(allow_none=True)
    user_id = fields.Integer()
    room_id = fields.Integer()
    invoice_id = fields.Integer()

class BookingSchema(Schema):
    id = fields.Integer()
    check_in = fields.String()
    check_out = fields.String()
    comment = fields.String(allow_none=True)
    user_id = fields.Integer()
    room_id = fields.Integer()
    invoice_id = fields.Integer()


class BookingUpdateSchema(Schema):
    id = fields.Integer()
    check_in = fields.String()
    check_out = fields.String()
    comment = fields.String(allow_none=True)
