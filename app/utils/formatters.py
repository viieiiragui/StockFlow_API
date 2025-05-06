from app.schemas.product_schema import ProductSchema

def format_product(product):
    return ProductSchema().dump(product)

def format_product_list(products):
    return ProductSchema(many=True).dump(products)

def format_transaction(transaction):
    return {
        "id": transaction.id,
        "product_id": transaction.product_id,
        "type": transaction.type.value,
        "quantity": transaction.quantity,
        "blockchain_hash": transaction.blockchain_hash,
        "user_id": transaction.user_id,
        "user_email": transaction.user.email,
        "created_at": transaction.created_at.isoformat()
    }

def format_transaction_list(transactions):
    return [format_transaction(tx) for tx in transactions]
