import sys

from colorama import Fore, Style


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
    else:
        return 0
