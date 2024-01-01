import asyncio
from typing import Any

import aiohttp
import regex as re
from tqdm.asyncio import tqdm_asyncio

from ..core.cache import Cache
from .config import BASE_URL, LIMIT, REGEX_FLAGS, TIMEOUT


class AsyncScraper:
    """Asynchronous scraper class.

    Attributes:
        cache (Cache): cache instance.
        progress_bar (bool): whether to display a progress bar.
        TIMEOUT (int): timeout for each request.
        LIMIT (int): maximum number of concurrent requests.
    """

    TIMEOUT: int = TIMEOUT
    LIMIT: int = LIMIT

    def __init__(self, cache: Cache, progress_bar: bool = True) -> None:
        """Initialize an AsyncScraper instance.

        Args:
            cache (Cache): cache instance.
            progress_bar (bool): whether to display a progress bar. Defaults
                to True.
        """
        self.cache = cache
        self.progress_bar = progress_bar
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.TIMEOUT),
            connector=aiohttp.TCPConnector(limit=self.LIMIT)
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
        async with self.session as session:
            if self._progress_bar:
                await tqdm_asyncio.gather(
                    *[self._process(item, collection) for item in collection],
                    desc="Scraping URLs",
                    bar_format=(
                        "{desc} {n_fmt} of {total_fmt}: {bar} ETA: "
                        + "{remaining}"
                    )
                )
            else:
                await asyncio.gather(
                    *[self._process(item, collection) for item in collection],
                )

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
                    flags=REGEX_FLAGS
                ).pop()

                collection[entry]["download-links"].update({
                    match.group(1).lower().replace(" ", "-").strip(":"):
                        f"{BASE_URL}{match.group(2)}"
                    for match in re.finditer(
                        r"<b>(.+?)<\/b>.*?href=\"(.+?)\".*?<br>",
                        data,
                        flags=REGEX_FLAGS
                    )
                })

                self.cache.set(entry, collection[entry])

        except Exception as exc:
            print(f"ERROR: Unable to get URL {url} due to {exc.__class__}.")
            print(f"{' ' * 4}> {exc}")


class DownloadDataExtractor(AsyncScraper):

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
                print(
                    f"ERROR: Unable to get URL {url} due to {exc.__class__}.")
                print(f"{' ' * 4}> {exc}")
