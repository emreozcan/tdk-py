"""Güncel Türkçe Sözlük\\
Updated Turkish Dictionary
"""

from string import punctuation
from typing import Annotated

from aiohttp import ClientSession
from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    Field,
    TypeAdapter,
    model_validator,
)

from tdk.enums import OriginLanguage
from tdk.tools import lowercase, dictionary_order
from tdk.internal.http import (
    API_BASE_URL,
    SITE_BASE_URL,
    make_http_session_optional,
)
from tdk.internal.utils import (
    StrOrNone,
    make_sync,
    assert_not_found,
    ValidatedProperty,
)

__all__ = [
    "GTSEntry",
    "GTSMeaning",
    "GTSMeaningExample",
    "GTSMeaningGroup",
    "GTSProverb",
    "GTSSynonym",
    "GTSAntonym",
    "GTSReference",
    "GTSCompoundWord",
    "GTSWriter",
    "get_gts_index",
    "get_gts_index_sync",
    "get_gts_circumflex_index",
    "get_gts_circumflex_index_sync",
    "search_gts",
    "search_gts_sync",
    "search_gts_proverbs_and_phrases",
    "search_gts_proverbs_and_phrases_sync",
    "get_gts_suggestions",
    "get_gts_suggestions_sync",
]


class GTSWriter(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "yazar_id"))
    full_name: str = Field(
        validation_alias=AliasChoices("full_name", "tam_adi")
    )
    short_name: str = Field(
        validation_alias=AliasChoices("short_name", "kisa_adi")
    )


class GTSMeaningExample(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "ornek_id"))
    meaning_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("meaning_id", "anlam_id"),
    )
    order: int | None = Field(
        default=None,
        validation_alias=AliasChoices("order", "ornek_sira"),
    )
    example: StrOrNone = Field(
        default=None,
        validation_alias=AliasChoices("example", "ornek"),
    )
    writers: list[GTSWriter] = Field(
        default_factory=lambda: [],
        validation_alias=AliasChoices("writers", "writer", "yazar"),
    )


class GTSProverb(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "madde_id"))
    proverb: str = Field(validation_alias=AliasChoices("proverb", "madde"))
    prefix: str | None = Field(
        default=None,
        validation_alias=AliasChoices("prefix", "on_taki"),
    )


class GTSCompoundWord(BaseModel):
    tdk_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("tdk_id", "madde_id"),
    )
    entry: str = Field(validation_alias=AliasChoices("entry", "madde"))


def _parse_compound_words(value):
    if isinstance(value, str):
        return [
            {"madde": word.strip()} for word in value.split(",") if word.strip()
        ]
    return value


CompoundWordList = Annotated[
    list[GTSCompoundWord],
    BeforeValidator(_parse_compound_words),
]


class GTSSynonym(BaseModel):
    meaning_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("meaning_id", "anlam_id"),
    )
    order: int | None = Field(
        default=None,
        validation_alias=AliasChoices("order", "sira"),
    )
    entry: str = Field(validation_alias=AliasChoices("entry", "deger"))
    target_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("target_id", "hedef_madde_id"),
    )


class GTSAntonym(GTSSynonym):
    pass


class GTSReference(BaseModel):
    tdk_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("tdk_id", "id"),
    )
    meaning_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("meaning_id", "anlam_id"),
    )
    reference: str = Field(
        validation_alias=AliasChoices("reference", "gosterim")
    )
    target: str | None = Field(
        default=None,
        validation_alias=AliasChoices("target", "hedef_madde"),
    )
    target_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("target_id", "hedef_madde_id"),
    )


