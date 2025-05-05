from marshmallow import Schema, fields, validate, ValidationError

class ProductSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Name must not be empty."),
        error_messages={"required": "The name field is required."}
    )

    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Category must not be empty."),
        error_messages={"required": "The category field is required."}
    )

    current_stock = fields.Int(
        required=True,
        validate=validate.Range(min=0, error="Current stock must be zero or positive."),
        error_messages={"required": "The current_stock field is required."}
    )
