"""
Users model module.

Defines the SQLAlchemy model for user entities, including authentication data,
permission levels, and timestamps.
"""

from app.infraDB.config.connection import db
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime, timezone
from enum import Enum as PyEnum


class PermissionType(PyEnum):
    """
    Enumeration of user permission levels.

    Attributes:
        ADMIN (str): Full access permissions.
        OPERATOR (str): Mid-level access permissions.
        VIEWER (str): Read-only access permissions.
    """
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"


class Users(db.Model):
    """
    SQLAlchemy model for users.

    Attributes:
        id (int): Primary key, auto-incremented identifier for the user.
        name (str): Full name of the user (required).
        email (str): Unique email address for authentication (required).
        password_hash (str): Hashed password for secure authentication (required).
        permission (PermissionType): User's permission level (admin, operator, viewer).
        created_at (datetime): UTC timestamp when the user was created.
        updated_at (datetime): UTC timestamp when the user was last updated.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    permission = Column(Enum(PermissionType, name="permissiontype", create_type=False), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
