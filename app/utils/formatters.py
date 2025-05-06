from app.schemas.product_schema import ProductSchema

def format_product(product):
    return ProductSchema().dump(product)

def format_product_list(products):
    return ProductSchema(many=True).dump(products)

def format_transaction(transaction):
    return {
        "id": transaction.id,
        "product_id": transaction.product_id,
        "user_id": transaction.user_id,
        "user_email": transaction.user.email if hasattr(transaction, "user") and transaction.user else None,
        "type": transaction.type.value,
        "quantity": transaction.quantity,
        "blockchain_hash": transaction.blockchain_hash,
        "created_at": transaction.created_at.isoformat()
    }

