"""
User service module.

Implements business logic for user operations, including creation with password hashing,
retrieval, update with password rehashing, and deletion, interacting with UsersRepository 
and enforcing domain rules such as uniqueness and existence checks.
"""

from app.infraDB.repositories.users_repository import UsersRepository
from app.infraDB.models.users import PermissionType
from app.utils.security import hash_password


def create_user_service(data):
    """
    Create a new user after validating uniqueness and hashing the password.

    Args:
        data (dict): User input data containing 'name', 'email', 'password', and 'permission'.

    Returns:
        Users: The newly created user instance.

    Raises:
        ValueError: If a user with the provided email already exists.
    """
    # Initialize the repository for user operations
    repo = UsersRepository()
    
    # Check if a user with the given email already exists
    existing_user = repo.select_user_by_email(data["email"])
    if existing_user:
        raise ValueError("User already exists")

    # Convert permission string to PermissionType enum
    permission = PermissionType(data["permission"])
    # Hash the plaintext password for secure storage
    hashed_pw = hash_password(data["password"])

    # Delegate user creation to the repository with hashed credentials
    return repo.insert_user(
        data["name"],
        data["email"],
        hashed_pw,
        permission
    )


def get_all_users_service():
    """
    Retrieve all users.

    Returns:
        list[Users]: List of all user instances.
    """
    # Initialize repository and fetch all users
    repo = UsersRepository()
    return repo.select_all_users()


def get_user_by_id_service(id: int):
    """
    Retrieve a user by their ID, raising an error if not found.

    Args:
        id (int): Identifier of the user to fetch.

    Returns:
        Users: The matching user instance.

    Raises:
        ValueError: If no user exists with the given ID.
    """
    repo = UsersRepository()
    # Fetch user; returns None if not found
    user = repo.select_user_by_id(id)
    if not user:
        raise ValueError("User not found")
    return user


def update_user_service(id, data):
    """
    Update an existing user, rehashing password if provided.

    Args:
        id (int): Identifier of the user to update.
        data (dict): Fields to update (may include 'name', 'email', 'password', 'permission').

    Returns:
        Users: The updated user instance.

    Raises:
        ValueError: If the user to update does not exist.
    """
    repo = UsersRepository()

    # If password is provided, hash it and replace in data
    if "password" in data:
        data["password_hash"] = hash_password(data["password"])
        del data["password"]  # Remove plaintext password

    # Delegate update to repository
    user = repo.update_user(
        id=id,
        name=data.get("name"),
        email=data.get("email"),
        password_hash=data.get("password_hash"),
        permission=data.get("permission")
    )

    # Raise error if update did not find an existing user
    if not user:
        raise ValueError("User not found")
    
    return user


def delete_user_service(id):
    """
    Delete a user by their ID, raising an error if not found.

    Args:
        id (int): Identifier of the user to delete.

    Returns:
        bool: True if deletion was successful.

    Raises:
        ValueError: If no user exists with the given ID.
    """
    repo = UsersRepository()
    # Attempt deletion; returns False if no rows affected
    success = repo.delete_user(id)

    if not success:
        raise ValueError("User not found")

    return True