"""Auxiliary tools module.

This module contains all auxiliary functions and classes used throughout the
package.

Author:
    Paulo Sanchez (@erlete)
"""


import sys

from colorama import Fore, Style

from .config import BASE_URL


def get_file_url(id_: str) -> str:
    """Get file URL from airfoil ID.

    Args:
        id_ (str): airfoil ID.

    Returns:
        str: file URL.
    """
    return f"{BASE_URL}/D/{id_}_infoDAT.php"


def parseFloat(string: str) -> float | None:
    """Parse a string to a float.

    Args:
        string (str): string to parse.

    Returns:
        float | None: parsed float or None if the string is not a float.
    """
    try:
        return float(string)
    except Exception:
        return None


def fprint(
    message: str = "",
    color: str = Fore.WHITE,
    style: str = Style.NORMAL
) -> None:
    """Print formatted text.

    Args:
        message (str, optional): message to print. Defaults to "".
        color (str, optional): text color. Defaults to Fore.WHITE.
        style (str, optional): text style. Defaults to Style.NORMAL.
    """
    print(f"{color}{style}{message}{Style.RESET_ALL}")


def get_limit() -> int:
    """Get data fetching limit argument from CLI.

    Returns:
        int: data fetching limit.
    """
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except Exception:
            return 0

    return 0
