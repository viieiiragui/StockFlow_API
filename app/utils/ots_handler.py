import subprocess
import os
import hashlib

# Define the absolute path for the folder where .ots and .bin files will be stored
OTS_FOLDER = os.getenv("OTS_DATA_PATH", os.path.join(os.getcwd(), "ots_data"))

def ensure_ots_folder():
    """
    Ensure that the OTS storage folder exists.
    If the directory does not exist, it is created.
    """
    if not os.path.exists(OTS_FOLDER):
        os.makedirs(OTS_FOLDER)

def generate_transaction_hash(product_id, quantity, transaction_type, user_email):
    """
    Generate a SHA256 hash in bytes from transaction data.

    Args:
        product_id (int): ID of the product involved in the transaction.
        quantity (int): Quantity of items moved.
        transaction_type (str): Type of transaction ('entry' or 'exit').
        user_email (str): Email of the user who performed the transaction.

    Returns:
        bytes: SHA256 hash of the formatted input data, encoded as bytes.
    """
    raw_data = f"{product_id}-{quantity}-{transaction_type}-{user_email}"
    return hashlib.sha256(raw_data.encode()).digest()

def create_timestamp_file(hash_bytes: bytes, filename: str) -> str:
    """
    Create a timestamp file (.ots) for a given hash by using OpenTimestamps.

    Args:
        hash_bytes (bytes): The transaction hash to be timestamped.
        filename (str): Name of the file to store the binary hash before stamping.

    Returns:
        str: Full path to the generated .ots file.
    """
    ensure_ots_folder()
    file_path = os.path.join(OTS_FOLDER, filename)

    # Save the hash as a binary file
    with open(file_path, "wb") as f:
        f.write(hash_bytes)

    # Run the OpenTimestamps client to generate the .ots proof
    subprocess.run(["ots", "stamp", file_path], check=True)

    # Return the path to the generated .ots file
    return file_path + ".ots"

def verify_ots_file(filename: str) -> dict:
    """
    Verify the timestamp (.ots file) using OpenTimestamps.

    Args:
        filename (str): Name of the .ots file to be verified.

    Returns:
        dict: A dictionary containing verification status and output details.
              If the file is not found or verification fails, returns an error message.
    """
    path = os.path.join(OTS_FOLDER, filename)

    if not os.path.exists(path):
        return {"success": False, "message": "OTS file not found."}

    try:
        # Run the verification command using the OTS CLI
        output = subprocess.check_output(["ots", "verify", path], stderr=subprocess.STDOUT)
        return {
            "success": True,
            "output": output.decode()
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "output": e.output.decode()
        }
