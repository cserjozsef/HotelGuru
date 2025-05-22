from marshmallow import Schema, fields


class RoleRequestSchema(Schema):
    name = fields.String()


class RoleResponseSchema(Schema):
    name = fields.String()


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
