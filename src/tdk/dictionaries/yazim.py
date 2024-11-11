from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import with_http_session
from tdk.internal.utils import make_sync, SoundURL, assert_not_found


class SpellingEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "yazim_id"))
    phrase: str = Field(validation_alias=AliasChoices("name", "sozu"))
    suffixes: str = Field(validation_alias=AliasChoices("suffixes", "ekler"))
    sound_url: SoundURL = Field(
        validation_alias=AliasChoices("sound_code", "seskod")
    )


spelling_entry_list_adapter = TypeAdapter(list[SpellingEntry])


@with_http_session
async def search_spelling(
    query: str, /, *, http_session: ClientSession
) -> list[SpellingEntry]:
    async with http_session.get(
        "https://sozluk.gov.tr/yazim",
        params={"ara": query},
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if not isinstance(res_data, list):
            assert_not_found(res_data)
            return []
        return spelling_entry_list_adapter.validate_python(res_data)


@make_sync(search_spelling)
def search_spelling_sync(): ...
