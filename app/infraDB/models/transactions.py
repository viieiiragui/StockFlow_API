from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from datetime import datetime, timezone
from app.infraDB.config.connection import db
from app.infraDB.models.users import Users

class TransactionType(PyEnum):
    ENTRY = "entry"
    EXIT = "exit"

class Transactions(db.Model):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionType, name="transactiontype", create_type=False), nullable=False)
    quantity = Column(Integer, nullable=False)
    blockchain_hash = Column(String(66), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = db.relationship("Users", backref="transactions")
