"""
Transaction input schema module.

Defines input validation schema for transactions using Marshmallow,
validating required product ID and quantity fields.
"""

from marshmallow import Schema, fields, validate


class TransactionInputSchema(Schema):
    """
    Schema for validating transaction payloads.

    Fields:
        product_id (int): ID of the product for the transaction; must be provided.
        quantity (int): Quantity of product to move; must be greater than zero.
    """
    # Product ID field: required integer
    product_id = fields.Int(
        required=True,
        error_messages={"required": "Product ID is required."}
    )
    
    # Quantity field: required integer and must be >= 1
    quantity = fields.Int(
        required=True,
        validate=validate.Range(
            min=1,
            error="Quantity must be greater than 0."
        ),
        error_messages={"required": "Quantity is required."}
    )
