"""Tarama Sözlüğü\\
Scans Dictionary
"""

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import make_sync, assert_not_found


__all__ = [
    "TaramaScan",
    "TaramaEntry",
    "search_tarama",
    "search_tarama_sync",
]


class TaramaScan(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "kelime_id"))
    word: str = Field(validation_alias=AliasChoices("word", "kelime"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))
    volume: int = Field(validation_alias=AliasChoices("volume", "cilt"))
    image: str = Field(validation_alias=AliasChoices("image", "resim"))


tarama_scan_list_adapter = TypeAdapter(list[TaramaScan])


class TaramaEntry(BaseModel):
    guide_id: int = Field(
        validation_alias=AliasChoices("guide_id", "kilavuz_id")
    )
    word: str = Field(validation_alias=AliasChoices("word", "kelime"))
    word_id: int = Field(validation_alias=AliasChoices("word_id", "kelime_no"))
    scans: list[TaramaScan] = Field(
        validation_alias=AliasChoices("scans", "taramalar")
    )


tarama_entry_list_adapter = TypeAdapter(list[TaramaEntry])


@make_http_session_optional
async def search_tarama(
    query: str, /, *, http_session: ClientSession
) -> list[TaramaEntry]:
    async with http_session.get(
        "https://sozluk.gov.tr/tarama",
        params={"ara": query},
    ) as resp:
        resp_data = await resp.json()
        if not isinstance(resp_data, list):
            assert resp_data == {"error": "Sonuç bulunamadı"}
            return []
        return tarama_entry_list_adapter.validate_python(resp_data)


@make_sync(search_tarama)
def search_tarama_sync(): ...


@make_http_session_optional
async def get_tarama_scans(
    tdk_id: int, /, *, http_session: ClientSession
) -> list[TaramaScan]:
    async with http_session.get(
        "https://sozluk.gov.tr/taramaId",
        params={"id": tdk_id},
    ) as resp:
        resp_data = await resp.json()
        if not isinstance(resp_data, list):
            assert_not_found(resp_data)
            return []
        return tarama_scan_list_adapter.validate_python(resp_data)


@make_sync(get_tarama_scans)
def get_tarama_scans_sync(): ...
