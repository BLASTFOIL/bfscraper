"""Cache utilities module.

Author:
    Paulo Sanchez (@erlete)
"""


import os
import pickle
from typing import Any


class Cache:
    """Cache class for storing data between runs.

    Attributes:
        filename (str): cache file path.
        cache (dict): cache dictionary.
    """

    def __init__(self, filename: str) -> None:
        """Initialize a Cache instance.

        Args:
            filename (str): cache file path.
        """
        self.filename = filename
        self.cache: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load cache from file."""
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as fp:
                self.cache = pickle.load(fp)

    def save(self) -> None:
        """Save cache to file."""
        with open(self.filename, "wb") as fp:
            pickle.dump(self.cache, fp)

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache.

        Args:
            key (str): key to get value for.
            default (Any): default value to return if key is not found.
                Defaults to None.

        Returns:
            Any: value from cache.
        """
        return self.cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key (str): key to set value for.
            value (Any): value to set.
        """
        self.cache[key] = value
        self.save()

    def __getitem__(self, key: str, default: Any = None) -> Any:
        """Get value from cache.

        Args:
            key (str): key to get value for.
            default (Any): default value to return if key is not found.
                Defaults to None.

        Returns:
            Any: value from cache.
        """
        return self.get(key, default)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set value in cache.

        Args:
            key (str): key to set value for.
            value (Any): value to set.
        """
        self.set(key, value)
