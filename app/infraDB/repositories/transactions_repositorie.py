"""
Transactions repository module.

Provides database operations for Transactions, including CRUD and queries by product or user,
using SQLAlchemy session management.
"""

from app.infraDB.models.transactions import Transactions, TransactionType
from app.infraDB.config.connection import db


class TransactionsRepository:
    """
    Repository for Transactions model.

    Methods:
        insert_transaction(product_id, type, quantity, blockchain_hash, user_id): Insert a new transaction record.
        delete_transaction(id): Delete a transaction by ID.
        select_all_transactions(): Retrieve all transactions.
        select_transactions_by_product(product_id): Retrieve transactions filtered by product.
        select_transaction_by_id(transaction_id): Retrieve a transaction by ID.
        select_transactions_by_user(user_id): Retrieve transactions for a specific user.
    """

    def insert_transaction(self, product_id, type, quantity, blockchain_hash, user_id):
        """
        Create and persist a new transaction.

        Args:
            product_id (int): ID of the associated product.
            type (TransactionType): Type of transaction (ENTRY or EXIT).
            quantity (int): Quantity moved in the transaction.
            blockchain_hash (str): Blockchain hash for integrity tracking.
            user_id (int): ID of the user performing the transaction.

        Returns:
            Transactions: The created transaction instance.
        """
        # Instantiate a Transactions model with provided data
        data_insert = Transactions(
            product_id=product_id,
            type=type,
            quantity=quantity,
            blockchain_hash=blockchain_hash,
            user_id=user_id
        )

        db.session.add(data_insert)
        db.session.commit()

        return data_insert

    def delete_transaction(self, id: int):
        """
        Delete a transaction by its ID.

        Args:
            id (int): Identifier of the transaction to delete.

        Returns:
            bool: True if deletion occurred, False otherwise.
        """
        # Perform delete operation on matching record
        result = db.session.query(Transactions).filter_by(id=id).delete()
        db.session.commit()

        # Return True if any rows were deleted
        return result > 0
    
    def select_all_transactions(self):
        """
        Retrieve all transactions from the database.

        Returns:
            list[Transactions]: List of all transaction instances.
        """
        return db.session.query(Transactions).all()

    def select_transactions_by_product(self, product_id: int):
        """
        Retrieve transactions filtered by product ID.

        Args:
            product_id (int): ID of the product to filter transactions by.

        Returns:
            list[Transactions]: List of matching transaction instances.
        """
        return db.session.query(Transactions).filter_by(product_id=product_id).all()

    def select_transaction_by_id(self, transaction_id: int):
        """
        Retrieve a single transaction by its ID.

        Args:
            transaction_id (int): Identifier of the transaction.

        Returns:
            Transactions or None: Matching transaction instance or None if not found.
        """
        return db.session.query(Transactions).filter_by(id=transaction_id).first()

    def select_transactions_by_user(self, user_id: int):
        """
        Retrieve transactions for a specific user.

        Args:
            user_id (int): ID of the user whose transactions to fetch.

        Returns:
            list[Transactions]: List of transaction instances for the given user.
        """
        return db.session.query(Transactions).filter(Transactions.user_id == user_id).all()
