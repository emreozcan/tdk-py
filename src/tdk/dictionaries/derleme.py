"""Derleme Sözlüğü (Türkiye Türkçesi Ağızları Sözlüğü)\\
Compilation Dictionary (Turkish Dialects Dictionary)
"""

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import StrOrNone, make_sync, assert_not_found


__all__ = [
    "DerlemeEntry",
    "search_derleme",
    "search_derleme_sync",
]


class DerlemeEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "madde_id"))
    masthead_id: int = Field(
        validation_alias=AliasChoices("masthead_id", "kunye_id")
    )
    entry: str = Field(validation_alias=AliasChoices("entry", "madde"))
    entry_with_numeral: str = Field(
        validation_alias=AliasChoices("entry_with_numeral", "madde_ekli")
    )
    actual_entry: StrOrNone = Field(
        validation_alias=AliasChoices("actual_entry", "asilk")
    )
    actual_entry_with_numeral: StrOrNone = Field(
        validation_alias=AliasChoices("actual_entry_with_numeral", "asilkelim")
    )
    see: StrOrNone = Field(validation_alias=AliasChoices("see", "bakin"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))
    city_html: StrOrNone = Field(
        validation_alias=AliasChoices("city_html", "sehir")
    )
    abbreviation: str = Field(
        validation_alias=AliasChoices("abbreviation", "kisaltma")
    )
    from_dict: str = Field(
        validation_alias=AliasChoices("from_dict", "eser_ad")
    )
    dict_author: StrOrNone = Field(
        validation_alias=AliasChoices("dict_author", "yazar_ad")
    )
    dict_publisher: str = Field(
        validation_alias=AliasChoices("dict_publisher", "yayinlayan")
    )
    published_place: str = Field(
        validation_alias=AliasChoices("published_place", "yayin_yeri")
    )
    published_year: int = Field(
        validation_alias=AliasChoices("published_year", "yayin_yil")
    )
    physical_volume_html: str = Field(
        validation_alias=AliasChoices("physical_volume_html", "fiziksel")
    )


derleme_entry_list_adapter = TypeAdapter(list[DerlemeEntry])


@make_http_session_optional
async def search_derleme(
    query: str, /, *, http_session: ClientSession
) -> list[DerlemeEntry]:
    async with http_session.get(
        "https://sozluk.gov.tr/derleme", params={"ara": query}
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if isinstance(res_data, list):
            return derleme_entry_list_adapter.validate_python(res_data)
        assert_not_found(res_data)
        return []


@make_sync(search_derleme)
def search_derleme_sync(): ...
