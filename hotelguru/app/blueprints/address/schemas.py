from marshmallow import Schema, fields


class AddressSchema(Schema):
    city = fields.String()
    street = fields.String()
    postalcode = fields.Integer()


class AddressUpdateSchema(Schema):
    id = fields.Integer()
    city = fields.String()
    street = fields.String()
    postalcode = fields.Integer()
