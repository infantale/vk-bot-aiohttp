from marshmallow import Schema, fields


class AdminSchema(Schema):
    email = fields.Str(required=True)