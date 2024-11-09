from typing import NewType

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, TypeAdapter

from tdk.internal.http import with_http_session
from tdk.internal.utils import IntOrNone, make_sync, StrOrNone


TermDictionaryName = NewType("TermDictionaryName", str)


class TermDictionary(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "eser_id"))
    name: TermDictionaryName = Field(validation_alias=AliasChoices("name", "eser_ad"))
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


class Term(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "terim_id", "soz_id"))
    equivalent_word: StrOrNone = Field(validation_alias=AliasChoices("equivalent_word", "eskterim"))
    term: str = Field(validation_alias=AliasChoices("term", "sozcuk", "terim"))
    english: StrOrNone = Field(validation_alias=AliasChoices("english", "ingiliz", "ingilizce"))
    french: StrOrNone = Field(validation_alias=AliasChoices("french", "fransiz"))
    german: StrOrNone = Field(validation_alias=AliasChoices("german", "alman"))
    latin: StrOrNone
    other: StrOrNone = Field(validation_alias=AliasChoices("other", "diger"))
    meaning: StrOrNone = Field(validation_alias=AliasChoices("meaning", "anlam", "tanim", "tanim_t"))
    dictionary_name: str = Field(validation_alias=AliasChoices("dictionary_name", "sozluk_ad"))
    dictionary_short_name: str = Field(validation_alias=AliasChoices("dictionary_short_name", "kist"))
    dilkarma: StrOrNone
    bkz: StrOrNone
    yaz: StrOrNone
    published_year: IntOrNone = Field(validation_alias=AliasChoices("published_year", "yaytar"))


@with_http_session
async def search_terms(
        dictionaries: list[TermDictionary | TermDictionaryName],
        query: str,
        *,
        http_session: ClientSession
) -> list[Term]:
    # Doesn't search pharmaceutics and nursing dictionaries.
    dictionary_names: list[str] = [
        d.name if isinstance(d, TermDictionary) else d
        for d in dictionaries
    ]
    terms: list[Term] = []
    if "İlaç ve Eczacılık Terimleri Sözlüğü" in dictionary_names:
        async with http_session.get(
            "https://sozluk.gov.tr/eczacilik",
            params={"ara": query}
        ) as res:
            res_data = await res.json(content_type="text/html; charset=utf-8")
            if isinstance(res_data, list):
                terms.extend(TypeAdapter(list[Term]).validate_python(res_data))
        dictionary_names.remove("İlaç ve Eczacılık Terimleri Sözlüğü")
    if "Hemşirelik Terimleri Sözlüğü" in dictionary_names:
        async with http_session.get(
            "https://sozluk.gov.tr/hemsirelik",
            params={"ara": query}
        ) as res:
            res_data = await res.json(content_type="text/html; charset=utf-8")
            if isinstance(res_data, list):
                terms.extend(TypeAdapter(list[Term]).validate_python(res_data))
        dictionary_names.remove("Hemşirelik Terimleri Sözlüğü")
    async with http_session.get(
        "https://sozluk.gov.tr/terim",
        params={
            "eser_ad": "@".join(dictionary_names),
            "ara": query,
        }
    ) as res:
        res_data = await res.json(content_type="text/html; charset=utf-8")
        if isinstance(res_data, list):
            terms.extend(TypeAdapter(list[Term]).validate_python(res_data))
    return TypeAdapter(list[Term]).validate_python(terms)


@make_sync(search_terms)
def search_terms_sync(): ...
