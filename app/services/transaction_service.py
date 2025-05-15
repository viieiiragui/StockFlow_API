"""
Transaction service module.

Implements business logic for entry and exit transactions,
including stock adjustments, hash generation, and retrieval/deletion operations,
interacting with ProductsRepository and TransactionsRepository.
"""

import os
from app.utils.ots_handler import OTS_FOLDER
from app.infraDB.repositories.transactions_repositorie import TransactionsRepository
from app.infraDB.repositories.products_repositorie import ProductsRepository
from app.infraDB.models.transactions import TransactionType
from app.utils.hash_generator import (
    generate_transaction_hash_hex,
    generate_transaction_hash_bytes,
    generate_ots_filename,
)
from app.utils.ots_handler import create_timestamp_file


def create_entry_transaction(data, user_id, user_email):
    """
    Process an entry transaction: increase stock, generate hash, and record transaction.

    Args:
        data (dict): Input data with 'product_id' and 'quantity'.
        user_id (int): ID of the user performing the transaction.
        user_email (str): Email of the user performing the transaction.

    Returns:
        Transactions: The created entry transaction instance.

    Raises:
        ValueError: If the product is not found.
    """
    # Extract relevant fields from input
    product_id = data["product_id"]
    quantity = data["quantity"]

    # Initialize repositories
    product_repo = ProductsRepository()
    transaction_repo = TransactionsRepository()

    # Add stock to product; returns None if product does not exist
    product = product_repo.add_stock(product_id, quantity)
    if not product:
        raise ValueError("Product not found")

    # Generate hash (hex and binary) and filename
    hash_bytes = generate_transaction_hash_bytes(product_id, quantity, "entry", user_email)
    hash_hex = generate_transaction_hash_hex(product_id, quantity, "entry", user_email)
    ots_filename = generate_ots_filename(product_id, quantity, "entry", user_email)

    # Create the .ots
    create_timestamp_file(hash_bytes, ots_filename)

    # Save transaction with hash and .ots name
    transaction = transaction_repo.insert_transaction(
        product_id=product_id,
        type=TransactionType.ENTRY,
        quantity=quantity,
        blockchain_hash=hash_hex,
        user_id=user_id,
        ots_filename=ots_filename + ".ots"
    )

    return transaction


def create_exit_transaction(data, user_email, user_id):
    """
    Process an exit transaction: verify stock, decrease stock, generate hash, and record transaction.

    Args:
        data (dict): Input data with 'product_id' and 'quantity'.
        user_email (str): Email of the user performing the transaction.
        user_id (int): ID of the user performing the transaction.

    Returns:
        Transactions: The created exit transaction instance.

    Raises:
        ValueError: If the product is not found or stock is insufficient.
    """
    # Extract relevant fields from input
    product_id = data["product_id"]
    quantity = data["quantity"]

    # Initialize repositories
    product_repo = ProductsRepository()
    transaction_repo = TransactionsRepository()

    # Fetch product to check availability
    product = product_repo.select_product_by_id(product_id)
    if not product:
        raise ValueError("Product not found")

    # Ensure sufficient stock exists for exit transaction
    if product.current_stock < quantity:
        raise ValueError("Insufficient stock for transaction")

    # Remove stock from product
    product_repo.remove_stock(product_id, quantity)

    # Generate hash (hex and binary) and filename
    hash_bytes = generate_transaction_hash_bytes(product_id, quantity, "exit", user_email)
    hash_hex = generate_transaction_hash_hex(product_id, quantity, "exit", user_email)
    ots_filename = generate_ots_filename(product_id, quantity, "exit", user_email)

    # Create the .ots
    create_timestamp_file(hash_bytes, ots_filename)

    # Save transaction with hash and .ots name
    transaction = transaction_repo.insert_transaction(
        product_id=product_id,
        type=TransactionType.EXIT,
        quantity=quantity,
        blockchain_hash=hash_hex,
        user_id=user_id,
        ots_filename=ots_filename + ".ots"
    )

    return transaction


def get_all_transactions_service():
    """
    Retrieve all transactions.

    Returns:
        list[Transactions]: List of all transaction instances.
    """
    repo = TransactionsRepository()
    return repo.select_all_transactions()


def get_transactions_by_product(product_id: int):
    """
    Retrieve transactions filtered by product ID.

    Args:
        product_id (int): ID of the product to filter transactions.

    Returns:
        list[Transactions]: List of matching transaction instances.
    """
    transaction_repo = TransactionsRepository()
    return transaction_repo.select_transactions_by_product(product_id)


def delete_transaction_by_id(id: int) -> bool:
    """
    Delete a transaction by its ID.

    Args:
        id (int): Identifier of the transaction to delete.

    Returns:
        bool: True if deletion occurred, False otherwise.
    """
    transaction_repo = TransactionsRepository()
    return transaction_repo.delete_transaction(id)


def get_transaction_by_id(transaction_id: int):
    """
    Retrieve a single transaction by its ID.

    Args:
        transaction_id (int): Identifier of the transaction.

    Returns:
        Transactions: The matching transaction instance.

    Raises:
        ValueError: If no transaction is found with the given ID.
    """
    transaction_repo = TransactionsRepository()
    transaction = transaction_repo.select_transaction_by_id(transaction_id)
    if not transaction:
        raise ValueError("Transaction not found")
    return transaction


def get_transactions_by_user(user_id):
    """
    Retrieve transactions performed by a specific user.

    Args:
        user_id (int): ID of the user whose transactions to fetch.

    Returns:
        list[Transactions]: List of transaction instances for the given user.
    """
    repo = TransactionsRepository()
    return repo.select_transactions_by_user(user_id)

def get_ots_file_by_transaction_id(transaction_id: int) -> dict:
    """
    Retrieve the .ots file metadata associated with a transaction.

    Args:
        transaction_id (int): The transaction ID.

    Returns:
        dict: A response with 'success', and either 'message' or 'directory'/'filename'.
    """
    transaction_repo = TransactionsRepository()
    transaction = transaction_repo.select_transaction_by_id(transaction_id)

    if not transaction:
        return {"success": False, "message": "Transaction not found"}

    if not transaction.ots_filename:
        return {"success": False, "message": "OTS file not associated with this transaction"}

    ots_path = os.path.join(OTS_FOLDER, transaction.ots_filename)

    if not os.path.isfile(ots_path):
        return {"success": False, "message": "OTS file not found on server"}

    return {
        "success": True,
        "directory": OTS_FOLDER,
        "filename": transaction.ots_filename
    }
