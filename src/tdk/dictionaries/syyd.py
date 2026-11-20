"""Sıkça Yapılan Yanlışlar Kılavuzu\\
Frequently Made Mistakes Guide

TDK no longer publishes this guide on its website.
"""

from pydantic import BaseModel, AliasChoices, Field, TypeAdapter

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import SoundURL, make_sync


__all__ = [
    "SYYDEntry",
    "search_syyd",
    "search_syyd_sync",
]


class SYYDEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "id"))
    incorrect: str = Field(
        validation_alias=AliasChoices("incorrect", "yanliskelime")
    )
    correct: str = Field(
        validation_alias=AliasChoices("correct", "dogrukelime")
    )
    sound_url: SoundURL = Field(
        validation_alias=AliasChoices("sound_url", "yanlisses")
    )
    # eskelime?
    meaning_html: str = Field(
        validation_alias=AliasChoices("meaning_html", "anlam1")
    )
    search: str = Field(validation_alias=AliasChoices("search", "yanlisara"))


syyd_entry_list_adapter = TypeAdapter(list[SYYDEntry])


@make_http_session_optional
async def search_syyd(query: str, /, *, http_session) -> list[SYYDEntry]:
    raise RuntimeError(
        "TDK no longer publishes the Frequently Made Mistakes Guide."
    )


@make_sync(search_syyd)
def search_syyd_sync(): ...
