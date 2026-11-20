"""Kişi Adları Sözlüğü\\
Person Name Dictionary
"""

from enum import IntEnum
from typing import Literal

from aiohttp import ClientSession
from pydantic import (
    BaseModel,
    Field,
    AliasChoices,
    TypeAdapter,
    model_validator,
)

from tdk.internal.http import API_BASE_URL, make_http_session_optional
from tdk.internal.utils import make_sync, adapt_input_to_enum, assert_not_found

__all__ = [
    "NameSearchGender",
    "NameSearchField",
    "NameGender",
    "NameMeaning",
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


class NameMeaning(BaseModel):
    origin: str = Field(validation_alias=AliasChoices("origin", "koken"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))
    gender: NameGender = Field(validation_alias=AliasChoices("gender", "cins"))


class NameEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "ad_id"))
    name: str = Field(validation_alias=AliasChoices("name", "ad"))
    meaning: str = Field(
        default="",
        validation_alias=AliasChoices("meaning", "anlam"),
    )
    origin: str = Field(
        default="",
        validation_alias=AliasChoices("origin", "koken"),
    )
    gender: NameGender = Field(validation_alias=AliasChoices("gender", "cins"))
    pronunciation: str | None = Field(
        default=None,
        validation_alias=AliasChoices("pronunciation", "soyleyis"),
    )
    meanings: list[NameMeaning] = Field(
        default_factory=list,
        validation_alias=AliasChoices("meanings", "anlamlar"),
    )

    @model_validator(mode="before")
    @classmethod
    def _flatten_meanings(cls, data):
        if not isinstance(data, dict):
            return data
        meanings = data.get("anlamlar")
        if not isinstance(meanings, list) or not meanings:
            return data
        data = dict(data)
        if "meaning" not in data and "anlam" not in data:
            data["meaning"] = "\n".join(
                str(meaning["anlam"])
                for meaning in meanings
                if meaning.get("anlam")
            )
        if "origin" not in data and "koken" not in data:
            data["origin"] = "; ".join(
                dict.fromkeys(
                    str(meaning["koken"])
                    for meaning in meanings
                    if meaning.get("koken")
                )
            )
        return data


name_list_adapter = TypeAdapter(list[NameEntry])


@make_http_session_optional
async def search_names(
    query: str,
    *,
    according_to: NameSearchField | Literal["name", "meaning"],
    gender: NameSearchGender | Literal["female", "male", "unisex", "either"],
    http_session: ClientSession,
) -> list[NameEntry]:
    search_gender = adapt_input_to_enum(gender, NameSearchGender)
    async with http_session.get(
        f"{API_BASE_URL}/kisi-ad",
        params={
            "ara": query,
            "gore": adapt_input_to_enum(according_to, NameSearchField).value,
            "cins": search_gender.value,
        },
    ) as res:
        res_data = await res.json()
        if not isinstance(res_data, list):
            assert_not_found(res_data)
            return []
        entries = name_list_adapter.validate_python(res_data)
        if search_gender != NameSearchGender.EITHER:
            entries = [
                entry for entry in entries if entry.gender == search_gender
            ]
        return entries


@make_sync(search_names)
def search_names_sync(): ...