class GTSMeaning(BaseModel):
    meaning: StrOrNone = Field(
        default=None,
        validation_alias=AliasChoices("meaning", "anlam"),
    )
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "anlam_id"))
    order: int | None = Field(
        default=None,
        validation_alias=AliasChoices("order", "anlam_sira"),
    )
    is_verb: bool = Field(
        default=False,
        validation_alias=AliasChoices("is_verb", "fiil"),
    )
    entry_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("entry_id", "madde_id"),
    )
    word_type: str | None = Field(
        default=None,
        validation_alias=AliasChoices("word_type", "sozcukTuru"),
    )
    examples: list[GTSMeaningExample] = Field(
        default_factory=list,
        validation_alias=AliasChoices(
            "examples", "orneklerListe", "orneklerliste"
        ),
    )
    properties: list[ValidatedProperty] = Field(
        default_factory=list,
        validation_alias=AliasChoices("properties", "ozelliklerListe"),
    )
    synonyms: list[GTSSynonym] = Field(
        default_factory=list,
        validation_alias=AliasChoices("synonyms", "anlamEsAnlam"),
    )
    antonyms: list[GTSAntonym] = Field(
        default_factory=list,
        validation_alias=AliasChoices("antonyms", "anlamKarsitAnlam"),
    )
    references: list[GTSReference] = Field(
        default_factory=list,
        validation_alias=AliasChoices("references", "anlamReferans"),
    )

    @model_validator(mode="after")
    def _derive_verb_state(self):
        if not self.is_verb and self.word_type == "fiil":
            self.is_verb = True
        return self


class GTSMeaningGroup(BaseModel):
    word_type: str = Field(validation_alias=AliasChoices("word_type", "tur"))
    meanings: list[GTSMeaning] = Field(
        default_factory=list,
        validation_alias=AliasChoices("meanings", "anlamlar"),
    )


class GTSEntry(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "madde_id"))
    order: int = Field(validation_alias=AliasChoices("order", "kac"))
    entry: str = Field(validation_alias=AliasChoices("entry", "madde"))
    plural: bool = Field(
        default=False,
        validation_alias=AliasChoices("plural", "cogul_mu", "cogulMu"),
    )
    proper: bool = Field(
        default=False,
        validation_alias=AliasChoices("proper", "ozel_mi", "ozelMi"),
    )
    origin_language: OriginLanguage = Field(
        default=OriginLanguage.ORIGINAL,
        validation_alias=AliasChoices(
            "origin_language", "lisan_kodu", "lisanKodu"
        ),
    )
    original: str | None = Field(
        default=None,
        validation_alias=AliasChoices("original", "lisanKoken", "lisan"),
    )
    origin_language_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "origin_language_name", "lisan_adi", "lisan"
        ),
    )
    entry_normalized: str | None = Field(
        default=None,
        validation_alias=AliasChoices("entry_normalized", "madde_duz"),
    )
    meanings: list[GTSMeaning] = Field(
        default_factory=list,
        validation_alias=AliasChoices("meanings", "anlamlarListe"),
    )
    meaning_groups: list[GTSMeaningGroup] = Field(
        default_factory=list,
        validation_alias=AliasChoices("meaning_groups", "anlamGruplari"),
    )
    proverbs: list[GTSProverb] = Field(
        default_factory=list,
        validation_alias=AliasChoices("proverbs", "atasozleri", "atasozu"),
    )
    compound_words: CompoundWordList = Field(
        default_factory=list,
        validation_alias=AliasChoices(
            "compound_words", "birlesikKelimeler", "birlesikler"
        ),
    )
    pronunciation: str | None = Field(
        default=None,
        validation_alias=AliasChoices("pronunciation", "telaffuz"),
    )
    syllabification: str | None = Field(
        default=None,
        validation_alias=AliasChoices("syllabification", "heceleme"),
    )
    phonemic: str | None = Field(
        default=None,
        validation_alias=AliasChoices("phonemic", "fonemik"),
    )
    sound_code: str | None = Field(
        default=None,
        validation_alias=AliasChoices("sound_code", "seskod"),
    )
    prefix: str | None = Field(
        default=None,
        validation_alias=AliasChoices("prefix", "on_taki"),
    )
    suffix: str | None = Field(
        default=None,
        validation_alias=AliasChoices("suffix", "taki"),
    )

    def _fill_meaning_ids(self, meaning: GTSMeaning, order: int):
        if meaning.entry_id is None:
            meaning.entry_id = self.tdk_id
        if meaning.order is None:
            meaning.order = order
        for example_order, example in enumerate(meaning.examples, start=1):
            if example.meaning_id is None:
                example.meaning_id = meaning.tdk_id
            if example.order is None:
                example.order = example_order

    @model_validator(mode="after")
    def _fill_missing_ids(self):
        for order, meaning in enumerate(self.meanings, start=1):
            self._fill_meaning_ids(meaning, order)
        for group in self.meaning_groups:
            for order, meaning in enumerate(group.meanings, start=1):
                self._fill_meaning_ids(meaning, order)
        return self


