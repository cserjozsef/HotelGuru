from marshmallow import Schema, fields


class AmenitySchema(Schema):
    name = fields.String()


class AmenityUpdateSchema(Schema):
    id = fields.Integer()
    name = fields.String()
