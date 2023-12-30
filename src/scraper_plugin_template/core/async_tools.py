import asyncio

import aiohttp
import regex as re
import requests
from colorama import Style
from tqdm.asyncio import tqdm_asyncio


class AsyncScraper:

    TIMEOUT: int = 0
    LIMIT: int = 50

    def __init__(self, urls: list[str]) -> None:
        self.urls = urls
        self.failed: list[str] = []
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.TIMEOUT),
            connector=aiohttp.TCPConnector(limit=self.LIMIT)
        )

    def scrape(self, progress_bar: bool = True) -> None:
        """Scrape URLs asynchronously with a progress bar.

        Args:
            progress_bar (bool, optional): whether to display a progress bar.
                Defaults to True.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run(progress_bar=progress_bar))

    async def run(self, progress_bar: bool = True) -> None:
        """Run asynchronous processes with a progress bar.

        Args:
            progress_bar (bool, optional): whether to display a progress bar.
                Defaults to True.
        """
        async with self.session as session:
            if progress_bar:
                ret = await tqdm_asyncio.gather(*[
                    self.process(url) for url in self.urls
                ], desc="Scraping URL", colour="WHITE",
                    bar_format=f"{Style.BRIGHT}{{desc}} {{n_fmt}} of {{total_fmt}}: {{bar}} ETA: {{remaining}}{Style.RESET_ALL}"
                )
            else:
                ret = await asyncio.gather(*[
                    self.process(url) for url in self.urls
                ])

    async def process(self, url: str, *args, **kwargs) -> None:
        """Single asynchronous process.

        Args:
            url (str): URL to scrape.
        """
        try:
            async with self.session.get(url=url) as response:
                data = await response.read()

        except Exception as exc:
            print(f"ERROR: Unable to get URL {url} due to {exc.__class__}.")
            print(f"{' ' * 4} > {exc}")
            self.failed.append(url)
            print(f"{' ' * 4} > {len(self.failed)} failed URLs so far.")
