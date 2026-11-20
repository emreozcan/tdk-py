"""Sıkça Karıştırılan Sözler Kılavuzu\\
Frequently Confused Words Guide

TDK no longer publishes this guide on its website.
"""

from aiohttp import ClientSession
from pydantic import BaseModel

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import SoundURL, make_sync


__all__ = [
    "SKSWord",
    "SKSEntry",
    "search_sks",
    "search_sks_sync",
]


class SKSWord(BaseModel):
    word: str
    # eskelime: str?
    meaning_html: str
    sound_url: SoundURL


class SKSEntry(BaseModel):
    tdk_id: int
    word_1: SKSWord
    word_2: SKSWord
    search: str


@make_http_session_optional
async def search_sks(
    query: str, /, *, http_session: ClientSession
) -> list[SKSEntry]:
    raise RuntimeError(
        "TDK no longer publishes the Frequently Confused Words Guide."
    )


@make_sync(search_sks)
def search_sks_sync(): ...
