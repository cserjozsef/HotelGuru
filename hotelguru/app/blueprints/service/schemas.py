from marshmallow import Schema, fields


class ServiceSchema(Schema):
    name = fields.String()
    price = fields.Integer()


class ServiceUpdateSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Integer()
