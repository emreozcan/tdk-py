from typing import Annotated

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, BeforeValidator

from tdk.internal.http import make_http_session_optional
from tdk.internal.utils import make_sync
from tdk.dictionaries.ysk import LoanwordEntry


__all__ = [
    "HomepageMixup",
    "HomepageProverb",
    "HomepageFrequentTypos",
    "HomepageRule",
    "HomepageWord",
    "HomepageContent",
    "get_homepage_content",
    "get_homepage_content_sync",
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
    incorrect: str = Field(
        validation_alias=AliasChoices("incorrect", "yanliskelime")
    )
    correct: str = Field(
        validation_alias=AliasChoices("correct", "dogrukelime")
    )


class HomepageRule(BaseModel):
    name: str = Field(validation_alias=AliasChoices("name", "adi"))
    url: str


class HomepageWord(BaseModel):
    word: str = Field(validation_alias=AliasChoices("word", "madde"))
    meaning: str = Field(validation_alias=AliasChoices("meaning", "anlam"))


ValidatedCounter = Annotated[
    tuple[int, ...],
    BeforeValidator(lambda v: tuple(map(int, v[0]["deger"].split(".")))),
]


class HomepageContent(BaseModel):
    counter: ValidatedCounter = Field(
        validation_alias=AliasChoices("sayac", "deger")
    )
    mixups: list[HomepageMixup] = Field(
        default_factory=list,
        validation_alias=AliasChoices("mixups", "karistirma"),
    )
    proverbs: list[HomepageProverb] = Field(
        default_factory=list,
        validation_alias=AliasChoices("proverbs", "atasozu"),
    )
    typos: list[HomepageFrequentTypos] = Field(
        default_factory=list,
        validation_alias=AliasChoices("frequent_typos", "syyd"),
    )
    rules: list[HomepageRule] = Field(
        default_factory=list, validation_alias=AliasChoices("rules", "kural")
    )
    loanword: LoanwordEntry = Field(
        default_factory=list,
        validation_alias=AliasChoices("loanword", "yabanci"),
    )
    words: list[HomepageWord] = Field(
        default_factory=list, validation_alias=AliasChoices("words", "kelime")
    )


@make_http_session_optional
async def get_homepage_content(
    *, http_session: ClientSession
) -> HomepageContent:
    async with http_session.get("https://sozluk.gov.tr/icerik") as response:
        return HomepageContent.model_validate(
            await response.json(content_type="text/html; charset=utf-8")
        )


@make_sync(get_homepage_content)
def get_homepage_content_sync(): ...
