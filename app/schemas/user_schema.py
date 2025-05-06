from marshmallow import Schema, fields, validate

class UserInputSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    permission = fields.Str(required=True, validate=validate.OneOf(["admin", "operator", "viewer"]))

class UserUpdateSchema(Schema):
    name = fields.Str(required=False)
    email = fields.Email(required=False)
    password = fields.Str(required=False, validate=validate.Length(min=6))
    permission = fields.Str(required=False, validate=validate.OneOf(["ADMIN", "VIEWER"]))
