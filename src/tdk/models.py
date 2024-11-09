from typing import List

from pydantic import BaseModel, Field, AliasChoices

from tdk.enums import OriginLanguage, ValidatedProperty


class Writer(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "yazar_id"))
    full_name: str = Field(validation_alias=AliasChoices("full_name", "tam_adi"))
    short_name: str = Field(validation_alias=AliasChoices("short_name", "kisa_adi"))


class MeaningExample(BaseModel):
    tdk_id: int = Field(validation_alias=AliasChoices("tdk_id", "ornek_id"))
    meaning_id: int = Field(validation_alias=AliasChoices("meaning_id", "anlam_id"))
    order: int = Field(validation_alias=AliasChoices("order", "ornek_sira"))
    example: str = Field(validation_alias=AliasChoices("example", "ornek"))
    writer: Writer | None = Field(default=None, validation_alias=AliasChoices("writer", "yazar"))


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
