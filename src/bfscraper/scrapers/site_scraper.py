"""Compound scraper for the whole site.

Author:
    Paulo Sanchez (@erlete)
"""


import json
import sys
from functools import wraps
from time import perf_counter

import regex as re
import requests
from hurry.filesize import size

from ..tools.cache import Cache
from ..tools.logger import Logger
from .async_components import (AsyncScraper, DownloadDataExtractor,
                               DownloadLinksExtractor)


class SiteScraper:
    """Site scraper class.

    Attributes:
        count (int): number of airfoils to scrape (-1 for all available).
        output (str): output file path.
        timeout (int): request timeout in seconds (-1 for no timeout).
        limit (int): simultaneous requests limit.
        verbose (bool): verbose mode.
        cache (Cache): cache instance.
    """

    def __init__(
        self,
        count: int,
        output: str,
        timeout: int,
        limit: int,
        verbose: bool
    ) -> None:
        """Initialize a SiteScraper instance.

        Args:
            count (int): number of airfoils to scrape (-1 for all available).
            output (str): output file path.
            timeout (int): request timeout in seconds (-1 for no timeout).
            limit (int): simultaneous requests limit.
            verbose (bool): verbose mode.
        """
        self.count = count
        self.output = output
        self.timeout = timeout
        self.limit = limit
        self.verbose = verbose

        self.cache = Cache(".bfscrapercache")

        Logger.ENABLED = self.verbose

    def timing(function):
        """Timing decorator.

        Args:
            function (callable): function to be decorated.

        Returns:
            callable: decorated function.
        """
        @wraps(function)
        def wrap(self, *args, **kw):
            ts = perf_counter()
            result = function(self, *args, **kw)
            te = perf_counter()

            Logger.success(f"Elapsed: {te - ts:.2f}s")
            return result

        return wrap

    @staticmethod
    def get_file_url(id_: str) -> str:
        """Get file URL from airfoil ID.

        Args:
            id_ (str): airfoil ID.

        Returns:
            str: file URL.
        """
        return f"{AsyncScraper.BASE_URL}/D/{id_}_infoDAT.php"

    @staticmethod
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

    @timing
    def _fetch_entries(self) -> requests.Response:
        """Fetch database entries.

        Returns:
            requests.Response: response object.
        """
        Logger.info("Fetching database entries...")
        return requests.get(AsyncScraper.TABLE_URL)

    @timing
    def _parse_entries(self, request: requests.Response) -> dict:
        """Parse database entries.

        Args:
            request (requests.Response): response object.

        Returns:
            dict: parsed data.
        """
        Logger.info("Parsing database entries...")
        return {
            (
                id_ := re.findall(
                    r"airfoil=([\d\w-]+)",
                    entry["Link"],
                    flags=AsyncScraper.REGEX_FLAGS
                )[0]
            ): {
                "name": entry["Name"],
                "family": entry["Family"],
                "links": {
                    "info": re.findall(
                        r"(http.+?)\"",
                        entry["Link"],
                        flags=AsyncScraper.REGEX_FLAGS
                    )[0],
                    "files": self.get_file_url(id_)
                },
                "download-links": {},
                "download-data": {},
                "data-sources": [
                    source.strip() for source in
                    entry["Data Sources"].split(" ")
                ],
                "optimizations": {
                    "thickness": self.parseFloat(entry["Thickness"]),
                    "x-thickness": self.parseFloat(entry["x Thickness"]),
                    "camber": self.parseFloat(entry["Camber"]),
                    "LD-Max": self.parseFloat(entry["LD Max"]),
                    "Cl-Max": self.parseFloat(entry["Cl Max"]),
                    "CdCl01": self.parseFloat(entry["CdCl01"]),
                    "CdCl04": self.parseFloat(entry["CdCl04"]),
                    "CdCl06": self.parseFloat(entry["CdCl06"])
                }
            }
            for entry in (
                request.json()[:self.count]
                if self.count > 0
                else request.json()
            )
        }

    @timing
    def _scrape_urls(self, data: dict) -> dict:
        """Scrape download URLs.

        Args:
            data (dict): parsed data.

        Returns:
            dict: scraped data.
        """
        Logger.info(f"Scraping {len(data)} URLs...")
        DownloadLinksExtractor(
            cache=self.cache,
            timeout=self.timeout,
            limit=self.limit,
            progress_bar=self.verbose
        ).scrape(data)
        self.cache.save()
        return data

    @timing
    def _download_airfoils(self, data: dict) -> dict:
        """Download all fetched and parsed airfoil data.

        Args:
            data (dict): scraped data.

        Returns:
            dict: downloaded data.
        """
        Logger.info(f"Downloading {len(data)} airfoils...")
        DownloadDataExtractor(
            cache=self.cache,
            timeout=self.timeout,
            limit=self.limit,
            progress_bar=self.verbose
        ).scrape(data)
        self.cache.save()
        return data

    @timing
    def _save_data(self, data: dict) -> None:
        """Save downloaded data.

        Args:
            data (dict): downloaded data.
        """
        Logger.info("Saving data...")
        with open(self.output, "w") as f:
            json.dump(data, f, indent=4)

    def _print_summary(self, data: dict) -> None:
        """Print scraping summary.

        Args:
            data (dict): downloaded data.
        """
        total_bytes_1 = sum(
            sum(sys.getsizeof(value)
                for value in entry['download-data'].values())
            for entry in data.values()
        )
        total_bytes_2 = sys.getsizeof(json.dumps(data, indent=4))

        Logger.success(
            f"Scraped {len(data)} airfoils with a total size of"
            f" {size(total_bytes_1)} ({size(total_bytes_2)} including metadata)."
        )

    def run(self) -> None:
        """Run the scraper."""
        Logger.info("Running scraper...")
        request = self._fetch_entries()
        data = self._parse_entries(request)
        data = self._scrape_urls(data)
        data = self._download_airfoils(data)
        self._save_data(data)
        self._print_summary(data)
