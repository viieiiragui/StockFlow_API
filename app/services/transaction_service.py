from app.infraDB.repositories.transactions_repositorie import TransactionsRepository
from app.infraDB.repositories.products_repositorie import ProductsRepository
from app.infraDB.models.transactions import TransactionType
from app.utils.hash_generator import generate_transaction_hash

def create_entry_transaction(data, user_id, user_email):
    product_id = data["product_id"]
    quantity = data["quantity"]

    product_repo = ProductsRepository()
    transaction_repo = TransactionsRepository()

    product = product_repo.add_stock(product_id, quantity)
    if not product:
        raise ValueError("Product not found")

    transaction_hash = generate_transaction_hash(
        product_id=product_id,
        quantity=quantity,
        transaction_type="entry",
        user_email=user_email
    )

    transaction = transaction_repo.insert_transaction(
        product_id=product_id,
        type=TransactionType.ENTRY,
        quantity=quantity,
        blockchain_hash=transaction_hash,
        user_id=user_id
    )

    return transaction
