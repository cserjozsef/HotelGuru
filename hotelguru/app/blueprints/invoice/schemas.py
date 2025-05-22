from marshmallow import Schema, fields


class InvoiceSchema(Schema):
    date = fields.String()
    method = fields.String()
    amount = fields.Integer()


class InvoiceUpdateSchema(Schema):
    id = fields.Integer()
    date = fields.String()
    method = fields.String()
    amount = fields.Integer()


class InvoiceRequestSchema(Schema):
    date = fields.Date(format='%Y-%m-%d')
    method = fields.String()
    amount = fields.Integer()
