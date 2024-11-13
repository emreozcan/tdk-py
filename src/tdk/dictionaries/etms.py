"""Etimoloji Sözlüğü\\
Etymology Dictionary
"""

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.tools import dictionary_order
from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import make_sync, StrOrNone, assert_not_found


__all__ = [
    "ETMSEntry",
    "get_etms_index",
    "get_etms_index_sync",
    "search_etms",
    "search_etms_sync",
]


@make_http_session_optional
async def get_etms_index(*, http_session: ClientSession) -> list[str]:
    async with http_session.get(
            "https://sozluk.gov.tr/etmsAutoComp.json"
    ) as response:
        return sorted(
            [entry["madde"] for entry in await response.json()],
            key=dictionary_order,
        )


@make_sync(get_etms_index)
def get_etms_index_sync(): ...


class ETMSEntry(BaseModel):
    entry: str = Field(validation_alias=AliasChoices("entry", "madde"))
    meaning: StrOrNone = Field(
        validation_alias=AliasChoices("meaning", "anlam")
    )
    meaning_1: StrOrNone = Field(
        validation_alias=AliasChoices("meaning_1", "anlam1")
    )
    meaning_2: StrOrNone = Field(
        validation_alias=AliasChoices("meaning_2", "anlam2")
    )
    meaning_3: StrOrNone = Field(
        validation_alias=AliasChoices("meaning_3", "anlam3")
    )
    meaning_4: StrOrNone = Field(
        validation_alias=AliasChoices("meaning_4", "anlam4")
    )
    meaning_5: StrOrNone = Field(
        validation_alias=AliasChoices("meaning_5", "anlam5")
    )
    meaning_6: StrOrNone = Field(
        validation_alias=AliasChoices("meaning_6", "anlam6")
    )
    meaning_7: StrOrNone = Field(
        validation_alias=AliasChoices("meaning_7", "anlam7")
    )
    meaning_8: StrOrNone = Field(
        validation_alias=AliasChoices("meaning_8", "anlam8")
    )
    explanation: StrOrNone = Field(
        validation_alias=AliasChoices("explanation", "aciklama")
    )
    turkish: StrOrNone = Field(validation_alias=AliasChoices("turkish", "tr"))
    see_1: StrOrNone = Field(validation_alias=AliasChoices("see_1", "bk1"))
    see_2: StrOrNone = Field(validation_alias=AliasChoices("see_2", "bk2"))
    see_3: StrOrNone = Field(validation_alias=AliasChoices("see_3", "bk3"))
    see_4: StrOrNone = Field(validation_alias=AliasChoices("see_4", "bk4"))
    source: StrOrNone = Field(validation_alias=AliasChoices("source", "kaynak"))


etms_entry_list_adapter = TypeAdapter(list[ETMSEntry])


@make_http_session_optional
async def search_etms(
    query: str, /, *, http_session: ClientSession
) -> list[ETMSEntry]:
    async with http_session.get(
        "https://sozluk.gov.tr/etms", params={"ara": query}
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if isinstance(res_data, list):
            return etms_entry_list_adapter.validate_python(res_data)
        assert_not_found(res_data)
        return []


@make_sync(search_etms)
def search_etms_sync(): ...
