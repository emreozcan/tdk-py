from enum import IntEnum
from typing import Literal

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import with_http_session
from tdk.internal.utils import make_sync, adapt_input_to_enum, assert_not_found


class SearchGender(IntEnum):
    FEMALE = 1
    MALE = 2
    UNISEX = 3
    EITHER = 4


class NameField(IntEnum):
    NAME = 1
    MEANING = 2


class NameGender(IntEnum):
    FEMALE = 1
    MALE = 2
    UNISEX = 3


class Name(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "ad_id"))
    name: str = Field(validation_alias=AliasChoices("name", "ad"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))
    origin: str = Field(validation_alias=AliasChoices("origin", "koken"))
    gender: NameGender = Field(validation_alias=AliasChoices("gender", "cins"))


name_list_adapter = TypeAdapter(list[Name])


@with_http_session
async def search_names(
    query: str,
    *,
    according_to: NameField | Literal[1, 2, "name", "meaning"],
    gender: (
            SearchGender
            | Literal[1, 2, 3, 4, "female", "male", "unisex", "either"]
    ),
    http_session: ClientSession,
) -> list[Name]:
    async with http_session.get(
        "https://sozluk.gov.tr/adlar",
        params={
            "ara": query,
            "gore": adapt_input_to_enum(according_to, NameField),
            "cins": adapt_input_to_enum(gender, SearchGender),
        },
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if not isinstance(res_data, list):
            assert_not_found(res_data)
            return []
        return name_list_adapter.validate_python(res_data)


@make_sync(search_names)
def search_names_sync(): ...
