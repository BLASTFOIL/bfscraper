import asyncio
import json
from time import perf_counter as pc

import regex as re
import requests
from colorama import Fore, Style

from .core.cache import Cache
from .tools.config import BASE_URL, REGEX_FLAGS, TABLE_URL, get_file_url
from .tools.scrapers import DownloadDataExtractor, DownloadLinksExtractor


def parseFloat(string: str) -> float | None:
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


fprint("INFO: Fetching database entries...", Fore.YELLOW, Style.BRIGHT)
cron = pc()
request = requests.get(TABLE_URL)
fprint(f"INFO: Done! ({pc() - cron:.2f}s)", Fore.GREEN, Style.BRIGHT)

fprint("INFO: Parsing database entries...", Fore.YELLOW, Style.BRIGHT)
cron = pc()
data = {
    (
        id_ := re.findall(
            r"airfoil=([\d\w-]+)",
            entry["Link"],
            flags=REGEX_FLAGS
        )[0]
    ): {
        "name": entry["Name"],
        "family": entry["Family"],
        "links": {
            "info": re.findall(
                r"(http.+?)\"",
                entry["Link"],
                flags=REGEX_FLAGS
            )[0],
            "files": get_file_url(id_)
        },
        "download-links": {},
        "download-data": {},
        "data-sources": [
            source.strip() for source in
            entry["Data Sources"].split(" ")
        ],
        "optimizations": {
            "thickness": parseFloat(entry["Thickness"]),
            "x-thickness": parseFloat(entry["x Thickness"]),
            "camber": parseFloat(entry["Camber"]),
            "LD-Max": parseFloat(entry["LD Max"]),
            "Cl-Max": parseFloat(entry["Cl Max"]),
            "CdCl01": parseFloat(entry["CdCl01"]),
            "CdCl04": parseFloat(entry["CdCl04"]),
            "CdCl06": parseFloat(entry["CdCl06"])
        }
    }
    for entry in request.json()
}
fprint(f"INFO: Done! ({pc() - cron:.2f}s)", Fore.GREEN, Style.BRIGHT)

data = {k: data[k] for k in list(data.keys())[:100]}  # REMOVEME

#  Data extraction and caching:
CACHE = Cache(".cache")

fprint("INFO: Scraping URLs...", Fore.YELLOW, Style.BRIGHT)
cron = pc()
DownloadLinksExtractor(cache=CACHE).scrape(data)
CACHE.save()
fprint(f"INFO: Done! ({pc() - cron:.2f}s)", Fore.GREEN, Style.BRIGHT)

fprint("INFO: Scraping data...", Fore.YELLOW, Style.BRIGHT)
cron = pc()
DownloadDataExtractor(cache=CACHE).scrape(data)
CACHE.save()
fprint(f"INFO: Done! ({pc() - cron:.2f}s)", Fore.GREEN, Style.BRIGHT)

# Data saving:
fprint("INFO: Saving data...", Fore.YELLOW, Style.BRIGHT)
cron = pc()
with open("bigfoil.json", "w") as f:
    json.dump(data, f, indent=4)

fprint(f"INFO: Done! ({pc() - cron:.2f}s)", Fore.GREEN, Style.BRIGHT)
