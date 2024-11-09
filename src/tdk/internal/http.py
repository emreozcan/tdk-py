from functools import wraps
from typing import Optional

import aiohttp

http_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://sozluk.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/99.0.4844.51 "
    "Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def session_maker() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(headers=http_headers)


def with_http_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if "http_session" in kwargs:
            return await func(*args, **kwargs)
        async with session_maker() as http_session:
            return await func(*args, http_session=http_session, **kwargs)

    # typing:
    wrapper.__annotations__ = func.__annotations__.copy()
    wrapper.__annotations__["http_session"] = Optional[aiohttp.ClientSession]

    return wrapper
