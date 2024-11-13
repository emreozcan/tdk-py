"""Yabancı Sözlere Karşılıklar Kılavuzu\\
Equivalents for Foreign Words Guide
"""

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import make_sync, assert_not_found


__all__ = [
    "LoanwordEntry",
    "search_loanwords",
    "search_loanwords_sync",
]


class LoanwordEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "karsid"))
    loanword: str = Field(validation_alias=AliasChoices("loanword", "kkelime"))
    origin: str = Field(validation_alias=AliasChoices("origin", "kkoken"))
    new_word: str = Field(
        validation_alias=AliasChoices("new_word", "kkarsilik")
    )
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))


loanword_entry_list_adapter = TypeAdapter(list[LoanwordEntry])


# query: abone
@make_http_session_optional
async def search_loanwords(query: str, *, http_session: ClientSession) \
        -> list[LoanwordEntry]:
    async with http_session.get(
        "https://sozluk.gov.tr/kilavuz",
        params={"prm": "ysk", "ara": query},
    ) as res:
        res_data = await res.json()
        if not isinstance(res_data, list):
            assert_not_found(res_data)
            return []
        return loanword_entry_list_adapter.validate_python(res_data)


@make_sync(search_loanwords)
def search_loanwords_sync(): ...
