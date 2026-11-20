from typing import Annotated

from aiohttp import ClientSession
from pydantic import BaseModel, Field, AliasChoices, BeforeValidator

from tdk.internal.http import API_BASE_URL, make_http_session_optional
from tdk.internal.utils import make_sync
from tdk.dictionaries.ysk import LoanwordEntry


__all__ = [
    "HomepageMixup",
    "HomepageProverb",
    "HomepageFrequentTypos",
    "HomepageRule",
    "HomepageWord",
    "HomepageTrendingWord",
    "HomepageContent",
    "get_homepage_content",
    "get_homepage_content_sync",
]


class HomepageMixup(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "id"))
    incorrect: str = Field(validation_alias=AliasChoices("incorrect", "yanlis"))
    correct: str = Field(validation_alias=AliasChoices("correct", "dogru"))


class HomepageProverb(BaseModel):
    proverb: str = Field(
        validation_alias=AliasChoices("proverb", "atasozu", "sozum")
    )
    meaning: str = Field(
        validation_alias=AliasChoices("meaning", "anlam", "anlami")
    )


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


class HomepageTrendingWord(HomepageWord):
    type: str | None = Field(default=None, validation_alias="type")


ValidatedCounter = Annotated[
    tuple[int, ...],
    BeforeValidator(lambda v: tuple(map(int, v[0]["deger"].split(".")))),
]


def _dicts_only(value):
    """Drop non-dict items that the old API occasionally returned."""
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return value


def _as_loanword_list(value):
    """Wrap the single loanword object returned by the API in a list."""
    if isinstance(value, dict):
        return [value] if value else []
    if value is None:
        return []
    return value


ValidatedLoanwordList = Annotated[
    list[LoanwordEntry],
    BeforeValidator(_as_loanword_list),
]


class HomepageContent(BaseModel):
    counter: ValidatedCounter = Field(
        validation_alias=AliasChoices("sayac", "deger")
    )
    mixups: Annotated[
        list[HomepageMixup], BeforeValidator(_dicts_only)
    ] = Field(
        default_factory=list,
        validation_alias=AliasChoices("mixups", "karistirma"),
    )
    proverbs: Annotated[
        list[HomepageProverb], BeforeValidator(_dicts_only)
    ] = Field(
        default_factory=list,
        validation_alias=AliasChoices("proverbs", "atasozu", "atasoz"),
    )
    typos: Annotated[
        list[HomepageFrequentTypos], BeforeValidator(_dicts_only)
    ] = Field(
        default_factory=list,
        validation_alias=AliasChoices("frequent_typos", "syyd"),
    )
    rules: Annotated[
        list[HomepageRule], BeforeValidator(_dicts_only)
    ] = Field(
        default_factory=list, validation_alias=AliasChoices("rules", "kural")
    )
    loanword: ValidatedLoanwordList = Field(
        default_factory=list,
        validation_alias=AliasChoices("loanword", "yabanci"),
    )
    words: Annotated[
        list[HomepageWord], BeforeValidator(_dicts_only)
    ] = Field(
        default_factory=list, validation_alias=AliasChoices("words", "kelime")
    )
    trending_words: Annotated[
        list[HomepageTrendingWord], BeforeValidator(_dicts_only)
    ] = Field(
        default_factory=list,
        validation_alias=AliasChoices("trending_words", "gundem"),
    )


@make_http_session_optional
async def get_homepage_content(
    *, http_session: ClientSession
) -> HomepageContent:
    async with http_session.get(f"{API_BASE_URL}/home-widget") as response:
        return HomepageContent.model_validate(await response.json())


@make_sync(get_homepage_content)
def get_homepage_content_sync(): ...
