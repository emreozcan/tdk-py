from typing import List, Annotated

from aiohttp import ClientSession
from pydantic import TypeAdapter, BaseModel, Field, AliasChoices, \
    BeforeValidator

from tdk.enums import ValidatedProperty, OriginLanguage
from tdk.http import with_http_session
from tdk.tools import lowercase, dictionary_order
from tdk.utils import make_sync


class Writer(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "yazar_id"))
    full_name: str = Field(validation_alias=AliasChoices("full_name", "tam_adi"))
    short_name: str = Field(validation_alias=AliasChoices("short_name", "kisa_adi"))


class MeaningExample(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "ornek_id"))
    meaning_id: int = Field(validation_alias=AliasChoices("meaning_id", "anlam_id"))
    order: int = Field(validation_alias=AliasChoices("order", "ornek_sira"))
    example: str = Field(validation_alias=AliasChoices("example", "ornek"))
    writers: list[Writer] = Field(default_factory=lambda: [], validation_alias=AliasChoices("writer", "yazar"))


class Proverb(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "madde_id"))
    proverb: str = Field(validation_alias=AliasChoices("proverb", "madde"))
    prefix: str | None = Field(validation_alias=AliasChoices("prefix", "on_taki"))


class Meaning(BaseModel):
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "anlam_id"))
    order: int = Field(validation_alias=AliasChoices("order", "anlam_sira"))
    is_verb: bool = Field(validation_alias=AliasChoices("is_verb", "fiil"))
    entry_id: int = Field(validation_alias=AliasChoices("entry_id", "madde_id"))
    examples: List[MeaningExample] = Field(default_factory=list, validation_alias=AliasChoices("examples", "orneklerListe"))
    properties: List[ValidatedProperty] = Field(default_factory=list, validation_alias=AliasChoices("properties", "ozelliklerListe"))


class Entry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "madde_id"))
    order: int = Field(validation_alias=AliasChoices("order", "kac"))
    entry: str = Field(validation_alias=AliasChoices("entry", "madde"))
    plural: bool = Field(validation_alias=AliasChoices("plural", "cogul_mu"))
    proper: bool = Field(validation_alias=AliasChoices("proper", "ozel_mi"))
    origin_language: OriginLanguage = Field(validation_alias=AliasChoices("origin_language", "lisan_kodu"))
    original: str = Field(validation_alias=AliasChoices("original", "lisan"))
    entry_normalized: str | None = Field(validation_alias=AliasChoices("entry_normalized", "madde_duz"))
    meanings: List[Meaning] = Field(default_factory=list, validation_alias=AliasChoices("meanings", "anlamlarListe"))
    proverbs: List[Proverb] = Field(default_factory=list, validation_alias=AliasChoices("proverbs", "atasozu"))
    pronunciation: str | None = Field(validation_alias=AliasChoices("pronunciation", "telaffuz"))
    prefix: str | None = Field(validation_alias=AliasChoices("prefix", "on_taki"))
    suffix: str | None = Field(validation_alias=AliasChoices("suffix", "taki"))



@with_http_session
async def get_index(*, http_session: ClientSession) -> list[str]:
    async with (http_session.get(
        "https://sozluk.gov.tr/autocomplete.json"
    ) as response):
        return sorted(
            [
                entry["madde"]
                for entry in
                await response.json()
            ],
            key=dictionary_order
        )


@make_sync(get_index)
def get_index_sync(): ...


@with_http_session
async def get_etms_index(query: str, /, *,
                         http_session: ClientSession) -> list[str]:
    async with http_session.get(
        "https://sozluk.gov.tr/etmsAutoComp.json",
        params={"ara": query}
    ) as response:
        return sorted(
            [
                entry["madde"]
                for entry in
                await response.json()
            ],
            key=dictionary_order
        )


@make_sync(get_etms_index)
def get_etms_index_sync(): ...


