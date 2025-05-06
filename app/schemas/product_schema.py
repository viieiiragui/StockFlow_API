from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

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

    add_stock = fields.Int(
        required=False,
        validate=validate.Range(min=1, error="Stock to add must be positive.")
    )

    code = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=10, error="Code must be between 1 and 10 characters."),
        error_messages={"required": "The code field is required."}
    )
