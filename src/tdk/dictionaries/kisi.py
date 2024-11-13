"""Kişi Adları Sözlüğü\\
Person Name Dictionary
"""

from enum import IntEnum
from typing import Literal

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import make_sync, adapt_input_to_enum, assert_not_found


__all__ = [
    "NameSearchGender",
    "NameSearchField",
    "NameGender",
    "NameEntry",
    "search_names",
    "search_names_sync",
]


class NameSearchGender(IntEnum):
    FEMALE = 1
    MALE = 2
    UNISEX = 3
    EITHER = 4


class NameSearchField(IntEnum):
    NAME = 1
    MEANING = 2


class NameGender(IntEnum):
    FEMALE = 1
    MALE = 2
    UNISEX = 3


class NameEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "ad_id"))
    name: str = Field(validation_alias=AliasChoices("name", "ad"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))
    origin: str = Field(validation_alias=AliasChoices("origin", "koken"))
    gender: NameGender = Field(validation_alias=AliasChoices("gender", "cins"))


name_list_adapter = TypeAdapter(list[NameEntry])


@make_http_session_optional
async def search_names(
    query: str,
    *,
    according_to: NameSearchField | Literal["name", "meaning"],
    gender: (
            NameSearchGender
            | Literal["female", "male", "unisex", "either"]
    ),
    http_session: ClientSession,
) -> list[NameEntry]:
    async with http_session.get(
        "https://sozluk.gov.tr/adlar",
        params={
            "ara": query,
            "gore": adapt_input_to_enum(according_to, NameSearchField),
            "cins": adapt_input_to_enum(gender, NameSearchGender),
        },
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if not isinstance(res_data, list):
            assert_not_found(res_data)
            return []
        return name_list_adapter.validate_python(res_data)


@make_sync(search_names)
def search_names_sync(): ...
