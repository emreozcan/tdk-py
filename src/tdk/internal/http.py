"""
This module provides helper functions for making HTTP requests.
"""
from collections.abc import MutableMapping
from functools import wraps
from typing import Optional

from aiohttp import ClientSession

default_headers: dict[str, str] = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://sozluk.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/99.0.4844.51 "
    "Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
"""Default headers for HTTP requests."""


def session_maker(**kwargs) -> ClientSession:
    """Create a [](aiohttp.ClientSession) with some default headers.

    This is preferred over creating a base [](aiohttp.ClientSession) because
    the TDK servers block requests that do not have headers.

    :param kwargs:
        Additional arguments to be passed to [](aiohttp.ClientSession).
        :::{important}
        If a `headers` argument is provided in `kwargs`,
        it will be modified to include the mandatory headers.
        Therefore it must be a [](collections.abc.MutableMapping).
        :::

    :raises TypeError:
        if a `headers` argument is provided and it is not a
        [](collections.abc.MutableMapping).
    """
    if "headers" not in kwargs:
        return ClientSession(headers=default_headers, **kwargs)
    if not isinstance(kwargs["headers"], MutableMapping):
        raise TypeError("headers must be a MutableMapping")
    kwargs["headers"].update(default_headers)
    return ClientSession(**kwargs)


def make_http_session_optional(func):
    """Make [](aiohttp.ClientSession) optional for functions that require it.

    Creates a decorator
    that provides a default [](aiohttp.ClientSession)
    created by [](session_maker)
    to the wrapped function.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if "http_session" in kwargs:
            return await func(*args, **kwargs)
        async with session_maker() as http_session:
            return await func(*args, http_session=http_session, **kwargs)

    # typing:
    wrapper.__annotations__ = func.__annotations__.copy()
    wrapper.__annotations__["http_session"] = Optional[ClientSession]

    return wrapper
