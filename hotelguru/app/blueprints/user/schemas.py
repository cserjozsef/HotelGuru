from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Email

class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class AddressSchema(Schema):
    city = fields.String(required=True)
    street = fields.String(required=True)
    postalcode = fields.Integer(required=True)

class UserRequestSchema(Schema):
    fname = fields.String(required=True)
    email = String(validate=Email(), required=True)
    password = fields.String(required=True)
    phone = fields.String()
    address = fields.Nested(AddressSchema, required=True)

class UserResponseSchema(Schema):
    id = fields.Integer()
    fname = fields.String()
    email = fields.String()
    phone = fields.String()
    address = fields.Nested(AddressSchema)
    roles = fields.List(fields.Nested(RoleSchema))
    token = fields.String()

class UserLoginSchema(Schema):
    email = String(validate=Email(), required=True)
    password = fields.String(required=True)
