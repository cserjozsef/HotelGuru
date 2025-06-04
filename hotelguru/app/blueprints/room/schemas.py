from marshmallow import Schema, fields
from app.blueprints.amenity.schemas import AmenitySchema


class RoomRequestSchema(Schema):
    type = fields.String()
    price = fields.Integer()
    capacity = fields.Integer()
    status = fields.String()
    description = fields.String()


class RoomSchema(Schema):
    id = fields.Integer()
    type = fields.String()
    price = fields.Integer()
    capacity = fields.Integer()
    status = fields.String()
    description = fields.String()
    amenities = fields.Nested(AmenitySchema, many=True)


class RoomUpdateSchema(Schema):
    id = fields.Integer()
    type = fields.String()
    price = fields.Integer()
    capacity = fields.Integer()
    description = fields.String()
    
class RoomUpdateStatusSchema(Schema):
    id = fields.Integer()
    status = fields.String()
    
