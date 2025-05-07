"""
Formatters module.

Provides utility functions to serialize model instances into JSON-serializable formats,
using Marshmallow schemas for products and manual mappings for transactions and users.
"""

from app.schemas.product_schema import ProductSchema


def format_product(product):
    """
    Serialize a single Product instance to a dictionary using ProductSchema.

    Args:
        product: A Product model instance to serialize.

    Returns:
        dict: Serialized product data.
    """
    # Use ProductSchema to dump the model into a JSON-compatible dict
    return ProductSchema().dump(product)


def format_product_list(products):
    """
    Serialize a list of Product instances to a list of dictionaries.

    Args:
        products (list): List of Product model instances to serialize.

    Returns:
        list[dict]: List of serialized product data.
    """
    # Many=True enables serialization of multiple objects
    return ProductSchema(many=True).dump(products)


def format_transaction(transaction):
    """
    Convert a Transaction model instance into a JSON-serializable dictionary.

    Args:
        transaction: A Transaction model instance with 'user' relationship loaded.

    Returns:
        dict: Serialized transaction data including nested user email and timestamps.
    """
    return {
        "id": transaction.id,
        "product_id": transaction.product_id,
        "user_id": transaction.user_id,
        # Safely access related user's email if available
        "user_email": (
            transaction.user.email
            if hasattr(transaction, "user") and transaction.user
            else None
        ),
        # Enum value for transaction type
        "type": transaction.type.value,
        "quantity": transaction.quantity,
        "blockchain_hash": transaction.blockchain_hash,
        # ISO 8601 formatted timestamp for client consumption
        "created_at": transaction.created_at.isoformat()
    }


def format_user(user):
    """
    Convert a Users model instance into a JSON-serializable dictionary.

    Args:
        user: A Users model instance with 'permission' Enum and timestamp fields.

    Returns:
        dict: Serialized user data including permission value and ISO timestamps.
    """
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        # Enum value for permission level
        "permission": user.permission.value,
        # ISO 8601 formatted creation timestamp
        "created_at": user.created_at.isoformat(),
        # ISO formatted update timestamp or None if not set
        "updated_at": (
            user.updated_at.isoformat()
            if hasattr(user, "updated_at") and user.updated_at
            else None
        )
    }
