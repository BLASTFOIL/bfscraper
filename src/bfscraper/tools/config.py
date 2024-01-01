import regex as re

# Regular expressions:
REGEX_FLAGS = re.IGNORECASE | re.DOTALL

#  Connection:
TIMEOUT = 0
LIMIT = 20

# Domain and routing:
BASE_URL = "https://bigfoil.com"
TABLE_URL = f"{BASE_URL}/bigtable1.json"


def get_file_url(id_: str) -> str:
    """Get file URL from airfoil ID.

    Args:
        id_ (str): airfoil ID.

    Returns:
        str: file URL.
    """
    return f"{BASE_URL}/D/{id_}_infoDAT.php"
