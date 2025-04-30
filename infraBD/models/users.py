from infraBD.config.connection import db
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime, timezone
from enum import Enum as PyEnum

class PermissionType(PyEnum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"

class Users(db.Model):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    permission = Column(Enum(PermissionType), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
