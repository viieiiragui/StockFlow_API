"""
Users repository module.

Provides database operations for Users, including CRUD and queries by email or ID,
using SQLAlchemy session management.
"""

from app.infraDB.models.users import Users, PermissionType
from app.infraDB.config.connection import db
from datetime import datetime, timezone


class UsersRepository:
    """
    Repository for Users model.

    Methods:
        insert_user(name, email, password_hash, permission): Insert a new user record.
        update_user(id, name, email, password_hash, permission): Update an existing user.
        delete_user(id): Delete a user by ID.
        select_all_users(): Retrieve all users.
        select_user_by_email(email): Retrieve a user by email.
        select_user_by_id(id): Retrieve a user by ID.
    """

    def insert_user(self, name: str, email: str, password_hash: str, permission: PermissionType):
        """
        Create and persist a new user.

        Args:
            name (str): Full name of the user.
            email (str): Unique email address for authentication.
            password_hash (str): Hashed password for secure storage.
            permission (PermissionType): Permission level for the user.

        Returns:
            Users: The created user instance.
        """

        # Instantiate a Users model with provided data
        data_insert = Users(
            name=name,
            email=email,
            password_hash=password_hash,
            permission=permission
        )

        db.session.add(data_insert)
        db.session.commit()
        return data_insert

    def update_user(self, id: int, name: str = None, email: str = None, password_hash: str = None, permission: PermissionType = None):
        """
        Update fields of an existing user.

        Args:
            id (int): ID of the user to update.
            name (str, optional): New full name for the user.
            email (str, optional): New unique email address.
            password_hash (str, optional): New hashed password.
            permission (PermissionType, optional): New permission level.

        Returns:
            Users or None: Updated user instance, or None if not found.
        """
        # Fetch the user by ID
        user = db.session.query(Users).filter(Users.id == id).first()
        if not user:
            # Return None if user does not exist
            return None

        # Update provided fields
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password_hash is not None:
            user.password_hash = password_hash
        if permission is not None:
            user.permission = permission

        user.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return user

    def delete_user(self, id: int):
        """
        Delete a user by its ID.

        Args:
            id (int): Identifier of the user to delete.

        Returns:
            bool: True if deletion occurred, False otherwise.
        """

        # Perform delete operation on matching record
        result = db.session.query(Users).filter(Users.id == id).delete()
        db.session.commit()

        # Return True if any rows were deleted
        return result > 0

    def select_all_users(self):
        """
        Retrieve all users from the database.

        Returns:
            list[Users]: List of all user instances.
        """

        return db.session.query(Users).all()
    
    def select_user_by_email(self, email):
        """
        Retrieve a single user by email address (case-sensitive).

        Args:
            email (str): Email address to search for.

        Returns:
            Users or None: Matching user instance or None if not found.
        """

        return db.session.query(Users).filter_by(email=email).first()

    def select_user_by_id(self, id: int):
        """
        Retrieve a single user by its ID.

        Args:
            id (int): Identifier of the user.

        Returns:
            Users or None: Matching user instance or None if not found.
        """
        
        return db.session.query(Users).filter_by(id=id).first()
