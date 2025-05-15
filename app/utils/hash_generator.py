import hashlib
from datetime import datetime, timezone

def generate_transaction_hash_bytes(product_id, quantity, transaction_type, user_email):
    """
    Generates a SHA256 hash in bytes (for OTS).
    """
    raw_data = f"{product_id}-{quantity}-{transaction_type}-{user_email}-{datetime.now(timezone.utc).isoformat()}"
    return hashlib.sha256(raw_data.encode()).digest()

def generate_transaction_hash_hex(product_id, quantity, transaction_type, user_email):
    """
    Generates a SHA256 hash as a readable hex string (for DB).
    """
    raw_data = f"{product_id}-{quantity}-{transaction_type}-{user_email}-{datetime.now(timezone.utc).isoformat()}"
    return hashlib.sha256(raw_data.encode()).hexdigest()

def generate_ots_filename(product_id, quantity, transaction_type, user_email):
    """
    Generates a unique filename for storing the hash and its .ots proof,
    based on transaction data and timestamp.

    Returns:
        str: Base filename without extension (.bin or .ots will be added)
    """

    safe_email = user_email.replace("@", "_at_").replace(".", "_")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    return f"transacao_{product_id}_{quantity}_{transaction_type}_{safe_email}_{timestamp}.bin"
