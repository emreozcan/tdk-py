from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import with_http_session
from tdk.internal.utils import make_sync, assert_not_found


class WesternEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "kelime_id"))
    word: str = Field(validation_alias=AliasChoices("word", "sozcuk"))
    short_language_code: str = Field(
        validation_alias=AliasChoices("short_language_code", "kistdil")
    )
    original: str = Field(validation_alias=AliasChoices("original", "dilacik"))
    meaning_html: str = Field(
        validation_alias=AliasChoices("meaning_html", "anlam")
    )


western_entry_list_adapter = TypeAdapter(list[WesternEntry])


@with_http_session
async def search_bati(query: str, *, http_session) -> list[WesternEntry]:
    async with http_session.get(
        "https://sozluk.gov.tr/bati", params={"ara": query}
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if isinstance(res_data, list):
            return western_entry_list_adapter.validate_python(res_data)
        assert_not_found(res_data)
        return []


@make_sync(search_bati)
def search_bati_sync(): ...