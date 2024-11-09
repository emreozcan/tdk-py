import aiohttp
from pydantic import TypeAdapter

from tdk.models import Entry
from tdk.networking import session_maker
from tdk.tools import lowercase, dictionary_order


def _with_or_without_session(func):
    async def wrapper(*args, **kwargs):
        if "http_session" in kwargs:
            return await func(*args, **kwargs)
        async with session_maker() as http_session:
            return await func(*args, http_session=http_session, **kwargs)

    # typing:
    wrapper.__annotations__ = func.__annotations__

    return wrapper


@_with_or_without_session
async def get_index(*, http_session: aiohttp.ClientSession) -> list[str]:
    async with (http_session.get(
        "https://sozluk.gov.tr/autocomplete.json"
    ) as response):
        return sorted(
            [
                entry["madde"]
                for entry in
                await response.json(content_type="text/html; charset=utf-8")
            ],
            key=dictionary_order
        )


@_with_or_without_session
async def search(query: str, *, http_session: aiohttp.ClientSession) \
        -> list[Entry]:
    query = lowercase(query, remove_unknown_characters=False)
    async with http_session.get(
        "https://sozluk.gov.tr/gts",
        params={"ara": query}
    ) as response:
        words = await response.json(content_type="text/html; charset=utf-8")
        if not isinstance(words, list):
            if words["error"] == "Sonuç bulunamadı":  # No results
                return []
            raise RuntimeError(f'The server responded with an error: {words["error"]}')
        return TypeAdapter(list[Entry]).validate_python(words)


@_with_or_without_session
async def get(id: int, *, http_session: aiohttp.ClientSession) -> Entry:
    async with http_session.get(
        "https://sozluk.gov.tr/gts_id",
        params={"id": id}
    ) as response:
        word = await response.json(content_type="text/html; charset=utf-8")
        if not isinstance(word, list):
            raise RuntimeError(f'The server responded with an error: {word["error"]}')
        return Entry(**word[0])


@_with_or_without_session
async def get_suggestion(query: str, *, http_session: aiohttp.ClientSession) \
        -> list[str]:
    async with http_session.get(
        "https://sozluk.gov.tr/oneri",
        params={"soz": query}
    ) as response:
        try:
            return [
                entry["madde"]
                for entry in
                await response.json(content_type="text/html; charset=utf-8")
            ]
        except Exception as e:
            raise RuntimeError(
                "The server returned an invalid response: "
                "https://github.com/emreozcan/tdk-py/issues/2"
                "#issuecomment-1153257967"
            ) from e
