from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import with_http_session
from tdk.internal.utils import IntOrNone, make_sync


class TermDictionary(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "eser_id"))
    name: str = Field(validation_alias=AliasChoices("name", "eser_ad"))
    published_year: IntOrNone = Field(validation_alias=AliasChoices("published_year", "yaytar"))


@with_http_session
async def get_term_dictionaries(*, http_session: ClientSession) \
        -> list[TermDictionary]:
    async with http_session.get("https://sozluk.gov.tr/terim?terim") as res:
        return TypeAdapter(list[TermDictionary]).validate_python(
            await res.json(content_type="text/html; charset=utf-8")
        )


@make_sync(get_term_dictionaries)
def get_term_dictionaries_sync(): ...