entry_list_adapter = TypeAdapter(list[GTSEntry])


def _normalize_query(query: str, /) -> str:
    """Normalize a query for the TDK search API.

    Unlike the old API, the new API is not tolerant of extra whitespace or
    punctuation, and it expects circumflexed vowels to be preserved.
    """
    query = lowercase(query, keep_nonletters=True, remove_hats=False)
    query = " ".join(query.split())
    return query.strip(punctuation)


@make_http_session_optional
async def get_gts_index(*, http_session: ClientSession) -> list[str]:
    async with http_session.get(
        f"{SITE_BASE_URL}/data/autocomplete.json"
    ) as response:
        return sorted(
            [entry["madde"] for entry in await response.json()],
            key=dictionary_order,
        )


@make_sync(get_gts_index)
def get_gts_index_sync(): ...


_CIRCUMFLEX_TRANSLATION = str.maketrans("âîû", "aiu")


@make_http_session_optional
async def get_gts_circumflex_index(
    *, http_session: ClientSession
) -> dict[str, str]:
    """Get the circumflex index.

    The TDK no longer publishes a separate circumflex index.
    This builds one from the regular index instead.

    :returns: A dictionary where the keys are entries without circumflex,
              and the values are the entries with.
    """
    index = await get_gts_index(http_session=http_session)
    circumflex_index: dict[str, str] = {}
    for entry in index:
        without_circumflex = entry.translate(_CIRCUMFLEX_TRANSLATION)
        if without_circumflex != entry:
            circumflex_index.setdefault(without_circumflex, entry)
    return circumflex_index


@make_sync(get_gts_circumflex_index)
def get_gts_circumflex_index_sync(): ...


@make_http_session_optional
async def search_gts(
    query: str, /, *, http_session: ClientSession
) -> list[GTSEntry]:
    query = _normalize_query(query)
    if not query:
        return []
    async with http_session.get(
        f"{API_BASE_URL}/gts-yeni",
        params={"ara": query, "searchType": "web"},
    ) as response:
        words = await response.json()
        if isinstance(words, list):
            return entry_list_adapter.validate_python(words)
        assert_not_found(words)
        return []


@make_sync(search_gts)
def search_gts_sync(): ...


@make_http_session_optional
async def search_gts_proverbs_and_phrases(
    query: str, /, *, http_session: ClientSession
) -> list[GTSEntry]:
    query = _normalize_query(query)
    if not query:
        return []
    async with http_session.get(
        f"{API_BASE_URL}/gts-yeni",
        params={"ara": query, "searchType": "web"},
    ) as res:
        res_data = await res.json()
        if isinstance(res_data, list):
            return entry_list_adapter.validate_python(res_data)
        assert_not_found(res_data)
        return []


@make_sync(search_gts_proverbs_and_phrases)
def search_gts_proverbs_and_phrases_sync(): ...


@make_http_session_optional
async def get_gts_suggestions(
    query: str, /, *, http_session: ClientSession
) -> list[str]:
    query = _normalize_query(query)
    if not query:
        return []
    async with http_session.get(
        f"{API_BASE_URL}/autocomplete", params={"ara": query}
    ) as response:
        entries = await response.json()
        if not isinstance(entries, list):
            assert_not_found(entries)
            return []
        return [
            entry["madde"] if isinstance(entry, dict) else str(entry)
            for entry in entries
        ]


@make_sync(get_gts_suggestions)
def get_gts_suggestions_sync(): ...
