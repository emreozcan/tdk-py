"""Sıkça Karıştırılan Sözler Kılavuzu\\
Frequently Confused Words Guide
"""

from aiohttp import ClientSession
from pydantic import BaseModel

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import SoundURL, make_sync, assert_not_found


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
    async with http_session.get(
        "https://sozluk.gov.tr/kilavuz",
        params={"prm": "sks", "ara": query},
    ) as resp:
        resp_data = await resp.json()
        if not isinstance(resp_data, dict):
            assert_not_found(resp_data)
            return []
        return [
            SKSEntry(
                tdk_id=f["id"],
                word_1=SKSWord(
                    word=f["kelime1"],
                    # eskelime=f["eskelime1"],
                    meaning_html=f["anlam1"],
                    sound_url=f["ses1"],
                ),
                word_2=SKSWord(
                    word=f["kelime2"],
                    # eskelime=f["eskelime2"],
                    meaning_html=f["anlam2"],
                    sound_url=f["ses2"],
                ),
                search=f["arama"],
            )
            for f in resp_data
        ]


@make_sync(search_sks)
def search_sks_sync(): ...
