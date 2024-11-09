import aiohttp
from pydantic import TypeAdapter

from tdk.models import Entry
from tdk.http import with_http_session
from tdk.tools import lowercase, dictionary_order


__all__ = [
    "get_index",
    "search",
    "get_suggestion",
]


@with_http_session
async def get_index(*, http_session: aiohttp.ClientSession) -> list[str]:
    async with (http_session.get(
        "https://sozluk.gov.tr/autocomplete.json"
    ) as response):
        return sorted(
            [
                entry["madde"]
                for entry in
                await response.json()
            ],
            key=dictionary_order
        )


@with_http_session
async def search(query: str, /, *, http_session: aiohttp.ClientSession) \
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




@with_http_session
async def get_suggestion(query: str, /, *, http_session: aiohttp.ClientSession) \
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
