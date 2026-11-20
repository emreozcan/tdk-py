"""Yabancı Sözlere Karşılıklar Kılavuzu\\
Equivalents for Foreign Words Guide
"""

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices

from tdk.internal.http import API_BASE_URL, make_http_session_optional
from tdk.internal.utils import StrOrNone, make_sync, assert_not_found

__all__ = [
    "LoanwordEntry",
    "search_loanwords",
    "search_loanwords_sync",
]


class LoanwordEntry(BaseModel):
    tdk_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("tdk_id", "karsid"),
    )
    loanword: str = Field(
        validation_alias=AliasChoices("loanword", "kkelime", "kelime")
    )
    origin: StrOrNone = Field(
        default=None,
        validation_alias=AliasChoices("origin", "kkoken", "koken"),
    )
    new_word: str = Field(
        validation_alias=AliasChoices("new_word", "kkarsilik", "karsilik")
    )
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))


# query: abone
@make_http_session_optional
async def search_loanwords(
    query: str, *, http_session: ClientSession
) -> list[LoanwordEntry]:
    async with http_session.get(
        f"{API_BASE_URL}/ysk",
        params={"ara": query},
    ) as res:
        res_data = await res.json()
        if isinstance(res_data, dict):
            res_data = [res_data]
        if not isinstance(res_data, list):
            assert_not_found(res_data)
            return []
        return [LoanwordEntry.model_validate(entry) for entry in res_data]


@make_sync(search_loanwords)
def search_loanwords_sync(): ...
