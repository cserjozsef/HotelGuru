from marshmallow import Schema, fields
from apiflask.fields import String
from apiflask.validators import Email
from app.blueprints.room.schemas import RoomSchema
from app.blueprints.address.schemas import AddressSchema


class UserRequestSchema(Schema):
    email = String(validate=Email())
    password = fields.String()
    name = fields.String()
    phone = fields.String()
    address = fields.Nested(AddressSchema)


class UserResponseSchema(Schema):
    name = fields.String()
    email = fields.String()
    token = fields.String()
    

class UserLoginSchema(Schema):
    email = String(validate=Email(), required=True)
    password = fields.String(required=True)
    

class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.String()
    address = fields.Nested(AddressSchema)
    room = fields.Nested(RoomSchema)


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class PayloadSchema(Schema):
    user_id = fields.Integer()
    email = fields.String()
    name = fields.String()
    role  = fields.List(fields.Nested(RoleSchema))
    exp = fields.Integer()


class UserUpdateSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    password = fields.String()
    name = fields.String()
    phone = fields.String()
    address = fields.Nested(AddressSchema)