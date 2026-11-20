"""Tarama Sözlüğü\\
Scans Dictionary
"""

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import API_BASE_URL, make_http_session_optional
from tdk.internal.utils import make_sync, assert_not_found


__all__ = [
    "TaramaScan",
    "TaramaEntry",
    "search_tarama",
    "search_tarama_sync",
    "get_tarama_scans",
    "get_tarama_scans_sync",
]


class TaramaScan(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "kelime_id"))
    word: str = Field(validation_alias=AliasChoices("word", "kelime"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))
    volume: str | int = Field(validation_alias=AliasChoices("volume", "cilt"))
    image: str = Field(validation_alias=AliasChoices("image", "resim"))


tarama_scan_list_adapter = TypeAdapter(list[TaramaScan])


class TaramaEntry(BaseModel):
    guide_id: int = Field(
        validation_alias=AliasChoices("guide_id", "kilavuz_id")
    )
    word: str = Field(validation_alias=AliasChoices("word", "kelime"))
    word_id: str | int = Field(
        validation_alias=AliasChoices("word_id", "kelime_no")
    )
    scans: list[TaramaScan] = Field(
        validation_alias=AliasChoices("scans", "taramalar", "tarama")
    )


tarama_entry_list_adapter = TypeAdapter(list[TaramaEntry])


@make_http_session_optional
async def search_tarama(
    query: str, /, *, http_session: ClientSession
) -> list[TaramaEntry]:
    async with http_session.get(
        f"{API_BASE_URL}/ts",
        params={"ara": query},
    ) as resp:
        resp_data = await resp.json()
        if not isinstance(resp_data, list):
            assert_not_found(resp_data)
            return []
        return tarama_entry_list_adapter.validate_python(resp_data)


@make_sync(search_tarama)
def search_tarama_sync(): ...


@make_http_session_optional
async def get_tarama_scans(
    tdk_id: int, /, *, http_session: ClientSession
) -> list[TaramaScan]:
    raise RuntimeError(
        "TDK no longer publishes a separate endpoint for Tarama scans. "
        "The scans are returned by search_tarama instead."
    )


@make_sync(get_tarama_scans)
def get_tarama_scans_sync(): ...
