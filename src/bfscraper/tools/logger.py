from colorama import Fore, Style


class Logger:

    @classmethod
    def info(cls, message: str, *args, **kwargs):
        print(Fore.YELLOW + Style.NORMAL
              + f":: [Info] :: {message}{Style.RESET_ALL}",
              *args, **kwargs)

    @classmethod
    def success(cls, message: str, *args, **kwargs):
        print(Fore.GREEN + Style.NORMAL
              + f":: [Success] :: {message}{Style.RESET_ALL}",
              *args, **kwargs)

    @classmethod
    def error(cls, message: str, *args, **kwargs):
        print(Fore.RED + Style.BRIGHT
              + f":: [Error] :: {message}{Style.RESET_ALL}",
              *args, **kwargs)

    @classmethod
    def warning(cls, message: str, *args, **kwargs):
        print(Fore.YELLOW + Style.BRIGHT
              + f":: [Warning] :: {message}{Style.RESET_ALL}",
              *args, **kwargs)
