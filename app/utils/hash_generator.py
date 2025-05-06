import hashlib
from datetime import datetime, timezone

def generate_transaction_hash(product_id, quantity, transaction_type, user_email):
    """
    Generates a SHA256 hash for a transaction including user context.
    Replace this logic with blockchain integration in the future.
    """
    raw_data = f"{product_id}-{quantity}-{transaction_type}-{user_email}-{datetime.now(timezone.utc).isoformat()}"
    return hashlib.sha256(raw_data.encode()).hexdigest()
