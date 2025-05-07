"""
Security utility module.

Provides functions for secure password operations, such as hashing passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plaintext password for secure storage.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: The resulting bcrypt-hashed password as a UTF-8 string.
    """
    # Encode the plaintext password to bytes
    password_bytes = password.encode("utf-8")
    # Generate a salt and hash the password
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Decode the hashed bytes back to a string for storage
    return hashed_bytes.decode("utf-8")
