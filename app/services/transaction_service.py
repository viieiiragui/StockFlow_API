from app.infraDB.repositories.transactions_repositorie import TransactionsRepository
from app.infraDB.repositories.products_repositorie import ProductsRepository
from app.infraDB.models.transactions import TransactionType
from app.utils.hash_generator import generate_transaction_hash
from datetime import timezone, datetime

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

def create_exit_transaction(data, user_email, user_id):
    product_id = data["product_id"]
    quantity = data["quantity"]

    product_repo = ProductsRepository()
    transaction_repo = TransactionsRepository()

    product = product_repo.select_product_by_id(product_id)
    if not product:
        raise ValueError("Product not found")

    if product.current_stock < data["quantity"]:
        raise ValueError("Insufficient stock for transaction")

    product_repo.remove_stock(product_id, quantity)

    transaction_hash = generate_transaction_hash(
        product_id=product_id,
        quantity=quantity,
        transaction_type="exit",
        user_email=user_email
    )

    transaction = transaction_repo.insert_transaction(
        product_id=product_id,
        type=TransactionType.EXIT,
        quantity=quantity,
        blockchain_hash=transaction_hash,
        user_id=user_id
    )

    return transaction

def get_all_transactions_service():
    repo = TransactionsRepository()
    return repo.select_all_transactions()

def get_transactions_by_product(product_id: int):
    transaction_repo = TransactionsRepository()
    return transaction_repo.select_transactions_by_product(product_id)

def delete_transaction_by_id(id: int) -> bool:
    transaction_repo = TransactionsRepository()
    return transaction_repo.delete_transaction(id)

def get_transaction_by_id(transaction_id: int):
    transaction_repo = TransactionsRepository()
    transaction = transaction_repo.select_transaction_by_id(transaction_id)
    if not transaction:
        raise ValueError("Transaction not found")
    return transaction

def get_transactions_by_user(user_id):
    repo = TransactionsRepository()
    return repo.select_transactions_by_user(user_id)
