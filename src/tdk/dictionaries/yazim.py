"""Yazım Kılavuzu\\
Spelling Guide

TDK now publishes this guide as a static website
at https://yazim.tdk.gov.tr without a search API.
"""

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import make_sync, SoundURL

__all__ = [
    "SpellingEntry",
    "search_spelling",
    "search_spelling_sync",
]


class SpellingEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "yazim_id"))
    phrase: str = Field(validation_alias=AliasChoices("name", "sozu"))
    suffixes: str = Field(validation_alias=AliasChoices("suffixes", "ekler"))
    sound_url: SoundURL = Field(
        validation_alias=AliasChoices("sound_code", "seskod")
    )


spelling_entry_list_adapter = TypeAdapter(list[SpellingEntry])


@make_http_session_optional
async def search_spelling(
    query: str, /, *, http_session: ClientSession
) -> list[SpellingEntry]:
    raise RuntimeError(
        "TDK no longer publishes a search API for the Spelling Guide. "
        "The guide is available at https://yazim.tdk.gov.tr."
    )


@make_sync(search_spelling)
def search_spelling_sync(): ...
