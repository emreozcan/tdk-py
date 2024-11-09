from typing import List, Annotated

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, BeforeValidator

from tdk.internal.http import with_http_session
from tdk.internal.utils import make_sync


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


ValidatedCounter = Annotated[
    tuple[int, ...],
    BeforeValidator(lambda v: tuple(map(int, v[0]["deger"].split("."))))
]


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
