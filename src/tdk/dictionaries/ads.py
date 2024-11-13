"""Atasözleri ve Deyimler Sözlüğü\\
Proverbs and Phrases Dictionary
"""

from enum import Enum

from pydantic import BaseModel, AliasChoices, Field, TypeAdapter

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import make_sync, assert_not_found


__all__ = [
    "SayingType",
    "SayingEntry",
    "search_saying",
    "search_saying_async",
]


class SayingType(Enum):
    PROVERB = "Atasözü"
    PHRASE = "Deyim"


class SayingEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "soz_id"))
    saying: str = Field(validation_alias=AliasChoices("saying", "sozum"))
    search: str = Field(validation_alias=AliasChoices("search", "atara"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlami"))
    key: str = Field(validation_alias=AliasChoices("key", "anahtar"))
    type: SayingType = Field(validation_alias=AliasChoices("type", "turu2"))
    # gosterim_tarihi: ? = ? (always null?)


saying_entry_adapter = TypeAdapter(list[SayingEntry])


@make_http_session_optional
async def search_saying(query: str, *, http_session) -> list[SayingEntry]:
    async with http_session.get(
        "https://sozluk.gov.tr/atasozu", params={"ara": query}
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if isinstance(res_data, list):
            return saying_entry_adapter.validate_python(res_data)
        assert_not_found(res_data)
        return []


@make_sync(search_saying)
def search_saying_async(): ...
