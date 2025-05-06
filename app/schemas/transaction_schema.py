from marshmallow import Schema, fields, validate

class TransactionInputSchema(Schema):
    product_id = fields.Int(required=True, error_messages={"required": "Product ID is required."})
    
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Quantity must be greater than 0."),
        error_messages={"required": "Quantity is required."}
    )
