"""Logger module for the bfscraper package.

Author:
    Paulo Sanchez (@erlete)
"""


from colorama import Fore, Style


class Logger:
    """Logger class.

    Attributes:
        ENABLED (bool): whether to enable logging.
    """

    ENABLED = True

    @classmethod
    def info(cls, message: str, *args, **kwargs) -> None:
        """Log an info message.

        Args:
            message (str): message to log.
            *args: positional arguments.
            **kwargs: keyword arguments.
        """
        if cls.ENABLED:
            print(Fore.YELLOW + Style.NORMAL
                  + f":: [Info] :: {message}{Style.RESET_ALL}",
                  *args, **kwargs)

    @classmethod
    def success(cls, message: str, *args, **kwargs) -> None:
        """Log a success message.

        Args:
            message (str): message to log.
            *args: positional arguments.
            **kwargs: keyword arguments.
        """
        if cls.ENABLED:
            print(Fore.GREEN + Style.NORMAL
                  + f":: [Success] :: {message}{Style.RESET_ALL}",
                  *args, **kwargs)

    @classmethod
    def error(cls, message: str, *args, **kwargs) -> None:
        """Log an error message.

        Args:
            message (str): message to log.
            *args: positional arguments.
            **kwargs: keyword arguments.
        """
        if cls.ENABLED:
            print(Fore.RED + Style.BRIGHT
                  + f":: [Error] :: {message}{Style.RESET_ALL}",
                  *args, **kwargs)

    @classmethod
    def warning(cls, message: str, *args, **kwargs) -> None:
        """Log a warning message.

        Args:
            message (str): message to log.
            *args: positional arguments.
            **kwargs: keyword arguments.
        """
        if cls.ENABLED:
            print(Fore.YELLOW + Style.BRIGHT
                  + f":: [Warning] :: {message}{Style.RESET_ALL}",
                  *args, **kwargs)
