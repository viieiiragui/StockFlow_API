"""
Transactions model module.

Defines the SQLAlchemy model for transaction entities, representing entry and exit
movements of products, including relationships to products and users.
"""

from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from datetime import datetime, timezone
from app.infraDB.config.connection import db
from app.infraDB.models.users import Users


class TransactionType(PyEnum):
    """
    Enumeration of transaction types.

    Attributes:
        ENTRY (str): Represents an entry transaction.
        EXIT (str): Represents an exit transaction.
    """
    ENTRY = "entry"
    EXIT = "exit"


class Transactions(db.Model):
    """
    SQLAlchemy model for transactions.

    Attributes:
        id (int): Primary key, auto-incremented identifier for the transaction.
        product_id (int): Foreign key referencing the associated product.
        user_id (int): Foreign key referencing the user who performed the transaction.
        type (TransactionType): Type of transaction ('entry' or 'exit').
        quantity (int): Quantity of product moved in this transaction.
        blockchain_hash (str): Hash string recording transaction integrity on blockchain.
        ots_filename (str): Directory where the ots file is saved.
        created_at (datetime): UTC timestamp when the transaction was created.
        user (Users): Relationship to the Users model.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionType, name="transactiontype", create_type=False), nullable=False)
    quantity = Column(Integer, nullable=False)
    blockchain_hash = Column(String(66), nullable=False)
    ots_filename = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationship to Users model; allows accessing user who made this transaction
    user = db.relationship("Users", backref="transactions")
