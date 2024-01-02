"""Main execution module.

Author:
    Paulo Sanchez (@erlete)
"""


import json
import sys
from time import perf_counter as pc

import regex as re
import requests
from colorama import Fore, Style
from hurry.filesize import size

from .core.cache import Cache
from .tools.aux import fprint, get_file_url, get_limit, parseFloat
from .tools.config import REGEX_FLAGS, TABLE_URL
from .tools.scrapers import DownloadDataExtractor, DownloadLinksExtractor

fprint("INFO: Fetching database entries...", Fore.YELLOW, Style.BRIGHT)
cron = pc()
request = requests.get(TABLE_URL)
fprint(f"INFO: Done! ({pc() - cron:.2f}s)", Fore.GREEN, Style.BRIGHT)

fprint("INFO: Parsing database entries...", Fore.YELLOW, Style.BRIGHT)
cron = pc()
limit = get_limit()
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
    for entry in (request.json()[:limit] if limit > 0 else request.json())
}
fprint(f"INFO: Done! ({pc() - cron:.2f}s)", Fore.GREEN, Style.BRIGHT)

#  Data extraction and caching:
CACHE = Cache(".cache")

fprint(f"INFO: Scraping {len(data)} URLs...", Fore.YELLOW, Style.BRIGHT)
cron = pc()
DownloadLinksExtractor(cache=CACHE).scrape(data)
CACHE.save()
fprint(f"INFO: Done! ({pc() - cron:.2f}s)", Fore.GREEN, Style.BRIGHT)

fprint(f"INFO: Downloading {len(data)} airfoils...", Fore.YELLOW, Style.BRIGHT)
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

# Summary:
total_bytes_1 = sum(
    sum(sys.getsizeof(value) for value in entry['download-data'].values())
    for entry in data.values()
)
total_bytes_2 = sys.getsizeof(json.dumps(data, indent=4))

print(
    Fore.GREEN + Style.BRIGHT
    + f"INFO: Scraped {len(data)} airfoils with a total size of"
    + f" {size(total_bytes_1)} ({size(total_bytes_2)} including metadata)."
    + Style.RESET_ALL
)
