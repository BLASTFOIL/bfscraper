"""Configuration module.

This module contains all constants and configuration variables used throughout
the package.

Author:
    Paulo Sanchez (@erlete)
"""


import regex as re

# Regular expressions:
REGEX_FLAGS = re.IGNORECASE | re.DOTALL

#  Connection:
TIMEOUT = 0
LIMIT = 20

# Domain and routing:
BASE_URL = "https://bigfoil.com"
TABLE_URL = f"{BASE_URL}/bigtable1.json"
