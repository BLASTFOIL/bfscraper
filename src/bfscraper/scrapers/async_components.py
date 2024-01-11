"""Scraping utilities module.

This module contains all classes and methods that make asynchronous scraping
possible.

Author:
    Paulo Sanchez (@erlete)
"""


import asyncio
from typing import Any

import aiohttp
import regex as re
from colorama import Fore, Style
from tqdm.asyncio import tqdm_asyncio

from ..tools.cache import Cache


class AsyncScraper:
    """Asynchronous scraper class.

    Attributes:
        cache (Cache): cache instance.
        failed (dict[str, list[str]]): failed URLs.
        timeout (int): timeout for each request.
        limit (int): maximum number of concurrent requests.
        progress_bar (bool): whether to display a progress bar.
        REGEX_FLAGS (int): regex flags.
        BASE_URL (str): base site URL.
        TABLE_URL (str): data table URL.
    """

    REGEX_FLAGS = re.IGNORECASE | re.DOTALL
    BASE_URL = "https://bigfoil.com"
    TABLE_URL = f"{BASE_URL}/bigtable1.json"

    def __init__(
        self,
        cache: Cache,
        timeout: int,
        limit: int,
        progress_bar: bool = True
    ) -> None:
        """Initialize an AsyncScraper instance.

        Args:
            cache (Cache): cache instance.
            timeout (int): timeout for each request.
            limit (int): maximum number of concurrent requests.
            progress_bar (bool): whether to display a progress bar. Defaults
                to True.
        """
        self.cache = cache
        self.progress_bar = progress_bar
        self._failed: dict[str, list[str]] = {}
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
            connector=aiohttp.TCPConnector(limit=limit)
        )

    @property
    def progress_bar(self) -> bool:
        """Get progress bar flag.

        Returns:
            bool: progress bar flag.
        """
        return self._progress_bar

    @progress_bar.setter
    def progress_bar(self, value: bool) -> None:
        """Set progress bar flag.

        Args:
            value (bool): progress bar flag.
        """
        if not isinstance(value, bool):
            raise TypeError("progress_bar must be a boolean value.")

        self._progress_bar = value

    @property
    def cache(self) -> Cache:
        """Get cache instance.

        Returns:
            Cache: cache instance.
        """
        return self._cache

    @cache.setter
    def cache(self, value: Cache) -> None:
        """Set cache instance.

        Args:
            value (Cache): cache instance.
        """
        if not isinstance(value, Cache):
            raise TypeError("cache must be a Cache instance.")

        self._cache = value

    @property
    def failed(self) -> dict[str, list[str]]:
        """Get failed URLs.

        Returns:
            dict[str, list[str]]: failed URLs.
        """
        return self._failed

    @property
    def session(self) -> aiohttp.ClientSession:
        """Get aiohttp session.

        Returns:
            aiohttp.ClientSession: aiohttp session.
        """
        return self._session

    async def _process(self, entry: Any, collection: Any) -> None:
        """Individual asynchronous process.

        Args:
            entry (Any): data entry.
            collection (Any): collection to be processed.
        """
        pass

    async def _gather(self, collection: Any) -> None:
        """Asyncio gather wrapper.

        Args:
            collection (Any): collection to be processed.
        """
        async with self._session as _:
            await tqdm_asyncio.gather(
                *[self._process(item, collection) for item in collection],
                disable=not self._progress_bar,
                smoothing=0.01,
                colour="YELLOW",
                bar_format=(
                    Style.BRIGHT + Fore.YELLOW
                    + "> {percentage:3.0f}% |"
                    + Style.RESET_ALL
                    + "{bar}"
                    + Style.BRIGHT + Fore.YELLOW
                    + "| <"
                )
            )

            if self._failed:
                print(
                    f"{Style.BRIGHT}{Fore.RED}ERROR: "
                    + f"{sum(len(value) for value in self._failed.values())} "
                    + f"URLs could not be scraped due to {len(self._failed)} "
                    + f"error types:{Style.RESET_ALL}"
                )

                print("\n".join(
                    f"{Fore.RED}{Style.BRIGHT}> {exception}:\n"
                    + Style.RESET_ALL + "\n".join(
                        f"{Fore.YELLOW}{' ' * 2}> {url}{Style.RESET_ALL}"
                        for url in urls
                    )
                    for exception, urls in self._failed.items()
                ) + "\n")

    def scrape(self, collection: Any) -> None:
        """Scrape URLs asynchronously.

        This method contains the asyncio event loop that runs the asynchronous
        processes.

        Args:
            collection (Any): collection to be processed.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._gather(collection=collection))


class DownloadLinksExtractor(AsyncScraper):
    """Download links extractor class."""

    async def _process(self, entry: Any, collection: Any) -> None:
        """Individual asynchronous process.

        Args:
            entry (Any): data entry.
            collection (Any): collection to be processed.
        """
        url = collection[entry]["links"]["files"]

        if self.cache.get(entry, {}).get("download-links"):
            collection[entry]["download-links"] = self.cache.get(
                entry
            )["download-links"]
            return

        try:
            async with self.session.get(url=url) as response:
                data = re.findall(
                    r"<\/div>(<b>.+?<br>)<br>",
                    (await response.read()).decode("utf-8").replace("\n", ""),
                    flags=AsyncScraper.REGEX_FLAGS
                ).pop()

                collection[entry]["download-links"].update({
                    match.group(1).lower().replace(" ", "-").strip(":"):
                        f"{AsyncScraper.BASE_URL}{match.group(2)}"
                    for match in re.finditer(
                        r"<b>(.+?)<\/b>.*?href=\"(.+?)\".*?<br>",
                        data,
                        flags=AsyncScraper.REGEX_FLAGS
                    )
                })

                self.cache.set(entry, collection[entry])

        except Exception as exc:
            self.failed.setdefault(exc.__class__.__name__, []).append(url)


class DownloadDataExtractor(AsyncScraper):
    """Download data extractor class."""

    async def _process(self, entry: Any, collection: Any) -> None:
        """Individual asynchronous process.

        Args:
            entry (Any): data entry.
            collection (Any): collection to be processed.
        """
        for name, url in collection[entry]["download-links"].items():
            if self.cache.get(entry, {}).get("download-data", {}).get(name):
                collection[entry]["download-data"][name] = self.cache.get(
                    entry
                )["download-data"][name]
                continue

            try:
                async with self.session.get(url=url) as response:
                    collection[entry]["download-data"][name] = (
                        await response.read()
                    ).decode("utf-8")

                    self.cache.set(entry, collection[entry])

            except Exception as exc:
                self.failed.setdefault(exc.__class__.__name__, []).append(url)
