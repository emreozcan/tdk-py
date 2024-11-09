from json import JSONDecodeError
from typing import List

from aiohttp import ClientSession
from pydantic import TypeAdapter, BaseModel, Field, AliasChoices

from tdk.etc.enums import ValidatedProperty, OriginLanguage
from tdk.etc.tools import lowercase, dictionary_order
from tdk.internal.http import with_http_session
from tdk.internal.utils import make_sync, assert_not_found


class Writer(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "yazar_id"))
    full_name: str = Field(
        validation_alias=AliasChoices("full_name", "tam_adi")
    )
    short_name: str = Field(
        validation_alias=AliasChoices("short_name", "kisa_adi")
    )


class MeaningExample(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "ornek_id"))
    meaning_id: int = Field(
        validation_alias=AliasChoices("meaning_id", "anlam_id")
    )
    order: int = Field(validation_alias=AliasChoices("order", "ornek_sira"))
    example: str = Field(validation_alias=AliasChoices("example", "ornek"))
    writers: list[Writer] = Field(
        default_factory=lambda: [],
        validation_alias=AliasChoices("writer", "yazar"),
    )


class Proverb(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "madde_id"))
    proverb: str = Field(validation_alias=AliasChoices("proverb", "madde"))
    prefix: str | None = Field(
        validation_alias=AliasChoices("prefix", "on_taki")
    )


class Meaning(BaseModel):
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "anlam_id"))
    order: int = Field(validation_alias=AliasChoices("order", "anlam_sira"))
    is_verb: bool = Field(validation_alias=AliasChoices("is_verb", "fiil"))
    entry_id: int = Field(validation_alias=AliasChoices("entry_id", "madde_id"))
    examples: List[MeaningExample] = Field(
        default_factory=list,
        validation_alias=AliasChoices("examples", "orneklerListe"),
    )
    properties: List[ValidatedProperty] = Field(
        default_factory=list,
        validation_alias=AliasChoices("properties", "ozelliklerListe"),
    )


class Entry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "madde_id"))
    order: int = Field(validation_alias=AliasChoices("order", "kac"))
    entry: str = Field(validation_alias=AliasChoices("entry", "madde"))
    plural: bool = Field(validation_alias=AliasChoices("plural", "cogul_mu"))
    proper: bool = Field(validation_alias=AliasChoices("proper", "ozel_mi"))
    origin_language: OriginLanguage = Field(
        validation_alias=AliasChoices("origin_language", "lisan_kodu")
    )
    original: str = Field(validation_alias=AliasChoices("original", "lisan"))
    entry_normalized: str | None = Field(
        validation_alias=AliasChoices("entry_normalized", "madde_duz")
    )
    meanings: List[Meaning] = Field(
        default_factory=list,
        validation_alias=AliasChoices("meanings", "anlamlarListe"),
    )
    proverbs: List[Proverb] = Field(
        default_factory=list,
        validation_alias=AliasChoices("proverbs", "atasozu"),
    )
    pronunciation: str | None = Field(
        validation_alias=AliasChoices("pronunciation", "telaffuz")
    )
    prefix: str | None = Field(
        validation_alias=AliasChoices("prefix", "on_taki")
    )
    suffix: str | None = Field(validation_alias=AliasChoices("suffix", "taki"))


entry_list_adapter = TypeAdapter(list[Entry])


@with_http_session
async def get_index(*, http_session: ClientSession) -> list[str]:
    async with http_session.get(
        "https://sozluk.gov.tr/autocomplete.json"
    ) as response:
        return sorted(
            [entry["madde"] for entry in await response.json()],
            key=dictionary_order,
        )


@make_sync(get_index)
def get_index_sync(): ...


@with_http_session
async def get_circumflex_index(
    *, http_session: ClientSession
) -> dict[str, str]:
    """
    :returns: A dictionary where the keys are entries without circumflex,
              and the values are the entries with.
    """
    async with http_session.get(
        "https://sozluk.gov.tr/assets/js/autocompleteSapka.json"
    ) as response:
        return await response.json()


@make_sync(get_circumflex_index)
def get_circumflex_index_sync(): ...


@with_http_session
async def search(query: str, /, *, http_session: ClientSession) -> list[Entry]:
    query = lowercase(query, keep_unknown_characters=False)
    async with http_session.get(
        "https://sozluk.gov.tr/gts", params={"ara": query}
    ) as response:
        words = await response.json(content_type="text/html; charset=utf-8")
        if isinstance(words, list):
            return entry_list_adapter.validate_python(words)
        assert_not_found(words)
        return []


@make_sync(search)
def search_sync(): ...


@with_http_session
async def search_proverbs_and_phrases(
    query: str, /, *, http_session: ClientSession
) -> list[Entry]:
    query = lowercase(query, keep_unknown_characters=False)
    async with http_session.get(
        "https://sozluk.gov.tr/gtsAtasozDeyim", params={"ara": query}
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if isinstance(res_data, list):
            return entry_list_adapter.validate_python(res_data)
        assert_not_found(res_data)
        return []


@make_sync(search_proverbs_and_phrases)
def search_proverbs_and_phrases_sync(): ...


@with_http_session
async def get_suggestions(
    query: str, /, *, http_session: ClientSession
) -> list[str]:
    async with http_session.get(
        "https://sozluk.gov.tr/oneri", params={"soz": query}
    ) as response:
        try:
            return [
                entry["madde"]
                for entry in await response.json(
                    content_type="text/html; charset=utf-8"
                )
            ]
        except JSONDecodeError as e:
            raise RuntimeError(
                "The server returned an invalid response: "
                "https://github.com/emreozcan/tdk-py/issues/2"
                "#issuecomment-1153257967"
            ) from e


@make_sync(get_suggestions)
def get_suggestions_sync(): ...