@with_http_session
async def search(query: str, /, *, http_session: ClientSession) \
        -> list[Entry]:
    query = lowercase(query, keep_unknown_characters=False)
    async with http_session.get(
        "https://sozluk.gov.tr/gts",
        params={"ara": query}
    ) as response:
        words = await response.json(content_type="text/html; charset=utf-8")
        if not isinstance(words, list):
            if words["error"] == "Sonuç bulunamadı":  # No results
                return []
            raise RuntimeError(f'The server responded with an error: {words["error"]}')
        return TypeAdapter(list[Entry]).validate_python(words)


@make_sync(search)
def search_sync(): ...


@with_http_session
async def search_proverbs_and_phrases(
        query: str, /, *, http_session: ClientSession) -> list[Entry]:
    query = lowercase(query, keep_unknown_characters=False)
    async with http_session.get(
        "https://sozluk.gov.tr/gtsAtasozDeyim",
        params={"ara": query}
    ) as response:
        return TypeAdapter(list[Entry]).validate_python(
            await response.json(content_type="text/html; charset=utf-8")
        )


@make_sync(search_proverbs_and_phrases)
def search_proverbs_and_phrases_sync(): ...


@with_http_session
async def get_suggestions(query: str, /, *,
                          http_session: ClientSession) -> list[str]:
    async with http_session.get(
        "https://sozluk.gov.tr/oneri",
        params={"soz": query}
    ) as response:
        try:
            return [
                entry["madde"]
                for entry in
                await response.json(content_type="text/html; charset=utf-8")
            ]
        except Exception as e:
            raise RuntimeError(
                "The server returned an invalid response: "
                "https://github.com/emreozcan/tdk-py/issues/2"
                "#issuecomment-1153257967"
            ) from e


@make_sync(get_suggestions)
def get_suggestions_sync(): ...


ValidatedCounter = Annotated[
    tuple[int, ...],
    BeforeValidator(lambda v: tuple(map(int, v[0]["deger"].split("."))))
]


class HomepageMixup(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "id"))
    incorrect: str = Field(validation_alias=AliasChoices("incorrect", "yanlis"))
    correct: str = Field(validation_alias=AliasChoices("correct", "dogru"))


class HomepageProverb(BaseModel):
    proverb: str = Field(validation_alias=AliasChoices("proverb", "atasozu"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))


class HomepageFrequentTypos(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "id"))
    incorrect: str = Field(validation_alias=AliasChoices("incorrect", "yanliskelime"))
    correct: str = Field(validation_alias=AliasChoices("correct", "dogrukelime"))


class HomepageRule(BaseModel):
    name: str = Field(validation_alias=AliasChoices("name", "adi"))
    url: str


class HomepageLoanword(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "karsid"))
    loanword: str = Field(validation_alias=AliasChoices("loanword", "kkelime"))
    origin: str = Field(validation_alias=AliasChoices("origin", "kkoken"))
    new_word: str = Field(validation_alias=AliasChoices("new_word", "kkarsilik"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))


class HomepageWord(BaseModel):
    word: str = Field(validation_alias=AliasChoices("word", "madde"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))


class HomepageContent(BaseModel):
    counter: ValidatedCounter = Field(validation_alias=AliasChoices("sayac", "deger"))
    mixups: List[HomepageMixup] = Field(default_factory=list, validation_alias=AliasChoices("mixups", "karistirma"))
    proverbs: List[HomepageProverb] = Field(default_factory=list, validation_alias=AliasChoices("proverbs", "atasozu"))
    typos: List[HomepageFrequentTypos] = Field(default_factory=list, validation_alias=AliasChoices("frequent_typos", "syyd"))
    rules: List[HomepageRule] = Field(default_factory=list, validation_alias=AliasChoices("rules", "kural"))
    loanword: HomepageLoanword = Field(default_factory=list, validation_alias=AliasChoices("loanword", "yabanci"))
    words: List[HomepageWord] = Field(default_factory=list, validation_alias=AliasChoices("words", "kelime"))


@with_http_session
async def get_homepage_content(*, http_session: ClientSession) -> HomepageContent:
    async with http_session.get("https://sozluk.gov.tr/icerik") as response:
        return HomepageContent.model_validate(
            await response.json(content_type="text/html; charset=utf-8")
        )


@make_sync(get_homepage_content)
def get_homepage_content_sync(): ...
